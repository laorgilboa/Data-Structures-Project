import time
import random
import sys
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from AVLTree import AVLTree

# CRITICAL: Regular BSTs can become highly unbalanced. 
# We increase the recursion limit to safely handle trees up to size ~350,000.
sys.setrecursionlimit(500000)

class AVLExperimentRunner:
    """A class to execute insertion experiments on AVL and regular BSTs and export the results."""
    
    def __init__(self, max_i=10, iterations=20, output_file='avl_experiments_results.xlsx'):
        self.max_i = max_i
        self.iterations = iterations
        self.output_file = output_file
        
        # Calculate n = 300 * 2^i
        self.n_values = [300 * (2 ** i) for i in range(1, self.max_i + 1)]
        
        # Dictionary to hold the extracted data
        self.results = {
            "Exp 1 - BST Ascending": [],
            "Exp 2 - AVL Ascending": [],
            "Exp 3 - AVL Random": [],
            "Exp 4 - BST Random": []
        }

    def _run_single_test(self, n, sequence, is_avl):
        """Runs a single insertion experiment and returns the raw metrics."""
        tree = AVLTree(is_avl)
        
        total_search_time = 0
        total_rotations = 0
        total_height_changes = 0
        
        start_time = time.time()
        
        for key in sequence:
            _, st, rot, hc = tree.insert(key, str(key))
            total_search_time += st
            total_rotations += rot
            total_height_changes += hc
            
        end_time = time.time()
        
        return {
            "Tree Size (n)": tree.size(),
            "Tree Height": tree.get_height(),
            "Rotations": total_rotations,
            "Height Changes": total_height_changes,
            "Run Time (Operations)": total_search_time + total_rotations + total_height_changes,
            "Run Time (ms)": (end_time - start_time) * 1000
        }

    def _run_random_test_averaged(self, n, is_avl):
        """Runs a randomized experiment multiple times and averages the results."""
        avg_results = {
            "Tree Size (n)": n, "Tree Height": 0, "Rotations": 0, 
            "Height Changes": 0, "Run Time (Operations)": 0, "Run Time (ms)": 0
        }
        
        for _ in range(self.iterations):
            seq = list(range(1, n + 1))
            random.shuffle(seq)
            
            res = self._run_single_test(n, seq, is_avl)
            
            avg_results["Tree Height"] += res["Tree Height"]
            avg_results["Rotations"] += res["Rotations"]
            avg_results["Height Changes"] += res["Height Changes"]
            avg_results["Run Time (Operations)"] += res["Run Time (Operations)"]
            avg_results["Run Time (ms)"] += res["Run Time (ms)"]
            
        # Calculate the average for each metric
        for key in ["Tree Height", "Rotations", "Height Changes", "Run Time (Operations)", "Run Time (ms)"]:
            avg_results[key] /= self.iterations
            
        return avg_results

    def run_all_experiments(self):
        """Executes all 4 experiments for all values of n."""
        print(f"Running Experiments up to n = {self.n_values[-1]}...")
        print(f"Randomized tests will be averaged over {self.iterations} iterations.")
        
        for n in self.n_values:
            print(f"Processing n = {n}...")
            
            # Exp 1 & 2: Deterministic
            self.results["Exp 1 - BST Ascending"].append(self._run_single_test(n, range(1, n + 1), is_avl=False))
            self.results["Exp 2 - AVL Ascending"].append(self._run_single_test(n, range(1, n + 1), is_avl=True))
            
            # Exp 3 & 4: Randomized
            self.results["Exp 3 - AVL Random"].append(self._run_random_test_averaged(n, is_avl=True))
            self.results["Exp 4 - BST Random"].append(self._run_random_test_averaged(n, is_avl=False))
            
        print("Experiments complete.")

    def export_to_excel(self):
        """Exports the stored results to an Excel workbook without extra formatting."""
        print(f"Writing results to {self.output_file}...")
        
        with pd.ExcelWriter(self.output_file) as writer:
            for sheet_name, data in self.results.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
        print("Done! Check your folder for the Excel file.")

# --- Execution Block ---
if __name__ == '__main__':
    # You can easily change max_i=10 or iterations=20 for testing
    runner = AVLExperimentRunner(max_i=10, iterations=20, output_file='avl_experiments_results.xlsx')
    runner.run_all_experiments()
    runner.export_to_excel()