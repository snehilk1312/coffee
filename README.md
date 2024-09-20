# Speciality Coffee Recommender

### This repository contains bunch of resources that will help to build a speciality coffee recommender system (for now Indian Beans only)

#### It will have following major parts roughly:
1. `coffee_database`
    1. `scraper` - Collects coffee data from each roasters site
    2. `ner` - Custom NER model trained for to scrape various properties related to speciality coffee.Will publically provide the `NER` model and till then a cleaned data sheet will be added in `data_store` if someone wants to use the data
         1. roaster
         2. altitude
         3. varietal
         4. processing
         5. estate
         6. roast level
         7. sensory notes - taste, aroma
         8. location
         9. producers/farmers/co-op society
         10. acidity
         11. body/texture
         12. aftertaste
         13. other properties - bitterness, sweetness, etc
     3. `transformer` - This part of the code that preprocess, cleans, does NER and transforms the data and finally provides with data that can be used to train recommender. Currently have working cleaner for most of the properties and is continuous WIP.
     4. `data_store` - This part will be the sharing point of finalized csv/data files if someone from coffee community wants to see the data.
     5. `sql` - It is also a part of transformer , will move it there soon.
