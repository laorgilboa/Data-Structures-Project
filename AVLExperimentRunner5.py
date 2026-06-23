import time
import pandas as pd
from collections import deque
from AVLTree import AVLTree

class AVLExperimentRunner5:
    def __init__(self):
        self.results = []

    def _build_perfect_tree_bfs(self, tree, n):
        # Use a queue to insert nodes level by level (Breadth-First Search)
        # This guarantees 0 rotations during construction and a perfect Balance Factor of 0 everywhere.
        queue = deque([(1, n)])
        
        while queue:
            start, end = queue.popleft()
            if start <= end:
                mid = (start + end) // 2
                tree.insert(mid, str(mid))
                
                # Append left and right subtrees to the queue to be processed later
                queue.append((start, mid - 1))
                queue.append((mid + 1, end))

    def run_perfect_tree_experiment(self):
        # Number of insert/delete repetitions 
        k = 10000 
        
        # We use heights 9 through 18 to generate perfect trees 
        # with sizes roughly matching the 300*2^i requirement (511 to 262,143)
        for h in range(9, 19):
            n = (2 ** h) - 1
            tree = AVLTree(True)
            
            # Phase 1: Build the perfect tree efficiently level-by-level
            self._build_perfect_tree_bfs(tree, n)
            
            # The key to insert: the new maximum key (causes worst-case updates)
            target_key = n + 1
            
            total_rotations = 0
            total_height_updates = 0
            total_search_time = 0
            
            start_time = time.perf_counter()
            
            # Phase 2: Operations sequence - insert and delete the target key k times
            for _ in range(k):
                node, st, rot, hc = tree.insert(target_key, "worst_case")
                
                total_search_time += st
                total_rotations += rot
                total_height_updates += hc
                
                # Deletion exactly restores the perfect tree state
                tree.delete(node)
                
            end_time = time.perf_counter()
            
            total_run_time_ms = (end_time - start_time) * 1000
            total_run_time_ops = total_search_time + total_rotations + total_height_updates
            
            # Calculate AVERAGES per operation (Amortized Cost)
            avg_rotations = total_rotations / k
            avg_height_updates = total_height_updates / k
            avg_run_time_ops = total_run_time_ops / k
            avg_run_time_ms = total_run_time_ms / k
            
            self.results.append({
                "Tree Size": n,
                "Tree Height": tree.get_height(),
                "Average Rotations": avg_rotations,
                "Average Height Updates": avg_height_updates,
                "Average Run Time (in ops)": avg_run_time_ops,
                "Average Run Time (in ms)": avg_run_time_ms
            })
            
            print(f"Completed experiment for height={h:2} | Tree Size={n}")

    def export_to_excel(self, filename="Experiment5_PerfectTree_Results.xlsx"):
        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False)
        print(f"\nResults successfully exported to {filename}")

if __name__ == '__main__':
    runner = AVLExperimentRunner5()
    runner.run_perfect_tree_experiment()
    runner.export_to_excel()