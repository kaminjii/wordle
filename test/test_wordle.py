import unittest
from parameterized import parameterized
import sys

sys.path.append("src")
from wordle import (
    tally,
    Matches,
    play_wordle,
    Game_State,
    Attempts,
    validate_lengths,
    Result,
)

globals().update(Matches.__members__)
globals().update(Attempts.__members__)
globals().update(Game_State.__members__)
globals().update(Result.__members__)


class TestWordleGame(unittest.TestCase):
    def canary_test(self):
        self.assertTrue(True)

    @parameterized.expand([
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5),
        ("FAVOR", "TESTS", [NO_MATCH] * 5),
        ("FAVOR", "RAPID", [PRESENT, EXACT_MATCH] + [NO_MATCH] * 3),
        ("FAVOR", "MAYOR", [NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH, EXACT_MATCH],),
        ("FAVOR", "RIVER", [NO_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],),
        ("FAVOR", "AMAST", [PRESENT, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
        ("SKILL", "SKILL", [EXACT_MATCH] * 5),
        ("SKILL", "SWIRL", [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],),
        ("SKILL", "CIVIL", [NO_MATCH, PRESENT, NO_MATCH, NO_MATCH, EXACT_MATCH]),
        ("SKILL", "SHIMS", [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, NO_MATCH],),
        ("SKILL", "SILLY", [EXACT_MATCH, PRESENT, PRESENT, EXACT_MATCH, NO_MATCH]),
        ("SKILL", "SLICE", [EXACT_MATCH, PRESENT, EXACT_MATCH, NO_MATCH, NO_MATCH]),
      ])
    def test_tally_guess(self, target, guess, expected):
        self.assertEqual(tally(target, guess), expected)

    def test_valid_input_greater(self):
        with self.assertRaisesRegex(ValueError, "Invalid Input"):
            validate_lengths("FAVOR", "FERVER")

    def test_valid_input_lesser(self):
        with self.assertRaisesRegex(ValueError, "Invalid Input"):
            validate_lengths("FAVOR", "FOR")

    def test_valid_guess(self):
        with self.assertRaisesRegex(ValueError, "Invalid Input"):
            validate_lengths("WHAT", "WHAT")

    def test_play_with_matching_target_and_guess(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_ZERO
        expected_result = {
            ATTEMPT: ATTEMPT_ZERO,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Amazing",
        }

        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_invalid_guess(self):
        target = "FAVOR"
        guess = "DEAL"
        attempt = Attempts.ATTEMPT_ZERO

        with self.assertRaisesRegex(ValueError, "Invalid Input"):
            play_wordle(target, guess, attempt)

    def test_play_first_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_ZERO

        expected_result = {
            ATTEMPT: ATTEMPT_ONE,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }

        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_second_winning(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_ONE
        
        expected_result = {
            ATTEMPT: ATTEMPT_ONE,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Splendid",
        }
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_second_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_ONE
        
        expected_result = {
            ATTEMPT: ATTEMPT_TWO,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)
        
    def test_play_second_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_ONE
        
        expected_result = {
            ATTEMPT: ATTEMPT_TWO,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_third_winning(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_TWO
        
        expected_result = {
            ATTEMPT: ATTEMPT_TWO,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Awesome",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_third_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_TWO
        
        expected_result = {
            ATTEMPT: ATTEMPT_THREE,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)
        
    def test_play_fourth_winning(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_THREE
        
        expected_result = {
            ATTEMPT: ATTEMPT_THREE,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Yay",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_fourth_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_THREE
        
        expected_result = {
            ATTEMPT: ATTEMPT_FOUR,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_fifth_winning(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_FOUR
        
        expected_result = {
            ATTEMPT: ATTEMPT_FOUR,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Yay",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)
        
    def test_play_fifth_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_FOUR
        
        expected_result = {
            ATTEMPT: ATTEMPT_FIVE,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)

    def test_play_sixth_winning(self):
        target = "FAVOR"
        guess = "FAVOR"
        attempt = Attempts.ATTEMPT_FIVE
        
        expected_result = {
            ATTEMPT: ATTEMPT_FIVE,
            FEEDBACK: [EXACT_MATCH] * 5,
            GAME_STATE: WIN,
            MESSAGE: "Yay",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)
        
    def test_play_sixth_non_winning(self):
        target = "FAVOR"
        guess = "FIVER"
        attempt = Attempts.ATTEMPT_FIVE
        
        expected_result = {
            ATTEMPT: ATTEMPT_FIVE,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: LOSE,
            MESSAGE: "",
        }
        
        self.assertEqual(play_wordle(target, guess, attempt), expected_result)
        
    def test_play_seventh_winning(self):
        with self.assertRaisesRegex(ValueError, "Invalid Attempt Number"):
            target = "FAVOR"
            guess = "FAVOR"
            attempt = 6
            
            play_wordle(target, guess, attempt)

    def test_play_eighth_non_winning(self):
        with self.assertRaisesRegex(ValueError, "Invalid Attempt Number"):
            target = "FAVOR"
            guess = "FIVER"
            attempt = 7
        
            play_wordle(target, guess, attempt)

    
    def test_play_incorrect_spelling(self):
        self.assertRaisesRegex(Exception, "Not a word", play_wordle, "FAVOR", "FEVER", Attempts.ATTEMPT_ZERO, lambda word: False)

    
    def test_play_correct_spelling(self):
        expected_result = {
            ATTEMPT: ATTEMPT_ONE,
            FEEDBACK: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH],
            GAME_STATE: IN_PROGRESS,
            MESSAGE: "",
        }

        result = play_wordle("FAVOR", "FEVER", Attempts.ATTEMPT_ZERO, lambda word : True)
        
        self.assertEqual(result, expected_result)

    def test_play_spelling_check_exception(self): 
        def is_spelling_correct(word):
            raise Exception("Network Error")

        self.assertRaisesRegex(Exception, "Network Error", play_wordle, "FAVOR", "FEVER", Attempts.ATTEMPT_ZERO, is_spelling_correct)
