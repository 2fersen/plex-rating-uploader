import time
import os
import requests
import json
from tmdb_api import add_rating, add_rating_episode
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


def get_metadata(rating_key: str, media_type: str):
    print(f'[Get_metadata] - rating_key: {rating_key}, media_type: {media_type}')
    if media_type == 'movie' or media_type == 'episode':
        url = f"{base_url}/library/metadata/{rating_key}"

        res = requests.get(url, headers=headers, data=payload)
        f = res.json()['MediaContainer']['Metadata'][0]
        user_rating = f.get('userRating')
        if not user_rating and media_type == 'movie':
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
    else:
        url = f"{base_url}/library/metadata/{rating_key}/children"

        res = requests.request("GET", url, headers=headers, data=payload).json()["MediaContainer"]['Metadata']

        episode_data = []
        season_data = []
        for season in res:
            print(f'[{rating_key}] - {season["title"]} has {season["leafCount"]}. Episodes')
            season_rating = season['ratingKey']
            url = f"{base_url}/library/metadata/{season_rating}/children"
            s_res = requests.request("GET", url, headers=headers, data=payload).json()

            # if season.get('userRating'):
            #     user_rating, ids = get_metadata(season_rating, media_type="movie")
            #     season_data.append([user_rating, ids, season['guid']])

            for episode in s_res['MediaContainer']['Metadata']:
                if episode.get('userRating'):
                    season_number = episode['parentIndex']
                    episode_number = episode['index']
                    user_rating, ids = get_metadata(episode['ratingKey'], media_type="movie")
                    episode_data.append([user_rating, ids, episode['guid'], season_number, episode_number])
                else:
                    continue

        return episode_data, season_data


def get_json_reviews():
    try:
        with open(os.path.join('data', 'rating_db.json'), 'r', encoding='utf-8') as json_file:
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

                if lib_type == 'movies':
                    user_rating, ids = get_metadata(rating_key, media_type="movie")

                    if data[lib_type].get(guid):
                        if data[lib_type][guid]['tmdb'] == user_rating:
                            print(f'[{i["title"]}] Already uploaded!')
                            continue
                        else:
                            print(f'[{i["title"]}] Rating changed from {data[lib_type][guid]['tmdb']} to {user_rating}')

                    if user_rating and ids.get('tmdb'):
                        if add_rating(ids['tmdb'], user_rating, lib_type):
                            print(f'[{i["title"]}] Review {user_rating} added!')

                            if lib_type == 'show' or lib_type == 'series':
                                data[lib_type][guid] = {"title": i["title"], "tmdb": user_rating, "imdb": "",
                                                        "tvdb": "",
                                                        "episodes": {}, "season": {}}
                            else:
                                data[lib_type][guid] = {"title": i["title"], "tmdb": user_rating, "imdb": "",
                                                        "tvdb": ""}
                            time.sleep(0.25)

                elif lib_type == 'show' or lib_type == 'series':
                    _, ids = get_metadata(rating_key, media_type="episode")
                    episode_data, season_data = get_metadata(rating_key, media_type="series")

                    if not data[lib_type].get(guid):
                        data[lib_type][guid] = {"title": i["title"], "tmdb": 0, "imdb": 0, "tvdb": 0, "episodes": {},
                                                "season": {}}

                    for episode in episode_data:
                        episode_user_rating = episode[0]
                        episode_ids = episode[1]
                        episode_guid = episode[2]
                        season_number = episode[3]
                        episode_number = episode[4]

                        if data[lib_type].get(guid) and data[lib_type][guid]['episodes'].get(episode_guid):
                            if data[lib_type][guid]['episodes'][episode_guid]['tmdb'] == episode_user_rating:
                                print(f'[{i["title"]}] Episode raiting already uploaded!')
                                continue
                            else:
                                print(
                                    f'[{i["title"]}] Episode rating changed from {data[lib_type][guid]["episodes"][episode_guid]['tmdb']} to {episode_user_rating}')

                        if episode_user_rating and episode_ids.get('tmdb'):
                            add_rating_episode(ids['tmdb'], episode_user_rating, season_number, episode_number)
                            print(f'[{i["title"]}] Review {episode_user_rating} added!')

                            data[lib_type][guid]['episodes'][episode_guid] = {"tmdb": episode_user_rating, "imdb": "",
                                                                              "tvdb": ""}
                            time.sleep(0.25)

                    # for season in season_data:
                    #     season_user_rating = season[0]
                    #     season_ids = season[1]
                    #     season_guid = season[2]
                    #
                    #     if data[lib_type].get(guid) and data[lib_type][guid]['season'].get(season_guid):
                    #         if data[lib_type][guid]['season'][season_guid]["tmdb"] == season_user_rating:
                    #             print(f'[{i["title"]}] Episode raiting already uploaded!')
                    #             continue
                    #         else:
                    #             print(
                    #                 f'[{i["title"]}] Season rating changed from {data[lib_type][guid]['season'][season_guid]['tmdb']} to {season_user_rating}')
                    #
                    #     if season_user_rating and season_ids.get('tmdb'):
                    #         add_review(season_ids['tmdb'], season_user_rating, lib_type)
                    #         print(f'[{i["title"]}] Review {season_user_rating} added!')
                    #
                    #         data[lib_type][guid]['season'][season_guid] = {"tmdb": season_user_rating, "imdb": "",
                    #                                                        "tvdb": ""}
                    #         time.sleep(0.25)
                else:
                    print(f"library-type: {lib_type}")
                    raise "Unsuported library type!"
    set_json_reviews(data)
    print('Finished!')


if __name__ == '__main__':
    print('Starting rating tracker!')
    while True:
        main()
        time.sleep(run_interval_in_minutes * 60)
