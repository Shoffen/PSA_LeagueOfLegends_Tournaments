from helpers import get_summoner_info, get_match_ids

summoner_name = "HKavav"
tag_line = "EUN1"


rank = get_summoner_info(summoner_name, tag_line)
print(rank)

match_ids = get_match_ids(summoner_name, tag_line)

print(match_ids)