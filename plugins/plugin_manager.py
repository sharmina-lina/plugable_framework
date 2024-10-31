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
    def __init__(self, config=None, plugin_sequence=None):
        self.config = config
        self.plugins = []
        self.plugin_sequence = plugin_sequence or []

    def load_plugins(self):
        print("Loading plugins in specified order...")
        plugin_folder = "plugins"
        
        for plugin_name in self.plugin_sequence:
            plugin_file = f"{plugin_name}.py"
            
            if plugin_file in os.listdir(plugin_folder):
                print(f"Loading plugin: {plugin_name}")
                
                # Convert plugin name to class name (e.g., "db_connect_plugin" -> "DbConnectPlugin")
                class_name = ''.join(word.capitalize() for word in plugin_name.split('_'))
                
                # Dynamically import the module and class
                module = importlib.import_module(f"{plugin_folder}.{plugin_name}")
                plugin_class = getattr(module, class_name)
                
                # Instantiate and configure the plugin
                self.plugins.append(plugin_class(self.config))

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.setup()
            result = plugin.run()
            if result is False:
                print("Error occurred during plugin execution. Exiting...")
                break
            plugin.teardown()
