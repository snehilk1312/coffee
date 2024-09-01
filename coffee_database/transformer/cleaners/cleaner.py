
import pandas as pd
import os,re,json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from attribute_cleaner.price_cleaner import price_cleaner
from attribute_cleaner.general_string_cleaner import text_cleaner
from attribute_cleaner.altitude_cleaner import extract_altitude
from attribute_cleaner.roast_level import get_roast_level
from datetime import datetime
import sqlalchemy

load_dotenv()

roaster_list = ['savorworks','bloom_coffee_roasters','blue_tokai','corridor_seven','curious_life','greysoul',
                'kapi_kottai','kc_roasters','koffie_genetics','naivo','quick_brown_fox'
                ]

# List of standard cols
standard_cols = ["roaster","name", "link", "price", "altitude", "varietal", "processing", 
                "estate", "roast_level", "tasting_notes", "description", 
                "country", "scraped_at","transformed_at","extra_properties"]

# Create an SQLAlchemy engine (replace with your actual database URL)
engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')


for roaster in roaster_list:

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
                    'wet_aroma': 'tasting_notes',
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

    col_text_cleaner = ['estate','varietal','processing','tasting_notes','acidity','body','aftertaste','description','variety']
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

    print(df.columns)
    df = df[standard_cols + ["extra_properties"]]

    # putting it into db
    conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
    df.to_sql(name = 'transformed_stg' , con=conn, index=False, if_exists='append',schema='public')

    print(f'{roaster} TRANSFORMED !!!')
    



