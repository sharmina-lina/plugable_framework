# plugins/plot_dashboard_plugin.py
from functions.plot_dashboard import plot_sysbench_dashboard, plot_ab_dashboard, plot_redis_dashboard, plot_k6_dashboard
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
        print("Plotting the Redis of application dashboard...")
        plot_redis_dashboard()
        print("Plotting the k6 load test dashboard...")
        plot_k6_dashboard()


        
        # Display all three images using matplotlib's imshow in a single figure
        fig, axs = plt.subplots(2, 2, figsize=(20, 15))  # Adjusted for three images

        # Load and display the saved images
        sysbench_img = plt.imread('./outputs/sysbench_dashboard.png')
        ab_img = plt.imread('./outputs/ab_dashboard.png')
        redis_img = plt.imread('./outputs/redis_dashboard.png')
        k6_img = plt.imread('./outputs/k6_dashboard.png')

        axs[0, 0].imshow(sysbench_img)
        axs[0, 0].axis('off')  # Hide axes for better visualization
        axs[0, 0].set_title('Dashboard of Database Performance')

        axs[0, 1].imshow(k6_img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Dashboard of Application load test')

        axs[1, 0].imshow(ab_img)
        axs[1, 0].axis('off')  # Hide axes for better visualization
        axs[1, 0].set_title('Dashboard of Load Balancer Performance')

        axs[1, 1].imshow(redis_img)
        axs[1, 1].axis('off')  # Hide axes for better visualization
        axs[1, 1].set_title('Dashboard of Redis Performance')

        plt.tight_layout()
        plt.show()