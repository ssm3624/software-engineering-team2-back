
def prepare_genre_movies(filtered_movies, links_dict, ratings_dict):
    return [
        {
            "title": movie['title'],
            "cover_url": links_dict[movie['movieId']]['URL'],
            "scope": ratings_dict.get(movie['movieId'], 5)
        } for movie in filtered_movies if movie['movieId'] in links_dict
    ]