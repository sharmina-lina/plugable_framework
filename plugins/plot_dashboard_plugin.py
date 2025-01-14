# plugins/plot_dashboard_plugin.py
from plot_dashboard import plot_sysbench_dashboard, plot_ab_dashboard
from plugins.plugin_manager import Plugin
import matplotlib.pyplot as plt

class PlotDashboardPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None
    
    def run(self):
        print("Plotting the sysbench dashboard...")
        plot_sysbench_dashboard()
        print("Plotting the apache benchmark(ab) dashboard...")
        plot_ab_dashboard()

        # Display both images using matplotlib's imshow in a single figure
        fig, axs = plt.subplots(1, 2, figsize=(20, 10))

        # Load and display the saved images
        sysbench_img = plt.imread('./outputs/sysbench_dashboard.png')
        ab_img = plt.imread('./outputs/ab_dashboard.png')

        axs[0].imshow(sysbench_img)
        axs[0].axis('off')  # Hide axes for better visualization
        axs[0].set_title('Dashboard of Database performance')

        axs[1].imshow(ab_img)
        axs[1].axis('off')  # Hide axes for better visualization
        axs[1].set_title('Dashboard of Load Balancer performance')

        plt.tight_layout()
        plt.show()
