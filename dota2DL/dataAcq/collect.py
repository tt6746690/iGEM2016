API_KEY = 'BE591D102BD4B3652CB310A39F7EA79C'

import dota2api
api = dota2api.Initialise(API_KEY)
match = api.get_match_details(match_id=1000193456)
print match
