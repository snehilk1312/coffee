import re

def clean_processing(notes):
    if not notes or notes!=notes:
        return None

    notes = notes.replace('naturals','natural')
    # Standardize separators: replace `;`, `|`, `/`, `&`, `+` with a comma
    notes = re.sub(r'[;|/&+]', ',', notes)
    notes = re.sub(r' and ', ',', notes)
    notes = re.sub(r'\b\d+\s?(?:hrs?|hours?)\b', '', notes)

    # Remove extra spaces around commas
    notes = re.sub(r'\s*,\s*', ', ', notes.strip())

    # Split by comma and strip extra spaces
    notes_list = [note.strip() for note in notes.split(',') if note.strip()]


    stop_words = ['arabica','robusta','processed','processes']
    # print(notes_list)

    final_list = []
    temp_list = []
    for j in notes_list:
        temp_list = [i.strip().strip('-').strip() for i in j.split()]
        temp_list = [i for i in temp_list if i not in stop_words]
        final_list.append(' '.join(temp_list))

    notes = ', '.join(list(set(final_list)))


    return notes

if __name__=="__main__":
    processing = """72 - hour carbonic maceration culture process ( yeast & lactic acid bacteria ) naturals slow dried for 29 days . , carbonic maceration"""
    print(clean_processing(processing))