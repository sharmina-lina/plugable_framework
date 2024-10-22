# parse_sysbench.py
import re
import pandas as pd

def parse_sysbench_output(file_path):
    intermediate_results = []
    final_stats = {}
    latency_stats = {}
    fairness_stats = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regex pattern with minor tweaks
    intermediate_pattern = re.compile(
        r'\[\s*(\d+)s\s*\]\s+thds:\s*(\d+)\s+tps:\s*([\d.]+)\s+qps:\s*([\d.]+)\s+\(r/w/o:\s*([\d.]+)/([\d.]+)/([\d.]+)\)\s+lat\s*\(ms,99%\):\s*([\d.]+)\s+err/s:\s*([\d.]+)\s+reconn/s:\s*([\d.]+)'
    )

    sql_stats_section = False
    latency_section = False
    fairness_section = False

    for line in lines:
        line = line.strip()

        # Debugging: print line being processed
        #print(f"Processing line: {line}")

        # Parse intermediate results
        match = intermediate_pattern.match(line)
        if match:
            time_sec = int(match.group(1))
            threads = int(match.group(2))
            tps = float(match.group(3))
            qps = float(match.group(4))
            read_qps = float(match.group(5))
            write_qps = float(match.group(6))
            other_qps = float(match.group(7))
            lat_99 = float(match.group(8))
            err_s = float(match.group(9))
            reconn_s = float(match.group(10))

            intermediate_results.append({
                'Time (s)': time_sec,
                'Threads': threads,
                'TPS': tps,
                'QPS': qps,
                'Read QPS': read_qps,
                'Write QPS': write_qps,
                'Other QPS': other_qps,
                'Latency 99% (ms)': lat_99,
                'Errors/s': err_s,
                'Reconnects/s': reconn_s
            })

        # Detect sections
        if line.startswith("SQL statistics:"):
            sql_stats_section = True
            continue
        if sql_stats_section:
            if line.startswith("queries performed:"):
                continue
            elif line.startswith("transactions:"):
                parts = line.split()
                final_stats['Transactions'] = int(parts[1])
                final_stats['Transactions/sec'] = float(parts[3].strip('()')) if parts[3] != 'per' else float(parts[2].strip('()'))
            elif line.startswith("queries:"):
                parts = line.split()
                final_stats['Total Queries'] = int(parts[1])
                final_stats['Queries/sec'] = float(parts[3].strip('()')) if parts[3] != 'per' else float(parts[2].strip('()'))
            elif line.startswith("ignored errors:"):
                parts = line.split()
                try:
                    final_stats['Ignored Errors'] = int(parts[2])
                    final_stats['Ignored Errors/sec'] = float(parts[4].strip('()'))
                except (IndexError, ValueError):
                    print(f"Warning: Unable to parse ignored errors line: {line}")
            elif line.startswith("reconnects:"):
                parts = line.split()
                try:
                    final_stats['Ignored Errors'] = int(parts[2])
                    final_stats['Ignored Errors/sec'] = float(parts[4].strip('()'))
                except (IndexError, ValueError):
                    print(f"Warning: Unable to parse ignored errors line: {line}")
            elif line == '':
                sql_stats_section = False

        if line.startswith("Latency (ms):"):
            latency_section = True
            continue
        if latency_section:
            if line.startswith("min:"):
                latency_stats['Min (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("avg:"):
                latency_stats['Avg (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("max:"):
                latency_stats['Max (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("99th percentile:"):
                latency_stats['99th Percentile (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("sum:"):
                latency_stats['Sum (ms)'] = float(line.split(':')[1].strip())
            elif line == '':
                latency_section = False

        if line.startswith("Threads fairness:"):
            fairness_section = True
            continue
        if fairness_section:
            if line.startswith("events (avg/stddev):"):
                parts = line.split(':')[1].strip().split('/')
                fairness_stats['Events Avg'] = float(parts[0])
                fairness_stats['Events StdDev'] = float(parts[1])
            elif line.startswith("execution time (avg/stddev):"):
                parts = line.split(':')[1].strip().split('/')
                fairness_stats['Execution Time Avg'] = float(parts[0])
                fairness_stats['Execution Time StdDev'] = float(parts[1])
            elif line == '':
                fairness_section = False

    # Convert intermediate results to DataFrame
    df_intermediate = pd.DataFrame(intermediate_results)

    return df_intermediate, final_stats, latency_stats, fairness_stats



