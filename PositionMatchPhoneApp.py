import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
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
    positions = [position.text for position in row.findall('Position')]
    players[name] = {'clubs': clubs, 'positions': positions}

formation_positions = [
    "Goalkeeper", "Right Back", "Center Back", "Center Back", "Left Back",
    "Midfielder", "Midfielder", "Midfielder", "Right Winger", "Left Winger", "Striker"
]

btn_id_to_position = {
    "midfielder_0": "Midfielder",
    "midfielder_1": "Midfielder",
    "midfielder_2": "Midfielder",
    "centerback_1": "Center Back",
    "centerback_2": "Center Back"
}

selected_clubs1 = [
    "Argentina", "France", "Brazil", "England", "Belgium", 
    "Croatia", "Netherlands", "Portugal", "Italy", "Spain", 
    "United States", "Mexico", "Morocco", "Switzerland", 
    "Germany", "Colombia", "Uruguay", "Denmark", "Japan", 
    "Sweden", "Senegal"
]

selected_clubs2 = [
    "Real Madrid", "Arsenal", "Manchester United", "Manchester City", 
    "Bayern Munich", "Juventus", "Paris Saint-Germain", "Borussia Dortmund", 
    "Ajax", "Barcelona", "Chelsea", "Liverpool", "RB Leipzig", "Porto", "Napoli", "PSV",
    "Atlético Madrid", "Benfica", "Tottenham Hotspur", "Inter Milan", "AC Milan", "Valencia",
    "Sevilla", "Roma", "Monaco", "Newcastle United", "Aston Villa", "Brighton Hove Albion", 
    "Feyenoord", "Bayer Leverkusen", "Sporting CP", "Fenerbahçe", "Real Sociedad", "Lazio", 
    "Fiorentina", "Galatasaray", "Atalanta", "Marseille", "Beşiktaş", "Girona", "West Ham United",
    "Villarreal", "Athletic Bilbao", "Lens", "Braga", "Lyon", "SC Freiburg", "Rennes", "Real Betis", 
    "VFL Wolfsburg", "Lille"
]

selected_clubs3 = [
    "Real Madrid", "Arsenal", "Manchester United", "Manchester City", 
    "Bayern Munich", "Juventus", "Paris Saint-Germain", "Borussia Dortmund", 
    "Ajax", "Barcelona", "Chelsea", "Liverpool", "RB Leipzig", "Porto", "Napoli", "PSV",
    "Atlético Madrid", "Benfica", "Tottenham Hotspur", "Inter Milan", "AC Milan", "Valencia",
    "Sevilla", "Roma", "Monaco", "Newcastle United", "Aston Villa", "Brighton Hove Albion", 
    "Feyenoord", "Bayer Leverkusen", "Sporting CP", "Fenerbahçe", "Real Sociedad", "Lazio", 
    "Fiorentina", "Galatasaray", "Atalanta", "Marseille", "Beşiktaş", "Girona", "West Ham United",
    "Villarreal", "Athletic Bilbao", "Lens", "Braga", "Lyon", "SC Freiburg", "Rennes", "Real Betis", 
    "Wolfsburg", "Lille", "Argentina", "France", "Brazil", "England", "Belgium", 
    "Croatia", "Netherlands", "Portugal", "Italy", "Spain", 
    "United States", "Mexico", "Morocco", "Switzerland", 
    "Germany", "Colombia", "Uruguay", "Denmark", "Japan", 
    "Sweden", "Senegal"
]
selected_clubs = selected_clubs1

def set_option(option):
    global selected_clubs
    if option == "Nations":
        selected_clubs = selected_clubs1
    elif option == "Clubs":
        selected_clubs = selected_clubs2
    elif option == "Nations and Clubs":
        selected_clubs = selected_clubs3

used_clubs = []


# Mapping of positions to grid coordinates for 4-3-3 formation
position_coordinates = {
    "Left Winger": (0, 0),
    "Striker": (1, 0),
    "Right Winger": (2, 0),
    "Midfielder": (0, 1),
    "Midfielder": (1, 1),
    "Midfielder": (2, 1),
    "Left Back": (0, 2),
    "Center Back": (1, 2),
    "Center Back": (2, 2),
    "Right Back": (3, 2),
    "Goalkeeper": (1, 3)
}

