# Speciality Coffee Recommender

### This repository contains resources to build a speciality coffee recommender system, with a focus on Indian beans for now.

---

### Why This Project?

For specialty coffee lovers, the search for the perfect cup is never-ending. Whether you're new to the world of specialty coffee or already know what you like but want to explore something similar — be it roast level or sensory nuances — the options can often feel overwhelming. After navigating this journey myself, filled with both disappointments and delightful surprises, I decided to create this coffee recommender to make the process easier for everyone.

By combining your brewing preferences with data, this tool suggests — with 95% confidence — the next beans you’ll love. It doesn’t just recommend, though. It learns from the experience of others, cross-verifying and fine-tuning its suggestions based on feedback from a community of coffee enthusiasts. Whether you’re looking to try something new or refine your favorites, this recommender ensures that every cup is one to savor.

This version highlights both the beginner-friendly aspect and the ability to make fine-tuned recommendations(be it roast level, estates, processing, etc) for experienced coffee drinkers. It also emphasizes the crowdsourced data angle to show how the system continually improves its recommendations based on community input. Let me know what you think!

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
    - Focuses on utilizing Reddit data for improving recommendations. Although initial work involved a `RAG` (LLM-based) approach, future iterations will use a classical recommendation system, combining content and collaborative methods.
  
3. **`llama-index-notebooks`**
    - Contains notebooks exploring `LLM`-based recommendations (RAG). While functional for beginners, it's not ideal for unseen beans and lacks focus on specific coffee properties.
  
This project consists of the following steps:

    Data Collection - In Progress
    Progress: [████░░░░░░] 40%
    Collecting data on user preferences, coffee bean varieties, roast levels, brewing methods, and sensory notes.

    Named Entity Recognition (NER) - In Progress
    Progress: [██████░░░░] 60%
    Identifying key entities like coffee bean characteristics, flavor notes, and roast profiles from user feedback using custom NER models.

    Data Transformation - In Progress
    Progress: [█████░░░░░] 50%
    Processing and structuring the data for use in the recommendation algorithms.

    Content-Based Recommendation - Not Started
    Progress: [░░░░░░░░░░] 0%
    Using user preferences and coffee characteristics to suggest similar beans they might enjoy.

    Collaborative Recommendation - Not Started
    Progress: [░░░░░░░░░░] 0%
    Leveraging community feedback and ratings to improve recommendations based on user similarity.

    Retrieval-Augmented Generation (RAG) - Not Started
    Progress: [░░░░░░░░░░] 0%
    Enhancing the recommendation system with retrieval-based techniques and generative models for better accuracy.
