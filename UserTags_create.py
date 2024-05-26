from fastapi import HTTPException

def create_user_tags_string(user_data):
    user_tags_list = []
    for row in user_data:
        if 'UserTags' in row:
            user_tags = row['UserTags']
            if isinstance(user_tags, list):
                user_tags_list.extend(user_tags)
            elif isinstance(user_tags, str):
                user_tags_list.append(user_tags)
            else:
                raise HTTPException(status_code=400, detail="UserTags must be a list or a string")
            
    user_tags_string = ' '.join(user_tags_list).strip()
    if not user_tags_string:
        raise HTTPException(status_code=400, detail="User tags are empty")
    
    return user_tags_string