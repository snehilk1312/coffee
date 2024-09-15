
import pandas as pd
import os,re,json,sys
from tqdm import tqdm
from dotenv import load_dotenv
from sqlalchemy import create_engine

from attribute_cleaner.price_cleaner import price_cleaner
from attribute_cleaner.general_string_cleaner import text_cleaner
from attribute_cleaner.altitude_cleaner import extract_altitude
from attribute_cleaner.roast_level import get_roast_level
from attribute_cleaner.extract_varietal import extract_varietal

from datetime import datetime
import sqlalchemy
import spacy
from sqlalchemy.types import VARCHAR,TIMESTAMP,BIGINT,NUMERIC,BOOLEAN,DATE,TEXT
from sqlalchemy.dialects.postgresql import JSONB

import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")

load_dotenv()

roaster_list = ['savorworks','bloom_coffee_roasters','blue_tokai','corridor_seven','curious_life','greysoul',
                'kapi_kottai','kc_roasters','koffie_genetics','naivo','quick_brown_fox'
                ]

# Create an SQLAlchemy engine (replace with your actual database URL)
engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')

nlp = spacy.load('/Users/snehil/Work/self/coffee/coffee_database/ner/output_try_3/model-best/')

def return_each_label(text):
    return_dict = {}
    final_dict = {}

    if text:
        doc = nlp(text.lower())
        
        for ent in doc.ents:
            # print(ent.label_)
            if ent.label_ not in return_dict.keys():
                return_dict[ent.label_] = [ent.text]
            else:
                return_dict[ent.label_].append(ent.text)

        for key,val in return_dict.items():
            final_dict[key] = ' , '.join(list(set(return_dict[key]))) if return_dict[key] else None
    return final_dict

