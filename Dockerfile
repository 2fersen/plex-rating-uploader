FROM python:3.12-alpine

#ENV PLEX_TOKEN="X-Plex-Token"
#ENV TMDB_API_KEY="API-Read-Access-Token"
#ENV RUN_INTERVAL_IN_MINUTES="60"
#ENV BASE_URL="http://192.168.50.226:32400"

COPY plex_api.py .
COPY tmdb_api.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data

CMD ["python", "plex_api.py"]