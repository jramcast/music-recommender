from recommender.domain.artist import Artist
import pylast
from typing import Iterable, List
from ..domain.track import Track


class LastFMListeningRepository:

    def __init__(self, apikey, apisecret, username) -> None:

        self.lastfm = pylast.LastFMNetwork(
            apikey,
            apisecret,
        )
        self.username = username

    def get_tracks(self) -> Iterable[Track]:
        user = self.lastfm.get_user(self.username)
        rawtracks: List[pylast.PlayedTrack] = user.get_recent_tracks()
        return [self.as_track(t) for t in rawtracks]

    def as_track(self, raw: pylast.PlayedTrack) -> Track:

        raw_artist: pylast.Artist = raw.track.artist

        print(raw.track.artist)
        artist = Artist(
            raw.track.artist.name,
            raw_artist.get_mbid(),
        )
        return Track(
            artist,
            raw.track.title
        )



# # Now you can use that object everywhere
# user = lastfm.get_user("jimmydj2000")
# print(user)

# print("TRack")
# track = lastfm.get_track("Vangelis", "Tears in the rain")

# print(track)
# print(track.get_wiki_summary())


# loved_tracks = user.get_loved_tracks(limit=5)
# print("loved tracks count", len(loved_tracks))

# print("LOVED TRACKS")
# for loved in loved_tracks:
#     pprint(loved.track.get_mbid())
#     print(loved.track.artist, loved.track.title)
#     print('************************')

# print("TOP TAGS")
# print([(each.item.name, each.weight) for each in user.get_top_tags()])