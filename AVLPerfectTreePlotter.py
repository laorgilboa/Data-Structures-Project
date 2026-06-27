import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

class AVLPerfectTreePlotter:
    """
    A class to read AVL perfect tree experiment results and plot the data
    alongside a theoretical log(n) curve to demonstrate their similarity.
    """
    def __init__(self, file_path: str = 'Experiment5_PerfectTree_Results.xlsx', output_image: str = 'amortized_cost_vs_logn.png'):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.script_dir, file_path)
        self.output_image = os.path.join(self.script_dir, output_image)

    def plot(self):
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' was not found.")
            return

        try:
            # Read the Excel file using the first row as headers
            df = pd.read_excel(self.file_path, header=0)
            
            if df.empty:
                print("Error: The Excel file is empty.")
                return

            # Extract data using exact column names matching the generated Excel file
            x_data = pd.to_numeric(df['Tree Size'], errors='coerce').dropna()
            
            # Using 'Average Run Time (in ops)' and 'Average Height Updates' for the Y-axes
            y_data_ops = pd.to_numeric(df['Average Run Time (in ops)'], errors='coerce').dropna()
            y_data_height = pd.to_numeric(df['Average Height Updates'], errors='coerce').dropna()

            plt.figure(figsize=(10, 6))

            # Plot 1: Empirical Average Run Time (Operations)
            plt.plot(x_data, y_data_ops, marker='o', linestyle='-', color='blue', 
                     label='Empirical: Average Run Time (ops)')
            
            # Plot 2: Empirical Average Height Updates
            plt.plot(x_data, y_data_height, marker='s', linestyle='--', color='orange', 
                     label='Empirical: Average Height Updates')

            # Create the theoretical log2(n) curve
            # We scale it so it visually aligns with the empirical data (using operations data)
            max_x = x_data.iloc[-1]
            max_y = y_data_ops.iloc[-1]
            scale_factor = 2
            #max_y / np.log2(max_x)
            
            # Generate smooth x values for the theoretical curve
            x_smooth = np.linspace(min(x_data), max(x_data), 500)
            y_theoretical = scale_factor * np.log2(x_smooth)

            # Plot 3: Theoretical Scaled log(n)
            plt.plot(x_smooth, y_theoretical, linestyle=':', color='red', linewidth=2.5, 
                     label='Theoretical: 2 * log₂(n)')

            # Formatting
            plt.title('Amortized Cost of Insertion vs. Tree Size', fontsize=14)
            plt.xlabel('Tree Size (n)', fontsize=12)
            plt.ylabel('Operations / Updates', fontsize=12)
            
            # Use linear scale to clearly see the logarithmic curve shape
            plt.xscale('linear')
            plt.yscale('linear')
            
            # Force X-axis to start at 0 so the first data point isn't glued to the Y-axis
            plt.xlim(left=0)
            
            plt.grid(True, which="both", ls="--", alpha=0.5)

            # Format X axis with standard commas (e.g., 250,000 instead of scientific notation)
            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            plt.legend(fontsize=11)
            plt.tight_layout()

            # Save and show
            plt.savefig(self.output_image)
            print(f"\nSuccess! Graph saved as '{self.output_image}'.")
            plt.show()

        except Exception as e:
            print(f"An error occurred: {e}")

# ==========================================
# Entry Point
# ==========================================
if __name__ == "__main__":
    plotter = AVLPerfectTreePlotter()
    plotter.plot()