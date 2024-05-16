from helpers import get_summoner_info

summoner_name = "HKavav"
tag_line = "EUN1"


rank = get_summoner_info(summoner_name, tag_line)
print(rank)