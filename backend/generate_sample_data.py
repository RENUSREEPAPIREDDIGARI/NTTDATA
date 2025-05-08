import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    # Create more comprehensive sample data
    devices = [
        'PACK001', 'PACK002', 'PACK003',  # Primary packaging lines
        'WRAP001', 'WRAP002',             # Wrapping machines
        'SEAL001', 'SEAL002', 'SEAL003'   # Sealing machines
    ]
    
    locations = [
        'PRODUCTION_LINE_1',
        'PRODUCTION_LINE_2',
        'PRODUCTION_LINE_3',
        'QUALITY_CONTROL',
        'FINAL_PACKAGING'
    ]
    
    # Generate months for both 2024 and 2025
    months = [f'2024-{str(i).zfill(2)}' for i in range(1, 13)] + [f'2025-{str(i).zfill(2)}' for i in range(1, 13)]
    
    data = []
    
    # Define performance profiles for different device types
    performance_profiles = {
        'PACK': {'base_availability': 0.85, 'base_performance': 0.90, 'base_quality': 0.95},
        'WRAP': {'base_availability': 0.80, 'base_performance': 0.85, 'base_quality': 0.92},
        'SEAL': {'base_availability': 0.75, 'base_performance': 0.80, 'base_quality': 0.90}
    }

    # Define yearly improvement factors (slight improvement in 2025)
    yearly_improvement = {
        2024: 1.0,
        2025: 1.05  # 5% improvement in base metrics for 2025
    }
    
    for device in devices:
        device_type = device[:4]  # Get device type prefix
        profile = performance_profiles[device_type]
        
        for location in locations:
            for month in months:
                year = int(month.split('-')[0])
                month_num = int(month.split('-')[1])
                
                # Apply yearly improvement factor
                improvement_factor = yearly_improvement[year]
                
                # Base values with yearly improvement
                planned_production_time = np.random.uniform(400, 500)  # hours
                
                # Apply seasonal variation (lower in summer months)
                seasonal_factor = 1.0
                if 6 <= month_num <= 8:  # Summer months
                    seasonal_factor = 0.9
                
                # Calculate operating time with maintenance periods
                maintenance_probability = 0.1  # 10% chance of maintenance
                has_maintenance = np.random.random() < maintenance_probability
                
                if has_maintenance:
                    maintenance_hours = np.random.uniform(20, 40)
                    operating_time = (planned_production_time - maintenance_hours) * seasonal_factor
                else:
                    operating_time = planned_production_time * seasonal_factor * profile['base_availability'] * improvement_factor
                
                # Calculate ideal cycle time based on device type (improved in 2025)
                base_cycle_time = {
                    'PACK': np.random.uniform(0.5, 1.0),
                    'WRAP': np.random.uniform(0.8, 1.5),
                    'SEAL': np.random.uniform(1.0, 2.0)
                }[device_type]
                
                ideal_cycle_time = base_cycle_time / improvement_factor  # Better cycle time in 2025
                
                # Calculate counts with quality variations
                total_count = int(operating_time * 60 / ideal_cycle_time)
                
                # Simulate quality issues with reduced probability in 2025
                quality_issue_probability = 0.05 / improvement_factor  # Lower probability in 2025
                has_quality_issues = np.random.random() < quality_issue_probability
                
                if has_quality_issues:
                    quality_factor = np.random.uniform(0.7, 0.9)
                else:
                    quality_factor = profile['base_quality'] * improvement_factor
                
                good_count = int(total_count * quality_factor)
                
                # Add some random variation to make data more realistic
                operating_time = operating_time * np.random.uniform(0.95, 1.05)
                total_count = int(total_count * np.random.uniform(0.98, 1.02))
                good_count = int(good_count * np.random.uniform(0.98, 1.02))
                
                data.append({
                    'device_id': device,
                    'location': location,
                    'month': month,
                    'planned_production_time': round(planned_production_time, 2),
                    'operating_time': round(operating_time, 2),
                    'total_count': total_count,
                    'good_count': good_count,
                    'ideal_cycle_time': round(ideal_cycle_time, 2),
                    'has_maintenance': has_maintenance,
                    'has_quality_issues': has_quality_issues
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to Excel
    file_path = 'data/sample_oee_data.xlsx'
    df.to_excel(file_path, index=False)
    
    # Generate summary statistics
    summary = df.groupby(['device_id', 'month']).agg({
        'planned_production_time': 'mean',
        'operating_time': 'mean',
        'total_count': 'sum',
        'good_count': 'sum',
        'has_maintenance': 'sum',
        'has_quality_issues': 'sum'
    }).round(2)
    
    print(f"Sample data generated and saved to {file_path}")
    print("\nSummary Statistics:")
    print(summary.head(15))  # Show first 15 rows of summary

if __name__ == "__main__":
    generate_sample_data() 