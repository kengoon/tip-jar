from kivy.properties import DictProperty
from kivy.uix.screenmanager import ScreenManager
from importlib import import_module
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class AppScreenManager(ScreenManager):
    """
    A custom ScreenManager that loads screens lazily.
    """
    screen_config = DictProperty(
        {
            "home screen": {
                "presentation": ("features.home.presentation", "HomeScreen")
            }
        }
    )

    def on_current(self, instance, value):
        """
        Loads a screen dynamically if it hasn't been loaded yet.
        """
        if not self.has_screen(value):
            screen_data = self.screen_config[value]
            presentation_module_path, presentation_class_name = screen_data["presentation"]
            presentation_module = import_module(presentation_module_path)
            presentation_class = getattr(presentation_module, presentation_class_name)
            presentation = presentation_class()
            self.add_widget(presentation)
        supra = super().on_current(instance, value)
        if len(self.children) > 1:
            self.remove_widget(self.children[1])
        return supra

