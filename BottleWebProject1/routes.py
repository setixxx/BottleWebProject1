"""
Updated routes module to include the graph coloring section.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file

# Import graph theory handler
from graph_theory_handler import load_theory, process_graph_coloring_request

# Paths for data and logos
UPLOAD_DIR = 'static/resources/logos'
DATA_FILE = 'static/resources/partners.json'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure resources directory exists
os.makedirs(os.path.join('static', 'resources'), exist_ok=True)

# Save graph coloring theory if it doesn't exist - Ensure this path is correct
THEORY_FILE_PATH = os.path.join(os.path.dirname(__file__), 'static', 'resources', 'graph_coloring_theory.md')
# Corrected path for THEORY_FILE within the module where it's defined or used
# Assuming graph_coloring_theory.md is in static/resources relative to app.py or where routes is run from.
# The graph_theory_handler.py uses a path relative to its own location or expects it.
# For consistency, graph_theory_handler.py should ideally define this.
# The provided code seems to handle it in graph_theory_handler.py

# ... (other routes like home, section1, section2, section3 remain the same) ...
@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/section1')
@view('section1')
def section1():
    return dict(
        year=datetime.now().year
    )

@route('/section2')
@view('section2')
def section2():
    return dict(
        year=datetime.now().year
    )

@route('/section3')
@view('section3')
def section3():
    return dict(
        year=datetime.now().year
    )


@route('/section4')
@view('section4')
def section4_get():
    """Renders section 4 - Graph Coloring (GET request)."""
    theory_content = load_theory()
    # Provide default values for initial rendering
    num_vertices = 6 # Default number of vertices
    # Create a default matrix for display if needed, or let JS handle initial empty state
    default_adj_matrix = [
        [0,1,1,1,0,0],
        [1,0,1,0,1,0],
        [1,1,0,1,1,1],
        [1,0,1,0,0,1],
        [0,1,1,0,0,1],
        [0,0,1,1,1,0]
    ]

    return dict(
        year=datetime.now().year,
        theory_content=theory_content,
        num_vertices=num_vertices,
        adjacency_matrix_values=default_adj_matrix, # Pass this for pre-filling
        # No graph results on initial GET
        graph_img=None,
        num_colors=None,
        node_colors=None,
        strategy='largest_first', # Strategy is fixed
        error=None
    )

@route('/section4', method='POST')
@view('section4')
def section4_post():
    """Process graph coloring form submission (POST request)."""
    theory_content = load_theory()
    form_data = request.forms

    # Get number of vertices
    try:
        num_vertices = int(form_data.get('num_vertices', 0))
        if not (1 <= num_vertices <= 15): # Max 15 vertices for performance/display
            raise ValueError("Number of vertices must be between 1 and 15.")
    except ValueError as e:
        return dict(
            year=datetime.now().year,
            theory_content=theory_content,
            num_vertices=form_data.get('num_vertices', 6), # return original input
            error=str(e),
            graph_img=None, num_colors=None, node_colors=None, strategy='largest_first'
        )

    # Reconstruct adjacency matrix from form
    adj_matrix = []
    current_matrix_values = [] # To send back to template if error
    try:
        for i in range(num_vertices):
            row = []
            current_row_values = []
            for j in range(num_vertices):
                cell_value = int(form_data.get(f'adj_matrix_{i}_{j}', 0))
                if cell_value not in [0, 1]:
                    raise ValueError(f"Invalid value in matrix cell ({i},{j}). Must be 0 or 1.")
                if i == j and cell_value != 0:
                    raise ValueError(f"Diagonal elements (cell {i},{j}) must be 0.")
                row.append(cell_value)
                current_row_values.append(cell_value)
            adj_matrix.append(row)
            current_matrix_values.append(current_row_values)

        # Validate symmetry
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if adj_matrix[i][j] != adj_matrix[j][i]:
                    raise ValueError("Adjacency matrix must be symmetric for an undirected graph.")

    except ValueError as e:
        return dict(
            year=datetime.now().year,
            theory_content=theory_content,
            num_vertices=num_vertices,
            adjacency_matrix_values=current_matrix_values if current_matrix_values else [[0]*num_vertices for _ in range(num_vertices)],
            error=f"Error in matrix input: {str(e)}",
            graph_img=None, num_colors=None, node_colors=None, strategy='largest_first'
        )

    # Process graph coloring (pass the reconstructed matrix)
    # The process_graph_coloring_request function in graph_theory_handler
    # will need to accept this raw matrix.
    # For now, we assume it does, or we adapt it.
    # We'll pass the matrix directly, not the form_data object for matrix.

    # The strategy is fixed to "largest_first"
    strategy = "largest_first"
    coloring_results = process_graph_coloring_request(raw_matrix=adj_matrix, strategy=strategy)

    return dict(
        year=datetime.now().year,
        theory_content=theory_content,
        num_vertices=num_vertices,
        adjacency_matrix_values=adj_matrix, # Send back the processed matrix
        graph_img=coloring_results.get('graph_img'),
        num_colors=coloring_results.get('num_colors'),
        node_colors=coloring_results.get('node_colors'),
        strategy=strategy, # Display the used strategy
        error=coloring_results.get('error', None)
    )

# Static files route (ensure this is present and correct)
@route('/static/<filepath:path>')
def server_static(filepath):
    # Assuming your static directory is at the root of your project,
    # and app.py is also at the root.
    # If app.py is in a subdirectory, adjust the root path.
    # For the project structure given, 'static' is a top-level directory.
    return static_file(filepath, root='./static/')