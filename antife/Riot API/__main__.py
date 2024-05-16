from helpers import get_summoner_info, get_match_ids, get_match, get_account_by_riot_id

summoner_name = "HKavav"
tag_line = "EUNE"
summoner_puuid = get_account_by_riot_id(summoner_name, tag_line)['puuid']

# IF THIS DOESN'T WORK
# Update API key with new one in settings.py (expires every 24 hours)
#
# make sure the regional things match the correct region in settings.py


# gets basic summoner information such as results of last 5 matches and rank
summoner = get_summoner_info(summoner_name, tag_line)
print(summoner)

# gets match ids, count default value 5
match_ids = get_match_ids(summoner_name, tag_line, 2)

# Gets our players statistics in a match
match = get_match(match_ids[0])
if summoner_puuid in match['metadata']['participants']:     # Checking if our player was in this match
    player_index = match['metadata']['participants'].index(summoner_puuid)      # Finding index of our player
else:
    None
player_match_statistics = match['info']['participants'][player_index] # Grabs all the data associated with the player
print(player_match_statistics)
print(match['info']['participants'][player_index]['win']) # example usage to check if the player won

