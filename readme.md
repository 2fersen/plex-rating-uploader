# Plex Rating Uploader

Plex Rating Uploader is a Python script that exports rated movies and shows from Plex and automatically uploads the
ratings to TMDB (The Movie Database) on a specified cycle. It requires a Plex token and a TMDB API key. Completed
uploads are cached in a JSON database, and if a rating changes, it is updated on TMDB accordingly. I would like to
add this feature for IMDB and TVDB as well, but IMDB does not seem to work at the moment, I will check TVDB soon.

## Features

- Automatically upload ratings from Plex to TMDB
- Upload movie, series and episode ratings
- Cache completed uploads in a JSON database
- Update ratings on TMDB when they change in Plex in the next configured cycle
- Configurable upload interval
- Dockerized for easy deployment
- soon rating of single series/show episodes

## Soon added features
- synchronize watchlist from TMDB to Plex and Plex to TMDB
- synchronize TMDB ratings to plex
- maybe add trakt support

## Prerequisites
- Python 3.x
- Plex token
- TMDB API key

## Setup

1. Get the Plex-Token

   Go to any of your libraries, click on any media, then click on "Get Info", then "View XML". Then you should get a
   long url, at the end of it
   you will find your Plex token. It should look like this: M1CPccYc-uHHnC1BBdc (of course this is not a valid token)

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

1. Pull the Docker container from GitHub:

   ```
   git clone https://github.com/2fersen/plex-rating-uploader
   ```

2. Setup the docker-compose.yml file so the container keeps running:

   Change the path to data folder from the cloned directory like this:

   ```
       volumes:
         - C:\Users\.....\data:/data
   ```

3. Update the .env with your keys and settings:
   Change the filename from:
   ```
   template.env_template
   ```

   To:
   ```
   .env
   ```

4. Run the container:
   ```
   docker-compose up -d
   ```
   ### Thats it!

5. For updating the container:
   ```
   sudo docker-compose down
   sudo docker-compose build --no-cache
   sudo docker-compose up -d
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
