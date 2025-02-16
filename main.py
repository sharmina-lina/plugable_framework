
# main.py
from plugins.plugin_manager import PluginManager
from config_loader import load_encrypted_config
def main():
    # Step 1: Load the encrypted config.yaml file using Ansible Vault
    config = load_encrypted_config(vault_file="config.yaml", vault_password_file="/Users/sharminalina/desktop/oslomet/thesis/vault_pass.txt")
    
    if not config:
        print("Error loading config. Exiting.")
        return
    
    # Step 2: Define the plugin execution sequence
    plugin_sequence = [
       
        "db_test_plugin",
        #"ycsb_plugin",
        "loadbalancer_test_plugin",
        "application_testing_plugin",
        "application_load_testing_plugin",
        "plot_dashboard_plugin"
        
    ]

    # Step 3: Initialize the PluginManager with the loaded configuration and sequence
    plugin_manager = PluginManager(config=config, plugin_sequence=plugin_sequence)

    #Step 4: Load and run all plugins

    plugin_manager.load_plugins()  # Load all plugins in the "plugins" folder
    plugin_manager.run_plugins()   # Execute the setup, run, and teardown for each plugin

if __name__ == "__main__":
    main()