valid_positions = {
    "Goalkeeper": ["Goalkeeper",],

    "Right Back": ["Full-backWingerForward","DefenderMidfielder","Full back","Right-BackRight wing-back","Fullback","Full-back/Winger","Right-Winger/Midfielder/right wing-back",
                   "Centre back/Right-Back","ForwardRight-Back","Right-Back/Right wing","Right-Back","Midfielder/Right Back","Right wing-back","Right-Winger/Right-Back","Centre-back/Right-Back",
                   "Full-Back","WingerFull-back","Defensive-Midfielder/Full-back","Right-Back/Defensive-Midfielder","Right-Back/Midfielder","Defender/Right-Back/Midfielder","Full-back",
                   "Defender/Midfielder","full-back","Right-WingerRight-Back","Right-Back/right wing-back","wing-back","Midfielder/Winger/Full-back","Right-Back/Winger","Defender",
                   "Right-Back/Right wing-back","Full-backAttacking-Midfielder","defender","Right Back","Right-Backmidfielder","DefenderDefensive-Midfielder","Defender/Defensive-Midfielder",
                   "Full-Back/Winger","right wing-back",],

    "Center Back": ["DefenderMidfielder","Center back","centre-back.","Defensive-MidfielderCentre back","centre back","Centre back/Right-Back","Defensive-Midfielder/Centre back",
                    "Centre-backLeft-Back","Centre-backDefensive-Midfielder","Centre-back/Right-Back","Defensive-Midfielder∙Centre-back","Defensive-MidfielderDefender","Back","sweeper","Midfielder/Defender",
                    "Central defender","Defender/Right-Back/Midfielder","Defender/Midfielder","Centre-Back","Centre back","Centre Back","Centre-back/Left-Back","Centre-back","Defender","Center Back",
                    "defender","Left-Back / Centre back/Midfielder","Center-back","Center-Back","DefenderDefensive-Midfielder","Defender/Defensive-Midfielder","centre-back",],

    "Left Back": ["Left Back","Full-backWingerForward","DefenderMidfielder","Full back","left wing-back","Fullback","Left-Back","Full-back/Winger","Left-Back/Midfielder/Left winger",
                  "Centre-backLeft-Back","Left-BackMidfielder","Left winger/left wing-back","Left-Back/left wing-back","Left wingback","Back","Full-Back","WingerFull-back","Defensive-Midfielder/Full-back",
                  "Full-back","Left-Back/wing-back","Defender/Midfielder","full-back","Left wing-back","wing-back","Left wing-backMidfielder","WingerLeft full-back","Centre-back/Left-Back","Midfielder/Winger/Full-back",
                  "Defender","Full-backAttacking-Midfielder","defender","Left-Back / Centre back/Midfielder","Winger/Left-Back","Defender/Defensive-Midfielder","Left-Back/Left winger","Full-Back/Winger",],

    "Midfielder": ["Defensive-MidfielderSweeper","DefenderMidfielder","Attacking-MidfielderRight-Winger","Attacking-Midfielder/winger","Defensive-MidfielderCentre back",
                   "Central Midfielder","Right-Winger/Midfielder/right wing-back","Left-Back/Midfielder/Left winger","Defensive-Midfielder/Centre back","Left-BackMidfielder",
                   "Midfielder/Forward","Midfield","Forward/Attacking-Midfielder","Midfielder","Attacking-Midfielder/forward","ForwardWingerMidfielder","Central midfielder/Attacking-Midfielder",
                   "Attacking-Midfielder/Winger","ForwardRight-Back","Attacking-Midfielder/Forward","Defensive    midfielder","Central midfielder","Centre midfielder","Defensive-Midfielder",
                   "Midfielder/Right Back","Central midfielder/Defensive-Midfielder","Attacking-Midfielder","Centre-backDefensive-Midfielder","Wide midfielder","Defensive-Midfielder∙Centre-back",
                   "Defensive-MidfielderDefender","central midfielder","Left winger/attacking midfielder","Midfielder/Defender","Defensive-Midfielder/Full-back","Right-Back/Defensive-Midfielder",
                   "attacking Midfielder","Right-Back/Midfielder","Defender/Right-Back/Midfielder","Attacking-Midfielder&Centre Forward","Defender/Midfielder","ForwardMidfielder","MidfielderWinger",
                   "Left wing-backMidfielder","Midfielder/Winger/Full-back","Forward/Midfielder","WingerAttacking-Midfielder","Full-backAttacking-Midfielder","midfielder","Attacking-MidfielderForward",
                   "Defensive Midfielder","Midfielder/Winger","ForwardAttacking-Midfielder","Left-Back / Centre back/Midfielder","Right-Backmidfielder","DefenderDefensive-Midfielder","attacking midfielder",
                   "Defender/Defensive-Midfielder","Attacking-Midfielderforward","Attacking-MidfielderWinger","Utility player","Attacking-MidfielderStriker",],

    "Right Winger": ["Full-backWingerForward","Attacking-MidfielderRight-Winger","Attacking-Midfielder/winger","Outside right","Full-back/Winger","Striker/Right Winger",
                     "Right-Winger/Midfielder/right wing-back","Forward", "Forward/Attacking-Midfielder","Attacking-Midfielder/forward","ForwardWingerMidfielder","winger","Attacking-Midfielder/Winger",
                     "Attacking-Midfielder/Forward","Right-Back/Right wing","ForwardLeft winger","Winger/Striker","forward","Right-Winger/Right-Back","Right-Winger","WingerFull-back","right-winger",
                     "Right-Left Winger","ForwardMidfielder","MidfielderWinger","Right-WingerRight-Back","StrikerForward","Midfielder/Winger/Full-back","Forward/Midfielder","Right-Back/Winger",
                     "WingerAttacking-Midfielder","Attacking-MidfielderForward","Right-Winger/Forward","Midfielder/Winger","ForwardAttacking-Midfielder","Winger/Left-Back","Winger/Forward",
                     "Attacking-Midfielderforward","Second-Striker/Winger","Attacking-MidfielderWinger","Full-Back/Winger","Winger","WingerForward","Forward/Winger"],

    "Left Winger": ["Left winger","Left Winger","Full-backWingerForward","Attacking-Midfielder/winger","Full-back/Winger","Left winger/Striker","Left-Back/Midfielder/Left winger",
                    "Forward","Midfielder/Forward", "Forward/Attacking-Midfielder","Attacking-Midfielder/forward","ForwardWingerMidfielder","winger","left winger","Left winger/left wing-back",
                    "Attacking-Midfielder/Winger","ForwardRight-Back","Attacking-Midfielder/Forward","ForwardLeft winger","Winger/Striker",
                    "forward","Left winger/attacking midfielder","WingerFull-back","Right-Left Winger","ForwardMidfielder","MidfielderWinger","StrikerForward","Midfielder/Winger/Full-back",
                    "Forward/Midfielder","Right-Back/Winger","WingerAttacking-Midfielder","Left wingerForward","Attacking-MidfielderForward","Midfielder/Winger","ForwardAttacking-Midfielder","Winger/Left-Back",
                    "Winger/Forward","Left-wingerStriker","Attacking-Midfielderforward","Second-Striker/Winger","Left-Back/Left winger","Attacking-MidfielderWinger","Full-Back/Winger","Winger","WingerForward",
                    "Forward/Winger"],

    "Striker": ["Striker","Full-backWingerForward","center forward","Second Striker","Left winger/Striker","Striker/Right Winger","Second-Striker","Forward","second forward",
                "Forward/Attacking-Midfielder","Attacking-Midfielder/forward","ForwardWingerMidfielder","ForwardRight-Back","Attacking-Midfielder/Forward","ForwardLeft winger","Winger/Striker",
                "forward","second striker","Attacking-Midfielder&Centre Forward","ForwardMidfielder","Centre-forward","StrikerForward","centre-forward","Forward/Midfielder","striker","Left wingerForward",
                "Attacking-MidfielderForward","Right-Winger/Forward","Second striker","ForwardAttacking-Midfielder","Winger/Forward","Left-wingerStriker","Centre forward","Attacking-Midfielderforward",
                "Second-Striker/Winger","Attacking-MidfielderStriker","WingerForward","Forward/Winger"]

}


