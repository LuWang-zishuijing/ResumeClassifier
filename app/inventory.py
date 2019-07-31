import random

movie_genres = {
    "adult": {"name": "Adult", "field_name": "is_adult" },
    "adventure": {"name": "Adventure", "field_name": "is_adventure" },
    "romance": {"name": "Romance", "field_name": "is_romance"},
    "history": {"name": "History" , "field_name": "is_history"},
    "crime": {"name": "Crime", "field_name": "is_crime"},
    "western": {"name": "Western", "field_name": "is_western"},
    "fantasy": {"name": "Fantasy", "field_name": "is_fantasy"},
    "documentary": {"name": "Documentary", "field_name": "is_documentary"},
    "horror": {"name": "Horror", "field_name": "is_horror"},
    "mystery": {"name": "Mystery" , "field_name": "is_mystery"},
    "reality_tv": {"name": "Reality-TV", "field_name": "is_reality_tv"},
    "talk_show": {"name": "Talk-Show", "field_name": "is_talk_show"},
    "sci_fi": {"name": "Sci-Fi", "field_name": "is_sci_fi"},
    "thriller": {"name": "Thriller", "field_name": "is_thriller"},
    "news": {"name": "News", "field_name": "is_news"},
    "action": {"name": "Action", "field_name": "is_action"},
    "war": {"name": "War", "field_name": "is_war"},
    "animation": {"name": "Animation", "field_name": "is_animation"},
    "short": {"name": "Short", "field_name": "is_short"},
    "game_show": {"name": "Game-Show", "field_name": "is_game_show"},
    "comedy": {"name": "Comedy", "field_name": "is_comedy"},
    "biography": {"name": "Biography", "field_name": "is_biography"},
    "sport": {"name": "Sport", "field_name": "is_sport"},
    "musical": {"name":  "Musical", "field_name": "is_musical"},
    "music": {"name": "Music", "field_name": "is_music"},
    "family": {"name": "Family" , "field_name": "is_family"},
    "drama": {"name": "Drama", "field_name": "is_drama"},
    "film_noir": {"name": "Film-Noir", "field_name": "is_film_noir"}
}

def find_random_genres(k):
    random_keys = random.sample(movie_genres.keys(), k)

    new_dict = {}

    for key in random_keys:
        new_dict[key] = movie_genres[key]

    return new_dict