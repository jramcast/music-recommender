
from recommender.domain.track import Track
from server import tracks


def test_main_works():
    for t in tracks:
        assert_valid_track(t)


def test_tracks_length_is_x():
    for t in tracks:
        print("ti", t)
    # print(list(tracks))
    assert len(list(tracks)) == 5


def assert_valid_track(t: Track):
    assert isinstance(t, Track)
    assert len(t.name) > 0
    assert len(t.artist.name) > 0
    assert t.artist.mbid is None or len(t.artist.mbid) > 0
