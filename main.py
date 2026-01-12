# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from Celes import get_bot_reply, BOT_NAME, speak

Window.clearcolor = (0, 0, 0, 1)  # Black background

class ChatBubble(AnchorLayout):
    def __init__(self, text, align="left", color=(1, 1, 1, 1), **kwargs):
        super().__init__(size_hint_y=None, **kwargs)
        self.anchor_x = "left" if align == "left" else "right"
        self.anchor_y = "top"

        label = Label(
            text=text,
            markup=True,
            size_hint=(None, None),
            padding=(12, 8),
            color=color,
            text_size=(Window.width * 0.7, None)
        )
        label.bind(texture_size=label.setter("size"))
        self.add_widget(label)
        self.height = label.height + 20

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.chat_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.chat_box.bind(minimum_height=self.chat_box.setter("height"))
        self.scroll.add_widget(self.chat_box)

        # Input bar
        self.input_bar = BoxLayout(size_hint_y=None, height=60, spacing=5, padding=[10,5,10,5])

        self.mic_btn = Button(size_hint_x=None, width=50, text="🎤")
        self.mic_btn.bind(on_press=self.voice_input)

        self.image_btn = Button(size_hint_x=None, width=50, text="📷")
        self.image_btn.bind(on_press=self.send_image_placeholder)

        self.input = TextInput(
            multiline=False,
            hint_text="Message Celes...",
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.5, 0.8, 1, 1),
            cursor_color=(0.5, 0.8, 1, 1)
        )

        self.send_btn = Button(size_hint_x=None, width=50, text="➡️")
        self.send_btn.bind(on_press=self.send_message)

        self.input_bar.add_widget(self.mic_btn)
        self.input_bar.add_widget(self.image_btn)
        self.input_bar.add_widget(self.input)
        self.input_bar.add_widget(self.send_btn)

        self.add_widget(self.scroll)
        self.add_widget(self.input_bar)

        self.add_bot_message(f"Hello! I'm {BOT_NAME}")

    def add_user_message(self, text):
        bubble = ChatBubble(f"[color=87ceeb]{text}[/color]", align="right")
        self.chat_box.add_widget(bubble)
        self.scroll.scroll_y = 0

    def add_bot_message(self, text):
        bubble = ChatBubble(f"[color=ff69b4]{BOT_NAME}: {text}[/color]", align="left")
        self.chat_box.add_widget(bubble)
        self.scroll.scroll_y = 0
        speak(text)  # TTS placeholder

    def send_message(self, *args):
        text = self.input.text.strip()
        if not text:
            return
        self.input.text = ""
        self.add_user_message(text)
        reply = get_bot_reply(text)
        self.add_bot_message(reply)

    def voice_input(self, *args):
        self.input.text = "User spoke: [placeholder]"  # Placeholder for voice

    def send_image_placeholder(self, *args):
        self.add_user_message("[Image sent]")  # Placeholder for images
        self.add_bot_message("[Image received]")  # Placeholder

class ChatApp(App):
    def build(self):
        return ChatUI()

if __name__ == "__main__":
    ChatApp().run()