import kivy
import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Line, Rectangle, Color
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import xml.etree.ElementTree as ET
import unicodedata
from kivy.graphics import Line

class FeatureLabel(Label):
    def __init__(self, bg_color, **kwargs):
        super(FeatureLabel, self).__init__(**kwargs)
        self.bg_color = bg_color
        self.color = (1, 1, 1, 1)  # Set text color to white
        self.valign = 'middle'  # Add this line
        self.bind(size=self._update_rect, pos=self._update_rect)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(1, 1, 1, 1)  # Set color to white for the border
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        self.text_size = instance.size  # Set text_size to the size of the label

    def on_size(self, *args):
        self.text_size = self.size  # Update text_size whenever the size changes
    
class AgeLabel(Label):
    def __init__(self, bg_color=(0.8, 0.8, 0.8, 1), direction=None, **kwargs):
        self.bg_color = bg_color
        self.direction = direction
        super(AgeLabel, self).__init__(**kwargs)

    def on_size(self, *args):
        Clock.schedule_once(lambda dt: self.draw_arrow(), 0.1)
        if self.canvas:
            if self.canvas.before:
                self.canvas.before.clear()
            with self.canvas.before:
                Color(*self.bg_color)
                Rectangle(pos=self.pos, size=self.size)
                Color(1, 1, 1, 1)  # Set color to white for the border
                Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)

    def draw_arrow(self):
        arrow_length = self.height * 0.6  # Adjust this value to change the arrow's size
        arrow_head_length = arrow_length * 0.2  # Adjust this value to change the arrowhead's size

        with self.canvas.after:  # Drawing on the canvas after the background
            Color(0, 0, 0, 1)  # Set the color to black
            if self.direction == 'up':
                Line(points=[self.right - 20, self.y + (self.height - arrow_length) / 2, self.right - 20, self.y + (self.height + arrow_length) / 2], width=1.5)
                Line(points=[self.right - 20, self.y + (self.height + arrow_length) / 2, self.right - 25, self.y + (self.height + arrow_length) / 2 - arrow_head_length], width=1.5)
                Line(points=[self.right - 20, self.y + (self.height + arrow_length) / 2, self.right - 15, self.y + (self.height + arrow_length) / 2 - arrow_head_length], width=1.5)
            elif self.direction == 'down':
                Line(points=[self.right - 20, self.y + (self.height - arrow_length) / 2, self.right - 20, self.y + (self.height + arrow_length) / 2], width=1.5)
                Line(points=[self.right - 20, self.y + (self.height - arrow_length) / 2, self.right - 25, self.y + (self.height - arrow_length) / 2 + arrow_head_length], width=1.5)
                Line(points=[self.right - 20, self.y + (self.height - arrow_length) / 2, self.right - 15, self.y + (self.height - arrow_length) / 2 + arrow_head_length], width=1.5)
                    
# Set the background color
Window.clearcolor = get_color_from_hex("#353839")

# Parse the XML data
tree = ET.parse('scraped_data.xml')
root = tree.getroot()

players = {}
for row in root.findall('row'):
    name = row.find('Name_of_the_player').text
    club = row.find('Club').text
    nation = row.find('Nation').text
    league = row.find('League').text
    position = row.find('Position').text
    age = row.find('Age').text  # Parse the age
    players[name] = {'league': league, 'club': club, 'age': age, 'nation': nation, 'position': position}  # Include age in the dictionary

POSITION_MAPPING = {
    "GK": {"GK"},
    "DEF": {"RB", "LB", "CB", "LWB", "RWB"},
    "MID": {"CDM", "CM", "RM", "LM", "CAM"},
    "FW": {"CF", "RW", "LW", "ST"}
}

def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

