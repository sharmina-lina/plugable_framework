# plugins/plugin_manager.py
import importlib
import os

class Plugin:
    def setup(self):
        pass

    def run(self):
        pass

    def teardown(self):
        pass

class PluginManager:
    def __init__(self, config=None):
        self.config = config
        self.plugins = []

    def load_plugins(self):
        print("Loading plugins...")
        plugin_folder = "plugins"
        for file in os.listdir(plugin_folder):
            if file.endswith("_plugin.py"):
                plugin_name = file[:-3]  # Strip off .py
                
                # Adjust to match plugin class naming
                class_name = ''.join(word.capitalize() for word in plugin_name.split('_'))  # Convert to camel case
                
                module = importlib.import_module(f"{plugin_folder}.{plugin_name}")
                
                # Dynamically load class
                plugin_class = getattr(module, class_name)
                
                # Pass the config to the plugin instance
                self.plugins.append(plugin_class(self.config))  # Pass config here

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.setup()
            result = plugin.run()
            if result is False:
                print("Error occurred during plugin execution. Exiting...")
                break
            plugin.teardown()
