from essentials.scraper import overwrite_cards
from essentials.data.cards import get_cards

# update all the cards

# WARNING: this will take a long time to run

overwrite_cards(get_cards(), [])
