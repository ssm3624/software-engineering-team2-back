from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Pre_Tag import get_tag

def recommend_movies_by_similarity(filtered_movies, user_tags_string, links_dict):
    vectorizer = TfidfVectorizer(stop_words=None, token_pattern=r'\b\w+\b')
    user_tfidf = vectorizer.fit_transform([user_tags_string])
    
    recommended_movies = []
    for movie in filtered_movies:
        movie_id = movie['movieId']
        tags_data = get_tag(movie_id)
        if tags_data and isinstance(tags_data, list):
            movie_tags_string = ' '.join(tag['tag'] for tag in tags_data if 'tag' in tag)
            movie_tfidf = vectorizer.transform([movie_tags_string])
            similarity_score = cosine_similarity(user_tfidf, movie_tfidf)[0][0]
            
            movie_title = movie['title']
            poster = links_dict[movie_id]['URL']
            overview = links_dict[movie_id]['overview']

            recommended_movies.append({
                "title": movie_title,
                "describe": overview,
                "cover_url": poster,
                "similarity_score": round(similarity_score, 3)
            })
    
    recommended_movies.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    if not recommended_movies:
        raise HTTPException(status_code=404, detail="No recommended movies found")
    
    return recommended_movies