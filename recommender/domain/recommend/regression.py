class RegressionRecommender:

    def __init__(self, user_to_songs_train, user_to_songs_eval, songs):
        self.training_set = user_to_songs_train
        self.evaluation_set = user_to_songs_eval

    def train(self):
        pass
        # for userid, songids in enumerate(self.training_set):
        #     print(userid, songids)
