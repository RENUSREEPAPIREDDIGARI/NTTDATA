from typing import Dict, Optional
import re
from datetime import datetime

class QueryProcessor:
    def __init__(self):
        self.month_pattern = r'(january|february|march|april|may|june|july|august|september|october|november|december)'
        self.month_map = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }

    def process_query(self, query: str) -> Dict[str, Optional[str]]:
        """
        Process natural language query and extract parameters
        Returns: Dictionary with device_id, location, and month
        """
        query = query.lower()
        result = {
            'device_id': None,
            'location': None,
            'month': None
        }

        # Extract device ID (now handles Pack001, PACK001, etc.)
        device_patterns = [
            r'(?:device\s+)?(?:pack|device)\s*(\d+)',  # matches pack001, device001
            r'for\s+(?:pack|device)\s*(\d+)',          # matches "for pack001"
            r'(?:pack|device)(\d+)'                     # matches PACK001 directly
        ]
        
        for pattern in device_patterns:
            device_match = re.search(pattern, query)
            if device_match:
                result['device_id'] = f"PACK{device_match.group(1).zfill(3)}"
                break

        # Extract location (now handles PRODUCTION_LINE_1, etc.)
        location_patterns = [
            r'(?:location\s+)?production[_\s]*line[_\s]*(\d+)',  # matches production line 1
            r'for\s+production[_\s]*line[_\s]*(\d+)',            # matches "for production line 1"
            r'in\s+production[_\s]*line[_\s]*(\d+)'              # matches "in production line 1"
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, query)
            if location_match:
                result['location'] = f"PRODUCTION_LINE_{location_match.group(1)}"
                break

        # Extract month
        month_match = re.search(self.month_pattern, query)
        if month_match:
            month_name = month_match.group(1)
            result['month'] = self.month_map[month_name]

        # Handle year if present
        year_match = re.search(r'20\d{2}', query)
        if year_match and result['month']:
            result['month'] = f"{result['month']}-{year_match.group(0)}"

        return result

    def generate_response(self, query: str, oee_data: Dict) -> str:
        """
        Generate a natural language response based on the query and OEE data
        """
        query = query.lower()
        response_parts = []

        # Add greeting if query starts with hi/hello
        if query.startswith(('hi', 'hello', 'hey')):
            response_parts.append("Hello! I'm your OEE assistant.")

        # Add OEE value
        response_parts.append(f"The OEE is {oee_data['oee']}%")

        # Add component details if requested
        if 'component' in query or 'breakdown' in query:
            response_parts.extend([
                f"Availability: {oee_data['availability']}%",
                f"Performance: {oee_data['performance']}%",
                f"Quality: {oee_data['quality']}%"
            ])

        # Add comparison if requested
        if 'compare' in query:
            response_parts.append("Would you like to compare this with another device or time period?")

        # Add suggestion if OEE is low
        if oee_data['oee'] < 80:
            response_parts.append("The OEE is below optimal levels. Would you like suggestions for improvement?")

        return "\n".join(response_parts) 