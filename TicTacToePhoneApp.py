import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from functools import partial
import xml.etree.ElementTree as ET
import random
import unicodedata

# Set the background color
Window.clearcolor = get_color_from_hex("#353839")

# Parse the XML data
tree = ET.parse('CombinedDataFinal.xml')
root = tree.getroot()

players = {}
for row in root.findall('row'):
    name = row.find('Name_of_the_player').text
    clubs = [club.text for club in row.findall('Club')]
    players[name] = clubs

selected_clubs_easy = [
    "Real Madrid", "Arsenal", "Manchester United", "Manchester City", 
    "Bayern Munich", "Juventus", "Paris Saint-Germain", "Borussia Dortmund", 
    "Ajax", "Barcelona", "Chelsea", "Liverpool"
]

selected_country = [
    "Argentina", "France", "Brazil", "England", "Belgium", 
    "Croatia", "Netherlands", "Portugal", "Italy", "Spain", 
    "United States", "Mexico", "Morocco", "Switzerland", 
    "Germany", "Colombia", "Uruguay", "Denmark", "Japan", 
    "Sweden", "Senegal"
]

selected_clubs_medium = [
    "Real Madrid", "Arsenal", "Manchester United", "Manchester City", 
    "Bayern Munich", "Juventus", "Paris Saint-Germain", "Borussia Dortmund", 
    "Ajax", "Barcelona", "Chelsea", "Liverpool", "RB Leipzig", "Porto", "Napoli", "PSV",
    "Atlético Madrid", "Benfica", "Tottenham Hotspur", "Inter Milan", "AC Milan", "Valencia",
    "Sevilla", "Roma", "Monaco"
]

selected_clubs_hard = [
    "Real Madrid", "Arsenal", "Manchester United", "Manchester City", 
    "Bayern Munich", "Juventus", "Paris Saint-Germain", "Borussia Dortmund", 
    "Ajax", "Barcelona", "Chelsea", "Liverpool", "RB Leipzig", "Porto", "Napoli", "PSV",
    "Atlético Madrid", "Benfica", "Tottenham Hotspur", "Inter Milan", "AC Milan", "Valencia",
    "Sevilla", "Roma", "Monaco", "Newcastle United", "Aston Villa", "Brighton Hove Albion", 
    "Feyenoord", "Bayer Leverkusen", "Sporting CP", "Fenerbahçe", "Real Sociedad", "Lazio", 
    "Fiorentina", "Galatasaray", "Atalanta", "Marseille", "Beşiktaş", "Girona", "West Ham United",
    "Villarreal", "Athletic Bilbao", "Lens", "Braga", "Lyon", "SC Freiburg", "Rennes", "Real Betis", 
    "Wolfsburg", "Lille"
]

selected_clubs_extreme = [
    "RB Leipzig", "Porto", "Napoli", "PSV", "Wolfsburg", "Lille", "Rennes", "Real Betis"
    "Atlético Madrid", "Benfica", "Tottenham Hotspur", "Inter Milan", "AC Milan", "Valencia",
    "Sevilla", "Roma", "Monaco", "Newcastle United", "Aston Villa", "Brighton Hove Albion", 
    "Feyenoord", "Bayer Leverkusen", "Sporting CP", "Fenerbahçe", "Real Sociedad", "Lazio", 
    "Fiorentina", "Galatasaray", "Atalanta", "Marseille", "Beşiktaş", "Girona", "West Ham United",
    "Villarreal", "Athletic Bilbao", "Lens", "Braga", "Lyon", "SC Freiburg"
]

selected_clubs = selected_clubs_easy

def set_difficulty(difficulty):
    global selected_clubs
    if difficulty == "easy":
        selected_clubs = selected_clubs_easy
    elif difficulty == "medium":
        selected_clubs = selected_clubs_medium
    elif difficulty == "hard":
        selected_clubs = selected_clubs_hard
    elif difficulty == "extreme":
        selected_clubs = selected_clubs_extreme

def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_players_for_two_clubs(club1, club2):
    """Return players who have played for both clubs."""
    return [player for player, clubs in players.items() if club1 in clubs and club2 in clubs]

