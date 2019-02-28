#!/usr/bin/env python
# coding: utf-8

# In[153]:


from concepts import Context
import pandas as pd


# # Creación de un retículo a partir de una película y sus películas similares
# Creación de un retículo a partir de una matriz binaria (path) que se encuentra en un csv, el id de una película recomendada (item_id) y el conjunto de películas similares a esa películas recomendada (sim_items).

# In[154]:


def calcular_reticulo(path, item_id, sim_items):
    
    """
        Creamos el reticulo a partir del csv donde se encuentran, por cada fila, el id de la peliculas, un 1 por cada
        característica que tenga esa peliculas y un 0 por cada característica que no tenga esa pelicula. 
        La librería necesita que los 1 se conviertan en X y los 0, en caracteres vacios.
    """
    
    df_movies = pd.read_csv(path) # cargar el dataframe
    
    # Filtro la matriz para que solo aparezcan los items que nos interesan 
    movies_list = [item_id] + sim_items.tolist()
    df_movies = df_movies.loc[df_movies['id'].isin(movies_list)]
    
    # Ajusto la matriz para que sea utilizada por la libreria
    df_movies = df_movies.replace([0, 1], ['', 'X']) # reemplazar los 1, por las X
    
    df_ids = df_movies['id']
    
    # Esto lo hago para evitar que un id con valor igual a 1, se sustituya por una X
    column_names = ['id'] + df_movies.columns.tolist() 
    df_movies['id'] = df_ids
    df_movies = df_movies[column_names]
    
    df_movies.to_csv("data/experiment_data/fca.csv",index=False) # pasarlo a un csv
    
    # en fca.csv tengo la estructura para crear el retculo, segun el formato de la libreria concepts
    r = Context.fromfile("data/experiment_data/fca.csv", frmat='csv') # crear el reticulo
    
    # visualizarlo
    lat = r.lattice
    lat.graphviz(view=True)




