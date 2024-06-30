import requests
import random
import time


def get_response():
    URL = "https://agilec.cs.uh.edu/words" 
    
    return requests.get(URL).text


def get_random_word(words, seed=time.time_ns()):
    if not hasattr(get_random_word, 'seed') or get_random_word.seed != seed:
        get_random_word.seed = seed
        random.seed(seed)

    return random.choice(words)
