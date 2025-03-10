"""
dodo.py - PyDoit task file for CIP Analysis

This file automates tasks such as:
  - Creating required directories,
  - Downloading CIP data from GitHub,
  - Running CIP analysis (via cip_analysis.py),
  - Converting and executing notebooks (e.g. main_cip.ipynb),
  - Generating summary statistics,
  - Compiling documentation.

Ensure that your CIP-related scripts (e.g., pull_bloomberg_cip_data.py, cip_analysis.py)
and notebooks (e.g., main_cip.ipynb) reside in the ./src/ folder.
"""

#######################################
## Configuration and Helpers for PyDoit
#######################################
import sys
import os
import shutil
from pathlib import Path
from doit.reporter import ConsoleReporter
from colorama import Fore, Style

sys.path.insert(1, "./src/")  # Add ./src/ to Python path

# Define paths
DATA_DIR = Path("./data")
MANUAL_DATA_DIR = Path("./data_manual")
OUTPUT_DIR = Path("./_output")
SRC_DIR = Path("./src")

# Custom reporter: print task lines in green
class GreenReporter(ConsoleReporter):
    def write(self, stuff, **kwargs):
        doit_mark = stuff.split(" ")[0].ljust(2)
        task = " ".join(stuff.split(" ")[1:]).strip() + "\n"
        output = (
            Fore.GREEN
            + doit_mark
            + f" {os.path.basename(os.getcwd())}: "
            + task
            + Style.RESET_ALL
        )
        self.outstream.write(output)

#######################################
## Helper Functions for Jupyter Tasks
#######################################
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --inplace ./src/{notebook}.ipynb"

def jupyter_to_html(notebook):
    return f"jupyter nbconvert --to html --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb"

def jupyter_to_latex(notebook):
    return f"jupyter nbconvert --to latex --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb"

def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"

#######################################
## PyDoit Tasks
#######################################

def task_download_cip_data():
    """
    Download CIP_2025.xlsx from GitHub and save it to the data_manual folder.
    """
    target_file = MANUAL_DATA_DIR / "CIP_2025.xlsx"

    def download():
        import requests
        url = "https://raw.githubusercontent.com/Kunj121/CIP/main/data_manual/CIP_2025.xlsx"
        response = requests.get(url)
        response.raise_for_status()  # Ensure a successful request
        os.makedirs(MANUAL_DATA_DIR, exist_ok=True)  # Ensure directory exists
        with open(target_file, "wb") as f:
            f.write(response.content)
        print(f"File saved to {target_file.resolve()}")

    return {
        "actions": [download],
        "targets": [str(target_file)],
        "uptodate": [False],
        "clean": True,
    }

def task_config():
    """Create directories for data and output if they don't exist."""
    def create_dirs():
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(MANUAL_DATA_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    return {
        "actions": [create_dirs],
        "targets": [str(DATA_DIR), str(OUTPUT_DIR), str(MANUAL_DATA_DIR)],
        "clean": True,
    }

def task_pull_cip():
    """
    Run CIP analysis and generate outputs in `_output/`.
    """
    return {
        "actions": ["cd src && ipython cip_analysis.py"],
        "file_dep": [
            "./src/cip_analysis.py",
            "./src/pull_bloomberg_cip_data.py",
            str(MANUAL_DATA_DIR / "CIP_2025.xlsx"),
        ],
        "targets": [
            str(OUTPUT_DIR / "cip_analysis_results.parquet"),
            str(OUTPUT_DIR / "spread_plot.pdf"),
            str(OUTPUT_DIR / "spread_plot.png"),
        ],
        "task_dep": ["download_cip_data"],  # Ensure data is downloaded first
        "clean": True,
    }

def task_run_notebooks():
    """
    Execute Jupyter notebooks, convert them to HTML & LaTeX,
    and copy output to `_output/`.
    """
    notebook = "main_cip"  # ✅ Only the base name, no `.ipynb`

    return {
        "actions": [
            f"jupyter nbconvert --execute --to notebook --inplace ./src/{notebook}.ipynb",
            f"jupyter nbconvert --to html --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb",
            f"jupyter nbconvert --to latex --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb",
        ],
        "file_dep": ["./src/main_cip.ipynb", str(MANUAL_DATA_DIR / "CIP_2025.xlsx")],
        "targets": [
            str(OUTPUT_DIR / "main_cip.html"),
            str(OUTPUT_DIR / "main_cip.tex"),
        ],
        "task_dep": ["download_cip_data"],  # Ensure data is available
        "clean": True,
    }

def task_summary_stats():
    """
    Generate CIP summary statistics and save LaTeX tables in `_output/`.
    """
    file_dep = ["./src/cip_analysis.py"]
    file_output = [
        str(OUTPUT_DIR / "cip_summary_overall.tex"),
        str(OUTPUT_DIR / "cip_correlation_matrix.tex"),
    ]

    return {
        "actions": [
            "ipython ./src/cip_analysis.py --summary True",
            "ipython ./src/cip_analysis.py --corr True",
        ],
        "file_dep": file_dep,
        "targets": file_output,  # ✅ No more conflicting spread_plot.pdf
        "clean": True,
    }

def task_compile_latex_docs():
    """Compile LaTeX documents to PDFs (if reports exist)."""
    file_dep = [
        str(OUTPUT_DIR / "main_cip.tex"),
    ]
    targets = [
        str(OUTPUT_DIR / "main_cip.pdf"),
    ]

    return {
        "actions": [
            "pdflatex -output-directory=_output _output/main_cip.tex"
        ],
        "file_dep": file_dep,
        "targets": targets,
        "clean": True,
    }

#######################################
## End of dodo.py
#######################################

# To run these tasks, install PyDoit (`pip install doit`) and then use:
#   doit list              # List all available tasks
#   doit download_cip_data # Download the CIP Excel file
#   doit pull_cip          # Run CIP analysis (depends on downloaded file)
#   doit run_notebooks     # Execute notebooks (including main_cip.ipynb)
#   doit summary_stats     # Generate summary statistics
#   doit compile_latex_docs # Convert LaTeX output to PDF