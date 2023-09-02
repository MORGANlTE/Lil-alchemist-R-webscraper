from bs4 import BeautifulSoup
import requests
import time

class Scraper():
    def get_image(self, soup):
        figure_element = soup.find('figure', class_='pi-item pi-image')
        if figure_element:
            a_tag = figure_element.find('a')
            if a_tag and 'href' in a_tag.attrs:
                image_url = a_tag['href']
            else:
                print("No image URL found within the <a> tag.")
        else:
            print("No <figure> element with class 'pi-item pi-image' found.")
            image_url = None
        return image_url
    
    def get_rarity_and_form_etc(self, soup):
        # The table for the rarity and form information
        tables_rarity_form = soup.find_all('table', class_='pi-horizontal-group')

        # Description
        descr = tables_rarity_form[0].find("td", attrs={'data-source': 'imagecaption'}).get_text(strip=True)

        # Base Attack
        base_attack = tables_rarity_form[1].find("td", attrs={'data-source': 'attack'}).get_text(strip=True)
        # Base Defense
        base_defense = tables_rarity_form[1].find("td", attrs={'data-source': 'defense'}).get_text(strip=True)
        # Base Power
        base_power = tables_rarity_form[1].find("td", attrs={'data-source': 'rarity'}).text.strip()

        # Rarity
        rarity = tables_rarity_form[2].find("td", attrs={'data-source': 'rarity'}).text.strip()
        # Form
        form = tables_rarity_form[2].find("td", attrs={'data-source': 'form'}).text.strip()

        # Fusion
        fusion = soup.find("div", class_="pi-item pi-data pi-item-spacing pi-border-color", attrs={'data-source': 'fusion'}).find("b").text.strip()

        # Where to acquire
        list_acquire = soup.find('div', class_='mw-parser-output').find('ul').find_all('li')
        where_to_acquire = []
        for elemnt in list_acquire:
            where_to_acquire.append(elemnt.text.strip())


        # The table with the level info
        table_level_info = soup.find('table', class_='article-table')

        # Initialize an empty dictionary to store the key-value pairs
        level_stats = {}

        # # Find all rows within the table except the header row
        rows = table_level_info.find_all('tr')[1:]
        for row in rows:
            # Extract the level, attack, and defense values
            level_img = row.find('th').find('img')  # Find the img tag
            level = level_img['alt']      # Extract the level from the alt attribute
            tds = row.find_all('td')      # Find all td tags
            attack = int(tds[0].text.strip())
            defense = int(tds[1].text.strip())
            level_stats[level] = {'Attack': attack, 'Defense': defense}

        return descr, base_attack, base_defense, base_power, rarity, form, fusion, where_to_acquire, level_stats

        
    def scrapedata(self, name):
        url = f'https://lil-alchemist.fandom.com/wiki/{name}'
        print("- " + url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        imgurl = self.get_image(soup)
        description, base_attack, base_defense, base_power, rarity, form, fusion, where_to_acquire, level_stats = self.get_rarity_and_form_etc(soup)
        
        print("\tImage URL:", imgurl)
        print(f"\tDescription: {description}")
        print(f"\tBase attack: {base_attack}")
        print(f"\tBase defense: {base_defense}")
        print(f"\tBase power: {base_power}")
        print(f"\tRarity: {rarity}")
        print(f"\tForm: {form}")
        print(f"\tFusion: {fusion}")
        print(f"\tWhere to acquire: {where_to_acquire}")
        print(f"\tStats per level: {level_stats}")


        return "Error"

#fl = open("nieuweTypeList.txt", "w")
#list_total=[]
scraper = Scraper()
counter = 1

for name in ["Bear"]:#"Chloe_(Card)"]:
    print(f"#{counter} {name}")
    try:
        response = scraper.scrapedata(name)
    except:
        print(f"Error on card {name}")
    #list_total.append(response)
    time.sleep(1)

    counter += 1

#fl.write(str(list_total))
#fl.close()



