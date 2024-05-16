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

def get_player_statistics_in_match(match_id, summoner_puuid):
    # Gets our player's statistics in a match
    match = get_match(match_id)
    if summoner_puuid in match['metadata']['participants']:  # Checking if our player was in this match
        player_index = match['metadata']['participants'].index(summoner_puuid)  # Finding index of our player
    else:
        return None  # Return None if player not found in the match

    player_match_statistics = match['info']['participants'][
        player_index]  # Grabs all the data associated with the player

    # Extracting required values
    champion_name = player_match_statistics['championName']
    champ_level = player_match_statistics['champLevel']
    kills = player_match_statistics['kills']
    deaths = player_match_statistics['deaths']
    assists = player_match_statistics['assists']
    lane = player_match_statistics['lane']
    total_damage_dealt = player_match_statistics['totalDamageDealt']
    total_damage_taken = player_match_statistics['totalDamageTaken']
    total_minions_killed = player_match_statistics['totalMinionsKilled']
    wards_killed = player_match_statistics['wardsKilled']
    wards_placed = player_match_statistics['wardsPlaced']
    win = player_match_statistics['win']

    return {
        'championName': champion_name,
        'champLevel': champ_level,
        'kills': kills,
        'deaths': deaths,
        'assists': assists,
        'lane': lane,
        'totalDamageDealt': total_damage_dealt,
        'totalDamageTaken': total_damage_taken,
        'totalMinionsKilled': total_minions_killed,
        'wardsKilled': wards_killed,
        'wardsPlaced': wards_placed,
        'win': win
    }


print(get_player_statistics_in_match(match_ids[0], summoner_puuid))



