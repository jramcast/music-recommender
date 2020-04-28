

def msd_average_precision(
    recommended_songs_for_user,
    user_library,
    rank_limit=500
):
    """
    Calculates average precision as in:
    The Million Song Dataset Challenge, McFee, B., Bertin-Mahieux. T., Ellis, D.P.W., and Lanckriet, G.R.G.
    4th International Workshop on Advances in Music Information Research (AdMIRe)
    https://bmcfee.github.io/papers/msdchallenge.pdf
    """

    library_length = len(user_library)
    num_positives = 0
    score = 0
    recommended_songs_for_user = recommended_songs_for_user[:rank_limit]
    for i, song in enumerate(recommended_songs_for_user):
        if song in user_library:
            num_positives += 1
            score += num_positives/(i+1)

    return score / min(library_length, rank_limit)


def msd_mAP(users, recommendations, user_libraries, rank_limit=500):
    score = 0

    for userid, recommendations_for_user in enumerate(recommendations):
        if not users[userid] in user_libraries:
            continue

        user_library = user_libraries[users[userid]]
        score += msd_average_precision(
            recommendations_for_user,
            user_library,
            rank_limit)

    return score / len(users)
