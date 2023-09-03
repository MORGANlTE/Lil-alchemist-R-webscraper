from bs4 import BeautifulSoup
import requests
import time
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from db_classes import Card, Combination, Recipe, Base, CardLevelStats
from cards import get_cards

# Create a SQLite database engine
engine = create_engine('sqlite:///card_database.db')

# Create an inspector
inspector = inspect(engine)

# Check if the "cards" table exists
if not inspector.has_table("cards"):
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)



# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

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

        # Find all rows within the table except the header row
        rows = table_level_info.find_all('tr')[1:]
        for row in rows:
            # Extract the level, attack, and defense values
            level_img = row.find('th').find('img')  # Find the img tag
            level = level_img['alt']      # Extract the level from the alt attribute
            tds = row.find_all('td')      # Find all td tags
            attack = int(tds[0].text.strip())
            defense = int(tds[1].text.strip())
            level_stats[level] = {'Attack': attack, 'Defense': defense}



        # The Card Recipes:

        table_recipes = soup.find('table', {'id': 'mw-customcollapsible-recipesTable'})
        recipes = []

        # If there is no table_recipes, then there are no recipes
        if table_recipes is None:
            recipes = []
        else:
            table_body = table_recipes.find('tbody')
            rows = table_body.find_all('tr')

            # Iterate through the rows and extract the names from the first and second columns
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    card1_name = columns[0].text.strip()
                    card2_name = columns[1].text.strip()
                    recipes.append((card1_name, card2_name))



         # The Card Combos:

        table_combos = soup.find('table', {'id': 'mw-customcollapsible-combosTable'})
        combos = []

        # If there is no table_recipes, then there are no recipes
        if table_combos is None:
            combos = []
        else:
            table_body = table_combos.find('tbody')
            rows = table_body.find_all('tr')

            # Iterate through the rows and extract the names from the first and second columns
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    card2_name = columns[0].text.strip()
                    result = columns[1].text.strip()
                    combos.append((card2_name, result))

        return descr, base_attack, base_defense, base_power, rarity, form, fusion, where_to_acquire, level_stats, recipes, combos

    def name_converter(self, name):
        # check if name ends with " (Card)"
        type_card = ""
        url_name = name
        real_name = name

        if name.endswith(" (Card)"):
            type_card = "Boss "
            url_name = name.replace(" ", "_")
            # remove everything after "_(" if this is present
            if "_(" in url_name:
                real_name = url_name[:url_name.index("_(")]
        
        if name.endswith(" (Onyx)"):
            url_name = name.replace(" ", "_")
            # remove everything after "_(" if this is present
            if "_(" in url_name:
                real_name = url_name[:url_name.index("_(")]


        return type_card, url_name, real_name

    def scrapedata(self, name):

        type_card, url_name, real_name = self.name_converter(name) 


        url = f'https://lil-alchemist.fandom.com/wiki/{url_name}'
        print("- " + url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        imgurl = self.get_image(soup)
        description, base_attack, base_defense, base_power, rarity, form, fusion, where_to_acquire, level_stats, recipes, combos = self.get_rarity_and_form_etc(soup)

        print(f"\tName: {real_name}")
        print("\tImage URL:", imgurl)
        print(f"\tDescription: {description}")
        print(f"\tBase attack: {base_attack}")
        print(f"\tBase defense: {base_defense}")
        print(f"\tBase power: {base_power}")
        print(f"\tRarity: {rarity}")
        print(f"\tForm: {type_card}{form}")
        print(f"\tFusion: {fusion}")
        print(f"\tWhere to acquire: {where_to_acquire}")
        print(f"\tStats per level: {level_stats}")
        print(f"\tRecipes:\n\t{recipes}")
        print(f"\tCombos:\n\t{combos}")
        
        # Create the Card instance first
        card = Card(
            name=real_name,
            full_name=name,
            image_url=imgurl,
            description=description,
            base_attack=base_attack,
            base_defense=base_defense,
            base_power=base_power,
            rarity=rarity,
            form=f"{type_card}{form}",
            fusion=fusion,
            where_to_acquire=json.dumps(where_to_acquire),
        )

        # Create CardLevelStats instances and set the relationship
        for level, stats in level_stats.items():
            attack = stats['Attack']
            defense = stats['Defense']
            
            card_level_stats = CardLevelStats(
                level=level,
                attack=attack,
                defense=defense,
            )

            # Set the relationship on both sides
            card.level_stats.append(card_level_stats)
            card_level_stats.card = card

            session.add(card_level_stats)

        # Add the Card instance to the session
        session.add(card)


        # If you have recipe data, create Recipe instances and add them to the session
        if recipes and recipes != []:
            for recipe in recipes:
                # check if the other card exists in the database
                card1 = recipe[0]
                card2 = recipe[1]
                result = card.full_name
                # check if opposite recipe exists in the database, in the recipe table
                opposite_recipe = session.query(Recipe).filter_by(card1=card2, card2=card1).first()

                if not opposite_recipe:
                    recipe = Recipe(
                        card1=card1,
                        card2=card2,
                        result=result,
                    )
                    session.add(recipe)

        # If you have combo data, create Combination instances and add them to the session
        if combos and combos != []:
            for combo in combos:
                # check if the other card exists in the database

                card1 = card.full_name
                card2 = combo[0]
                result = combo[1]
                # check if opposite combo exists in the database, in the combo table
                opposite_combo = session.query(Combination).filter_by(card1=card2, card2=card1).first()

                if not opposite_combo:
                    combo = Combination(
                        card1=card1,
                        card2=card2,
                        result=result,
                    )
                    session.add(combo)

        # Commit changes to the database
        session.commit()

        print(f"Added {card.name} to database")
        return "Success"

scraper = Scraper()
counter = 1

# print(get_cards())

for name in get_cards():
    print(f"#{counter} {name}")
    try:
        response = scraper.scrapedata(name)
    except Exception as e:
        print(f"Error on card {name}")
        print(e)
        # print where the error occurs
        import traceback
        traceback.print_exc()
    # Close the session
    #list_total.append(response)
    time.sleep(2)

    counter += 1
session.close()

#fl.write(str(list_total))
#fl.close()



