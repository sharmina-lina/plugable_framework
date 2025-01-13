# plugins/parse_sysbench_plugin.py
from parse_sysbench import parse_sysbench_output
from pandas import Series
from plugins.plugin_manager import Plugin

class ParseSysbenchPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def run(self):
        print("Parsing sysbench output...")
        df_intermediate, final_stats, latency_stats, fairness_stats = parse_sysbench_output('./outputs/sysbench_metrics.txt')
        
        if not df_intermediate.empty:
            print("Saving parsed data to CSV...")
            df_intermediate.to_csv("./outputs/sysbench_intermediate.csv", index=False)
            Series(final_stats).to_csv('./outputs/sysbench_sql_stats.csv')
            Series(latency_stats).to_csv('./outputs/sysbench_latency_stats.csv')
            Series(fairness_stats).to_csv('./outputs/sysbench_fairness_stats.csv')
        else:
            print("Parsed data is empty. Check the input file or parsing logic.")
