medium_light_keywords = ['bright', 'fruity', 'citrus', 'juicy', 'floral', 'tea', 'honey', 'apricot', 'light']
medium_keywords = ['balanced', 'sweet', 'round', 'sugar', 'chocolate', 'nuts', 'cocoa', 'melon', 'grape']
medium_dark_keywords = ['dark','chocolate', 'earthy', 'spicy', 'mellow', 'bitter', 'nutmeg', 'cardamom', 'full-bodied']

def get_roast_level(roast_level_raw,description):

    if not roast_level_raw:
        return None
    if not description:
        description=''
    # Convert to lowercase for easier comparison
    roast_level_raw_lower = roast_level_raw.lower()  
    description = description.lower()
    
    # custom case seen in 1 example
    if roast_level_raw == 'slightly above medium roast with 20% dtr & total roast time of 10 mins.':
        return 'MEDIUM_DARK'
    
    elif 'med' in roast_level_raw_lower and 'light' in roast_level_raw_lower:
        return 'MEDIUM_LIGHT'
    elif 'med' in roast_level_raw_lower and 'dark' in roast_level_raw_lower:
        return 'MEDIUM_DARK'
    elif 'med' in roast_level_raw_lower:
        return 'MEDIUM'
    elif 'dark' in roast_level_raw_lower:
        return 'DARK'
    elif 'light' in roast_level_raw_lower:
        return 'LIGHT'
    elif 'espresso' in roast_level_raw_lower:
        return 'MEDIUM_DARK'
    elif 'filter' in roast_level_raw_lower:
        return 'MEDIUM_LIGHT'
    elif roast_level_raw_lower == 'omni roast':
        # Check for keywords in the description

        medium_light_count = sum(description.count(word) for word in medium_light_keywords)
        medium_count = sum(description.count(word) for word in medium_keywords)
        medium_dark_count = sum(description.count(word) for word in medium_dark_keywords)

        if medium_dark_count > medium_count and medium_dark_count > medium_light_count:
            return "MEDIUM_DARK"
        elif medium_count > medium_light_count:
            return "MEDIUM"
        elif medium_light_count > 0:
            return "MEDIUM_LIGHT"
        else:
            return "MEDIUM"
    else:
        return None

if __name__=='__main__':
    print(get_roast_level(              
               roast_level_raw = "omni roast",           
               description = """
                we’ve made much progress on our exploration of fine robustas in the effort to showcase the high quality of robusta coffee produced in india. most of indian robusta is exported to europe and australia while the major volume of what stays in the country is used by instant coffee manufacturers and roasters focused on mass-produced commercial blends for espresso and south indian filter coffee. with revolutionary advancements in farming, fermentation and post-harvest processing, our producers are now inducing a great deal of excitement in the robusta space. this washed lot from venkids valley estate delivers a lip-smacking espresso with spicy expressions of nutmeg and cardamom and a strong dark chocolate finish. our omni-roast has helped tailor this lot for an interesting experience in manual brews as well with pourover brewing and aeropress delivering a full-bodied cup with similar spice notes and an underlying jaggery sweetness. if you are a robusta enthusiast or a coffee lover with a curious mind, we highly recommend this lot that showcases the promising future of indian washed robustas. cardamom
                nutmeg dark chocolate we’ve made much progress on our exploration of fine robustas in the effort to showcase the high quality of robusta coffee produced in india. most of indian robusta is exported to europe and australia while the major volume of what stays in the country is used by instant coffee manufacturers and roasters focused on mass-produced commercial blends for espresso and south indian filter coffee. with revolutionary advancements in farming, fermentation and post-harvest processing, our producers are now inducing a great deal of excitement in the robusta space. this washed lot from venkids valley estate delivers a lip-smacking espresso with spicy expressions of nutmeg and cardamom and a strong dark chocolate finish. our omni-roast has helped tailor this lot for an interesting experience in manual brews as well with pourover brewing and aeropress delivering a full-bodied cup with similar spice notes and an underlying jaggery sweetness. if you are a robusta enthusiast or a coffee lover with a curious mind, we highly recommend this lot that showcases the promising future of indian washed robustas.
                """)
)
    