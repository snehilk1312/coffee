import re
import pandas as pd

def get_estate(text):
    if not text:
        return None
    if text != text:
        return None

    df = pd.read_csv('/Users/snehil/Work/self/coffee/coffee_database/data_store/coffee_estates.csv')

    text = text.replace('c & t','c&t')

    stop_words = ['plantation','estate','and', '&', '-','valley','giri','tat']
    text_list = [i.strip() for i in text.strip().split() if len(i)>2 and i not in stop_words]

    estate_list = df['Estate'].to_list()

    return_dict = {
        'estate': [],
        'producers': [],
        'location': [],
        'altitude': [],
        'country': []
    }

    for word in text_list:
        if word == 'unnakki' or word == 'unakki':
            word = 'unnaki'
        if word == 'baarbara':
            word = 'barbara'
        if word == 'pearl':
            word = 'ratna'
        if word == 'bitcode' or word=='belur':
            word = 'biccode'
        for p_estate in estate_list:
            if word in p_estate.lower().strip() and p_estate.lower().strip() not in stop_words:
                is_match = df[df['Estate'] == p_estate].iloc[0]

                if is_match['Estate'] and is_match['Estate']==is_match['Estate']:
                    return_dict['estate'].append(is_match['Estate'].lower())
                if is_match['Producers'] and is_match['Producers']==is_match['Producers']:
                    return_dict['producers'].append(is_match['Producers'].lower())
                if is_match['Location'] and is_match['Location']==is_match['Location']:
                    return_dict['location'].append(is_match['Location'].lower())
                if is_match['State'] and is_match['State']==is_match['State']:
                    return_dict['location'].append(is_match['State'].lower())
                if is_match['Average Altitude'] and is_match['Average Altitude']==is_match['Average Altitude']:
                    return_dict['altitude'].append(is_match['Average Altitude'])
                if is_match['Country'] and is_match['Country']==is_match['Country']:
                    return_dict['country'].append(is_match['Country'].lower())

    return_dict = {
        key:  ', '.join(dict.fromkeys(value)) if key != 'altitude' else (
            sum(dict.fromkeys(value)) / len(dict.fromkeys(value))
            if len(dict.fromkeys(value)) > 0
            else None  # or any other default value that makes sense for your context
        )
        for key, value in return_dict.items()
    }

    return_dict = {k: (v if v != '' else None) for k, v in return_dict.items()}

    return return_dict

if __name__=="__main__":
    print(get_estate('salawara'))