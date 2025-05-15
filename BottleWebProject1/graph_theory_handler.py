"""
Module for handling graph coloring operations and theory.
"""

import os
import markdown
import json
from graph_coloring import get_graph_coloring_data # Assuming this takes matrix and strategy

# Path to theory file - ensure this path is correct relative to where this script is run
# Or use an absolute path or a path derived from a base directory.
# For a typical Bottle setup where app.py is the main entry point,
# this path might need to be relative to app.py or handled by app.py.
# If graph_theory_handler.py is in the same directory as app.py, then:
THEORY_FILE = os.path.join(os.path.dirname(__file__), 'static', 'resources', 'graph_coloring_theory.md')
# If the static folder is one level up from where app.py is (e.g. app is in a src folder)
# then it would be different. Based on provided structure, this should work if
# this handler is in the root with app.py, and static is a subdir.
# However, the original structure suggests static is at the same level as app.py.
# The most robust way is to pass the path from routes.py or app.py if necessary.
# For now, assuming 'static/resources/graph_coloring_theory.md' is accessible from execution path.

# Let's try a more robust path assuming 'static' is a sibling to the directory of app.py/routes.py
# (or directly in the root if this file is also in root)
# If 'views' and 'static' are siblings of app.py, this path needs to be based from app.py.
# The provided files `routes.py` `snippetFromFront` places THEORY_FILE as `os.path.join('static', 'resources', 'graph_coloring_theory.md')`
# which assumes the current working directory is the project root.
# Let's keep it simple and assume 'static' is findable from the CWD.
# A better way:
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # If handler is in a subdir
# THEORY_FILE = os.path.join(BASE_DIR, 'static', 'resources', 'graph_coloring_theory.md')
# For now, use the simpler path as per existing snippets if they worked.

THEORY_FILE = 'static/resources/graph_coloring_theory.md' # Path relative to project root

DEFAULT_MATRIX = [
    [0, 1, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0]
]

def load_theory():
    """Load graph coloring theory from file."""
    try:
        # More robust path based on the location of this file:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Assuming static folder is at the same level as the directory containing app.py, routes.py etc.
        # If graph_theory_handler.py is in the root:
        theory_file_path = os.path.join(current_dir, 'static', 'resources', 'graph_coloring_theory.md')
        # If graph_theory_handler.py is inside a subdir like 'handlers' and static is in root:
        # theory_file_path = os.path.join(os.path.dirname(current_dir), 'static', 'resources', 'graph_coloring_theory.md')

        # Sticking to user provided file path:
        # THEORY_FILE is already defined above.

        if os.path.exists(THEORY_FILE):
            with open(THEORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                html_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'toc'])
                return html_content
        else:
            return f"<p>Theory file not found. Looked for: {os.path.abspath(THEORY_FILE)}. Please ensure it exists.</p>"
    except Exception as e:
        return f"<p>Error loading theory: {str(e)}</p>"

def process_graph_coloring_request(raw_matrix=None, strategy="largest_first"):
    """
    Process graph coloring request.
    Accepts either raw_matrix (list of lists) or uses default.
    Strategy is fixed to 'largest_first' by default in section4.
    """
    matrix_to_process = None
    error_message = None

    if raw_matrix:
        # Validate matrix structure (basic validation, more can be added)
        if not isinstance(raw_matrix, list) or not all(isinstance(row, list) for row in raw_matrix):
            error_message = "Invalid matrix format: Should be a list of lists."
        elif not raw_matrix:
            error_message = "Matrix is empty."
        else:
            rows = len(raw_matrix)
            if rows > 0 and not all(len(row) == rows for row in raw_matrix):
                error_message = "Matrix is not square."
            else:
                matrix_to_process = raw_matrix
    else: # Default case if no matrix is provided (e.g., initial load with default behavior)
        matrix_to_process = DEFAULT_MATRIX
        strategy = "largest_first" # Ensure strategy is set for default

    if error_message:
        return {
            "error": error_message,
            "graph_img": None, "num_colors": 0, "node_colors": [], "strategy": strategy
        }

    if matrix_to_process:
        try:
            # get_graph_coloring_data should already accept a matrix and strategy
            return get_graph_coloring_data(matrix_to_process, strategy)
        except Exception as e:
            return {
                "error": f"Error during graph coloring: {str(e)}",
                "graph_img": None, "num_colors": 0, "node_colors": [], "strategy": strategy
            }
    else: # Should not happen if logic is correct, but as a fallback
        return {
            "error": "No matrix data to process.",
            "graph_img": None, "num_colors": 0, "node_colors": [], "strategy": strategy
        }