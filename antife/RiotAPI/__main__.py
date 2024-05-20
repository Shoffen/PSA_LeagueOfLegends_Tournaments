from helpers import get_summoner_info, get_match_ids, get_player_statistics_in_match, get_account_by_riot_id

summoner_name = "LAFLAMEIVN"
tag_line = "EUNE"
summoner_puuid = get_account_by_riot_id(summoner_name, tag_line)['puuid']
print(summoner_puuid)

# IF THIS DOESN'T WORK
# Update API key with new one in settings.py (expires every 24 hours)
#
# make sure the regional things match the correct region in settings.py


summoner = get_summoner_info(summoner_name, tag_line)
if summoner:
    # Access the first dictionary in the list
    first_entry = summoner[0]
    # Get the tier value from the dictionary
    tier = first_entry.get('tier', 'unranked')
    print("Summoner Tier:", tier)
else:
    print("Summoner not found or API request failed.")

# gets match ids, count default value 5
match_ids = get_match_ids(summoner_name, tag_line, 5)  # Get 5 match IDs

for match_id in match_ids:
    player_statistics = get_player_statistics_in_match(match_id, summoner_puuid)
    print(player_statistics)



