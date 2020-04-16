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

## Conda env

I'm switching to conda. To activate the environment, run:

```
conda activate music-recommender
```

Conda cheatsheet:  https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf

## Experiments

Use one of the commands in `recommender/app/commands`, for example:

```sh
pipenv run python recommender/app/commands/train_max_likelooh_recommender.py
```

If using conda, first activate the env, and then run the command as usual

```sh
python recommender/app/commands/run_msd_recommendation.py
```