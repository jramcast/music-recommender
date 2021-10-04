# music-recommender
Music recommendation experiments


# Bring up the DB

Then run the  mongo container

```sh
make mongo
```

# Data download

To download data from last.fm, use:

```sh
python -m recommender.bin.download_lastfm
```

Then, to download acoustic info for each song from spotify, run

```sh
pipenv run ./download_spotify.py
```

## Experiments

Use one of the commands in `recommender/app/commands`, for example:

```sh
python recommender/app/commands/train_max_likelooh_recommender.py
```

If using conda, first activate the env, and then run the command as usual

```sh
python recommender/app/commands/run_msd_recommendation.py
```