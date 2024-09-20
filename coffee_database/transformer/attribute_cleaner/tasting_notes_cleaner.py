import re

def clean_notes(notes):
    if not notes or notes!=notes:
        return None

    notes = notes.replace('dark roastchocolate fudge','chocolate fudge')
    notes = notes.replace('c acao','cacao')

    # Standardize separators: replace `;`, `|`, `/`, `&`, `+` with a comma
    notes = re.sub(r'[;|/&+]', ',', notes)
    notes = re.sub(r' and ', ',', notes)

    # Remove extra spaces around commas
    notes = re.sub(r'\s*,\s*', ', ', notes.strip())

    # Split by comma and strip extra spaces
    notes_list = [note.strip() for note in notes.split(',') if note.strip()]


    stop_words = ['10', 'a', 'acidity', 'aftertaste', 'aroma', 'bodied', 'body', 'bold', 'butter', 'characteristics', 
        'characters', 'chopped', 'clean', 'complex', 'driven', 'dryness', 'essence', 'finish', 'follow', 
        'followed', 'full', 'heavy', 'hint', 'hints', 'juicy', 'leading', 'light', 'like', 'lingering', 
        'long', 'malic', 'med', 'medium', 'mouthfeel', 'nostalgia', 'notes', 'of', 'prominent', 'rich', 
        'rounded', 'shieldtail', 'short', 'silky', 'smooth', 'soft', 'sourness', 'sparkling', 'sweetness', 
        'trace', 'traces', 'underlying', 'velvety', 'with'
    ]
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
    tasting_notes = 'bold, long aftertaste with a finish of clove'
    print(clean_notes(tasting_notes))