import requests
from urllib.parse import urlencode
import settings


def get_account_by_riot_id(summoner_name, tag_line):
    """
    Wrapper for ACCOUNT-V1 API portal
    Gets information about an account by their their summoner name and tag line
    :return: Account information as a dictionary or None if there's an issue
    """

    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None


def get_summoner_info(summoner_name, region=settings.DEFAULT_REGION_CODE):
    """
    Wrapper for SUMMONER-V4 API portal
    Gets information about a summoner by their name
    :return: Summoner information as a dictionary or None if there's an issue
    """

    params = {
        'api_key': settings.API_KEY
    }

    api_url = f"https://{region}.api.riotgames.com/riot/summoner/v4/summoners/by-name/{summoner_name}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None
