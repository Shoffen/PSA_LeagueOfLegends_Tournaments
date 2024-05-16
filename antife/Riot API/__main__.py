from helpers import get_summoner_info, get_match_ids, get_player_statistics_in_match, get_account_by_riot_id

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

player_statistics = get_player_statistics_in_match(match_ids[0], summoner_puuid)
print(player_statistics)



