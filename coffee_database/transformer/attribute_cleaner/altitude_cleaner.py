import re

def extract_altitude(text):
    """
    Extracts altitude information from a given text string and converts it to meters.

    Args:
    text (str): A string containing altitude information.

    Returns:
    Tuple[float, float]: A tuple containing the minimum altitude and maximum altitude in meters,
                         or None if no altitudes are found.
    """
    if not text:
        return None
    # Define regex patterns to extract altitude in meters or feet
    altitude_pattern = re.compile(r'(\d{3,4})\s*[-–]?\s*(\d{3,4})?\s*(m|M|masl|MASL|asl|ASL|meters|ft|Feet|feet)?', re.IGNORECASE)
    
    # Find all matches in the input text
    matches = altitude_pattern.findall(text)
    
    if not matches:
        return None
    
    # Convert matches to numeric values and handle ranges
    altitudes = []
    for match in matches:
        low = int(match[0])
        high = int(match[1]) if match[1] else low
        unit = match[2].lower() if match[2] else 'm'  # Default to 'm' if no unit is specified
        
        # Convert to meters if the unit is in feet
        if 'ft' in unit or 'feet' in unit:
            low = str(low * 0.3048)
            high = str(high * 0.3048)
        
        altitudes.append(f"{low}-{high}")
    
    # Return the first match as a tuple (min_altitude, max_altitude) in meters
    return altitudes[0]

if __name__=="__main__":
    altitude = '1320 – 1870 masl'
    print(extract_altitude(altitude))
    altitude = '4000+ Feet'
    print(extract_altitude(altitude))
    altitude = None
    print(extract_altitude(None))