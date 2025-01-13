# plugins/parse_ab_plugin.py
from parse_ab import parse_ab_output
from pandas import Series, DataFrame
from plugins.plugin_manager import Plugin

class ParseAbPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def run(self):
        print("Parsing ab output...")

        # Parse the ab_metrics.txt file
        summary_stats, connection_times_df, percentiles_df = parse_ab_output('./outputs/ab_metrics.txt')

        if summary_stats:
            print("Summary_state data to CSV...")

            # Save summary statistics to a CSV file
            DataFrame([summary_stats]).to_csv("./outputs/ab_summary_stats.csv", index=False)
        else:
            print("Summary_state data is empty. Check the input file or parsing logic.")

            # Save connection times and latency percentiles
        if not connection_times_df.empty:
            print("Connection time is saving ...")
            connection_times_df.to_csv('./outputs/ab_connection_times.csv', index=False)
        else:
            print("Connection_time data is empty. Check the input file or parsing logic.")
        if not percentiles_df.empty:
            print("Percentiles is saving...")
            percentiles_df.to_csv('./outputs/ab_percentiles.csv', index=False)
            

        else:
            print("Percentile data is empty. Check the input file or parsing logic.")
