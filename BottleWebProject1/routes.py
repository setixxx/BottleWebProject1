"""
Updated routes module to include the graph coloring section.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, \
    static_file

# Import graph theory handler
from graph_theory_handler import load_theory, process_graph_coloring_request

# Paths for data and logos
UPLOAD_DIR = 'static/resources/logos'
DATA_FILE = 'static/resources/partners.json'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure resources directory exists
os.makedirs(os.path.join('static', 'resources'), exist_ok=True)

# Save graph coloring theory if it doesn't exist
THEORY_FILE = os.path.join('static', 'resources', 'graph_coloring_theory.md')
if not os.path.exists(THEORY_FILE):
    with open(THEORY_FILE, 'w', encoding='utf-8') as f:
        f.write("""# Graph Theory: Graph Coloring

Graph coloring is a special case of graph labeling; it is an assignment of labels (traditionally called "colors") to elements of a graph subject to certain constraints.

## Vertex Coloring

Vertex coloring is the most common graph coloring problem. The problem is to assign colors to the vertices of a graph such that no two adjacent vertices share the same color. This is called a proper vertex coloring.

The minimum number of colors needed to color a graph G is called its chromatic number, denoted χ(G).

## Applications of Graph Coloring

Graph coloring has applications in various fields:

1. **Scheduling**: Assigning time slots to classes or exams to avoid conflicts
2. **Register Allocation**: Optimizing computer register usage in compilers
3. **Map Coloring**: Ensuring adjacent regions have different colors
4. **Frequency Assignment**: Allocating frequencies to radio stations to avoid interference
5. **Sudoku Puzzles**: Solving and generating Sudoku puzzles

## Greedy Coloring Algorithm

The greedy coloring algorithm is a simple approach to color the vertices of a graph:

1. Order the vertices in some specific order v₁, v₂, ..., vₙ
2. For each vertex vᵢ:
   - Consider the colors already assigned to its adjacent vertices
   - Assign to vᵢ the smallest available color not used by any adjacent vertex

This algorithm doesn't guarantee the minimum number of colors (chromatic number), but it provides a practical solution with reasonable performance. The number of colors used depends on the order of vertices.

### Welsh-Powell Algorithm

The Welsh-Powell algorithm is a specific implementation of the greedy approach:

1. Sort vertices by degree (number of connections) in descending order
2. Assign the first color to the first vertex and to all vertices not adjacent to it
3. Repeat step 2 with a new color until all vertices are colored

### Brooks' Theorem

Brooks' theorem states that for any connected undirected graph G, the chromatic number χ(G) is at most the maximum degree Δ(G), unless G is a complete graph or an odd cycle, in which case χ(G) = Δ(G) + 1.

This provides a theoretical upper bound for graph coloring algorithms.""")

# Load data on startup
companies = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)


@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(year=datetime.now().year)


# Routes for sections 1-4
@route('/section1')
@view('section1')
def section1():
    """Renders section 1."""
    return dict(
        year=datetime.now().year
    )


@route('/section2')
@view('section2')
def section2():
    """Renders section 2."""
    return dict(
        year=datetime.now().year
    )


@route('/section3')
@view('section3')
def section3():
    """Renders section 3."""
    return dict(
        year=datetime.now().year
    )


@route('/section4')
@view('section4')
def section4():
    """Renders section 4 - Graph Coloring."""
    # Load theory content
    theory_content = load_theory()

    # Process graph coloring with default values
    coloring_results = process_graph_coloring_request()

    return dict(
        year=datetime.now().year,
        theory_content=theory_content,
        graph_img=coloring_results.get('graph_img'),
        num_colors=coloring_results.get('num_colors'),
        node_colors=coloring_results.get('node_colors'),
        strategy=coloring_results.get('strategy'),
        error=coloring_results.get('error', None)
    )


@route('/section4', method='POST')
@view('section4')
def section4_post():
    """Process graph coloring form submission."""
    # Load theory content
    theory_content = load_theory()

    # Process form data
    coloring_results = process_graph_coloring_request(request.forms)

    return dict(
        year=datetime.now().year,
        theory_content=theory_content,
        graph_img=coloring_results.get('graph_img'),
        num_colors=coloring_results.get('num_colors'),
        node_colors=coloring_results.get('node_colors'),
        strategy=coloring_results.get('strategy'),
        error=coloring_results.get('error', None)
    )