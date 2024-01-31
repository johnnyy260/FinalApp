from TicTacToePhoneApp import TicTacToe, set_difficulty
from PositionMatchPhoneApp import FormationGame, set_option
from PlayerGuessPhoneApp import PlayerGuessGame
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

class BackgroundImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'soccer-wallpaper-2.jpg'
        self.allow_stretch = True
        self.keep_ratio = False

class BackgroundImageHome(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'soccer-wallpaper.jpg'
        self.allow_stretch = True
        self.keep_ratio = False

class OptionSelector(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundImageHome())
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        for option in ["Nations", "Clubs", "Nations and Clubs"]:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_press=self.set_and_start_formation_game)
            layout.add_widget(btn)

        # Return to Home button
        home_button = Button(text="Return to Home", size_hint_y=None, height=44)
        home_button.bind(on_press=self.return_to_home)
        layout.add_widget(home_button)
        
        self.add_widget(layout)

    def set_and_start_formation_game(self, instance):
        set_option(instance.text)
        self.manager.current = 'formation_game'

    def return_to_home(self, instance):
        self.manager.current = 'start'

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundImageHome())
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Existing TicTacToe start button
        start_button = Button(text="Start TicTacToe Game", size_hint_y=None, height=44)
        start_button.bind(on_press=self.start_tictactoe_game)
        layout.add_widget(start_button)

        # New FormationGame start button
        formation_game_button = Button(text="Start Formation Game", size_hint_y=None, height=44)
        formation_game_button.bind(on_press=self.start_formation_game)
        layout.add_widget(formation_game_button)

        # New PlayerGuessGame start button
        player_guess_game_button = Button(text="Start Player Guess Game", size_hint_y=None, height=44)
        player_guess_game_button.bind(on_press=self.start_player_guess_game)
        layout.add_widget(player_guess_game_button)

        self.add_widget(layout)

    def start_tictactoe_game(self, instance):
        self.manager.current = 'difficulty_selector'

    def start_formation_game(self, instance):
        self.manager.current = 'formation_game'

    def start_formation_game(self, instance):
        self.manager.current = 'option_selector'  # Navigate to OptionSelector instead

    def start_player_guess_game(self, instance):
        self.manager.current = 'player_guess_game'

    def start_player_guess_game(self, instance):
        self.manager.current = 'difficulty_selector_player_guess'

class DifficultySelector(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundImageHome())
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        for difficulty in ["easy", "medium", "hard", "extreme"]:
            btn = Button(text=difficulty.capitalize(), size_hint_y=None, height=44)
            btn.bind(on_press=self.set_and_start)
            layout.add_widget(btn)

        # Return to Home button
        home_button = Button(text="Return to Home", size_hint_y=None, height=44)
        home_button.bind(on_press=self.return_to_home)
        layout.add_widget(home_button)
        
        self.add_widget(layout)

    def set_and_start(self, instance):
        set_difficulty(instance.text.lower())
        self.manager.current = 'tic_tac_toe'

    def return_to_home(self, instance):
        self.manager.current = 'start'

class DifficultySelectorPlayerGuess(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundImageHome())
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        for difficulty in ["Easy", "Medium", "Hard"]:
            btn = Button(text=difficulty, size_hint_y=None, height=44)
            btn.bind(on_press=self.set_and_start)
            layout.add_widget(btn)

        # Return to Home button
        home_button = Button(text="Return to Home", size_hint_y=None, height=44)
        home_button.bind(on_press=self.return_to_home)
        layout.add_widget(home_button)
        
        self.add_widget(layout)

    def set_and_start(self, instance):
        self.manager.get_screen('player_guess_game').difficulty = instance.text.lower()
        self.manager.current = 'player_guess_game'

    def return_to_home(self, instance):
        self.manager.current = 'start'

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super(TicTacToeScreen, self).__init__(**kwargs)
        self.add_widget(BackgroundImage())
        self.tictactoe = None

    def on_enter(self):
        # Only create a new TicTacToe instance if one doesn't already exist
        if not self.tictactoe:
            self.tictactoe = TicTacToe()
            self.add_widget(self.tictactoe)

    def on_pre_leave(self):
        # Remove the TicTacToe instance from the screen before leaving
        if self.tictactoe:
            self.remove_widget(self.tictactoe)
            self.tictactoe = None

class FormationGameScreen(Screen):
    def __init__(self, **kwargs):
        super(FormationGameScreen, self).__init__(**kwargs)
        self.add_widget(BackgroundImage())
        self.formation_game = None

    def on_enter(self):
        # Only create a new FormationGame instance if one doesn't already exist
        if not self.formation_game:
            self.formation_game = FormationGame()
            self.add_widget(self.formation_game)

    def on_pre_leave(self):
        # Remove the FormationGame instance from the screen before leaving
        if self.formation_game:
            self.remove_widget(self.formation_game)
            self.formation_game = None

class PlayerGuessGameScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayerGuessGameScreen, self).__init__(**kwargs)
        self.add_widget(BackgroundImage())
        self.player_guess_game = None
        self.difficulty = "easy"  # default difficulty

    def on_enter(self):
        # Only create a new PlayerGuessGame instance if one doesn't already exist
        if not self.player_guess_game:
            self.player_guess_game = PlayerGuessGame(difficulty=self.difficulty)
            self.add_widget(self.player_guess_game)

    def on_pre_leave(self):
        # Remove the PlayerGuessGame instance from the screen before leaving
        if self.player_guess_game:
            self.remove_widget(self.player_guess_game)
            self.player_guess_game = None

class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(DifficultySelector(name='difficulty_selector'))
        sm.add_widget(TicTacToeScreen(name='tic_tac_toe'))
        sm.add_widget(OptionSelector(name='option_selector'))  # Add this line for OptionSelector
        sm.add_widget(FormationGameScreen(name='formation_game'))
        sm.add_widget(PlayerGuessGameScreen(name='player_guess_game'))
        sm.add_widget(DifficultySelectorPlayerGuess(name='difficulty_selector_player_guess'))
        return sm

if __name__ == '__main__':
    TicTacToeApp().run()