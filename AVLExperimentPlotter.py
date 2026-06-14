import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

class AVLExperimentPlotter:
    """
    A class to read AVL tree experiment results and plot the data.
    Uses a Logarithmic Y-axis to compare extremely fast and extremely slow algorithms side-by-side.
    """
    def __init__(self, file_path: str = 'avl_experiments_results.xlsx', output_image: str = 'runtime_graph_logarithmic.png'):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.script_dir, file_path)
        self.output_image = os.path.join(self.script_dir, output_image)

    def extract_pure_numbers(self, raw_data):
        """Extracts pure numbers and drops text."""
        s = pd.Series(raw_data).astype(str)
        s = s.str.replace(',', '', regex=False)
        s = s.str.extract(r'([-+]?\d*\.?\d+)', expand=False)
        return pd.to_numeric(s, errors='coerce')

    def plot(self):
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' was not found.")
            return

        excel_file = pd.ExcelFile(self.file_path)
        plt.figure(figsize=(10, 6))

        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)
                num_cols = len(df.columns)
                
                if df.empty or num_cols == 0:
                    continue

                # X is Column A (0), Y is Column F (5) or the last column
                x_data_raw = df.iloc[:, 0]
                y_data_raw = df.iloc[:, 5] if num_cols >= 6 else df.iloc[:, -1]
                
                x_data_numeric = self.extract_pure_numbers(x_data_raw)
                y_data_numeric = self.extract_pure_numbers(y_data_raw)
                
                clean_df = pd.DataFrame({'x': x_data_numeric, 'y': y_data_numeric}).dropna().sort_values(by='x')
                
                # ==========================================
                # LOG SCALE SAFETY: You cannot calculate log(0).
                # If any operation was so fast it recorded as 0, 
                # we change it to 0.001 ms so the point can still be drawn.
                # ==========================================
                clean_df.loc[clean_df['y'] <= 0, 'y'] = 0.001
                
                if clean_df.empty:
                    continue
                
                plt.plot(clean_df['x'], clean_df['y'], marker='o', label=sheet_name)
                print(f"Loaded '{sheet_name}' ({len(clean_df)} points)")

            except Exception as e:
                print(f"Error processing '{sheet_name}': {e}")

        # Formatting
        plt.title('Run Time vs. Tree Size (Logarithmic Scale)')
        plt.xlabel('Tree Size (n)')
        plt.ylabel('Run Time (ms) - Log Scale')
        
        if plt.gca().get_legend_handles_labels():
            plt.legend()
        
        # ==========================================
        # LOG SCALE SETTINGS
        # ==========================================
        plt.yscale('log')
        plt.xlim(0, 310000)
        
        # Better grid formatting for log scales (shows minor and major lines)
        plt.grid(True, which="both", ls="--", alpha=0.5)

        # Force the axis labels to use clean commas instead of scientific notation
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        # For Y axis on log scale, this ensures we see "1,000" instead of "10^3"
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{y:g}"))

        plt.tight_layout()

        # Save and show
        plt.savefig(self.output_image)
        print(f"\nSuccess! Graph saved as '{self.output_image}'.")
        plt.show()

# ==========================================
# Entry Point
# ==========================================
if __name__ == "__main__":
    plotter = AVLExperimentPlotter(file_path='avl_experiments_results.xlsx')
    plotter.plot()