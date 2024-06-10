import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join('data', '.env'))

tmdb_api_key = os.environ.get('TMDB_API_KEY')

if not tmdb_api_key:
    raise 'Missing TMDB api key!'

base_url = 'https://api.themoviedb.org'
api_key = f"Bearer {tmdb_api_key}"


def add_rating(video_id: str, rating: int | str | float, lib_type: str):
    print(f'[TMDB-API] - Video-ID: {video_id}, Raiting: {rating}, Library-Type: {lib_type}')
    if lib_type == 'show' or lib_type == 'series':
        lib_type = 'tv'
    elif lib_type == 'movies':
        lib_type = 'movie'
    else:
        raise f'Wrong library type: "{lib_type}'

    url = f"{base_url}/3/{lib_type}/{video_id}/rating"

    payload = "{\"value\"" + f':{rating}' + "}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": api_key
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 201:
        return True
    else:
        print(f"TMDB error status message: {response.json()['status_message']}")
        raise "TMDB API error"


def add_rating_episode(video_id: str, rating: int | str | float, season, episode):
    """
    https://developer.themoviedb.org/reference/tv-episode-add-rating
    """

    url = f"{base_url}/3/tv/{video_id}/season/{season}/episode/{episode}/rating"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": api_key
    }

    payload = "{\"value\"" + f':{rating}' + "}"

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 201:
        return True
    else:
        print(f"TMDB error status message: {response.json()['status_message']}")
        raise "TMDB API error"
