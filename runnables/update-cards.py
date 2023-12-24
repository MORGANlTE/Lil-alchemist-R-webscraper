from essentials.scraper import overwrite_cards

# add a card to the cards_to_scrape list to scrape it
# if it's an onyx aswell, add it to the onyx_cards_to_scrape list

onyx_cards_to_scrape = ["Rainbow"]
cards_to_scrape = [
    "Miniature",
    "Microraptor",
    "Bonsai",
    "Flapjack Octopus",
    "White Dwarf",
    "Water Bear",
    "Mini Clone",
    "Pygmy Jerboa",
    "Conscience",
    "Power Nap",
    "Bumblebee Bat",
    "Thumbelina",
    "Protozoan Villain",
    "Spider Mite",
]


overwrite_cards(cards_to_scrape, onyx_cards_to_scrape)
