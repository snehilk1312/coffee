import re

def text_cleaner(input_string):
    # Step 1: Convert to lowercase
    if not input_string:
        return None 
    if input_string=='Not available' or input_string=='Blue Tokai Coffee Roasters':
        return None

    cleaned = input_string.lower()
    
    # Step 2: Remove specific unwanted strings like 'nbsp', 'NBSP'
    cleaned = re.sub(r'(\bnbsp\b|\bNBSP\b)', '', cleaned)
    cleaned = cleaned.replace('grown at 4200 msl','')
    cleaned = cleaned.replace('instagram','')
    cleaned = cleaned.replace('&amp','')
    cleaned = cleaned.replace('&#39;',"'")


    # Step 3: Normalize multiple spaces, newlines, and punctuation marks to a single one
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Replace multiple spaces/newlines with a single space
    cleaned = re.sub(r'([.,!?&|;:()\[\]{}-])\1+', r'\1', cleaned)  # Replace multiple punctuation marks with a single one
    
    # Step 4: Ensure there is always a space before and after punctuation (except single quotes)
    cleaned = re.sub(r"([.,!?&;:()\[\]{}'\"-])", r" \1 ", cleaned)  # Space around punctuation

    cleaned = re.sub(r'\s+', ' ', cleaned)  # Remove any additional spaces created
    cleaned = cleaned.strip()     # Remove any additional space at end or start

    # Step 5: Remove punctuation at the start or end of the line
    cleaned = re.sub(r'^[.,!?&;:\[\]{}-]+|[.,!?&;:\[\]{}-]+$', '', cleaned)

    # custom

    # removing this specific set coz problems in NER
    # cleaned = re.sub(r"\s'\s", "'", cleaned)
    # cleaned = re.sub(r'\s"\s', '"', cleaned)
    # cleaned = re.sub(r"\s-\s", "-", cleaned)


    # Step 6: Final strip to remove leading/trailing whitespace
    cleaned = cleaned.strip()
    
    cleaned = re.sub(r'^[.,!?&;:\[\]{}-]+|[.,!?&;:\[\]{}-]+$', '', cleaned)
    cleaned = cleaned.strip()


    return cleaned

if __name__=="__main__":
    # Example usage
    strings_to_clean = [

    """red apples , followed by a luscious malic acidity and a velvety body"""
    ]

    cleaned_strings = [text_cleaner(s) for s in strings_to_clean]
    print(cleaned_strings)
