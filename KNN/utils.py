import pandas as pd
import numpy as np
import statistics

def rating_dif(row):
    """
        Funcion que crea una columna con las diferencias entre los ratings reales del item y los ratings de los items
        similares
    """
    #print(row)
    differences = [(abs(row['real_rating'] - row[dim])) for dim in range(len(row) - 1)]
    #return statistics.mean(differences)
    return differences

def rating_mean(row):
    """
        Funcion que crea una columna con la media de las diferencias
    """
    #print(row['differences'])
    if 'differences' in row.index:
        return statistics.mean(row['differences'])
    else:
        return 0.0


def rating_pstdev(row):
    """
        Funcion que crea una columna con la desviacion tipica de las diferencias
    """
    if 'differences' in row.index:
        return statistics.pstdev(row['differences'])
    else:
        return 0


def calculate_mean_ratings(sim_DF, test_movies, user, k):
    """
        Funcion que calcula la media de la diferencias de los ratings 
    """
    
    # Get train data by user
    trainset_DF = pd.read_csv('data/experiment_data/trainset.csv')
    train_user_data = trainset_DF[trainset_DF.userId == user]
    
    # Get test data by user
    testset_DF = pd.read_csv('data/experiment_data/predicted_values.csv')
    test_user_data = testset_DF[testset_DF.userId == user]

    if len(test_user_data) > 0:
        # De cada película del test obtenemos los K más similares y nos quedamos con sus ratings
        predicted_ratings = {}
        for i in range(len(test_movies)):
            most_similar_movies = sim_DF.iloc[i].sort_values(ascending=False).index.values[:k]
            rating_predicted = train_user_data[train_user_data.movieId.isin(most_similar_movies)].rating.values
            predicted_ratings[test_movies[i]] = rating_predicted

        predicted_ratings_DF = pd.DataFrame.from_dict(predicted_ratings, orient='index')
        predicted_ratings_DF['real_rating'] = test_user_data.predicted.values    

        # Calculamos la media de diferencias de cada rating
        predicted_ratings_DF['differences'] = predicted_ratings_DF.apply(lambda row: rating_dif(row), axis=1)
        predicted_ratings_DF['mean'] = predicted_ratings_DF.apply(lambda row: rating_mean(row), axis=1)
        #predicted_ratings_DF['pstdev'] = predicted_ratings_DF.apply(lambda row: rating_pstdev(row), axis=1)

        # media total
        mean_total = statistics.mean(predicted_ratings_DF['mean'].tolist())

        return mean_total
    else:
        return 0.0

def get_all_movies(user):
    q_path = 'data/matrices_data/q_user_{}.csv'.format(user)
    q_u = pd.read_csv(q_path)
    return q_u.movieId.values

def get_train_test_movies(user):
    trainset_DF = pd.read_csv('data/experiment_data/trainset.csv')
    train_user_data = trainset_DF[trainset_DF.userId == user]
    
    testset_DF = pd.read_csv('data/experiment_data/testset.csv')
    test_user_data = testset_DF[testset_DF.userId == user]
    
    test_movies = test_user_data.movieId.values
    train_movies = train_user_data.movieId.values
    
    return train_movies, test_movies

def filter_similarity_matrix(dataframe, test_movies, train_movies, movies_ids):
    # Ponemos los id de las películas en las filas de similitud
    #print(len(dataframe))
    #print(len(movies_ids))
    dataframe['movieId'] = movies_ids

    # Nos quedamos con las filas que son películas de evaluación
    final_items_sim_DF = pd.DataFrame(dataframe[dataframe.movieId.isin(test_movies)])

    # Cambiamos los nombres de las columnas
    names = {}
    for i in range(len(movies_ids)):
        names[str(i)] = movies_ids[i]

    final_items_sim_DF.rename(index=str, columns=names, inplace=True)
    # Calculamos las películas a eliminar
    movies_to_drop = np.setdiff1d(movies_ids, train_movies)
    #print(final_items_sim_DF.columns.values)
    final_items_sim_DF.drop(columns=movies_to_drop, inplace=True)
    final_items_sim_DF.drop(columns=['movieId'], inplace=True)
    return final_items_sim_DF