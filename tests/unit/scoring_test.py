from recommender.domain.scoring import msd_average_precision


def test_ap_1():
    recommendation = [1, 2, 3]
    actual = [1, 2, 3]

    ap = msd_average_precision(recommendation, actual)

    assert ap == 1


def test_ap_0():
    recommendation = [4, 5, 6]
    actual = [1, 2, 3]

    ap = msd_average_precision(recommendation, actual)

    assert ap == 0


def test_ap():
    recommendation = [5, 6, 1, 2, 3]
    actual = [1, 2, 3, 5, 6]

    ap = msd_average_precision(recommendation, actual)

    assert ap == 0.8