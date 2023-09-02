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
    
    def get_rarity_and_form(self, soup):
        # Find the table containing the rarity and form information
        tables = soup.find_all('table', class_='pi-horizontal-group')

        descr = tables[0].find("td", attrs={'data-source': 'imagecaption'}).get_text(strip=True)

        base_attack = tables[1].find("td", attrs={'data-source': 'attack'}).get_text(strip=True)
        base_defense = tables[1].find("td", attrs={'data-source': 'defense'}).get_text(strip=True)
        base_power = tables[1].find("td", attrs={'data-source': 'rarity'}).text.strip()

        rarity = tables[2].find("td", attrs={'data-source': 'rarity'}).text.strip()
        form = tables[2].find("td", attrs={'data-source': 'form'}).text.strip()

        fusion = soup.find("div", class_="pi-item pi-data pi-item-spacing pi-border-color", attrs={'data-source': 'fusion'}).find("b").text.strip()

        return descr, base_attack, base_defense, base_power, rarity, form, fusion

        
    def scrapedata(self, name):
        url = f'https://lil-alchemist.fandom.com/wiki/{name}'
        print("- " + url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        imgurl = self.get_image(soup)
        description, base_attack, base_defense, base_power, rarity, form, fusion = self.get_rarity_and_form(soup)
        
        print("\tImage URL:", imgurl)
        print(f"\tDescription: {description}")
        print(f"\tBase attack: {base_attack}")
        print(f"\tBase defense: {base_defense}")
        print(f"\tBase power: {base_power}")
        print(f"\tRarity: {rarity}")
        print(f"\tForm: {form}")
        print(f"\tFusion: {fusion}")


        return "Error"

#fl = open("nieuweTypeList.txt", "w")
#list_total=[]
scraper = Scraper()
counter = 1

for name in ["Chloe_(Card)"]:
  print(f"#{counter} {name}")
  response = scraper.scrapedata(name)
  #list_total.append(response)
  time.sleep(1)

  counter += 1

#fl.write(str(list_total))
#fl.close()



