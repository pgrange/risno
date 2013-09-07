from fetch_le_bon_coin import *

locations = [
  33114,
  33125,
  33650,
  33720,
  33730,
  33770,
  33830,
  40160,
  40210,
  40410,
  40460,
]

for location in locations:
  insert_to_db(parse_le_bon_coin(open_search_url_for_location(str(location))))

