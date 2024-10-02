import re

def extract_varietal(text):
    if not text:
        return None
    if text != text:
        return None
    text = text.lower()

    coffee_varieties_dict = {
        'baitan': 'batian',
        'batian': 'batian',
        'bourbon': 'bourbon',
        'castillo': 'castillo',
        'cataui': 'catuai',
        'catimor': 'catimor',
        'catimore': 'catimor',
        'catuai': 'catuai',
        'catuaí': 'catuai',
        'catura': 'caturra',
        'caturra': 'caturra',
        'cautai': 'catuai',
        'cauvery': 'cauvery',
        'cavery': 'cauvery',
        'chandragiri': 'chandragiri',
        'cxr': 'cxr',
        'geisha': 'geisha',
        'hdt': 'hibrido de timor',
        'hemavathy': 'hemavathy',
        'kent': 'kents',
        'kents': 'kents',
        'liberica': 'liberica',
        'mundo novo': 'mundo novo',
        'papayo': 'papayo',
        'peradeniya': 'peradeniya',
        'red catuai': 'red catuai',
        'yellow catuai': 'yellow catuai',
        'red bourbon': 'red bourbon',
        'ruby': 'ruby',
        'ruiru': 'ruiru',
        'sachimore': 'sarchimor',
        'san ramon': 's7, san ramon',
        'sarchi': 'sarchi',
        'sarchimor': 'sarchimor',
        'sarchimore': 'sarchimor',
        'timor': 'timor',
        'tuby': 'tuby'
    }

    matches = re.findall(r'\d+', text)

    all_varietal = []

    if matches:
        for i in matches:
            if i=='5' and '5b' in text:
                all_varietal.append('sln-5b')
            if i=='5' and '5a' in text:
                all_varietal.append('sln-5a')
            if i=='5' and '5a' not in text and '5b' not in text:
                all_varietal.append('sln-5')
            if i=='11' and 'ruiru' in text:
                all_varietal.append('ruiru-11')
            if i!='5' and i!='11':
                all_varietal.append(f"sln-{int(i)}")

    for i in coffee_varieties_dict.keys():
        if 'red' not in i and 'yellow' not in i:
            for j in i.split():
                if j in text:
                    all_varietal.append(coffee_varieties_dict[i])
        else:
            if 'red' in i and 'bourbon' in i and 'red' in text and 'bourbon' in text:
                all_varietal.append('red bourbon')
            if 'yellow' in i and 'bourbon' in i and 'yellow' in text and 'bourbon' in text:
                all_varietal.append('yellow bourbon')
            if 'red' in i and 'catuai' in i and 'red' in text and 'catuai' in text:
                all_varietal.append('red catuai')
            if 'yellow' in i and 'catuai' in i and 'yellow' in text and 'catuai' in text:
                all_varietal.append('yellow catuai')

        all_varietal = list(set(all_varietal))

        if 'red catuai' in all_varietal and 'catuai' in all_varietal:
            all_varietal.remove('catuai')
        if 'yellow catuai' in all_varietal and 'catuai' in all_varietal:
            all_varietal.remove('catuai')
        if 'red bourbon' in all_varietal and 'bourbon' in all_varietal:
            all_varietal.remove('bourbon')
        if 'yellow bourbon' in all_varietal and 'bourbon' in all_varietal:
            all_varietal.remove('bourbon')
        if 'sarchi' in all_varietal and 'sarchi' not in text.split():
            all_varietal.remove('sarchi')
        if 'timor' in all_varietal and 'timor' not in text.split():
            all_varietal.remove('timor')

    return ', '.join(list(set(all_varietal)))

if __name__=="__main__":
    print(extract_varietal('sln - 9 & sln - 795'))
    print(extract_varietal('HDT X CATAUI'))