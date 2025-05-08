import pandas as pd
from typing import Dict, List, Tuple
import numpy as np

class DataValidator:
    REQUIRED_COLUMNS = [
        'device_id',
        'location',
        'month',
        'planned_production_time',
        'operating_time',
        'total_count',
        'good_count',
        'ideal_cycle_time'
    ]

    @staticmethod
    def validate_data(df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Validate the Excel data structure and content
        Returns: (is_valid, validation_results)
        """
        validation_results = {
            'missing_columns': [],
            'invalid_data_types': [],
            'negative_values': [],
            'zero_values': [],
            'data_consistency': []
        }

        # Check required columns
        missing_columns = [col for col in DataValidator.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            validation_results['missing_columns'] = missing_columns
            return False, validation_results

        # Validate data types
        numeric_columns = ['planned_production_time', 'operating_time', 'total_count', 'good_count', 'ideal_cycle_time']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                validation_results['invalid_data_types'].append(col)

        # Check for negative values
        for col in numeric_columns:
            if (df[col] < 0).any():
                validation_results['negative_values'].append(col)

        # Check for zero values in critical columns
        critical_columns = ['planned_production_time', 'operating_time', 'total_count']
        for col in critical_columns:
            if (df[col] == 0).any():
                validation_results['zero_values'].append(col)

        # Check data consistency
        if 'operating_time' in df.columns and 'planned_production_time' in df.columns:
            if (df['operating_time'] > df['planned_production_time']).any():
                validation_results['data_consistency'].append('Operating time exceeds planned production time')

        if 'good_count' in df.columns and 'total_count' in df.columns:
            if (df['good_count'] > df['total_count']).any():
                validation_results['data_consistency'].append('Good count exceeds total count')

        # Check if any validation errors occurred
        has_errors = any(len(value) > 0 for value in validation_results.values())
        
        return not has_errors, validation_results

    @staticmethod
    def get_validation_message(validation_results: Dict) -> str:
        """Generate a human-readable validation message"""
        messages = []

        if validation_results['missing_columns']:
            messages.append(f"Missing required columns: {', '.join(validation_results['missing_columns'])}")

        if validation_results['invalid_data_types']:
            messages.append(f"Invalid data types in columns: {', '.join(validation_results['invalid_data_types'])}")

        if validation_results['negative_values']:
            messages.append(f"Negative values found in columns: {', '.join(validation_results['negative_values'])}")

        if validation_results['zero_values']:
            messages.append(f"Zero values found in critical columns: {', '.join(validation_results['zero_values'])}")

        if validation_results['data_consistency']:
            messages.extend(validation_results['data_consistency'])

        return "\n".join(messages) if messages else "Data validation successful" 