from essentials.scraper import overwrite_packs

# add a card to the cards_to_scrape list to scrape it
# if it's an onyx aswell, add it to the onyx_cards_to_scrape list

packs_to_scrape = [
    "Golem",
    "Turkey Day",
    "Carver of Doom",
    "Harvest",
    "Plymouth Rock",
    "Robot Turkey",
    "Turkey Zombie",
    "Arcane Golem",
]


overwrite_packs(packs_to_scrape)
