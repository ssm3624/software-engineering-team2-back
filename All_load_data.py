from fastapi import HTTPException

from Pre_Movie import get_movie
from Pre_UserID import get_userid
from Pre_Rating import get_rating
from Pre_Post import get_post


def load_data():
    movies_data = get_movie()
    links_data = get_post()
    ratings_data = get_rating()
    user_data = get_userid()
    
    if not movies_data or not links_data or not ratings_data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return movies_data, links_data, ratings_data, user_data