def get_clubs_with_common_players():
    """Get clubs with common players."""
    attempts = 0
    while attempts < 1000:  # Limit the number of attempts to avoid infinite loops
        clubs = random.sample(selected_clubs, 6)
        vertical = clubs[:3]
        horizontal = clubs[3:]
        valid = True
        for club1 in vertical:
            for club2 in horizontal:
                common_players = get_players_for_two_clubs(club1, club2)
                if not common_players:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            print(f"Selected clubs: {clubs}")  # Debugging line
            return clubs
        attempts += 1
    raise ValueError("Couldn't find clubs with common players after multiple attempts.")

all_clubs = get_clubs_with_common_players()
vertical_clubs = all_clubs[:3]
horizontal_clubs = all_clubs[3:]

class GameExplanationPopup(Popup):
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "How to Play"
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Explanation label
        explanation = (
            "Welcome to Football Tic-Tac-Toe!\n\n"
            "Objective: The goal of this game is to name football players who have played for two given football clubs. "
            "The first player to name three such players in a row wins!\n\n"
            "How to Play:\n"
            "1. Setup: The game board is similar to a traditional tic-tac-toe board with nine squares.\n\n"
            "2. Starting the Game: Two football clubs are shown at each spot of the nine squares.\n\n"
            "3. Taking Turns: Player X goes first. On their turn, a player must name a footballer who has played for both of the given clubs. "
            "If the player names a correct footballer, they get to place their symbol (either X or O) on the board. "
            "Players take turns naming footballers and placing their symbols on the board.\n\n"
            "4. Winning the Game: The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins the game!\n\n"
            "Note: If a player has only participated in the youth team and not the first team of a club, it is not considered that the player has played for the club during his career.\n\n"
        )
        explanation_label = Label(
            text=explanation, 
            font_size=20, 
            halign='left',  # Align the text to the left
            size_hint_y=None  # Important for ScrollView
        )
        explanation_label.bind(texture_size=explanation_label.setter('size'))  # Set the size based on the content
        
        # Method to update the text_size of the explanation_label
        def update_text_size(instance, value):
            explanation_label.text_size = (value[0], None)

        # ScrollView
        scroll_view = ScrollView(size_hint=(1, 0.8))  # Adjust the size_hint_y value to fit within the popup
        scroll_view.bind(size=update_text_size)  # Bind the size of the scroll_view to update_text_size method
        scroll_view.add_widget(explanation_label)
        layout.add_widget(scroll_view)
        
        # Start button
        start_button = Button(text="Start Game", size_hint_y=None, height=44)
        start_button.bind(on_press=start_game_callback)
        layout.add_widget(start_button)
        
        self.content = layout

class PlayerNameDialog(Popup):
    message = ''

    def __init__(self, horizontal_clubs, vertical_clubs, check_player_callback, i, j, **kwargs):
        super().__init__(**kwargs)
        self.horizontal_clubs = horizontal_clubs
        self.vertical_clubs = vertical_clubs
        self.i = i
        self.j = j
        self.check_player_callback = check_player_callback
        self.club1 = self.horizontal_clubs[j]
        self.club2 = self.vertical_clubs[i]
        self.title = f"Name a player who has played for both {self.club1} and {self.club2}"

        # Create a BoxLayout to hold the TextInput and Button
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create the TextInput for player name
        self.player_input = TextInput(hint_text="Enter player's name", multiline=False)
        self.player_input.bind(text=self.on_text)  # Bind the on_text method to the text input
        layout.add_widget(self.player_input)

        # Create a Button to close the popup
        close_button = Button(text="Close", size_hint_y=None, height=44)
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        # Create a Button to submit the entered name
        submit_button = Button(text="Submit", size_hint_y=None, height=44)
        submit_button.bind(on_press=self.submit_player_name)
        layout.add_widget(submit_button)

        # Styling the TextInput and Button
        self.player_input.background_color = get_color_from_hex("#FFFFFF")
        self.player_input.foreground_color = get_color_from_hex("#333333")
        submit_button.background_color = get_color_from_hex("#4CAF50")
        submit_button.color = get_color_from_hex("#FFFFFF")

        # Set the layout as the content of the Popup
        self.content = layout

        # Create a dropdown for autocomplete
        self.dropdown = DropDown()

    def on_text(self, instance, value):
        """Called when the text in the TextInput changes."""
        # Clear the dropdown
        self.dropdown.clear_widgets()

        # If the text input is empty, don't populate the dropdown
        if not value.strip():
            return

        # Normalize the input value
        normalized_value = remove_diacritics(value.lower())

        # Filter player names based on the current input
        matching_players = [name for name in players if normalized_value in remove_diacritics(name.lower())]

        # Limit the number of matching players to 10
        matching_players = matching_players[:10]

        # Add the matching players to the dropdown
        for player in matching_players:
            btn = Button(text=player, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_player(btn.text))
            self.dropdown.add_widget(btn)

        # Check if the dropdown is already open
        if self.dropdown.parent:
            # If it's open, just update its position
            self.dropdown.pos = (self.player_input.x, self.player_input.y - self.dropdown.height)
        else:
            # If it's not open, open it
            if matching_players and self._is_open:  # Check if the popup is still open
                self.dropdown.open(self.player_input)

    def select_player(self, player_name):
        """Set the selected player name in the TextInput and close the dropdown."""
        self.player_input.text = player_name
        self.dropdown.dismiss()

    def submit_player_name(self, instance):
        """Called when the submit button is pressed."""
        player_name = self.player_input.text
        self.dismiss()  # Close the popup
        self.check_player_callback(player_name, self.club1, self.club2, self.i, self.j)

