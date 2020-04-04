# music-recommender
Music recommendation experiments


# Bring up the DB

Stop your local mongo service:

```sh
sudo service mongod stop
```

Then run the dockerized mongo

```sh
pipenv run mongo
```

# Data download

To download data from last.fm, use:

```sh
pipenv run ./download_lastfm.py
```

Then, to download acoustic info for each song from spotify, run

```sh
pipenv run ./download_spotify.py
```

## Experiments

Use one of the commands in `recommender/app/commands`, for example:

```sh
pipenv run python recommender/app/commands/train_max_likelooh_recommender.py
```