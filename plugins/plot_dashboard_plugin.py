# plugins/plot_dashboard_plugin.py
from plot_dashboard import plot_sysbench_dashboard
from plugins.plugin_manager import Plugin

class PlotDashboardPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None
    
    def run(self):
        print("Plotting the sysbench dashboard...")
        plot_sysbench_dashboard()
