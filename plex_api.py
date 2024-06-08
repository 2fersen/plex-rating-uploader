import time
import os
import requests
import json
from tmdb_api import add_review
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join('data', '.env'))
plex_token = os.environ.get('PLEX_TOKEN')

if not plex_token:
    raise 'Missing Plex token!'

run_interval_in_minutes = os.environ.get('RUN_INTERVAL_IN_MINUTES')

if not run_interval_in_minutes.isnumeric():
    raise 'Incorrect value for RUN_INTERVAL_IN_MINUTES'
else:
    run_interval_in_minutes = int(run_interval_in_minutes)

base_url = os.environ.get('BASE_URL')
payload = {}
headers = {
    'Accept': 'application/json',
    'X-Plex-Token': plex_token
}


def get_all_libraries():
    global payload, headers
    url = f"{base_url}/library/sections"

    res = requests.request("GET", url, headers=headers, data=payload)

    libs = {"series": [], 'movies': []}

    try:
        for i in res.json()['MediaContainer']['Directory']:
            lib_type = i['type']

            if lib_type == 'show':
                libs["series"].append(i['key'])
            elif lib_type == 'movie':
                libs["movies"].append(i['key'])
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError(f"Are you sure you added the correct X-Plex-Token? Your current token is '{plex_token}'")
    return libs


def get_library(lib_key: str):
    global payload, headers
    url1 = f"{base_url}/library/sections/{lib_key}/all"

    res = requests.request("GET", url1, headers=headers, data=payload)
    lib = res.json()['MediaContainer']['Metadata']

    return lib


def get_metadata(rating_key: str):
    url = f"{base_url}/library/metadata/{rating_key}"

    res = requests.get(url, headers=headers, data=payload)
    f = res.json()['MediaContainer']['Metadata'][0]
    user_rating = f.get('userRating')
    if not user_rating:
        return None, None

    ids = {"tmdb": None, "imdb": None, "tvdb": None}
    for i in f['Guid']:
        idd = i["id"]
        if "imdb" in idd:
            ids["imdb"] = idd.replace('imdb://', '')
        elif "tmdb" in idd:
            ids["tmdb"] = idd.replace('tmdb://', '')
        elif "tvdb" in idd:
            ids["tvdb"] = idd.replace('tvdb://', '')

    return user_rating, ids


def get_json_reviews():
    try:
        with open(os.path.join('data', 'rating_db.json'), 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print('Json file not found, creating new one')
        data = {"series": {}, "movies": {}}
        return data


def set_json_reviews(data: dict):
    with open(os.path.join('data', 'rating_db.json'), 'w', encoding='utf-8') as save:
        json.dump(data, indent=4, fp=save, ensure_ascii=False)


def main():
    data = get_json_reviews()
    libs = get_all_libraries()

    for lib_type, lib_keys in libs.items():
        for c_lib in lib_keys:
            library = get_library(c_lib)

            for i in library:
                rating_key = i['ratingKey']
                guid = i['guid']
                user_rating, ids = get_metadata(rating_key)

                if data[lib_type].get(guid):
                    if data[lib_type][guid]['tmdb'] == user_rating:
                        print(f'[{i["title"]}] Already uploaded!')
                        continue

                if user_rating is not None and ids.get('tmdb'):
                    add_review(ids['tmdb'], user_rating, lib_type)
                    print(f'[{i["title"]}] Review {user_rating} added!')

                    if lib_type == 'show' or lib_type == 'series':
                        data[lib_type][guid] = {"tmdb": user_rating, "imdb": "", "tvdb": "", "childs": {}}
                    else:
                        data[lib_type][guid] = {"tmdb": user_rating, "imdb": "", "tvdb": ""}
                    time.sleep(0.25)
                else:
                    pass
    set_json_reviews(data)
    print('Finished!')


print('Starting rating tracker!')
while True:
    main()
    time.sleep(run_interval_in_minutes * 60)
