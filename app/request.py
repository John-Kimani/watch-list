
import urllib.request,json
from .models import Movie

Movie = Movie

# getting api key
api_key = None
# Getting the movie base url
base_url = None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['MOVIE_API_KEY']
    base_url = app.config['MOVIE_API_BASE_URL']


def get_movies(category):
    '''
    Function that gets json response to our url request
    '''
    get_movies_url = base_url.format(category,api_key) # method that replaces {} placeholder in the api url with my api key
    print('**********')
    print(get_movies_url)
    with urllib.request.urlopen(get_movies_url) as url: #function that sends a request as a url
        get_movies_data = url.read() # reads the response and stores it in a variable
        get_movies_response = json.loads(get_movies_data) # converts the json reponse to a python dictionary

        movie_results = None

        if get_movies_response['results']:
            movie_results_list = get_movies_response['results']
            movie_results = process_results(movie_results_list)

    return movie_results

def process_results(movie_list):
    '''
    Function that processes the movies result and transform them to a list of objects
    Args:
        movie_results: A list of dictionaries that contain movie details

    Returns: 
        movie_results: A list of movie objects
    '''
    movie_results = [] # list that stores new created objects
    for movie_item in movie_list: # loop through the dictionary
        id = movie_item.get('id')
        title = movie_item.get('original_title')
        overview = movie_item.get('overview')
        poster = movie_item.get('poster_path')
        vote_average = movie_item.get('vote_average')
        vote_count = movie_item.get('vote_count')

        if poster:
            movie_object = Movie(id, title, overview, poster, vote_average, vote_count)
            movie_results.append(movie_object)

    return movie_results

def get_movie(id):
    get_movie_details_url = base_url.format(id, api_key)
    print('******')
    print(get_movie_details_url)

    with urllib.request.urlopen(get_movie_details_url) as url:
        movie_details_data = url.read()
        movie_details_response = json.loads(movie_details_data)

        movie_object = None
        if movie_details_response:
            id = movie_details_response.get('id')
            title = movie_details_response.get('original_title')
            overview = movie_details_response.get('overview')
            poster = movie_details_response.get('poster_path')
            vote_average = movie_details_response.get('vote_average')
            vote_count = movie_details_response.get('vote_count')

            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)

        return movie_object

def search_movie(movie_name):
    search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,movie_name)
    print('***************')
    print(search_movie_url)

    with urllib.request.urlopen(search_movie_url) as url:
        search_movie_data = url.read()
        search_movie_response = json.loads(search_movie_data)

        search_movie_results = None

        if search_movie_response['results']:
            search_movie_list = search_movie_response['results']
            search_movie_results = process_results(search_movie_list)


    return search_movie_results