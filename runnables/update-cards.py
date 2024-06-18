from essentials.scraper import overwrite_cards

# add a card to the cards_to_scrape list to scrape it
# if it's an onyx aswell, add it to the onyx_cards_to_scrape list

onyx_cards_to_scrape = []
cards_to_scrape = ["Adventure", "Arcanomancer", "Bear Owl", "Draconic Deity", "Gothic Horror", "Loot Hoarder", "Mimic", "The Party", "Adopted Monster", "Familiar Companions", "Magical Mayhem", "Nightmarish Swarms", "Planar Privateer", "Submerged Shrine", "Monkey (Onyx)", "Pirate", "Big Mojo", "Demon Puncher", "Giant Anti-Heroes", "Larcenous Pets", "Nautilus 20K", "Off the Map", "The Fortune's Cookie", "Barrage", "Cyber Corsair", "Dread Pirate", "Feisty Figurehead", "Treasure Hunters", "Vampirate", "Precious Ring Lore (Onyx)"]


overwrite_cards(cards_to_scrape, onyx_cards_to_scrape)
