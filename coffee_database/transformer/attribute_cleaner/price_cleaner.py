import re


def price_cleaner(text):
    """
    Extracts the  price from a given text string and return a floats

    Args:
    text (str): A string containing price information.

    Returns:
    float: The maximum numeric price extracted from the text, or None if no prices are found.
    """

    try:
        if not text:
            return None

        # Define regex pattern to extract the numeric part of the price
        price_pattern = re.compile(r'(?:[\₹]|Rs?\.?)\s*([\d,]+(?:\.\d+)?)', re.IGNORECASE)
        
        # Find all matches in the input text
        matches = price_pattern.findall(text)
        
        # Convert the matches to numeric format
        numeric_prices = [float(match.replace(',', '')) for match in matches if match]
        
        # Return the maximum price or None if no prices are found
        return max(numeric_prices) if numeric_prices else None
    except:
        return None
        