"""
MSD H5 to csv converter
Modifies code in https://github.com/AumitLeon/million-songs/blob/master/get_data.py
"""
import os
import csv
import pandas as pd
import json
from . import hdf5_getters

track_to_file = {}

songid_to_trackid = {}


def find(songid, data_dir):
    global track_to_file
    global songid_to_trackid

    if not songid_to_trackid:
        songid_to_trackid = _load_song_to_track_map()

    if not track_to_file:
        track_to_file = _load_song_files(data_dir)

    try:
        trackid = songid_to_trackid[songid]
        return track_to_file[trackid]
    except KeyError:
        raise SongNotFound


class SongNotFound(Exception):
    pass


def load(csv_filepath):
    return pd.read_csv(csv_filepath)


def to_csv(data_dir, out_filepath):
    # Open the CSV file we will write to
    with open(out_filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "track_id", "artist_id", "artist_mbid",
            "artist_name", "title", "artist_location", "release", "hotness",
            "familiarity", "danceability", "duration", "energy", "loudness",
            "year", "tempo", "analysis_rate", "end_of_fade_in", "key",
            "artist_mbrainz_tags", "artist_echonest_tags"]
            # "key_confidence", "mode", "mode_confidence",
            # "start_of_fade_out", "time_signature",
            # "time_signature_conf"]
        )

        writer.writeheader()

        # Recursively visit each sub-dir till we reach the h5 files
        # Strip punctuation from features that are strings

        BATCH_SIZE = 100

        batch = []

        for root, dirs, filenames in os.walk(data_dir):
            for f in filenames:
                h5 = hdf5_getters.open_h5_file_read(os.path.join(root, f))
                num_songs = hdf5_getters.get_num_songs(h5)

                for i in range(num_songs):
                    # Field list: http://millionsongdataset.com/pages/field-list/
                    track_id = hdf5_getters.get_track_id(
                        h5, songidx=i).decode()
                    artist_id = hdf5_getters.get_artist_id(
                        h5, songidx=i).decode()
                    artist_mbid = hdf5_getters.get_artist_mbid(
                        h5, songidx=i).decode()
                    artist = hdf5_getters.get_artist_name(
                        h5, songidx=i).decode()
                    title = hdf5_getters.get_title(
                        h5, songidx=i).decode()
                    artist_loc = hdf5_getters.get_artist_location(
                        h5, songidx=i).decode()
                    release = hdf5_getters.get_release(
                        h5, songidx=i).decode()
                    hotness = hdf5_getters.get_artist_hotttnesss(
                        h5, songidx=i)
                    familiarity = hdf5_getters.get_artist_familiarity(
                        h5, songidx=i)
                    danceability = hdf5_getters.get_danceability(
                        h5, songidx=i)
                    duration = hdf5_getters.get_duration(
                        h5, songidx=i)
                    energy = hdf5_getters.get_energy(
                        h5, songidx=i)
                    loudness = hdf5_getters.get_loudness(
                        h5, songidx=i)
                    year = hdf5_getters.get_year(
                        h5, songidx=i)
                    tempo = hdf5_getters.get_tempo(
                        h5, songidx=i)
                    analysis_rate = hdf5_getters.get_analysis_sample_rate(
                        h5, songidx=i)
                    end_of_fade_in = hdf5_getters.get_end_of_fade_in(
                        h5, songidx=i)
                    key = hdf5_getters.get_key(
                        h5, songidx=i)
                    key_confidence = hdf5_getters.get_key_confidence(
                        h5, songidx=i)
                    mode = hdf5_getters.get_mode(
                        h5, songidx=i)
                    mode_confidence = hdf5_getters.get_mode_confidence(
                        h5, songidx=i)
                    start_of_fade_out = hdf5_getters.get_start_of_fade_out(
                        h5, songidx=i)
                    time_signature = hdf5_getters.get_time_signature(
                        h5, songidx=i)
                    time_signature_conf = hdf5_getters.get_time_signature_confidence(
                        h5, songidx=i)
                    artist_mbrainz_tags = [
                        tag.decode() for tag in hdf5_getters.get_artist_mbtags(
                            h5, songidx=i)
                    ]
                    artist_echonest_tags = [
                        tag.decode() for tag in hdf5_getters.get_artist_terms(
                            h5, songidx=i)
                    ]

                    batch.append({
                        "artist_id": artist_id,
                        "artist_mbid": artist_mbid,
                        "track_id": track_id,
                        "artist_name": artist,
                        "title": title,
                        "artist_location": artist_loc,
                        "release": release,
                        "hotness": hotness,
                        "familiarity": familiarity,
                        "danceability": danceability,
                        "duration": duration,
                        "energy": energy,
                        "loudness": loudness,
                        "year": year,
                        "tempo": tempo,
                        "analysis_rate": analysis_rate,
                        "end_of_fade_in": end_of_fade_in,
                        "key": key,
                        "artist_mbrainz_tags": artist_mbrainz_tags,
                        "artist_echonest_tags": artist_echonest_tags
                    })

                    if len(batch) == BATCH_SIZE:
                        writer.writerows(batch)
                        batch = []

                h5.close()

                # Print the current song and arists:
                print(f"{artist} - {title}")


def _load_song_files(data_dir):
    index_filepath = "./data/song-file-map.json"
    files_by_trackid = {}

    try:
        with open(index_filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        print("Building tracks to files index file...")
        for root, dirs, filenames in os.walk(data_dir):
            for f in filenames:
                # TODO Review taste_profile_song_to_tracks
                filename = os.path.join(root, f)
                h5 = hdf5_getters.open_h5_file_read(filename)
                num_songs = hdf5_getters.get_num_songs(h5)

                for i in range(num_songs):
                    track_id = hdf5_getters.get_track_id(
                        h5, songidx=i).decode()

                    files_by_trackid[track_id] = (filename, i)

                h5.close()

        with open("./data/song-file-map.json", "w") as f:
            json.dump(files_by_trackid, f)

        return files_by_trackid


def _load_song_to_track_map():
    filepath = "./data/msdchallenge/kaggle_challenge_files/taste_profile_song_to_tracks.txt"

    with open(filepath, "r") as f:
        data = {}
        for row in f.readlines():
            ids = row.strip().split("\t")[:2]
            if len(ids) == 2:
                songid, trackid = ids
                data[songid] = trackid

        return data
