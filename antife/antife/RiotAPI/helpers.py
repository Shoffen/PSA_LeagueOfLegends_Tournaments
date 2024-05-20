import requests
from urllib.parse import urlencode
import antife.RiotAPI.settings as settings


def get_account_by_riot_id(summoner_name, tag_line, region=settings.DEFAULT_REGION):
    """
    Wrapper for ACCOUNT-V1 API portal
    Gets information about an account by their their summoner name and tag line
    :return: Account information as a dictionary or None if there's an issue
    """

    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None


def get_summoner_ids(puuid, region_code=settings.DEFAULT_REGION_CODE):
    """
    Wrapper for SUMMONER-V4 API portal
    Gets information about a summoner by their name
    :return: Summoner information as a dictionary or None if there's an issue
    """

    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region_code}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None


def get_summoner_info(summoner_name, tag_line, region=settings.DEFAULT_REGION, region_code=settings.DEFAULT_REGION_CODE, ):
    """
    Wrapper for LEAGUE-V4 API portal
    Gets information about a summoner by their name and tagline
    :return: Summoner information as a dictionary or None if there's an issue
    """

    puuid = get_account_by_riot_id(summoner_name, tag_line, region)['puuid']
    id = get_summoner_ids(puuid, region_code)['id']


    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region_code}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None

def get_match_ids(summoner_name, tag_line, match_count=5, region=settings.DEFAULT_REGION):
    """
    Wrapper for MATCH-V5 API portal
    Gets match ids depending on the count by summoner name and tag line
    :return: Match ids as a dictionary or None if there's an issue
    """

    puuid = get_account_by_riot_id(summoner_name, tag_line, region)['puuid']
    params = {
        'count': match_count,
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None

def get_match(matchId, region=settings.DEFAULT_REGION, region_code=settings.DEFAULT_REGION_CODE):
    """
    Wrapper for MATCH-V5 API portal
    Gets a match by it's match id
    :return: All match statistics, for every single player and overall match information
    """
    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None


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

    # Extract match duration and start time
    match_duration_seconds = match['info']['gameDuration']  # Duration of the match in seconds
    match_start_time = match['info']['gameStartTimestamp']  # Start time of the match (Unix timestamp)

    # Convert match duration from seconds to minutes and seconds
    match_duration_minutes = match_duration_seconds // 60
    match_duration_seconds_remainder = match_duration_seconds % 60

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
        'win': win,
        'matchDurationMinutes': match_duration_minutes,
        'matchDurationSeconds': match_duration_seconds_remainder,
        'matchStartTime': match_start_time
    }
