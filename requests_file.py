import requests
import random
from secret_info import ts, hashVal, api_public_key
from models import db, MarvelCharacters, ComicsCharacters, MarvelComics

def get_character(character_name):
    url  = "https://gateway.marvel.com:443/v1/public/characters"
    resp = requests.get(url,
                        params={"ts": ts,
                                "apikey": api_public_key,
                                "hash": hashVal,
                                "name": character_name})

    if len(resp.json()['data']["results"]) ==0:
        return False
    else:
        name = resp.json()['data']["results"][0]["name"]
        id = resp.json()['data']["results"][0]["id"]
        thumbnail_path = resp.json()['data']["results"][0]["thumbnail"]["path"]
        thumbnail_extension = resp.json()['data']["results"][0]["thumbnail"]["extension"]
        thumbnail = thumbnail_path+ "."+thumbnail_extension
        description = resp.json()['data']["results"][0]["description"]
        return id, name, thumbnail, description
    
def schuffle(lst):
    shuffled_list = lst[:]  # Make a copy of the original list
    
    list_len = len(shuffled_list)
    for i in range(list_len - 1, 0, -1):  # Iterate from the end to the beginning
        random_index = random.randint(0, i)
        shuffled_list[i], shuffled_list[random_index] = shuffled_list[random_index], shuffled_list[i]
    
    return shuffled_list


def get_character_comics(character_id):
    url  = f"https://gateway.marvel.com:443/v1/public/characters/{character_id}/comics"
    resp = requests.get(url,
                        params={"ts": ts,
                                "apikey": api_public_key,
                                "hash": hashVal})
    if len(resp.json()['data']["results"]) ==0:
        return False
    else:
        comics = resp.json()['data']["results"]
        num_comics = len(comics)
        list = [num for num in range(num_comics)]
        schuffled_list = schuffle(list)
        first_five = schuffled_list[0:5]
        five_random_comics=[resp.json()['data']["results"][i]["title"] for i in first_five]
        their_five_ids= [resp.json()["data"]["results"][i]["id"] for i in first_five]
        combined_dict = dict(zip(their_five_ids, five_random_comics))
        return combined_dict

def save_some_characters_to_db():
    characters_list=['hulk', 'thor', 'iron man']
    for ch in characters_list:
        if get_character(ch) != False:
            id, name, thumbnail, description = get_character(ch)
            new_ch = MarvelCharacters(id=id, name=name, thumbnail=thumbnail, description=description)
            db.session.add(new_ch)
            db.session.commit()

            if get_character_comics(id)!= False:
                random_comics = get_character_comics(id)
                for comics_id, comics_title in random_comics.items():
                    comics_in_db = MarvelComics.query.filter_by(id = comics_id).first()
                    if comics_in_db == None:
                        new_comics = MarvelComics(id = comics_id, title = comics_title)
                        db.session.add(new_comics)
                        db.session.commit()

                    new_comics_character = ComicsCharacters(character_id =id, comics_id = comics_id)
                    db.session.add(new_comics_character)
                    db.session.commit()