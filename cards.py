from cardnames import cards

def get_cards():
  no_duplicates = {}

  # Use set to remove duplicates
  no_duplicates = set(cards)

  # Sort the set alphabetically and convert it back to a list
  sorted_cards = sorted(no_duplicates)  
  
  return sorted_cards