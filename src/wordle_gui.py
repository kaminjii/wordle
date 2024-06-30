import pygame
from enum import Enum
from wordle import Attempts, Result, Matches, Game_State, play_wordle
from agilecs_spellcheck_service import is_spelling_correct
from agilecs_wordbank_service import get_response, get_random_word

class Color(Enum):
    BLACK = (18, 18, 18)
    GREEN = (108, 169, 101)
    YELLOW = (200, 182, 83)
    GRAY = (120, 124, 127)
    WHITE = (255, 255, 255)

class Dimension(Enum):
    SCREEN_WIDTH = 384
    SCREEN_HEIGHT = 600
    NUM_COLS = 5
    NUM_ROWS = 6
    CELL_SIZE = 60
    BORDER_WIDTH = 2
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 40

class WordleGui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Dimension.SCREEN_WIDTH.value, Dimension.SCREEN_HEIGHT.value))
        pygame.display.set_caption("Wordle")
        self.active_col = 0
        self.guesses  = [[""] * Dimension.NUM_COLS.value for _ in range(Dimension.NUM_ROWS.value)]
        self.attempt = Attempts.ATTEMPT_ZERO
        self.button_active = False
        self.exit_game = False
        self.game_over = False
        self.button_rect = pygame.Rect((Dimension.SCREEN_WIDTH.value - Dimension.BUTTON_WIDTH.value) // 2, Dimension.SCREEN_HEIGHT.value - 60, Dimension.BUTTON_WIDTH.value, Dimension.BUTTON_HEIGHT.value)
        self.feedback_list = [[None] * Dimension.NUM_COLS.value for _ in range(Dimension.NUM_ROWS.value)]
        self.result_text = None
        self.not_a_word_active = False
        self.word_bank = get_response().split()
        self.target_word = get_random_word(self.word_bank)
        print(self.target_word)

    def draw_cell_with_border(self, cell_x, cell_y, color):
        pygame.draw.rect(self.screen, Color.GRAY.value, (cell_x, cell_y, Dimension.CELL_SIZE.value, Dimension.CELL_SIZE.value))
        pygame.draw.rect(self.screen, color, (cell_x + Dimension.BORDER_WIDTH.value, cell_y + Dimension.BORDER_WIDTH.value, Dimension.CELL_SIZE.value - 2 * Dimension.BORDER_WIDTH.value, Dimension.CELL_SIZE.value - 2 * Dimension.BORDER_WIDTH.value))


    def draw_cell_no_border(self, cell_x, cell_y, color):
        pygame.draw.rect(self.screen, color, (cell_x, cell_y, Dimension.CELL_SIZE.value, Dimension.CELL_SIZE.value))


    def draw_text(self, cell_x, cell_y, guess_letter):
        font = pygame.font.Font(None, 36)
        text = font.render(guess_letter, True, "white")
        text_rect = text.get_rect(center=(cell_x + Dimension.CELL_SIZE.value // 2, cell_y + Dimension.CELL_SIZE.value // 2))
        self.screen.blit(text, text_rect)


    def draw_cell(self, cell_x, cell_y, guess_letter = None, color = Color.BLACK.value, border = True):
        if border:
            self.draw_cell_with_border(cell_x, cell_y, color)
        else: 
            self.draw_cell_no_border(cell_x, cell_y, color)
        if guess_letter:
            self.draw_text(cell_x, cell_y, guess_letter)


    def draw_row(self, row_y, guess_row, feedback):
        X_OFFSET = 66
        for row_index, (guess_letter, match) in enumerate(zip(guess_row, feedback)):
            colors = {
                Matches.EXACT_MATCH: Color.GREEN.value,
                Matches.PRESENT: Color.YELLOW.value,
                Matches.NO_MATCH: Color.GRAY.value,
            }
            color = colors.get(match, Color.BLACK.value)
            border = False if match in (Matches.EXACT_MATCH, Matches.PRESENT, Matches.NO_MATCH) else True

            self.draw_cell(30 + X_OFFSET * row_index, row_y, guess_letter, color, border)


    def draw_grid(self):
        Y_OFFSET = 66
        for row_index, (guess_row, feedback) in enumerate(zip(self.guesses, self.feedback_list)):
            self.draw_row(90 + Y_OFFSET * row_index, guess_row, feedback)


    def draw_submit_button(self):
        if self.button_active:
            pygame.draw.rect(self.screen, Color.GREEN.value, self.button_rect)
        else:
            pygame.draw.rect(self.screen, Color.GRAY.value, self.button_rect)
        
        font = pygame.font.Font(None, 24)
        text = font.render("Submit", True, Color.WHITE.value)
        text_rect = text.get_rect(center = self.button_rect.center)
        self.screen.blit(text, text_rect)


    def draw_result_text(self):
        if self.game_over and self.result_text:
            text_rect = self.result_text.get_rect(center=(Dimension.SCREEN_WIDTH.value // 2, Dimension.SCREEN_HEIGHT.value // 2))
            text_surface = pygame.Surface((text_rect.width + 70, text_rect.height + 50))
            text_surface.fill((255, 255, 255))
            self.screen.blit(text_surface, (text_rect.x - 35, text_rect.y - 25))
            self.screen.blit(self.result_text, text_rect)


    def handle_backspace_input(self):
        if self.active_col > 0:
            self.guesses[self.attempt.value][self.active_col - 1] = ""
            self.active_col -= 1
            self.button_active = False
    

    def handle_alphabet_input(self, event):
        self.guesses[self.attempt.value][self.active_col] = event.unicode.upper()
        self.active_col += 1
        self.button_active = self.active_col == Dimension.NUM_COLS.value 
    

    def draw_win_message(self, result_message):
        font = pygame.font.Font(None, 45)
        self.result_text = font.render(result_message, True, Color.BLACK.value)
        self.game_over = True


    def draw_lose_message(self):
        font = pygame.font.Font(None, 25)
        self.result_text = font.render(f"It was {self.target_word}, better luck next time", True, Color.BLACK.value)
        self.game_over = True
                            

    def handle_wordle_logic(self):
        result = play_wordle(self.target_word, "".join(self.guesses[self.attempt.value]), self.attempt)
        self.feedback_list[self.attempt.value] = result[Result.FEEDBACK]
        
        if result[Result.GAME_STATE] == Game_State.WIN:
            self.draw_win_message(result[Result.MESSAGE])
        elif result[Result.GAME_STATE] == Game_State.LOSE:
            self.draw_lose_message()
        else:
            self.attempt = result[Result.ATTEMPT]
            self.active_col = 0
            self.button_active = False  
            
            
    def draw_not_a_word(self):
        font = pygame.font.Font(None, 20)
        incorrect_spelling_text = font.render("Not a word", True, Color.BLACK.value)
        text_rect = incorrect_spelling_text.get_rect(center=(Dimension.SCREEN_WIDTH.value // 2, 60))            
        text_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
        text_surface.fill((255, 255, 255))
        self.screen.blit(text_surface, (text_rect.x - 10, text_rect.y - 10))
        self.screen.blit(incorrect_spelling_text, text_rect)        


    def handle_spellcheck(self):
        if not is_spelling_correct("".join(self.guesses[self.attempt.value])):
            self.not_a_word_active = True
            self.draw_not_a_word()
            return
        return True
    
    
    def handle_submit(self):
        if self.button_active:
            if not self.handle_spellcheck():
                return
            self.handle_wordle_logic()


    def handle_return_input(self):
        self.handle_submit()


    def handle_keydown(self, event):
        submit_actions = {
            pygame.K_BACKSPACE: self.handle_backspace_input,
            pygame.K_RETURN: self.handle_return_input
        }

        if self.not_a_word_active:
            self.not_a_word_active = False
            self.screen.fill(Color.BLACK.value)


        if event.key in submit_actions:
            submit_actions[event.key]()
        elif event.unicode.isalpha() and self.active_col < Dimension.NUM_COLS.value:
            self.handle_alphabet_input(event)


    def handle_mouse_click(self, event):
        if self.button_rect.collidepoint(event.pos):
            self.handle_submit()
                
                
    def handle_quit(self, event):
        self.exit_game = True  
                    

    def draw_display(self):
        self.draw_grid()
        self.draw_submit_button()
        self.draw_result_text()
        pygame.display.flip()  


    def run(self):
        while not self.exit_game:
            pygame.display.flip()

            actions = {
                pygame.KEYDOWN: self.handle_keydown,
                pygame.MOUSEBUTTONDOWN: self.handle_mouse_click,
                pygame.QUIT: self.handle_quit
            }

            for event in pygame.event.get():
                if event.type in actions:
                    actions[event.type](event)

            self.draw_display()

        pygame.display.quit()
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = WordleGui()
    game.run()