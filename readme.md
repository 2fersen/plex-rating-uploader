# Plex Rating Uploader

Plex Rating Uploader is a Python script that exports rated movies and shows from Plex and automatically uploads the
ratings to TMDB (The Movie Database) on a specified cycle. It requires a Plex token and a TMDB API key. Completed
uploads are cached in a JSON database, and if a rating changes, it is updated on TMDB accordingly. I would like to 
add this feature for IMDB and TVDB as well, but IMDB does not seem to work at the moment, I will check TVDB soon.

## Features

- Automatically upload ratings from Plex to TMDB
- Cache completed uploads in a JSON database
- Update ratings on TMDB if they change in Plex
- Configurable upload interval
- Dockerized for easy deployment
- soon rating of single series/show episodes

## Prerequisites

- Python 3.x
- Plex token
- TMDB API key


## Setup

1. Get the Plex-Token

   ```
   Press F12 to open up the developer console, and then click on the settings icon. 
   
   After that, click in the name section on one of the requests (yellow marked):
   requests?X-Plex-Product=Plex ...
   users?X-Plex-Product=Plex ...
   
   After that klick on the payload tab, there you can find your X-Plex-Token
   ```

![Screenshot](/screenshots/1.JPG)

![Screenshot](/screenshots/2.JPG)

2. Get the TMDB API key
   ```
   To get the TMDB api klick on the link below, register and just fill out the form with random things, for the url you need to provide, just add plex.tv or anything else.
   
   You will need the "API Read Access Token" not the "API Key"
   ```
   [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

## Installation
### Docker

1. Pull the Docker image:

   ```
   docker pull 2fersen/plex-rating-uploader
   ```

2. Run the container:

Create or download a folder named "data" with two files: "rating_db.json" and ".env".

If you create it yourself, populate the "rating_db.json" file with the following content:
```
{"series": {}, "movies": {}}
```

The ".env" file should look like this, but make sure to fill in your own values for the variables:
```
PLEX_TOKEN=YOUR-X-Plex-Token
TMDB_API_KEY=API-Read-Access-Token
RUN_INTERVAL_IN_MINUTES=60
BASE_URL=http://192.168.50.226:32400
```

After that, copy the path to the "data" folder where both files are located, and you'll be ready to proceed with the following command:
```
docker run -it -v "path\to\your\data":/data 2fersen/plex-rating-uploader
```

### Manual

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Edit the `.env` file with your Plex token and TMDB API key:

   ```
   PLEX_TOKEN=YOUR-X-Plex-Token
   TMDB_API_KEY=API-Read-Access-Token
   RUN_INTERVAL_IN_MINUTES=60
   BASE_URL=http://192.168.50.226:32400
   ```

4. Run the script:

   ```
   python plex_api.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
