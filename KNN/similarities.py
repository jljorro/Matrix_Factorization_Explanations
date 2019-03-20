import pandas as pd
import numpy as np

from scipy.spatial.distance import pdist, squareform
from scipy.spatial.distance import euclidean, cosine, cityblock


def get_binary_similarity_matrix():
    binary_prop = pd.read_csv('data/experiment_data/movies_binary.csv')
    
    movies_prop = binary_prop.drop(columns=['id']).values
    movies_sim_values = pdist(movies_prop, equal_sim)
    movies_similarity = pd.DataFrame(squareform(movies_sim_values))
    
    return movies_similarity


def get_similarity_matrix(user, similarity_function):    
    q_path = 'data/matrices_data/q_user_{}.csv'.format(user)
    q_u = pd.read_csv(q_path)
    
    movies_prop = q_u.drop(columns=['movieId']).values
    movies_sim_values = pdist(movies_prop, similarity_function)
    movies_similarity = pd.DataFrame(squareform(movies_sim_values))
    
    return movies_similarity


# Creamos la función de similitud
# ¡OJO! Para evitar similitudes muy altas (debido a la cantidad de ceros)
# solo contamos, para la similitud, las propiedades que tengan valor 1 en
# alguno de los items.
def equal_sim(item1, item2):
    equ = np.sum(np.logical_and(item1, item2))
    atr = np.sum(np.logical_or(item1, item2))
    
    ''' 
    for i in range(len(item1)):
        if item1[i] != item2[i]:
            dif = dif + 1
        if item1[i] == 1 or item2[i] == 1:
            atr = atr + 1
    '''
    return float(equ) / float(atr)


def euclidean_sim(item1, item2):
    return 1 / (1 + euclidean(item1, item2))


def cosine_sim(item1, item2):
    return 1 / (1 + cosine(item1, item2))


def manhattan_sim(item1, item2):
    return 1 / (1 + cityblock(item1, item2))