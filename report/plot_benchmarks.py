import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Add Source directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Source'))
from main import compare_all_algorithms

def main():
    print("Running benchmarks to generate charts...")
    timeout_limit = 30
    results = compare_all_algorithms('../Source/Inputs', '../Source/Outputs', timeout_seconds=timeout_limit)
    
    if not results:
        print("No results found.")
        return
        
    # Group data by algorithm
    test_cases = sorted(list(set([r['input_file'][-12:] for r in results]))) # input-01.txt, etc.
    algo_names = list(set([r['algorithm'].split(' (')[0] for r in results]))
    
    algorithms = {algo: {'time': [0.0]*len(test_cases), 'nodes': [0]*len(test_cases), 'timeout': [False]*len(test_cases)} for algo in algo_names}
    tc_to_idx = {tc: i for i, tc in enumerate(test_cases)}
    
    for r in results:
        algo = r['algorithm'].split(' (')[0]
        idx = tc_to_idx[r['input_file'][-12:]]
        
        algorithms[algo]['time'][idx] = r.get('time', 0.0)
        
        nodes = r.get('nodes_expanded', 0)
        try:
            nodes_val = int(float(nodes))
        except (ValueError, TypeError):
            nodes_val = 1
        algorithms[algo]['nodes'][idx] = nodes_val
        algorithms[algo]['timeout'][idx] = r.get('is_timeout', False)

    x = np.arange(len(test_cases))
    width = 0.8 / len(algorithms) if algorithms else 0.2
    
    # 1. Plot Execution Time
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (algo, data) in enumerate(algorithms.items()):
        offset = (i - len(algorithms)/2 + 0.5) * width
        plot_time = [max(1e-4, t) for t in data['time']]
        bars = ax.bar(x + offset, plot_time, width, label=algo)
        
        # Add timeout indicator
        for j, is_to in enumerate(data['timeout']):
            if is_to:
                ax.text(x[j] + offset, plot_time[j] * 1.2, 'T.O.', ha='center', va='bottom', fontsize=8, color='red', rotation=90)
                
    ax.set_yscale('log')
    
    # Get current ymax and increase it by a factor of 10 to leave space for T.O. tags
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(bottom=1e-4, top=ymax * 10)
    
    ax.set_ylabel('Execution Time (seconds) - Log Scale')
    ax.set_title(f'Algorithm Comparison: Execution Time (Timeout: {timeout_limit}s)')
    ax.set_xticks(x)
    ax.set_xticklabels(test_cases, rotation=45)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Add a line for timeout limit
    ax.axhline(y=timeout_limit, color='r', linestyle='--', alpha=0.5, label='Timeout Limit')
    
    plt.tight_layout()
    plt.savefig('time_benchmark.png')
    print("Saved time_benchmark.png")
    
    # 2. Plot Nodes Expanded
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (algo, data) in enumerate(algorithms.items()):
        offset = (i - len(algorithms)/2 + 0.5) * width
        plot_nodes = [max(1, n) for n in data['nodes']]
        bars = ax.bar(x + offset, plot_nodes, width, label=algo)
        
        for j, is_to in enumerate(data['timeout']):
            if is_to:
                ax.text(x[j] + offset, plot_nodes[j] * 1.2, 'T.O.', ha='center', va='bottom', fontsize=8, color='red', rotation=90)

    ax.set_yscale('log')
    
    # Get current ymax and increase it by a factor of 10 to leave space for T.O. tags
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(bottom=1, top=ymax * 10)
    
    ax.set_ylabel('Nodes Expanded / Inferences - Log Scale')
    ax.set_title('Algorithm Comparison: Nodes Expanded')
    ax.set_xticks(x)
    ax.set_xticklabels(test_cases, rotation=45)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('nodes_benchmark.png')
    print("Saved nodes_benchmark.png")

if __name__ == "__main__":
    main()
