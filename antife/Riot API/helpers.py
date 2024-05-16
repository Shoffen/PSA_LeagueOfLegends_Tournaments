import requests
from urllib.parse import urlencode
import settings


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