class GameExplanationPopup(Popup):
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "How to Play"
        self.size_hint = (0.8, 0.6)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Explanation label
        explanation = (
            "Welcome to the Player Guess Game!\n\n"
            "Objective: Guess the secret football player.\n\n"
            "How to Play:\n"
            "1. Enter the name of a football player in the provided text input.\n\n"
            "2. Click on the 'Guess' button to check if the player's details matches the secret player.\n\n"
            "3. The player's details such as club, league, age, nation, and position will be displayed on the screen. If the guessed player's details match the secret player's details, the corresponding detail will turn green. Otherwise, it will turn red.\n\n"
            "4. If the age of the guessed player is less than the random player's age, an upward arrow will be displayed next to the age. If it's greater, a downward arrow will be shown.\n\n"
            "5. If you guess the correct player, a popup will appear congratulating you!\n\n"
            "6. You can reset the game or return to the home screen using the provided buttons.\n\n"
            "Note: Use the dropdown suggestions for easier player name input. The game also provides an explanation popup when it starts to guide new players.\n\n"
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

class CongratulationsPopup(Popup):
    def __init__(self, reset_game_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Congratulations!"
        self.size_hint = (0.6, 0.4)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Modified Label to ensure text fits within the popup
        congrats_label = Label(
            text="You've successfully guessed the player!",
            size_hint_y=None,
            height=44,
            halign='center',  # Horizontal alignment
            valign='middle',  # Vertical alignment
            text_size=(self.width * 0.9, None)  # Set the width for text bounding box
        )
        congrats_label.bind(size=self.adjust_text_size)  # Bind the size of the label to adjust its text size
        layout.add_widget(congrats_label)

        # Reset button
        reset_button = Button(text="Play again", size_hint_y=None, height=44)
        reset_button.bind(on_press=self.reset_and_dismiss)
        layout.add_widget(reset_button)

        # Close button
        close_button = Button(text="Close", size_hint_y=None, height=44)
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.reset_game_callback = reset_game_callback
        self.content = layout

    def adjust_text_size(self, instance, value):
        """Adjust the text size of the label based on its size."""
        instance.text_size = (value[0] * 0.9, None)

    def reset_and_dismiss(self, instance):
        """Reset the game and dismiss the popup."""
        self.reset_game_callback()  # Call the reset_game_callback to reset the game
        self.dismiss()  # Dismiss the popup

class GameOverPopup(Popup):
    def __init__(self, reset_game_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Game Over!"
        self.size_hint = (0.6, 0.4)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Modified Label to ensure text fits within the popup
        congrats_label = Label(
            text="The correct player was {self.random_player_name}.",
            size_hint_y=None,
            height=44,
            halign='center',  # Horizontal alignment
            valign='middle',  # Vertical alignment
            text_size=(self.width * 0.9, None)  # Set the width for text bounding box
        )
        congrats_label.bind(size=self.adjust_text_size)  # Bind the size of the label to adjust its text size
        layout.add_widget(congrats_label)

        # Reset button
        reset_button = Button(text="Play again", size_hint_y=None, height=44)
        reset_button.bind(on_press=self.reset_and_dismiss)
        layout.add_widget(reset_button)

        # Close button
        close_button = Button(text="Close", size_hint_y=None, height=44)
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.reset_game_callback = reset_game_callback
        self.content = layout

    def adjust_text_size(self, instance, value):
        """Adjust the text size of the label based on its size."""
        instance.text_size = (value[0] * 0.9, None)

    def reset_and_dismiss(self, instance):
        """Reset the game and dismiss the popup."""
        self.reset_game_callback()  # Call the reset_game_callback to reset the game
        self.dismiss()  # Dismiss the popup
        
class PlayerGuessGame(BoxLayout):
    def __init__(self, difficulty="easy", **kwargs):
        super(PlayerGuessGame, self).__init__(**kwargs)
        self.difficulty = difficulty
        self.orientation = 'vertical'
        self.spacing = 10

        # Input for player's name
        self.player_input = TextInput(hint_text="Enter player's name", multiline=False, size_hint_y=None, height=44)
        self.add_widget(self.player_input)

        # Guess button
        self.guess_button = Button(text="Guess", size_hint_y=None, height=44)
        self.guess_button.bind(on_press=self.check_player)
        self.add_widget(self.guess_button)

        # Results layout with increased spacing
        self.results_layout = GridLayout(cols=5, spacing=20, padding=[0, 0, 0, 0])
        self.add_widget(self.results_layout)

        # Add a label to display the guessed player's name
        self.guessed_player_label = Label(text="", font_size=20, halign='center', valign='middle', size_hint_y=None, height=44)
        self.add_widget(self.guessed_player_label)

        # Select a random player for the first round
        self.select_random_player()
        print(f"Random Player: {self.random_player_name}")  # Print the random player's name to the terminal

        # Create a dropdown for autocomplete
        self.dropdown = DropDown()
        self.player_input.bind(text=self.on_text)  # Bind the on_text method to the text input

        # Add the Return to Home button at the bottom
        self.home_button = Button(text="Return to Home", size_hint_y=None, height=44)
        self.home_button.bind(on_press=self.return_to_home)
        self.add_widget(self.home_button)

        # Show the GameExplanationPopup when the game starts
        self.show_game_explanation()

        # Initialize the tries counter
        self.tries = 0

    def show_game_explanation(self):
        # Define the callback function to start the game
        def start_game_callback(instance):
            # For now, just close the popup. You can add more logic here if needed.
            popup.dismiss()

        # Create and open the GameExplanationPopup
        popup = GameExplanationPopup(start_game_callback=start_game_callback)
        popup.open()


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

    def show_congrats_popup(self, *args):
        """Show the congratulations popup."""
        congrats_popup = CongratulationsPopup(reset_game_callback=self.reset_game)
        congrats_popup.open()
    
    def show_game_over_popup(self, *args):
        """Show the game over popup."""
        game_over_popup = GameOverPopup(reset_game_callback=self.reset_game)
        game_over_popup.content.children[2].text = f"The correct player was {self.random_player_name}."  # Update the label text with the correct player's name
        game_over_popup.open()

    def enable_guess_button(self, *args):
        """Enable the "Guess" button."""
        self.guess_button.disabled = False

    def animate_correct_features(self, dt):
        """Animate the appearance of the correct features."""
        random_player_data = players[self.random_player_name]
        delay = 0.5  # Initial delay before the first box appears
        last_anim = None  # To store the last animation object

        # Calculate the font size based on the screen width
        font_size = Window.width * 0.03  # Adjust the multiplier (0.03) as needed

        for feature, value in random_player_data.items():
            color = (1, 1, 1, 1)  # White text color
            bg_color = (0, 1, 0, 1)  # Green box color for correct features
            label = FeatureLabel(
                bg_color=bg_color,
                text=value, 
                font_size=font_size, 
                size_hint_y=None, 
                height=44, 
                color=color, 
                bold=True,
                text_size=(self.width/5, None),  # Set the width for text bounding box
                halign='center'  # Center-align the text
            )
            self.results_layout.add_widget(label)
            last_anim = Animation(opacity=1, duration=0.5)
            Clock.schedule_once(lambda dt, label=label: last_anim.start(label), delay)
            delay += 0.5  # Increase the delay for the next box

        # Use the on_complete event of the last animation to show the game over popup
        if last_anim:  # Ensure last_anim is not None
            last_anim.on_complete = self.show_game_over_popup

    def check_player(self, instance):
        # Disable the "Guess" button to prevent further clicks during the animation
        self.guess_button.disabled = True
        player_name = self.player_input.text
        if player_name in players:
            # Update the guessed player's name label
            self.guessed_player_label.text = f"Guessed Player: {player_name}"
            player_data = players[player_name]
            random_player_data = players[self.random_player_name]
            
            # Convert the positions of both guessed player and random player
            for category, positions in POSITION_MAPPING.items():
                if player_data['position'] in positions:
                    player_data['position'] = category
                if random_player_data['position'] in positions:
                    random_player_data['position'] = category

            # Calculate the font size based on the screen width
            font_size = Window.width * 0.03  # Adjust the multiplier (0.03) as needed

            def animate_label(label, delay):
                """Function to animate the appearance of a label."""
                label.opacity = 0  # Start with an opacity of 0 (invisible)
                anim = Animation(opacity=1, duration=0.5)
                Clock.schedule_once(lambda dt: anim.start(label), delay)
                return anim  # Return the animation object

            delay = 0.5  # Initial delay before the first box appears
            last_anim = None  # To store the last animation object
            for feature, value in player_data.items():
                color = (1, 1, 1, 1)  # White text color
                bg_color = (1, 0, 0, 1)  # Red box color by default
                direction = None
                if random_player_data[feature] == value:  # Compare with the random player's feature
                    bg_color = (0, 1, 0, 1)  # Green box color if they match
                if feature == 'age' and bg_color == (1, 0, 0, 1):  # If the feature is age and the box color is red
                    guessed_age = int(value)
                    random_age = int(random_player_data[feature])
                    if guessed_age < random_age:
                        direction = 'up'
                    else:
                        direction = 'down'
                if feature == 'age':
                    label = AgeLabel(
                        bg_color=bg_color,
                        text=value, 
                        font_size=font_size * 1.2, 
                        size_hint_y=None, 
                        height=44, 
                        color=color, 
                        bold=True,
                        text_size=(self.width/5, None),  # Set the width for text bounding box
                        halign='center',  # Center-align the text
                        direction=direction
                    )
                else:
                    label = FeatureLabel(
                        bg_color=bg_color,
                        text=value, 
                        font_size=font_size, 
                        size_hint_y=None, 
                        height=44, 
                        color=color, 
                        bold=True,
                        text_size=(self.width/5, None),  # Set the width for text bounding box
                        halign='center'  # Center-align the text
                    )
                self.results_layout.add_widget(label)
                last_anim = animate_label(label, delay)
                delay += 0.5  # Increase the delay for the next box
                self.player_input.text = ""

            
            # If the guessed player is the random player, select a new random player for the next round
            if player_name == self.random_player_name:
                self.random_player_name = random.choice(list(players.keys()))
                while self.random_player_name == player_name:  # Ensure the new random player is not the same as the guessed player
                    self.random_player_name = random.choice(list(players.keys()))
                
                # Use the on_complete event of the last animation to show the congratulations popup
                if last_anim:  # Ensure last_anim is not None
                    last_anim.on_complete = self.show_congrats_popup
            else:
                # Increment the tries counter
                self.tries += 1

                # Check if the maximum number of tries has been reached
                if self.tries >= 8:
                    # Disable the "Guess" button
                    self.guess_button.disabled = True
                    # Display the correct features using the same animation
                    for feature, value in random_player_data.items():
                        color = (1, 1, 1, 1)  # White text color
                        bg_color = (0, 1, 0, 1)  # Green box color for correct features
                        label = FeatureLabel(
                            bg_color=bg_color,
                            text=value, 
                            font_size=font_size, 
                            size_hint_y=None, 
                            height=44, 
                            color=color, 
                            bold=True,
                            text_size=(self.width/5, None),  # Set the width for text bounding box
                            halign='center'  # Center-align the text
                        )
                        self.results_layout.add_widget(label)
                        last_anim = animate_label(label, delay)
                        delay += 0.5  # Increase the delay for the next box

                    # If there's an animation, show the "Game Over" popup after the animation completes
                    if last_anim:
                        last_anim.on_complete = self.show_game_over_popup
                    else:
                        # If there's no animation, show the "Game Over" popup immediately
                        self.show_game_over_popup()
                elif last_anim:
                    # If there's an animation, re-enable the "Guess" button after the animation completes
                    last_anim.on_complete = self.enable_guess_button
                else:
                    # If there's no animation, re-enable the "Guess" button immediately
                    self.enable_guess_button()
        else:
            # Player not found
            popup = Popup(title='Error', content=Label(text="Player not found!"), size_hint=(0.6, 0.3))
            popup.bind(on_dismiss=self.enable_guess_button)  # Re-enable the "Guess" button when the popup is dismissed
            popup.open()
            self.player_input.text = ""  # Clear the player input

    def reset_game(self):
        """Reset the game to its initial state."""
        # Clear the results layout
        self.results_layout.clear_widgets()
        # Clear the player input
        self.player_input.text = ""
        # Clear the guessed player text
        self.guessed_player_label.text = ""
        # Select a new random player
        self.select_random_player()
        # Reset the tries counter
        self.tries = 0
        # Enable the "Guess" button
        self.enable_guess_button()

    def return_to_home(self, instance):
        # Reset the game
        self.reset_game()
        # Change the screen to the starting screen
        App.get_running_app().root.current = 'start'

    def select_random_player(self):
        if self.difficulty == "easy":
            self.random_player_name = random.choice(list(players.keys())[:150])
        elif self.difficulty == "medium":
            self.random_player_name = random.choice(list(players.keys())[150:300])
        else:  # hard
            self.random_player_name = random.choice(list(players.keys())[300:])

class PlayerGuessApp(App):
    def build(self):
        return PlayerGuessGame()

if __name__ == '__main__':
    PlayerGuessApp().run()