def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
class GameExplanationPopup(Popup):
    def __init__(self, start_countdown_callback, **kwargs):
        super().__init__(**kwargs)
        self.start_countdown_callback = start_countdown_callback
        self.title = "How to Play"
        self.size_hint = (0.8, 0.6)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create the ScrollView
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)  # Allow only vertical scrolling

        # Add the game explanation text
        explanation_label = Label(
            text="Welcome to Position Match!\n\n" 
            "Objective: The aim of this game is to correctly name football players based on their playing position and association with a given club or nation.\n\n" 
            "How to Play:\n" 
            "1. Setup: At the start of the game, you'll be presented with a 4-3-3 football formation, showing 11 empty positions on the field.\n\n" 
            "2. Starting the Game: A football club or nation will be displayed on the screen.\n\n" 
            "3. Fill the positions: Click on any position on the field. Your task is to name a footballer who has either played for the displayed club in his career or currently represents the displayed nation and plays in the chosen position.\n\n" 
            "4. Progressing: If your answer is correct, the chosen position will be filled with the player's name, and a new club or nation will be shown. Continue filling in the positions by naming the correct players.\n\n" 
            "5. Winning the Game: The challenge is to successfully fill all 11 positions within the given time frame. Complete the formation to win the game!\n\n",
            size_hint_y=None,  # Important for scrolling
            size_hint_x=1,    # Ensure it takes the full width
            shorten=False,  # Ensure text doesn't get truncated
            halign='left',  # Align text to the left
            valign='top'
        )
        explanation_label.bind(texture_size=explanation_label.setter('size'))  # Set the size based on the content

        # Method to update the text_size of the explanation_label
        def update_text_size(instance, value):
            explanation_label.text_size = (value[0], None)

        # Bind the size of the scroll_view to update_text_size method
        scroll_view.bind(size=update_text_size)

        scroll_view.add_widget(explanation_label)
        layout.add_widget(scroll_view)

        # Modify the close button to also start the countdown
        close_button = Button(text="Start Game", size_hint_y=None, height=44)
        close_button.bind(on_press=self.start_countdown_and_dismiss)
        layout.add_widget(close_button)

        self.content = layout
    def start_countdown_and_dismiss(self, instance):
        self.start_countdown_callback()
        self.dismiss()

