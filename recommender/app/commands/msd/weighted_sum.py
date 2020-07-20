
songs = ["a", "b", "c"]

songs_similarity = {
    "a": { "a": 1, "b": 0.3, "c": 0.2 },
    "b": { "a": 0.3, "b": 1, "c": 0.9 },
    "c": { "a": 0.2, "b": 0.9, "c": 1 },
}


listens = {
    "user1": ["a", "b"],
    "user2": ["c"],
    "user3": ["b"]
}


def score(user, target_song):
    score = 0
    for song in songs:
        similarity = songs_similarity[target_song][song]
        score += similarity * int(song in listens[user])

    return score


print(score("user3", "a"))
