from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm

base_url = 'https://www.imdb.com/title/tt'

def get_title(text):
    #pattern = re.compile('(.*)(\s\(\d\d\d\d\))')
    return text#pattern.search(text).group(1)

def is_genre(href):
    return href and "genres=" in href 

def is_keyword(href):
    return href and "keywords=" in href

def is_director(href):
    return href and "tt_ov_dr" in href

def get_genres(html):
    genres = []
    for g in html.find_all(href=is_genre):
        genres.append(g.text.strip())
    
    return set(genres)

def get_keywords(html):
    keywords = []
    for g in html.find_all(href=is_keyword):
        keywords.append(g.text.strip())
    
    return set(keywords)

def get_director(html):
    return html.find(href=is_director).text

def is_writer(href):
    return href and "tt_ov_wr" in href and "name" in href

def get_writers(html):
    writers = []
    for g in html.find_all(href=is_writer):
        writers.append(g.text.strip())
    
    return set(writers)

def is_star(href):
    return href and "tt_ov_st_sm" in href and "name" in href

def get_stars(html):
    stars = []
    for g in html.find_all(href=is_star):
        stars.append(g.text.strip())
    
    return set(stars)

def is_company(href):
    return href and "/company/" in href and "cons_tt_dt_co_"

def get_companies(html):
    companies = []
    for g in html.find_all(href=is_company):
        companies.append(g.text.strip())
    
    return set(companies)

def procesarPagina(url, idMovie):
    """
    Carga y  procesa el contenido de una URL usando request
    Muestra un mensaje de error en caso de no poder cargar la página
    """
     # Realizamos la petición a la web
    req = requests.get(url)

    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text,"lxml")
        
        # Procesamos el HTML descargado
        return procesaHTML(html,idMovie,url)        
        
    else:
        print ("ERROR {}".format(statusCode))

def procesaHTML(html, idMovie, url=""):
    """
    Procesa el contenido HTML de una página web
    html es un objeto BS4
    url es la URL de la página contenida en html_doc
    """
    movie = {}
    movie['id'] = idMovie
    movie['title'] = get_title(html.title.text)    
    # movie['year'] = html.find('div', class_='title_wrapper').h1.a.text
    movie['genres'] = get_genres(html)
    movie['keywords'] = get_keywords(html)
    movie['director'] = get_director(html)
    movie['writers'] = get_writers(html)
    movie['stars'] = get_stars(html)
    movie['companies'] = get_companies(html)
    
    return movie

def get_all_movies_data(imdb_index):
    movies = []
    fail_ids = []
    
    for i in tqdm(range(len(imdb_index))):

        idMovie = int(imdb_index.iloc[i]['movieId'])

        url = base_url + str(int(imdb_index.iloc[i]['imdbId'])).zfill(7)

        m = procesarPagina(url,idMovie)

        m['id'] = int(imdb_index.iloc[i]['movieId'])
        if m is None:
            fail_ids.append(imdb_index.iloc[i]['movieId'])
        else:
            movies.append(m)
            
    return movies