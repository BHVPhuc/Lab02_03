import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Add Source directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Source'))
from main import compare_all_algorithms

def main():
    print("Running benchmarks to generate charts...")
    results = compare_all_algorithms('../Source/Inputs', '../Source/Outputs')
    
    if not results:
        print("No results found.")
        return
        
    # Group data by algorithm
    test_cases = sorted(list(set([r['input_file'][-12:] for r in results]))) # input-01.txt, etc.
    algo_names = list(set([r['algorithm'].split(' (')[0] for r in results]))
    
    algorithms = {algo: {'time': [0.0]*len(test_cases), 'nodes': [0]*len(test_cases)} for algo in algo_names}
    tc_to_idx = {tc: i for i, tc in enumerate(test_cases)}
    
    for r in results:
        algo = r['algorithm'].split(' (')[0]
        idx = tc_to_idx[r['input_file'][-12:]]
        algorithms[algo]['time'][idx] = r['time']
        algorithms[algo]['nodes'][idx] = r['nodes_expanded']

    x = np.arange(len(test_cases))
    width = 0.8 / len(algorithms) if algorithms else 0.2
    
    # 1. Plot Execution Time
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (algo, data) in enumerate(algorithms.items()):
        offset = (i - len(algorithms)/2 + 0.5) * width
        ax.bar(x + offset, data['time'], width, label=algo)
        
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Algorithm Comparison: Execution Time')
    ax.set_xticks(x)
    ax.set_xticklabels(test_cases, rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.savefig('time_benchmark.png')
    print("Saved time_benchmark.png")
    
    # 2. Plot Nodes Expanded
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (algo, data) in enumerate(algorithms.items()):
        offset = (i - len(algorithms)/2 + 0.5) * width
        ax.bar(x + offset, data['nodes'], width, label=algo)
        
    ax.set_ylabel('Nodes Expanded / Inferences')
    ax.set_title('Algorithm Comparison: Nodes Expanded')
    ax.set_xticks(x)
    ax.set_xticklabels(test_cases, rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.savefig('nodes_benchmark.png')
    print("Saved nodes_benchmark.png")

if __name__ == "__main__":
    main()
