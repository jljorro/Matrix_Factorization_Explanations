from surprise import Dataset
from surprise import Reader
from surprise import NMF
import src.similarities as sim

from scipy.spatial.distance import pdist, squareform

import numpy as np

class NMF_XAI:

    def __init__(self):
        self.recommendation_algorithm = NMF()
        pass

    def _create_user_item_dictionary(self, training_df):
        uniques_users = np.unique(training_df['userId'].values)
        uniques_movies = np.unique(training_df['movieId'].values)

        self.users_dict = {}
        for i in range(len(uniques_users)):
            self.users_dict[uniques_users[i]] = i 

        self.movies_dict = {}
        for i in range(len(uniques_movies)):
            self.movies_dict[uniques_movies[i]] = i
        

    def fit(self, training_df, movies_attr_df):
        # Save data
        self.training_df = training_df
        self.movies_attr_df = movies_attr_df
        self._create_user_item_dictionary(training_df)

        # Prepare the training data
        reader = Reader(rating_scale=(1,5))
        train_data = Dataset.load_from_df(training_df, reader).build_full_trainset()

        # Train the model
        self.recommendation_algorithm.fit(train_data)

        # Obtain Q and P matrices
        self.Q = self.recommendation_algorithm.qi
        self.P = self.recommendation_algorithm.pu

    def predict(self, user_id, movie_id):
        return self.recommendation_algorithm.estimate(user_id, movie_id)

    def _get_movies_preview(self, user_id):
        return self.training_df[self.training_df['userId'] == user_id]['movieId'].values

    def get_examples(self, user_id, movie_id, n=10):
        # Get movies preview by the user
        movies_preview = self._get_movies_preview(user_id)
        movies = np.append(movies_preview, movie_id) # Add the movie to predict
        movies_index = [self.movies_dict[movie_id] for movie_id in movies]

        # Get the user and movie latent factors
        pu = self.P[self.users_dict[user_id]]
        qi = self.Q[movies_index]

        # Compute the qu matrix
        qui = pu * qi
    
        # Calculate similarity
        movies_sim = squareform(pdist(qui, sim.cosine_sim))
        movies_order = movies_sim[-1].argsort()[::-1]
        movies_order = movies_order[:-1] # Remove the movie recommended

        return movies_preview[movies_order[:n]]