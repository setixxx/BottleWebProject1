"""
Module for handling graph coloring operations and theory.
"""

import os
import markdown
import json
from graph_coloring import get_graph_coloring_data

# Path to theory file
THEORY_FILE = os.path.join('static', 'resources', 'graph_coloring_theory.md')
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
        if os.path.exists(THEORY_FILE):
            with open(THEORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                # Convert markdown to HTML
                html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
                return html_content
        else:
            return "<p>Theory file not found. Please make sure the file exists at the correct path.</p>"
    except Exception as e:
        return f"<p>Error loading theory: {str(e)}</p>"

def process_graph_coloring_request(form_data=None):
    """Process graph coloring request from form data."""
    if form_data and form_data.get('adjacency_matrix'):
        try:
            # Parse adjacency matrix from form data
            matrix_str = form_data.get('adjacency_matrix')
            matrix = json.loads(matrix_str)
            
            # Parse strategy
            strategy = form_data.get('strategy', 'largest_first')
            
            # Process graph coloring
            return get_graph_coloring_data(matrix, strategy)
        except Exception as e:
            return {
                "error": f"Error processing graph coloring: {str(e)}",
                "graph_img": None,
                "num_colors": 0,
                "node_colors": [],
                "strategy": "largest_first"
            }
    else:
        # Use default matrix if no form data provided
        return get_graph_coloring_data(DEFAULT_MATRIX, "largest_first")