class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        global all_clubs, vertical_clubs, horizontal_clubs
        all_clubs = get_clubs_with_common_players()
        vertical_clubs = all_clubs[:3]
        horizontal_clubs = all_clubs[3:]

        self.horizontal_club_images = [Image() for _ in horizontal_clubs]
        self.vertical_club_images = [Image() for _ in vertical_clubs]

        # Initialize the countdown timer
        self.countdown = 20
        self.countdown_label = Label(text=f"Time left: {self.countdown}s", font_size=20, color=get_color_from_hex("#FFFFFF"))

        super(TicTacToe, self).__init__(**kwargs)
        self.cols = 4
        self.rows = 10  # Adjusted the number of rows to accommodate the turn label
        self.grid_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.turn = 0  # 0 for 'X', 1 for 'O'
        self.game_over = False

        # Reset button
        self.reset_button = Button(text="New Game", size_hint_y=None, height=44, size_hint_x=1.2)
        self.reset_button.bind(on_press=self.reset_game)

        # Home button
        self.home_button = Button(text="Return to Home", size_hint_y=None, height=44, size_hint_x=1.2)
        self.home_button.bind(on_press=self.return_to_home)

        # Turn label
        self.turn_label = Label(text="Turn: X", font_size=20, color=get_color_from_hex("#FFFFFF"))

        # Call the reset_game method to set the initial layout
        self.reset_game()
        
        # Add an attribute to keep track of the currently opened popup
        self.current_popup = None

        # Display the game explanation popup when the game starts
        self.explanation_popup = GameExplanationPopup(self.start_game, size_hint=(0.9, 0.6))
        self.explanation_popup.bind(on_open=self.stop_countdown)  # Stop the countdown when the popup is opened
        self.explanation_popup.open()

    def start_game(self, instance):
        """Start the game and countdown timer."""
        self.explanation_popup.dismiss()
        self.start_countdown()  # This will start the countdown when the user starts the game

    def stop_countdown(self, instance):
        """Stop the countdown timer."""
        if hasattr(self, 'countdown_event'):
            Clock.unschedule(self.countdown_event)
    
    def start_countdown(self):
        """Start the countdown timer."""
        # Cancel any existing countdown timer
        if hasattr(self, 'countdown_event'):
            Clock.unschedule(self.countdown_event)

        self.countdown = 20
        self.update_countdown_label()
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        """Update the countdown timer."""
        if self.countdown > 0:
            self.countdown -= 1
            self.update_countdown_label()
        else:
            # Time's up! Switch the turn
            self.turn += 1
            mark = 'X' if self.turn % 2 == 0 else 'O'
            self.turn_label.text = f"Turn: {mark}"
            self.start_countdown()  # Restart the countdown for the next player
            
            # If the current_popup is open, dismiss it
            if self.current_popup and self.current_popup._is_open:
                # Dismiss the dropdown of the current_popup if it's open
                if self.current_popup.dropdown and self.current_popup.dropdown.parent:
                    self.current_popup.dropdown.dismiss()
                self.current_popup.dismiss()
                self.current_popup = None

    def update_countdown_label(self):
        """Update the countdown label text."""
        self.countdown_label.text = f"Time left: {self.countdown}s"

    def return_to_home(self, instance):
        # Reset the game
        self.reset_game(instance)
        # Change the screen to the starting screen
        App.get_running_app().root.current = 'start'

    def reset_and_dismiss_win_popup(self, instance):
        self.reset_game(instance)
        self.win_popup.dismiss()

    def reset_and_dismiss_draw_popup(self, instance):
        self.reset_game(instance)
        self.draw_popup.dismiss()

    def check_win(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.grid_buttons[i][0].text == self.grid_buttons[i][1].text == self.grid_buttons[i][2].text and self.grid_buttons[i][0].text != " ":
                return True
            if self.grid_buttons[0][i].text == self.grid_buttons[1][i].text == self.grid_buttons[2][i].text and self.grid_buttons[0][i].text != " ":
                return True
        if self.grid_buttons[0][0].text == self.grid_buttons[1][1].text == self.grid_buttons[2][2].text and self.grid_buttons[0][0].text != " ":
            return True
        if self.grid_buttons[0][2].text == self.grid_buttons[1][1].text == self.grid_buttons[2][0].text and self.grid_buttons[0][2].text != " ":
            return True
        return False
    
    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.grid_buttons[i][j].text == " ":
                    return False
        return True

    def reset_game(self, instance=None):
        global all_clubs, vertical_clubs, horizontal_clubs
        all_clubs = get_clubs_with_common_players()
        vertical_clubs = all_clubs[:3]
        horizontal_clubs = all_clubs[3:]

        self.turn = 0
        self.clear_widgets()  # Clear all widgets
        self.game_over = False

        # Check if countdown_event exists before unscheduling
        if hasattr(self, 'countdown_event'):
            Clock.unschedule(self.countdown_event)

        # Update the club images
        for i, club in enumerate(horizontal_clubs):
            self.horizontal_club_images[i].source = f"Club Logo/{club.replace(' ', '_')}.png"
        for i, club in enumerate(vertical_clubs):
            self.vertical_club_images[i].source = f"Club Logo/{club.replace(' ', '_')}.png"

        # Re-add the club logos and buttons to the grid
        self.add_widget(Label(text="", size_hint_x=None, width=Window.width/4))  # Empty label for top-left corner
        for img in self.horizontal_club_images:
            img.size_hint_x = None
            img.width = Window.width/4
            self.add_widget(img)

        for i in range(3):
            self.vertical_club_images[i].size_hint_x = None
            self.vertical_club_images[i].width = Window.width/4
            self.add_widget(self.vertical_club_images[i])
            for j in range(3):
                btn = Button(text=" ", font_size=40, size_hint_x=None, width=Window.width/4)
                btn.background_color = [1, 1, 1, 1]  # Reset to default white color
                btn.bind(on_press=partial(self.on_click, i=i, j=j))
                self.grid_buttons[i][j] = btn  # Update the reference in the list
                self.add_widget(btn)

        # Add the "Turn" label and the countdown label just below the TicTacToe grid
        self.add_widget(self.turn_label)  # Add the turn label back to the grid
        self.add_widget(self.countdown_label)  # Re-add the countdown label to the grid
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        # Then add the reset and home buttons
        self.add_widget(self.home_button)  # Re-add the "Return to Home" button
        self.add_widget(self.reset_button)
        

        # Restart the countdown timer
        self.start_countdown()

    def on_click(self, instance, i, j):
        if not self.game_over and self.grid_buttons[i][j].text == " ":
            club1 = horizontal_clubs[j]
            club2 = vertical_clubs[i]
            dialog = PlayerNameDialog(horizontal_clubs, vertical_clubs, self.check_player, i, j, size_hint=(0.8, 0.4))
            dialog.open()
            
            # Styling the Popup
            dialog.background_color = get_color_from_hex("#FFFFFF")
            dialog.title_color = get_color_from_hex("#F5F5F5")

            # Update the turn label
            mark = 'X' if self.turn % 2 == 0 else 'O'
            self.turn_label.text = f"Turn: {mark}"
            self.grid_buttons[i][j].font_size = 100
            
            # Set the current_popup attribute to the opened popup
            self.current_popup = dialog

    def check_player(self, player_name, club1, club2, i, j):
        mark = 'X' if self.turn % 2 == 0 else 'O'
        if player_name in players and club1 in players[player_name] and club2 in players[player_name]:
            self.grid_buttons[i][j].text = mark
            if mark == 'X':
                self.grid_buttons[i][j].background_color = [1, 0, 0, 1]  # Red for 'X'
            else:
                self.grid_buttons[i][j].background_color = [0, 1, 0, 1]  # Green for 'O'
            if self.check_win():
                self.game_over = True
                layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
                layout.add_widget(Label(text=f"Player {mark} wins!"))
                
                # Define the win_popup first
                self.win_popup = Popup(title='Winner!', content=layout, size_hint=(0.8, 0.4))
                
                # Now bind the on_press event of the close_button
                close_button = Button(text="Close", size_hint_y=None, height=44)
                close_button.bind(on_press=self.win_popup.dismiss)
                layout.add_widget(close_button)
                
                # Bind the reset_game method to the New Game button and dismiss the popup
                reset_button = Button(text="New Game", size_hint_y=None, height=44)
                reset_button.bind(on_press=self.reset_and_dismiss_win_popup)
                layout.add_widget(reset_button)
                
                self.win_popup.open()
                return # End the function here to prevent further moves
            self.turn += 1
        else:
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None, height=Window.height * 0.4)
            
            error_label = Label(
                text=f"Incorrect! {player_name} hasn't played for both {club1} and {club2}.",
                size_hint_y=None,
                height=44,
                halign='center',  # Horizontal alignment
                valign='top',  # Vertical alignment
                text_size=(self.width * 0.9, None)  # Set the width for text bounding box
            )
            error_label.bind(size=self.adjust_text_size)  # Bind the size of the label to adjust its text size
            layout.add_widget(error_label)

            # Define the error_popup first
            error_popup = Popup(title='Error', content=layout, size_hint=(0.8, 0.4))
            
            # Now bind the on_press event of the close_button
            close_button = Button(text="Close", size_hint_y=None, height=44)
            close_button.bind(on_press=error_popup.dismiss)
            layout.add_widget(close_button)
            
            error_popup.open()
            self.turn += 1

            # Styling the Popup
            error_popup.background_color = get_color_from_hex("#FFFFFF")
            error_popup.title_color = get_color_from_hex("#FF0000")
        
        # Restart the countdown timer after checking the player
        self.start_countdown()

        # Update the turn label after checking the player
        mark = 'X' if self.turn % 2 == 0 else 'O'
        self.turn_label.text = f"Turn: {mark}"

    def adjust_text_size(self, instance, value):
        """Adjust the text size of the label based on its size."""
        instance.text_size = (value[0] * 0.9, None)

        # Restart the countdown timer after checking the player
        self.start_countdown()

        
        # Update the turn label after checking the player
        mark = 'X' if self.turn % 2 == 0 else 'O'
        self.turn_label.text = f"Turn: {mark}"

        if self.check_draw():
            self.game_over = True
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            layout.add_widget(Label(text="It's a draw!"))
            
            # Define the draw_popup first
            self.draw_popup = Popup(title='Draw!', content=layout, size_hint=(0.8, 0.4))
            
            # Now bind the on_press event of the close_button
            close_button = Button(text="Close", size_hint_y=None, height=44)
            close_button.bind(on_press=self.draw_popup.dismiss)
            layout.add_widget(close_button)
            
            # Bind the reset_game method to the New Game button and dismiss the popup
            reset_button = Button(text="Reset Game", size_hint_y=None, height=44)
            reset_button.bind(on_press=self.reset_and_dismiss_draw_popup)
            layout.add_widget(reset_button)
            
            self.draw_popup.open()
            return # End the function here to prevent further moves

    def get_button_coords(self):
        for i in range(3):
            for j in range(3):
                if self.grid_buttons[i][j].text == " ":
                    return i, j
                
class TicTacToeApp(App):
    def build(self):
        return TicTacToe()

