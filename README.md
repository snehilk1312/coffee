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

---
