# Speciality Coffee Recommender

### This repository contains resources to build a speciality coffee recommender system (focusing on Indian beans for now).

#### Major Components:

1. **`coffee_database`**
    1. **`scraper`**  
       Collects coffee data from roasters' websites.
    2. **`ner`**  
       Custom NER model for extracting speciality coffee properties (roaster, altitude, varietal, processing, etc.). Data will be available in `data_store` for public use until the model is finalized/shared. Although the model training code is already in the repo. Some of the features:
        - Roaster
        - Altitude
        - Varietal
        - Processing
        - Estate
        - Roast level
        - Sensory notes (taste, aroma)
        - Location
        - Producers/farmers/co-op society
        - Acidity
        - Body/texture
        - Aftertaste
        - Other properties (bitterness, sweetness, etc.)
    3. **`transformer`**  
       Preprocesses, cleans, and performs NER on data to create training data for the recommender. Continuous WIP.
    4. **`data_store`**  
       Finalized CSV/data files for community use.
    5. **`sql`**  
       Currently part of the transformer module but will be relocated.

2. **`pushshift_dumps`**
    - Reddit have always been a great place for discussions and learning (inspite of it's decreasing standard nowadays) . There is too much valuable data thats have been there that can make any recommendation system shine if used correctly. The current content of this folder has some outdated data and scripts but I will be updating it once the part `coffee_database` will have considerable closure.
    - In the first attempt I rode the `LLM` hype and created a recommendation sysyem based on `RAG` which although not completely awful, was of little use.
    - In the current Iteration , the `LLMised` pipeline will be used to assist main recommender which will be classical Recommendation system - a combination of content+collaborative methods.

3. **`llama-index-notebooks`**
   - This is also a part of `LLM` based attempt to make recommender based on RAG, not awful and gives good enough recommendation(if you are just starting), but won't work with unseen beans and is not based on coffee properties. It has some learning material which needs to be cleaned.
---
