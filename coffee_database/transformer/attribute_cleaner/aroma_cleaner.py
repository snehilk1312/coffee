import re

def clean_aroma(notes):
    if not notes or notes!=notes:
        return None

    notes = notes.replace('blackcurrant',',black currant')
    # Standardize separators: replace `;`, `|`, `/`, `&`, `+` with a comma
    notes = re.sub(r'[;|/&+]', ',', notes)
    notes = re.sub(r' and ', ',', notes)

    # Remove extra spaces around commas
    notes = re.sub(r'\s*,\s*', ', ', notes.strip())

    # Split by comma and strip extra spaces
    notes_list = [note.strip() for note in notes.split(',') if note.strip()]


    stop_words = ["and", "&", "rich", "strong", "like", "deep", "followed", "by", "a", "luscious", "malic", 
        "acidity", "velvety", "body", "come", "through", "beautifully", "when", "you", "allow", 
        "the", "brew", "to", "cool", "down", "little", "sandalwood", "estate","sweetness","aroma",
        '10','aftertaste', 'aroma', 'bodied', 'body', 'bold', 'characteristics', 
        'characters', 'chopped', 'clean', 'complex', 'driven', 'dryness', 'essence', 'finish', 'follow', 
        'full', 'heavy', 'hint', 'hints', 'juicy', 'leading', 'light', 'lingering', 
        'long', 'med', 'medium', 'mouthfeel', 'nostalgia', 'notes', 'of', 'prominent', 
        'rounded', 'shieldtail', 'short', 'silky', 'smooth', 'soft', 'sourness', 'sparkling', 'sweetness', 
        'trace', 'traces', 'underlying', 'with']
    # print(notes_list)

    final_list = []
    temp_list = []
    for j in notes_list:
        temp_list = [i.strip() for i in j.split()]
        temp_list = [i for i in temp_list if i not in stop_words]
        final_list.append(' '.join(temp_list))

    notes = ', '.join(final_list)


    return notes

if __name__=="__main__":
    aroma = 'candied orange & jasmine blackcurrant jam & sugarcane'
    print(clean_aroma(aroma))