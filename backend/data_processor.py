import pandas as pd
from typing import Optional, Dict, List
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.df = None
        if data_path:
            self.load_data()

    def load_data(self):
        """Load and preprocess the Excel data"""
        try:
            logger.debug(f"Loading data from: {self.data_path}")
            self.df = pd.read_excel(self.data_path)
            logger.debug(f"Data loaded successfully. Shape: {self.df.shape}")
            # Convert date columns to datetime if they exist
            date_columns = [col for col in self.df.columns if 'date' in col.lower()]
            for col in date_columns:
                self.df[col] = pd.to_datetime(self.df[col])
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise Exception(f"Error loading data: {str(e)}")

    def calculate_oee(self, device_id: Optional[str] = None, 
                     location: Optional[str] = None, 
                     month: Optional[str] = None) -> Dict:
        """
        Calculate OEE based on the formula: OEE = Availability × Performance × Quality
        
        Availability = Operating Time / Planned Production Time
        Performance = (Total Count × Ideal Cycle Time) / Operating Time
        Quality = Good Count / Total Count
        """
        if self.df is None:
            logger.error("No data loaded")
            return {"error": "No data loaded. Please upload data first."}

        try:
            # Filter data based on parameters
            filtered_df = self.df.copy()
            logger.debug(f"Initial data shape: {filtered_df.shape}")
            
            if device_id:
                filtered_df = filtered_df[filtered_df['device_id'] == device_id]
                logger.debug(f"After device_id filter: {filtered_df.shape}")
            if location:
                filtered_df = filtered_df[filtered_df['location'] == location]
                logger.debug(f"After location filter: {filtered_df.shape}")
            if month:
                filtered_df = filtered_df[filtered_df['month'] == month]
                logger.debug(f"After month filter: {filtered_df.shape}")

            if filtered_df.empty:
                logger.warning(f"No data found for: device_id={device_id}, location={location}, month={month}")
                return {
                    "oee": 0,
                    "availability": 0,
                    "performance": 0,
                    "quality": 0,
                    "message": "No data found for the specified parameters"
                }

            # Calculate OEE components
            planned_production_time = filtered_df['planned_production_time'].sum()
            operating_time = filtered_df['operating_time'].sum()
            total_count = filtered_df['total_count'].sum()
            good_count = filtered_df['good_count'].sum()
            ideal_cycle_time = filtered_df['ideal_cycle_time'].mean()

            logger.debug(f"Raw values: ppt={planned_production_time}, ot={operating_time}, tc={total_count}, gc={good_count}, ict={ideal_cycle_time}")

            # Calculate components (all values between 0 and 1)
            availability = (operating_time / planned_production_time) if planned_production_time > 0 else 0
            
            # Calculate theoretical production time based on ideal cycle time
            theoretical_production_time = total_count * ideal_cycle_time / 60  # Convert to hours
            performance = (theoretical_production_time / operating_time) if operating_time > 0 else 0
            
            quality = (good_count / total_count) if total_count > 0 else 0

            logger.debug(f"Component values: a={availability}, p={performance}, q={quality}")

            # Ensure all components are between 0 and 1
            availability = min(max(availability, 0), 1)
            performance = min(max(performance, 0), 1)
            quality = min(max(quality, 0), 1)

            # Calculate OEE
            oee = availability * performance * quality

            # Convert to percentages for display
            return {
                "oee": round(oee * 100, 2),
                "availability": round(availability * 100, 2),
                "performance": round(performance * 100, 2),
                "quality": round(quality * 100, 2),
                "message": f"OEE Calculation Results:\n"
                         f"Availability: {round(availability * 100, 2)}%\n"
                         f"Performance: {round(performance * 100, 2)}%\n"
                         f"Quality: {round(quality * 100, 2)}%\n"
                         f"Overall OEE: {round(oee * 100, 2)}%"
            }

        except Exception as e:
            logger.error(f"Error calculating OEE: {str(e)}")
            return {"error": f"Error calculating OEE: {str(e)}"}

    def get_available_filters(self) -> Dict[str, List]:
        """Get available filter options"""
        if self.df is None:
            return {
                "device_ids": [],
                "locations": [],
                "months": []
            }
            
        return {
            "device_ids": self.df['device_id'].unique().tolist(),
            "locations": self.df['location'].unique().tolist(),
            "months": self.df['month'].unique().tolist()
        } 