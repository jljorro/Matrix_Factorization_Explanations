import pandas as pd
import numpy as np

def filter_similarity_matrix(dataframe, test_movies, train_movies, movies_ids):
    # Ponemos los id de las películas en las filas de similitud
    dataframe['movieId'] = movies_ids

    # Nos quedamos con las filas que son películas de evaluación
    final_items_sim_DF = pd.DataFrame(dataframe[dataframe.movieId.isin(test_movies)])

    # Cambiamos los nombres de las columnas
    names = {}
    for i in range(len(movies_ids)):
        names[i] = movies_ids[i]

    final_items_sim_DF.rename(index=str, columns=names, inplace=True)

    # Calculamos las películas a eliminar
    movies_to_drop = np.setdiff1d(movies_ids, train_movies)
    final_items_sim_DF.drop(columns=movies_to_drop, inplace=True)
    final_items_sim_DF.drop(columns=['movieId'], inplace=True)
    return final_items_sim_DF