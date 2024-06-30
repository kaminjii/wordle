import requests

def get_response(word):   
    URL = "http://agilec.cs.uh.edu/spellcheck"
            
    return requests.get(URL, params = {"check" : word}).text

def parse_response(response_text):
    if response_text not in ['true', 'false']:
        raise ValueError("No response found")
    
    return response_text == 'true' 
    
    
def is_spelling_correct(guess):
    return parse_response(get_response(guess))
