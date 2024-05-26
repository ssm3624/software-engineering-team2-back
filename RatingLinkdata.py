def prepare_dicts(ratings_data, links_data):
    ratings_dict = {item['movieId']: item['rating'] for item in ratings_data}
    links_dict = {item['movieId']: {'URL': item['URL'], 'overview': item.get('overview', '')} for item in links_data}
    
    return ratings_dict, links_dict