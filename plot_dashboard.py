# plot_dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_sysbench_dashboard():
    # Load data from CSV files
    df = pd.read_csv('./outputs/sysbench_intermediate.csv')
    latency = pd.read_csv('./outputs/sysbench_latency_stats.csv', index_col=0).squeeze()
    fairness = pd.read_csv('./outputs/sysbench_fairness_stats.csv', index_col=0).squeeze()

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # TPS Over Time
    sns.lineplot(ax=axs[0,0], data=df, x='Time (s)', y='TPS', marker='o')
    axs[0,0].set_title('Transactions Per Second (TPS) Over Time')
    axs[0,0].set_xlabel('Time (seconds)')
    axs[0,0].set_ylabel('TPS')
    axs[0,0].grid(True)

    # QPS Over Time
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='QPS', marker='o', label='Total QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Read QPS', marker='o', label='Read QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Write QPS', marker='o', label='Write QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Other QPS', marker='o', label='Other QPS')
    axs[0,1].set_title('Queries Per Second (QPS) Over Time')
    axs[0,1].set_xlabel('Time (seconds)')
    axs[0,1].set_ylabel('QPS')
    axs[0,1].legend()
    axs[0,1].grid(True)

    # Latency Metrics
    latency.drop('Sum (ms)').plot(kind='bar', ax=axs[1,0], color=['blue', 'green', 'red', 'purple'])
    axs[1,0].set_title('Latency Metrics (ms)')
    axs[1,0].set_ylabel('Latency (ms)')
    axs[1,0].set_xlabel('')
    axs[1,0].grid(axis='y')

    # Thread Fairness Metrics
    fairness.plot(kind='bar', ax=axs[1,1], color=['orange', 'cyan'])
    axs[1,1].set_title('Thread Fairness Metrics')
    axs[1,1].set_ylabel('Value')
    axs[1,1].set_xlabel('')
    axs[1,1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/sysbench_dashboard.png')
    #plt.show()

def plot_ab_dashboard():
    # Load data from CSV files
    summary_stats = pd.read_csv('./outputs/ab_summary_stats.csv')
    connection_times = pd.read_csv('./outputs/ab_connection_times.csv')
    percentiles = pd.read_csv('./outputs/ab_percentiles.csv')

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Connection Times
    connection_times.plot(kind='bar', ax=axs[0], color=['blue', 'green', 'red', 'purple'])
    axs[0].set_title('Connection Times (ms)')
    axs[0].set_ylabel('Time (ms)')
    axs[0].set_xlabel('Category')
    axs[0].grid(axis='y')

    # Percentiles
    percentiles.plot(kind='bar', x='Percentile', y='Time (ms)', ax=axs[1], color='orange')
    axs[1].set_title('Latency Percentiles')
    axs[1].set_ylabel('Time (ms)')
    axs[1].set_xlabel('Percentile')
    axs[1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/ab_dashboard.png')
    #plt.show()
