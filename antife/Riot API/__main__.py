from helpers import get_summoner_info, get_account_by_riot_id

summoner_name = "HKavav"
tag_line = "EUNE"

summoner = get_account_by_riot_id(summoner_name, tag_line)
print(summoner['puuid'])