class PlayerPositionDialog(Popup):
    def __init__(self, club_logo, position, check_player_callback, button_instance, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.7, 0.4)  # 70% of the window size
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centered in the window
        self.club_logo = club_logo
        self.position = position
        self.check_player_callback = check_player_callback
        self.title = f"Name a player for {self.position} at {self.club_logo}"

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

        self.button_instance = button_instance

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
            if matching_players:
                self.dropdown.open(self.player_input)

    def select_player(self, player_name):
        """Set the selected player name in the TextInput and close the dropdown."""
        self.player_input.text = player_name
        self.dropdown.dismiss()

    def submit_player_name(self, instance):
        player_name = self.player_input.text
        self.dismiss()
        self.check_player_callback(player_name, self.club_logo, self.position, self.button_instance)


class FormationGame(BoxLayout):
    def __init__(self, **kwargs):
        super(FormationGame, self).__init__(**kwargs)
        # Display the game explanation popup
        self.game_explanation_popup = GameExplanationPopup(self.start_countdown)
        self.game_explanation_popup.open()
        self.orientation = 'vertical'
        self.spacing = 10
        self.position_buttons = {}

        # Attackers
        attackers_wrapper = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[0, 5, 0, 0])  # Reduced height and padding
        attackers_layout = GridLayout(cols=3, size_hint=(3, 1), spacing=20)  # Added spacing between columns
        for position in ["Left Winger", "Striker", "Right Winger"]:
            position_box = BoxLayout(padding=[10, 0])  # Padding on the left and right
            self.add_position_button(position, position_box)
            attackers_layout.add_widget(position_box)
        #attackers_wrapper.add_widget(BoxLayout())  # Left spacer
        attackers_wrapper.add_widget(attackers_layout)
        #attackers_wrapper.add_widget(BoxLayout())  # Right spacer
        self.add_widget(BoxLayout(size_hint_y=None, height=30))  # Adjust height as needed
        self.add_widget(attackers_wrapper)
        self.add_widget(BoxLayout(size_hint_y=None, height=30))  # Adjust height as needed

        # Midfielders
        midfielders_wrapper = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        midfielders_layout = GridLayout(cols=3, size_hint=(1.5, 1), spacing=20)  # Adjusted size_hint for width to 0.7 from 2
        for idx, position in enumerate(["Midfielder", "Midfielder", "Midfielder"]):
            position_box = BoxLayout(padding=[10, 0])  # Padding on the left and right
            self.add_position_button(position, position_box, f"midfielder_{idx}")
            midfielders_layout.add_widget(position_box)

        left_spacer = BoxLayout(size_hint=(0.15, 1))  # Adjusted size_hint for width to 0.15
        right_spacer = BoxLayout(size_hint=(0.15, 1))  # Adjusted size_hint for width to 0.15

        midfielders_wrapper.add_widget(left_spacer)
        midfielders_wrapper.add_widget(midfielders_layout)
        midfielders_wrapper.add_widget(right_spacer)
        self.add_widget(midfielders_wrapper)
        self.add_widget(BoxLayout(size_hint_y=None, height=30))  # Adjust height as needed

        # Defenders
        defenders_wrapper = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        defenders_layout = GridLayout(cols=4, size_hint=(5, 1), spacing=2)  # Added spacing between columns
        for idx, position in enumerate(["Left Back", "Center Back", "Center Back", "Right Back"]):
            position_box = BoxLayout(padding=[10, 0])  # Padding on the left and right
            if position == "Center Back":
                self.add_position_button(position, position_box, f"centerback_{idx}")
            else:
                self.add_position_button(position, position_box)
            defenders_layout.add_widget(position_box)
        #defenders_wrapper.add_widget(BoxLayout())  # Left spacer
        defenders_wrapper.add_widget(defenders_layout)
        #defenders_wrapper.add_widget(BoxLayout())  # Right spacer
        self.add_widget(defenders_wrapper)
        self.add_widget(BoxLayout(size_hint_y=None, height=10))  # Adjust height as needed

        # Goalkeeper (placed in the center below defenders)
        goalkeeper_wrapper = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        spacer_left = BoxLayout()  # Left spacer
        goalkeeper_layout = GridLayout(cols=1, size_hint=(1, 1))  # Adjusted size_hint for width
        btn = Button(text="Goalkeeper", font_size=20, size_hint=(2, 1))
        self.position_buttons["goalkeeper_btn"] = btn
        btn.bind(on_press=self.select_position)
        goalkeeper_layout.add_widget(btn)
        spacer_right = BoxLayout()  # Right spacer
        goalkeeper_wrapper.add_widget(spacer_left)
        goalkeeper_wrapper.add_widget(goalkeeper_layout)
        goalkeeper_wrapper.add_widget(spacer_right)
        self.add_widget(goalkeeper_wrapper)
        self.add_widget(BoxLayout(size_hint_y=None, height=50))  # Adjust height as needed


        # Club logo and name
        club_logo_wrapper = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, pos_hint={'center_x': 0.5})

        self.club_logo = Image(size_hint=(None, None), size=(140, 140), pos_hint={'center_x': 0.5})
        club_logo_wrapper.add_widget(self.club_logo)

        self.club_name_label = Label(font_size=24, size_hint=(None, None), size=(100, 30), halign='center', valign='middle', pos_hint={'center_x': 0.5})
        self.club_name_label.bind(size=self.club_name_label.setter('text_size'))
        club_logo_wrapper.add_widget(self.club_name_label)

        self.add_widget(club_logo_wrapper)
        self.load_random_club()

        # Add a countdown timer label at the top with "Time left:" prefix
        self.timer_label = Label(text="Time left: 100", font_size=30, size_hint_y=None, height=30, color=get_color_from_hex("#FFFFFF"))
        self.add_widget(self.timer_label)
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))

        # Start the countdown timer
        self.seconds_left = 100

        # Add the Return to Home button at the bottom
        self.home_button = Button(text="Return to Home", size_hint_y=None, height=44)
        self.home_button.bind(on_press=self.return_to_home)
        self.add_widget(self.home_button)

    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_event = Clock.schedule_interval(self.update_timer, 1)

    def reset_position_buttons(self):
        """Reset the font size of the position buttons to the original size."""
        for btn in self.position_buttons.values():
            btn.font_size = 20  # Set this to the original font size
    
    def update_timer(self, dt):
        """Update the countdown timer."""
        if self.seconds_left > 0:
            self.seconds_left -= 1
            # Update the label with "Time left:" prefix
            self.timer_label.text = f"Time left: {self.seconds_left}"
        else:
            # Stop the countdown when it reaches 0
            Clock.unschedule(self.countdown_event)
            self.show_loss_popup()  # Assuming you have a method to show the loss popup

    def show_loss_popup(self):
        """Display the 'You lost!' popup with 'Close' and 'Play again' buttons."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="You lost!"))

        # Close button
        close_button = Button(text="Finish without countdown", size_hint_y=None, height=44)
        close_button.bind(on_press=lambda x: loss_popup.dismiss())
        layout.add_widget(close_button)

        # Play again button
        play_again_button = Button(text="Play again", size_hint_y=None, height=44)
        play_again_button.bind(on_press=lambda x: self.play_again(loss_popup))  # Pass the loss_popup instance
        layout.add_widget(play_again_button)

        loss_popup = Popup(title='Game Over', content=layout, size_hint=(0.8, 0.4))
        loss_popup.open()

    def return_to_home(self, instance):
        # Reset the game
        self.reset_game()
        # Change the screen to the starting screen
        App.get_running_app().root.current = 'start'

    def add_position_button(self, position, layout, btn_id=None):
        btn = Button(text=position, font_size=self.get_font_size(position), size_hint=(0.33, 1))
        btn.btn_id = btn_id  # Set the custom btn_id property
        btn.bind(on_press=self.select_position)
        self.position_buttons[btn_id if btn_id else position] = btn
        layout.add_widget(btn)

    def get_font_size(self, position):
        if len(position) > 10:
            return 16  # Adjust this value as needed
        else:
            return 20  # Default font size

    def load_random_club(self):
        global selected_clubs, used_clubs
        if not selected_clubs:  # If all clubs have been used, reset the list
            selected_clubs, used_clubs = used_clubs, []

        club = random.choice(selected_clubs)
        selected_clubs.remove(club)
        used_clubs.append(club)
        self.club_logo.source = f"Club Logo/{club.replace(' ', '_')}.png"
        self.club_name_label.text = club

    def select_position(self, instance):
        position = instance.text
        dialog = PlayerPositionDialog(self.club_logo.source.split('/')[-1].replace('.png', '').replace('_', ' '), position, self.check_player, instance)
        dialog.open()

    def check_player(self, player_name, club, formation_position, button_instance):
        if player_name in players:
            if club not in players[player_name]['clubs']:
                # Show error popup for club mismatch
                layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
                
                error_label = Label(
                    text=f"Incorrect! {player_name} doesn't play for {club}.",
                    size_hint_y=None,
                    height=44,
                    halign='center',  # Horizontal alignment
                    valign='middle',  # Vertical alignment
                )
                error_label.bind(texture_size=error_label.setter('size'))  # Adjust the size based on the content
                layout.add_widget(error_label)

                error_popup = Popup(title='Error', content=layout, size_hint=(0.8, 0.4))
                
                close_button = Button(text="Close", size_hint_y=None, height=44)
                close_button.bind(on_press=error_popup.dismiss)
                layout.add_widget(close_button)
                
                # Method to update the text_size of the error_label
                def adjust_text_size(instance, value):
                    error_label.text_size = (value[0] * 0.9, None)

                # Bind the size of the error_popup to adjust_text_size method
                error_popup.bind(size=adjust_text_size)
                
                error_popup.open()
                return

            # Check if the player's position is in the list of valid positions for the formation position
            if any(pos in players[player_name]['positions'] for pos in valid_positions[formation_position]):
                button_instance.text = player_name
                button_instance.text_size = (button_instance.width * 0.9, None)  # 90% of button width
                button_instance.halign = 'center'
                button_instance.valign = 'middle'
                
                # Adjust font size based on the length of the player's name
                if len(player_name) > 15:
                    button_instance.font_size = 14  # Adjust this value as needed
                else:
                    button_instance.font_size = 20  # Default font size

                button_instance.disabled = True
                if all([btn.disabled for btn in self.position_buttons.values()]):
                    self.show_win_popup()
                else:
                    self.load_random_club()
            else:
                # Show error popup for position mismatch
                layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
                
                error_label = Label(
                    text=f"Incorrect! {player_name} doesn't play as {formation_position} for {club}.",
                    size_hint_y=None,
                    height=44,
                    halign='center',  # Horizontal alignment
                    valign='middle',  # Vertical alignment
                )
                error_label.bind(texture_size=error_label.setter('size'))  # Adjust the size based on the content
                layout.add_widget(error_label)

                error_popup = Popup(title='Error', content=layout, size_hint=(0.8, 0.4))
                
                close_button = Button(text="Close", size_hint_y=None, height=44)
                close_button.bind(on_press=error_popup.dismiss)
                layout.add_widget(close_button)
                
                # Method to update the text_size of the error_label
                def adjust_text_size(instance, value):
                    error_label.text_size = (value[0] * 0.9, None)

                # Bind the size of the error_popup to adjust_text_size method
                error_popup.bind(size=adjust_text_size)
                
                error_popup.open()

    def reset_game(self):
        for btn_id, btn in self.position_buttons.items():
            if btn_id in btn_id_to_position:
                btn.text = btn_id_to_position[btn_id]
            elif btn_id == "goalkeeper_btn":
                btn.text = "Goalkeeper"
            else:
                # Reset the other buttons based on their btn_id
                btn.text = btn_id.replace('_', ' ').title()
            btn.disabled = False
        self.load_random_club()

    def show_win_popup(self):
        """Display the 'You won!' popup with 'Close' and 'Play again' buttons."""
        # Cancel the countdown timer
        Clock.unschedule(self.countdown_event)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="You won!"))

        # Close button
        close_button = Button(text="Close", size_hint_y=None, height=44)
        close_button.bind(on_press=lambda x: win_popup.dismiss())
        layout.add_widget(close_button)

        # Play again button
        play_again_button = Button(text="Play again", size_hint_y=None, height=44)
        play_again_button.bind(on_press=lambda x: self.play_again(win_popup))  # Pass the win_popup instance
        layout.add_widget(play_again_button)

        win_popup = Popup(title='Congratulations!', content=layout, size_hint=(0.8, 0.4))
        win_popup.open()

    def play_again(self, win_popup_instance):
        """Reset the game and close the popup."""
        self.reset_game()
        win_popup_instance.dismiss()
        # Reset the font size of the position buttons
        self.reset_position_buttons()
        # Reset the countdown timer
        self.seconds_left = 100
        self.timer_label.text = "100"
        self.countdown_event = Clock.schedule_interval(self.update_timer, 1)


class FormationGameApp(App):
    def build(self):
        return FormationGame()

if __name__ == '__main__':
    FormationGameApp().run()