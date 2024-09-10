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

    return cleaned

if __name__=="__main__":
    # Example usage
    strings_to_clean = [

    """


    anuswaram in carnatic parlance means a note between notes and denotes complex melodic movements that rāga-s tend to employ.we sometimes receive small lots of coffee that really captivate us with their complexity or innovative processing. we feel that anuswaram is a fitting name for featuring these intriguing lots.for the third of this series, we have three very special arabica lots which come from small growers in sirangalli village , high up in the pushpagiris (coorg). a washed , a honey and a natural.all three lots have been carefully processed in collaboration with the good folks of south india coffee company. two of them being processed at mooleh manay estate.for the washed lot, ripe cherries were harvested and sent to the community washing center. floats were removed after which the coffee was pulped and then washed. the resulting cup is very sweet, very balanced and sparkles with a lemon-candy like acidity.for the honey, ripe cherries were harvested and brought back to mooleh manay’s processing unit, then floated and fermented in cherry form. the coffee cherries are then pulped using an waterless eco pulper , keeping most of the mucilage intact. the coffee is then sent to the patios to dry , raking at regular intervals. all this care results in a cup bright cup that brims with oodles of fruitiness; reminding us of peaches and green apples.for the natural , ripe cherries were harvested and brought back to mooleh manay’s processing unit, then floated and fermented in bags to keep the environment anoxic. the cherries are then dried on raised beds inside a poly tunnel for a fortnight and were raked regularly. the resulting cup has tons of texture and an acidity that reminds us of plums.we wanted you guys to experience all of the haul from sirangalli village and the best way to do this is a sampler set of 3× 100g. anuswaram # 3 is a delight across all manual brews and covers a wide gamut of flavour experiences, from clean and crisp to fruity and punchy.kudos to south india coffee company for having initiated this project and giving smallholder farms , a much needed entry into the speciality coffee scene.




    """
    ]

    cleaned_strings = [text_cleaner(s) for s in strings_to_clean]
    print(cleaned_strings)
