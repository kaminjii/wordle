from enum import Enum

class Matches(Enum):
    EXACT_MATCH = "Exact Match"
    PRESENT = "Present"
    NO_MATCH = "No Match"


class Attempts(Enum):
    ATTEMPT_ZERO = 0
    ATTEMPT_ONE = 1
    ATTEMPT_TWO = 2
    ATTEMPT_THREE = 3
    ATTEMPT_FOUR = 4
    ATTEMPT_FIVE = 5

class Game_State(Enum):
    WIN = "win"
    LOSE = "lose"
    IN_PROGRESS = "in progress"


class Result(Enum):
    FEEDBACK = "feedback"
    GAME_STATE = "game state"
    MESSAGE = "message"
    ATTEMPT = "attempt"

def validate_lengths(target, guess):
    WORD_LENGTH = 5

    if len(guess) != WORD_LENGTH or len(target) != WORD_LENGTH:
        raise ValueError("Invalid Input")


def count_positional_matches(target, guess, letter):
    return sum(1 for i in range(len(target)) if target[i] == guess[i] and target[i] == letter)


def count_number_of_occurrences_until_position(position, word, letter):
    return word[: position + 1].count(letter)


def tally_for_position(position, target, guess):
    if target[position] == guess[position]:
        return Matches.EXACT_MATCH

    letter_at_position = guess[position]

    positional_matches = count_positional_matches(target, guess, letter_at_position)

    non_positional_occurrences_in_target = count_number_of_occurrences_until_position(len(target) - 1, target, letter_at_position) - positional_matches

    number_of_occurrences_in_guess_until_position = count_number_of_occurrences_until_position(position, guess, letter_at_position)
    
    if non_positional_occurrences_in_target >= number_of_occurrences_in_guess_until_position:
        return Matches.PRESENT

    return Matches.NO_MATCH


def tally(target, guess):
    return [tally_for_position(i, target, guess) for i in range(len(guess))]


def set_game_state(feedback, attempt):
    if attempt not in Attempts.__members__.values(): 
        raise ValueError("Invalid Attempt Number")

    return Game_State.WIN if feedback == [Matches.EXACT_MATCH] * 5 else Game_State.LOSE if attempt == Attempts.ATTEMPT_FIVE else Game_State.IN_PROGRESS


def set_message(game_state, attempt):
    if game_state == Game_State.WIN:
        message_map = {
            Attempts.ATTEMPT_ZERO: "Amazing",
            Attempts.ATTEMPT_ONE: "Splendid",
            Attempts.ATTEMPT_TWO: "Awesome",
        }

        return message_map.get(attempt, "Yay")
    return ""


def set_attempt(game_state, attempt):
    return attempt if game_state == Game_State.WIN or game_state == Game_State.LOSE else Attempts(attempt.value + 1)
    

def play_wordle(target, guess, attempt, is_correct_spelling=lambda word : True):
    validate_lengths(target, guess)

    if not is_correct_spelling(guess):
       raise Exception("Not a word")

    result = {}

    result[Result.FEEDBACK] = tally(target, guess)

    result[Result.GAME_STATE] = set_game_state(result[Result.FEEDBACK], attempt)

    result[Result.MESSAGE] = set_message(result[Result.GAME_STATE], attempt)

    result[Result.ATTEMPT] = set_attempt(result[Result.GAME_STATE], attempt)

    return result
