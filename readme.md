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

   ```
   [Unit]
   Description=Plex Rating Uploader
   Requires=docker.service
   After=docker.service
   
   [Service]
   WorkingDirectory=/opt/plex-rating-uploader
   ExecStart=/usr/local/bin/docker-compose up
   ExecStop=/usr/local/bin/docker-compose down
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   ```
   sudo systemctl daemon-reload
   sudo systemctl enable plex-rating-uploader
   sudo systemctl start plex-rating-uploader
   ```

Ich habe ein python script geschrieben, welches von plex bewertete serien und filme exportiert und die bewertungen
automatisch nach einem gewissen zyklus zu tmdb uploaded. Hierfür wird ein Plex-token und ein TMDB api schlüssel
benötigt. bereits erledigte uploads werden zwischengespeichert in einer json datenbank, falls sich die bewertung ändert,
wird die bewertung natürlich auch wieder auf tmdb angepasst. Ich plane außerdem den script für IMDB sowie TVDB zu
erweitern.

Ich habe hierfür auch einen docker container erstellt er heißt: "plex-rating-uploader" es ist möglich in dem Dockerfile
seinen plex token einzufügen oder man wird beim ersten ausführen dazu aufgefordert. Das Intervall für den upload lässt
sich auch bei der installation per docker in minuten festlegen

kannst du mir hierfür eine readme.md datei für github erstellen? ich benötige nur ein beispieldatei. Bitte auf englisch

[Unit]
Description=Plex Rating Uploader Service
Requires=docker.service
After=docker.service

[Service]
Restart=always
WorkingDirectory=/path/to/your/compose/directory
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

Ersetzen Sie `/path/to/your/compose/directory` durch das tatsächliche Verzeichnis, in dem sich Ihre `docker-compose.yml` Datei befindet.

2. Aktualisieren Sie die Systemd-Konfiguration, um den neuen Service zu laden:

```
sudo systemctl daemon-reload
```

3. Starten Sie den Service und aktivieren Sie ihn, um ihn beim Systemstart auszuführen:

```
sudo systemctl start plex-rating-uploader.service
sudo systemctl enable plex-rating-uploader.service
```