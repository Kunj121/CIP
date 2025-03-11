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
import shutil


sys.path.insert(1, "./src/")  # Add ./src/ to Python path

import sys
import os
sys.path.append(os.path.abspath("src"))  # Ensure `src/` is in the path

from src.settings import config

DATA_DIR = (config("DATA_DIR"))
OUTPUT_DIR = (config("OUTPUT_DIR"))
MANUAL_DATA_DIR = (config("MANUAL_DATA_DIR"))
PUBLISH_DIR = (config("PUBLISH_DIR"))


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


#the above formats the doit file making it easier to read


#######################################
## Helper Functions for Jupyter Tasks
#######################################
def jupyter_execute_notebook(notebook):
    return (f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --execute --to notebook --"
            f"inplace --ExecutePreprocessor.allow_errors=True ./src/{notebook}.ipynb")

def jupyter_to_html(notebook):
    return f"jupyter nbconvert --to html --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb"

def jupyter_to_latex(notebook):
    return f"jupyter nbconvert --to latex --output-dir={OUTPUT_DIR} ./src/{notebook}.ipynb"

def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"

#######################################
## PyDoit Tasks
#######################################

def task_config():
    """Create directories for data and output if they don't exist."""
    def create_dirs():
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(MANUAL_DATA_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(PUBLISH_DIR, exist_ok=True)

    return {
        "actions": [create_dirs],
        "targets": [str(DATA_DIR), str(OUTPUT_DIR), str(MANUAL_DATA_DIR), str(PUBLISH_DIR)],
        "clean": True,
    }

def task_download_cip_data():
    """
    Download CIP_2025.xlsx from GitHub and save it to the manual data folder.
    """
    target_file = MANUAL_DATA_DIR / "CIP_2025.xlsx"

    def download():
        import requests
        url = "https://raw.githubusercontent.com/Kunj121/CIP/main/data_manual/CIP_2025.xlsx"
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(MANUAL_DATA_DIR, exist_ok=True)
        with open(target_file, "wb") as f:
            f.write(response.content)
        print(f"File saved to {target_file.resolve()}")

    return {
        "actions": [download],
        "targets": [str(target_file)],
        "uptodate": [False],
        "clean": True,
    }



def task_clean_data():
    """Run the CIP data cleaning script."""
    tidy_data_file = DATA_DIR / "tidy_data.csv"
    return {
        "actions": ["ipython ./src/clean_data.py"],
        "file_dep": [str(MANUAL_DATA_DIR / "CIP_2025.xlsx")],
        "targets": [str(tidy_data_file)],
        "clean": True,
    }


def task_run_notebooks():
    """Execute Jupyter notebooks and convert them to HTML & LaTeX."""
    notebook = "main_cip"

    return {
        "actions": [
            jupyter_execute_notebook(notebook),
            jupyter_to_html(notebook),
            jupyter_to_latex(notebook),
            # convert_html_to_png  # Move PNGs and process files
        ],
        "file_dep": ["./src/main_cip.ipynb", str(MANUAL_DATA_DIR / "CIP_2025.xlsx")],
        "targets": [
            str(OUTPUT_DIR /"html_files"/ "main_cip.html"),
            str(OUTPUT_DIR / "main_cip.tex"),
        ],
        "task_dep": ["download_cip_data"],
        "clean": True,
    }


def task_pull_cip():
    """Run CIP analysis and rename output plots correctly."""

    def rename_output_files():
        """Rename automatically generated plots to expected filenames."""
        import os
        from pathlib import Path

        old_files = {
            "main_cip_9_0.png": "cip_spread_plot_replication.png",
            "main_cip_14_0.png": "cip_spread_plot_2025.png",
        }
        output_dir = OUTPUT_DIR / "main_cip_files"

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for old_name, new_name in old_files.items():
            old_path = output_dir / old_name
            new_path = output_dir / new_name  # Keep it in main_cip_files
            if old_path.exists():
                old_path.rename(new_path)
                print(f"Renamed {old_path} → {new_path}")
            else:
                print(f"Warning: {old_path} not found.")

    return {
        "actions": [
            "cd src && ipython cip_analysis.py",
            rename_output_files  # Rename after execution
        ],
        "file_dep": [
            "./src/cip_analysis.py",
            "./src/pull_bloomberg_cip_data.py",
            str(MANUAL_DATA_DIR / "CIP_2025.xlsx"),
        ],
        "targets": [
            str(OUTPUT_DIR / "main_cip_files" / "cip_spread_plot_replication.png"),
            str(OUTPUT_DIR / "main_cip_files" / "cip_spread_plot_2025.png"),
        ],
        "task_dep": ["download_cip_data"],
        "clean": True,
    }

def task_summary_stats():
    """Generate summary statistics and save them as HTML files."""
    def generate_summary():
        # Ensure we correctly import the required functions
        from src.directory_functions import save_cip_statistics_as_html
        from src.pull_bloomberg_cip_data import compute_cip
        from src.cip_analysis import compute_cip_statistics

        # Step 1: Compute CIP data
        cip_data = compute_cip()

        # Step 2: Compute statistics
        stats_dict = compute_cip_statistics(cip_data)

        # Debugging: Check if 'overall_statistics' exists
        if "overall_statistics" not in stats_dict:
            raise KeyError("Error: 'overall_statistics' key is missing from stats_dict!")

        # Step 3: Save statistics as HTML
        save_cip_statistics_as_html(stats_dict)

    return {
        "actions": [generate_summary],
        "file_dep": ["./src/pull_bloomberg_cip_data.py", "./src/cip_analysis.py"],
        "targets": [
            str(OUTPUT_DIR / "cip_summary_overall.html"),
            str(OUTPUT_DIR / "cip_correlation_matrix.html"),
            str(OUTPUT_DIR / "cip_annual_statistics.html"),
        ],
        "clean": True,
    }

import shutil

def copy_notebook():
    """Copy main_cip.ipynb from src to output and rename it paper.ipynb."""
    src_path = Path("src/main_cip.ipynb")
    dest_path = PUBLISH_DIR / "paper.ipynb"

    shutil.copy2(src_path, dest_path)  # Copy and preserve metadata
    print(f"Copied {src_path} → {dest_path}")

def task_generate_paper():
    """Generate a LaTeX paper from the copied Jupyter Notebook."""
    paper_notebook = PUBLISH_DIR / "paper.ipynb"
    paper_tex = PUBLISH_DIR / "paper.tex"


    return {
        "actions": [
            copy_notebook,  # Copy first
            f"jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.allow_errors=True {paper_notebook}",
            f"jupyter nbconvert --to latex --output-dir={PUBLISH_DIR} {paper_notebook}",
            f"pdflatex -output-directory={PUBLISH_DIR} {paper_tex}",
            # Comment out or remove the following line if no bibliography is needed
            # f"bibtex {paper_tex.with_suffix('')}",
            f"pdflatex -output-directory={PUBLISH_DIR} {paper_tex}",
            f"pdflatex -output-directory={PUBLISH_DIR} {paper_tex}"
        ],
        "file_dep": [],
        "targets": [str(paper_tex)],
        "task_dep": [],
        "clean": True,
    }

def task_clean_reports():
    """Remove unnecessary output files."""
    files_to_remove = [
        PUBLISH_DIR / "paper.aux",
        PUBLISH_DIR / "paper.log",
        PUBLISH_DIR / "paper.out",
        PUBLISH_DIR / "paper_files",
    ]

    def remove_files():
        for file in files_to_remove:
            if file.exists():
                file.unlink()
                print(f"Removed {file}")
            else:
                print(f"File not found: {file}")

    return {
        "actions": [remove_files],
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