import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join('data', '.env'))

tmdb_api_key = os.environ.get('TMDB_API_KEY')

if not tmdb_api_key:
    raise 'Missing TMDB api key!'

base_url = 'https://api.themoviedb.org'
api_key = f"Bearer {tmdb_api_key}"


def add_review(video_id: str, raiting: str, lib_type: str):
    if lib_type == 'show' or lib_type == 'series':
        lib_type = 'tv'
    elif lib_type == 'movies':
        lib_type = 'movie'
    else:
        raise f'Wrong library type: "{lib_type}'

    url = f"{base_url}/3/{lib_type}/{video_id}/rating"

    payload = "{\"value\"" + f':{raiting}' + "}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": api_key
    }

    response = requests.post(url, data=payload, headers=headers)

    # print(response.json()['status_message'])
    if response.status_code == 201:
        return True
    else:
        return False
