import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

class MusicPlayer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Текущий трек
        self.current_track = None
        self.sound = None
        self.playlist = []
        self.current_index = 0

        # Заголовок
        self.title_label = Label(
            text="🎵 Мой Плеер",
            font_size='24sp',
            size_hint_y=0.15
        )
        self.add_widget(self.title_label)

        # Название трека
        self.track_label = Label(
            text="Трек не выбран",
            font_size='16sp',
            size_hint_y=0.2
        )
        self.add_widget(self.track_label)

        # Кнопка выбора папки
        self.folder_btn = Button(
            text="📁 Выбрать папку с музыкой",
            size_hint_y=0.15,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.folder_btn.bind(on_press=self.open_file_chooser)
        self.add_widget(self.folder_btn)

        # Кнопки управления
        controls = BoxLayout(size_hint_y=0.15, spacing=10)

        self.prev_btn = Button(text="⏮", font_size='24sp')
        self.prev_btn.bind(on_press=self.play_prev)
        controls.add_widget(self.prev_btn)

        self.play_btn = Button(text="▶", font_size='24sp')
        self.play_btn.bind(on_press=self.toggle_play)
        controls.add_widget(self.play_btn)

        self.next_btn = Button(text="⏭", font_size='24sp')
        self.next_btn.bind(on_press=self.play_next)
        controls.add_widget(self.next_btn)

        self.add_widget(controls)

        # Кнопка выхода
        self.exit_btn = Button(
            text="Выход",
            size_hint_y=0.1,
            background_color=(1, 0.3, 0.3, 1)
        )
        self.exit_btn.bind(on_press=self.stop_app)
        self.add_widget(self.exit_btn)

    def open_file_chooser(self, instance):
        """Открывает диалог выбора папки"""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.mp3', '*.wav', '*.ogg']
        )
        content.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        select_btn = Button(text="Выбрать")
        cancel_btn = Button(text="Отмена")

        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        popup = Popup(
            title="Выбери папку с музыкой",
            content=content,
            size_hint=(0.9, 0.9)
        )

        def select_folder(instance):
            if filechooser.selection:
                folder = os.path.dirname(filechooser.selection[0])
                self.load_playlist(folder)
                popup.dismiss()

        select_btn.bind(on_press=select_folder)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def load_playlist(self, folder):
        """Загружает все аудиофайлы из папки"""
        self.playlist = []
        for file in os.listdir(folder):
            if file.endswith(('.mp3', '.wav', '.ogg')):
                self.playlist.append(os.path.join(folder, file))

        if self.playlist:
            self.current_index = 0
            self.load_track(self.playlist[0])
            self.track_label.text = f"Загружено треков: {len(self.playlist)}"
        else:
            self.track_label.text = "В папке нет музыки"

    def load_track(self, path):
        """Загружает трек"""
        if self.sound:
            self.sound.stop()

        self.current_track = path
        self.sound = SoundLoader.load(path)

        if self.sound:
            self.track_label.text = f"🎵 {os.path.basename(path)}"

    def toggle_play(self, instance):
        """Play / Pause"""
        if not self.sound:
            return

        if self.sound.state == 'play':
            self.sound.stop()
            self.play_btn.text = "▶"
        else:
            self.sound.play()
            self.play_btn.text = "⏸"

    def play_next(self, instance):
        """Следующий трек"""
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_track(self.playlist[self.current_index])
        if self.sound:
            self.sound.play()
            self.play_btn.text = "⏸"

    def play_prev(self, instance):
        """Предыдущий трек"""
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_track(self.playlist[self.current_index])
        if self.sound:
            self.sound.play()
            self.play_btn.text = "⏸"

    def stop_app(self, instance):
        """Выход"""
        if self.sound:
            self.sound.stop()
        App.get_running_app().stop()

class MusicPlayerApp(App):
    def build(self):
        return MusicPlayer()

if __name__ == '__main__':
    MusicPlayerApp().run()
