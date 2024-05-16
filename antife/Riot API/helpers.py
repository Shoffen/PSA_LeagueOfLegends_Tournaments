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


def get_summoner_ids(puuid, region=settings.DEFAULT_REGION_CODE):
    """
    Wrapper for SUMMONER-V4 API portal
    Gets information about a summoner by their name
    :return: Summoner information as a dictionary or None if there's an issue
    """

    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None


def get_summoner_info(summoner_name, tag_line, region=settings.DEFAULT_REGION_CODE):
    """
    Wrapper for SUMMONER-V4 API portal
    Gets information about a summoner by their name
    :return: Summoner information as a dictionary or None if there's an issue
    """

    summoner = get_account_by_riot_id(summoner_name, tag_line)
    id = get_summoner_ids(summoner['puuid'])


    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id['id']}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None