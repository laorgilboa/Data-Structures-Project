import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

class AVLExperimentPlotter:
    """
    A class to read AVL tree experiment results and plot the data.
    Generates two graphs: a Macro view (all data) and a Zoomed view (for fast algorithms).
    """
    def __init__(self, file_path: str = 'avl_experiments_results.xlsx'):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.script_dir, file_path)
        
        # Define the names for the two output images
        self.output_image_full = 'runtime_graph_full_scale.png'
        self.output_image_zoomed = 'runtime_graph_zoomed_scale.png'

    def extract_pure_numbers(self, raw_data):
        """Extracts only pure numbers and ignores text/junk."""
        s = pd.Series(raw_data).astype(str)
        s = s.str.replace(',', '', regex=False)
        s = s.str.extract(r'([-+]?\d*\.?\d+)', expand=False)
        return pd.to_numeric(s, errors='coerce')

    def draw_graph(self, data_dict, title, max_x, max_y, filename, figure_number):
        """Helper method to draw and save a specific graph based on parameters."""
        plt.figure(figure_number, figsize=(10, 6))
        
        # Draw the lines
        for sheet_name, df in data_dict.items():
            plt.plot(df['x'], df['y'], marker='o', label=sheet_name)
            
        # Formatting
        plt.title(title)
        plt.xlabel('Tree Size (n)')
        plt.ylabel('Run Time (ms)')
        
        # Only draw legend if we have lines
        if plt.gca().get_legend_handles_labels():
            plt.legend()
            
        plt.grid(True)
        
        # Apply strict scales
        plt.xlim(0, max_x)
        plt.ylim(0, max_y)

        # Clean axis numbers with commas
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        plt.tight_layout()

        # Save the graph
        save_path = os.path.join(self.script_dir, filename)
        plt.savefig(save_path)
        print(f"Success! Saved: '{filename}'")

    def plot(self):
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' was not found.")
            return

        excel_file = pd.ExcelFile(self.file_path)
        
        # Dictionary to store all the cleaned data so we only read the file once
        processed_data = {}

        print("--- Extracting Data ---")
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)
                num_cols = len(df.columns)
                
                if df.empty or num_cols == 0:
                    continue

                # X is Column A (0), Y is Column F (5) or the last column
                x_data_raw = df.iloc[:, 0]
                y_data_raw = df.iloc[:, 5] if num_cols >= 6 else df.iloc[:, -1]
                
                # Extract clean numbers
                x_data_numeric = self.extract_pure_numbers(x_data_raw)
                y_data_numeric = self.extract_pure_numbers(y_data_raw)
                
                # Clean and sort
                clean_df = pd.DataFrame({'x': x_data_numeric, 'y': y_data_numeric}).dropna().sort_values(by='x')
                
                if clean_df.empty:
                    continue
                
                # Save to our dictionary
                processed_data[sheet_name] = clean_df
                print(f"Loaded '{sheet_name}' ({len(clean_df)} points)")

            except Exception as e:
                print(f"Error processing '{sheet_name}': {e}")

        if not processed_data:
            print("No valid data found to plot. Exiting.")
            return

        print("\n--- Generating Graphs ---")
        
        # ==========================================
        # GRAPH 1: The Macro Scale
        # X: 0 - 310,000 | Y: 0 - 2,000,000
        # ==========================================
        self.draw_graph(
            data_dict=processed_data,
            title='Run Time vs. Tree Size (Full Scale)',
            max_x=310000,
            max_y=2000000,
            filename=self.output_image_full,
            figure_number=1
        )

        # ==========================================
        # GRAPH 2: The Zoomed Scale
        # X: 0 - 310,000 | Y: 0 - 1,200
        # ==========================================
        self.draw_graph(
            data_dict=processed_data,
            title='Run Time vs. Tree Size (Zoomed for AVL/Fast Operations)',
            max_x=310000,
            max_y=1200,
            filename=self.output_image_zoomed,
            figure_number=2
        )

        # Show both graphs on screen simultaneously
        plt.show()

# ==========================================
# Entry Point
# ==========================================
if __name__ == "__main__":
    plotter = AVLExperimentPlotter(file_path='avl_experiments_results.xlsx')
    plotter.plot()