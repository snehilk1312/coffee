# Speciality Coffee Recommender

### This repository contains resources to build a speciality coffee recommender system, with a focus on Indian beans for now.

---

### Major Components:

1. **`coffee_database`**
    - **`scraper`**: Collects coffee data from roasters' websites.
    - **`ner`**: Custom NER model for extracting coffee properties. Data will be available in `data_store` for public use until the model is finalized/shared. Features extracted:
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
    - **`transformer`**: Preprocesses, cleans, and transforms data for the recommender. Continuous WIP.
    - **`data_store`**: Finalized CSV/data files for public use.
    - **`sql`**: Currently part of the transformer, but will be relocated soon.

2. **`pushshift_dumps`**
    - Focuses on utilizing Reddit data for improving recommendations. Although initial work involved a `RAG` (LLM-based) approach, future iterations will use a classical recommendation system, combining content based and collaborative recommender.
  
3. **`llama-index-notebooks`**
    - Contains notebooks exploring `LLM`-based recommendations (RAG). While functional for beginners, it's not ideal for unseen beans and lacks focus on specific coffee properties.