for roaster in tqdm(roaster_list, desc="Processing roasters"):
    # List of standard cols
    standard_cols = ["roaster","name", "link", "price", "altitude", "varietal", "processing", 
                "estate", "roast_level", "tasting_notes", "description", 
                "country", "scraped_at","transformed_at"
                ,"extra_properties","ner_properties"
                ]

    # Define your SQL query
    query = f"""
    select * from raw_scraped.{roaster}
    """
    
    df = pd.read_sql(query, con=engine)
    df.columns = [re.sub(r'[^\w]+', '_', i.lower()).strip('_') for i in df.columns]

    if roaster=='blue_tokai':
        df.rename(columns={'tasting_notes':'bt_tasting_notes'},inplace=True)

    df.rename(columns={'origin': 'estate',
                    'process': 'processing',
                    'elevation': 'altitude',
                    'roast': 'roast_level',
                    'flavor': 'tasting_notes',
                    'tastes_like': 'tasting_notes',
                    'roasting_profile': 'roast_level',
                    'estate_name': 'estate',
                    'roast_profile': 'roast_level',
                    'roaster_thoughts': 'description',
                    'product_name': 'name',
                    'url': 'link',
                    'name_of_coffee': 'name',
                    'varieties': 'varietal',
                    'flavor_notes': 'tasting_notes',
                    }, inplace=True)

    columns_missing_from_standard_table = [i for i in standard_cols if i not in df.columns.tolist()]
    df[columns_missing_from_standard_table] = None

    df['description'] = df['description'].fillna('') + ' ' + df['name'].fillna('')

    col_text_cleaner = ['description']
    for text_col in col_text_cleaner:
        try:
            df[text_col] = df[text_col].apply(text_cleaner)
        except KeyError:
            pass

    if 'variety' in df.columns:
        df['varietal'] = df['varietal'].where(df['varietal'].notna(), df['variety'])
        df.drop(['variety'],inplace=True,axis=1)
    if 'bt_tasting_notes' in df.columns:
        df['tasting_notes'] = df['tasting_notes'].where(df['tasting_notes'].notna(), df['bt_tasting_notes'])
        df.drop(['bt_tasting_notes'],inplace=True,axis=1)


    df["extra_properties"] = df.apply(lambda row: {col: row[col] for col in df.columns if col not in standard_cols}, axis=1)
    df['extra_properties'] = df['extra_properties'].apply(json.dumps)

    df["ner_properties"] = df['description'].apply(return_each_label)
    df["ner_properties"] = df["ner_properties"].apply(json.dumps)

    # taking care of extra or less columns
    df = df[standard_cols]  

    idx = df.groupby('name')['scraped_at'].idxmax()
    df = df.loc[idx]
    df.reset_index(drop=True,inplace=True)
    df["roaster"] = roaster 
    df['price'] = df.price.apply(price_cleaner)
    df['altitude'] = df.altitude.apply(extract_altitude)
    df['roast_level'] = df.apply(lambda row: get_roast_level(row['roast_level'], row['description']), axis=1)
    
    df['country'] = df['country'].where(df['country'].notna(), 'india')
    df['transformed_at'] = datetime.now()    

    # taking missing cols from NER dict

    # Altitude Filling from jsonb
    # Extract 'ELEVATION' from 'ner_properties' column (assuming it's JSON)
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('ELEVATION') if pd.notnull(x) else None)
    df['json_placeholder'] = df['json_placeholder'].apply(extract_altitude)
    # Fill null values in 'altitude' with values from 'altitude_backup'
    df['altitude'] = df['altitude'].fillna(df['json_placeholder'])
    df.drop(['json_placeholder'],axis=1,inplace=True)

    # Estate Filling from jsonb
    # Extract 'ESTATE' from 'ner_properties' column (assuming it's JSON)
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('ESTATE') if pd.notnull(x) else None)

    # Fill null values in 'estate' or concatenate existing values with json placeholder
    df['estate'] = df.apply(
        lambda row: row['json_placeholder'] if pd.isna(row['estate']) 
                    else (f"{row['estate']}, {row['json_placeholder']}" if pd.notna(row['json_placeholder']) else row['estate']),
        axis=1
    )
    df.drop(['json_placeholder'], axis=1, inplace=True)

    # Varietal Filling from jsonb
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('VARIETAL') if pd.notnull(x) else None)
    df['varietal'] = df.apply(
        lambda row: row['json_placeholder'] if pd.isna(row['varietal']) 
                    else (f"{row['varietal']}, {row['json_placeholder']}" if pd.notna(row['json_placeholder']) else row['varietal']),
        axis=1
    )
    df.drop(['json_placeholder'], axis=1, inplace=True)

    # Processing Filling from jsonb
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('PROCESSING') if pd.notnull(x) else None)
    df['processing'] = df.apply(
        lambda row: row['json_placeholder'] if pd.isna(row['processing']) 
                    else (f"{row['processing']}, {row['json_placeholder']}" if pd.notna(row['json_placeholder']) else row['processing']),
        axis=1
    )
    df.drop(['json_placeholder'], axis=1, inplace=True)

    # Roast Level Filling from jsonb
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('ROAST LEVEL') if pd.notnull(x) else None)
    df['json_placeholder'] = df.apply(lambda row: get_roast_level(row['json_placeholder'], row['description']), axis=1)

    df['roast_level'] = df['roast_level'].fillna(df['json_placeholder'])
    df.drop(['json_placeholder'],axis=1,inplace=True)


    # Tasting Notes Filling from jsonb
    df['json_placeholder'] = df['ner_properties'].apply(lambda x: json.loads(x).get('TASTING NOTES') if pd.notnull(x) else None)
    df['tasting_notes'] = df['tasting_notes'].fillna(df['json_placeholder'])
    df.drop(['json_placeholder'],axis=1,inplace=True)


    # EXTRA COLS

    # Location 
    df['region'] = df['extra_properties'].apply(lambda x: json.loads(x).get('region') if pd.notnull(x) else None)
    df['location'] = df['extra_properties'].apply(lambda x: json.loads(x).get('location') if (pd.notnull(x) and json.loads(x).get('location')!='Not available') else None)
    df['LOCATION'] = df['ner_properties'].apply(lambda x: json.loads(x).get('LOCATION') if pd.notnull(x) else None)

    df['location'] = df['region'].fillna(df['location'])
    df['location'] = df['location'].fillna(df['LOCATION'])
    df.drop(['region','LOCATION'],axis=1,inplace=True)

    # Producers 
    df['planters'] = df['extra_properties'].apply(lambda x: json.loads(x).get('planters') if pd.notnull(x) else None)
    df['producers'] = df['extra_properties'].apply(lambda x: json.loads(x).get('producers') if pd.notnull(x) else None)
    df['FARMER'] = df['ner_properties'].apply(lambda x: json.loads(x).get('FARMER') if pd.notnull(x) else None)

    df['producers'] = df['planters'].fillna(df['producers'])
    df['producers'] = df['producers'].fillna(df['FARMER'])
    df.drop(['planters','FARMER'],axis=1,inplace=True)

    # Coffee type 
    df['type'] = df['extra_properties'].apply(lambda x: json.loads(x).get('type') if pd.notnull(x) else None)
    df['COFFEE TYPE'] = df['ner_properties'].apply(lambda x: json.loads(x).get('COFFEE TYPE') if pd.notnull(x) else None)

    df['coffee_type'] = df['type'].fillna(df['COFFEE TYPE'])
    df.drop(['type','COFFEE TYPE'],axis=1,inplace=True)

    # Aroma 
    df['dry_aroma'] = df['extra_properties'].apply(lambda x: json.loads(x).get('dry_aroma') if pd.notnull(x) else None)
    df['wet_aroma'] = df['extra_properties'].apply(lambda x: json.loads(x).get('wet_aroma') if pd.notnull(x) else None)

    df['aroma'] = df.apply(
        lambda row: f"{row['dry_aroma']} {row['wet_aroma']}".strip() if row['dry_aroma'] or row['wet_aroma'] else 
        (json.loads(row['ner_properties']).get('AROMA') if pd.notnull(row['ner_properties']) else None),
        axis=1
    )
    df.drop(['wet_aroma','dry_aroma'],axis=1,inplace=True)

    # Acidity
    df['acidity'] = df['extra_properties'].apply(lambda x: json.loads(x).get('acidity') if (pd.notnull(x) and json.loads(x).get('acidity')!='Not available') else None)
    df['ACIDITY'] = df['ner_properties'].apply(lambda x: json.loads(x).get('ACIDITY') if pd.notnull(x) else None)

    df['acidity'] = df['acidity'].fillna(df['ACIDITY'])
    df.drop(['ACIDITY'],axis=1,inplace=True)

    # Body/Texture
    df['BODY'] = df['ner_properties'].apply(lambda x: json.loads(x).get('BODY') if pd.notnull(x) else None)
    df['body'] = df['extra_properties'].apply(lambda x: json.loads(x).get('body') if (pd.notnull(x) and json.loads(x).get('body')!='Not available') else None)

    df['body'] = df['BODY'].fillna(df['body'])
    df.drop(['BODY'],axis=1,inplace=True)

    # Other properties, aftertaste

    df['aftertaste'] = df['extra_properties'].apply(lambda x: json.loads(x).get('aftertaste') if (pd.notnull(x) and json.loads(x).get('aftertaste')!='Not available') else None)
    df['AFTERTASTE'] = df['ner_properties'].apply(lambda x: json.loads(x).get('AFTERTASTE') if pd.notnull(x) else None)

    df['aftertaste'] = df['aftertaste'].fillna(df['AFTERTASTE'])
    df['aftertaste'] = df['aftertaste'].apply(lambda x: f"{x} aftertaste" if pd.notnull(x) else x)
    df['other_properties'] = df['ner_properties'].apply(lambda x: json.loads(x).get('COFFEE_PROPERTIES') if pd.notnull(x) else None)
    df['other_properties'] = df['other_properties'].fillna('') + ' ' + df['aftertaste'].fillna('')
    df.drop(['AFTERTASTE','aftertaste'],axis=1,inplace=True)


    addition_cols = ['location','producers','coffee_type','aroma','acidity','body','other_properties']
    standard_cols.extend(addition_cols)

    # print(standard_cols)

    df = df[standard_cols]

    df.drop(['ner_properties','extra_properties'],axis=1,inplace=True)

    col_text_cleaner = ['estate','varietal','processing','tasting_notes','acidity','body','aftertaste','variety','location','producers',
    'coffee_type','aroma','other_properties'
    ]
    for text_col in col_text_cleaner:
        try:
            df[text_col] = df[text_col].apply(text_cleaner)
        except KeyError:
            pass

    # standard cols
    df.varietal = df.varietal.apply(extract_varietal)

    # putting it into db
    conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
    # df.to_sql(name = 'transformed_stg' , con=conn, index=False, if_exists='append',dtype=type_col,schema='public')
    df.to_sql(name = 'transformed_stg' , con=conn, index=False, if_exists='append',schema='public')

    print(f'{roaster} TRANSFORMED !!!')
    



