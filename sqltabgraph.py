import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def plot_buffers(sqlite_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    
    query = """
    SELECT buffers.operation_id, buffers.address, buffers.max_size_per_bank, operations.name
    FROM buffers
    JOIN operations ON buffers.operation_id = operations.operation_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    grouped_by_name = df.groupby('name')

    root = tk.Tk()
    root.title("L1 Utilization Visualizer")

    tab_control = ttk.Notebook(root)

    for name, group in grouped_by_name:
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=name)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        grouped_by_id = group.groupby('operation_id')
        
        for operation_id, sub_group in grouped_by_id:
            addresses = sub_group['address']
            sizes = sub_group['max_size_per_bank']
            ax.errorbar([operation_id] * len(addresses), addresses, yerr=sizes, fmt='o', alpha=0.7)
        
        ax.set_ylabel('Address + Size')
        ax.set_title(f'L1 Utilization for {name}')
        ax.grid(True, axis='y')
        
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Plot buffers from SQLite file.')
    parser.add_argument('sqlite_file', type=str, help='Path to the SQLite file')
    args = parser.parse_args()
    
    plot_buffers(args.sqlite_file)
