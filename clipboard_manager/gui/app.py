import os
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import LabelBase

# Set window size
Window.size = (400, 40)  # Spotlight style width/height
Window.borderless = True
Window.top = 100  # Position from top of screen
Window.left = 100  # Position from left
Window.clearcolor = (0, 0, 0, 0)  # Fully transparent background

# Construct the absolute path for the font file
font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSansMono.ttf')

# Register DejaVu Sans Mono font
LabelBase.register(name='DejaVuSansMono', fn_regular=font_path)

class SpotlightSearch(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Background rectangle with rounded corners and semi-transparent color
            Color(0, 0, 0, 0.7)  # black, 70% opacity
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Add TextInput on top
        self.input = TextInput(
            hint_text='Search...',
            font_name='DejaVuSansMono',
            font_size=16,
            background_color=(0,0,0,0),
            foreground_color=(1,1,1,1),
            cursor_color=(1,1,1,1),
            padding_y=(8,8),
            multiline=False
        )
        self.add_widget(self.input)
        self.input.size_hint = (1,1)
        self.input.pos_hint = {"x":0, "y":0}

    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# class SpotlightApp(App):
#     def build(self):
#         return SpotlightSearch()

# if __name__ == "__main__":
#     SpotlightApp().run()
