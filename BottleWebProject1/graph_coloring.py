"""
Graph coloring algorithm implementation.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from bottle import request, response, template
import os

def create_graph_from_adjacency_matrix(matrix):
    """Create a networkx graph from an adjacency matrix."""
    G = nx.Graph()
    
    # Add nodes
    n = len(matrix)
    for i in range(n):
        G.add_node(i)
    
    # Add edges
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] == 1:
                G.add_edge(i, j)
    
    return G

def greedy_coloring(G, strategy="largest_first"):
    """
    Apply greedy coloring algorithm to graph G.
    
    Parameters:
    - G: networkx graph
    - strategy: vertex ordering strategy 
      (options: "largest_first", "random", "smallest_last", "independent_set", "connected_sequential")
    
    Returns:
    - color_map: dictionary mapping nodes to colors
    """
    # Get ordered vertices based on strategy
    if strategy == "largest_first":
        # Sort vertices by degree in descending order
        vertices = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    elif strategy == "random":
        # Random ordering
        vertices = list(G.nodes())
        np.random.shuffle(vertices)
    elif strategy == "smallest_last":
        # Remove vertices with smallest degree, color in reverse order
        vertices = list(nx.coloring.strategy_smallest_last(G))
    elif strategy == "independent_set":
        # Try to find large independent sets
        vertices = list(nx.coloring.strategy_independent_set(G))
    elif strategy == "connected_sequential":
        # BFS-based ordering
        vertices = list(nx.coloring.strategy_connected_sequential(G))
    else:
        # Default to largest first
        vertices = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    
    # Initialize color map
    color_map = {}
    
    # For each vertex
    for vertex in vertices:
        # Get colors of adjacent vertices
        neighbor_colors = {color_map.get(neighbor) for neighbor in G.neighbors(vertex) if neighbor in color_map}
        
        # Find the smallest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        
        # Assign color to vertex
        color_map[vertex] = color
    
    return color_map

def visualize_graph_coloring(G, color_map):
    """
    Visualize the graph with coloring.
    
    Parameters:
    - G: networkx graph
    - color_map: dictionary mapping nodes to colors
    
    Returns:
    - base64_img: base64 encoded image
    - num_colors: number of colors used
    """
    # Define a color palette
    color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Map integer colors to actual colors
    node_colors = [color_palette[color_map[node] % len(color_palette)] for node in G.nodes()]
    
    # Get positions for all nodes
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=18, 
            font_weight='bold', width=2, edge_color='gray', alpha=0.9)
    
    # Calculate number of colors used
    num_colors = len(set(color_map.values()))
    
    # Add title
    plt.title(f"Graph Coloring (Using {num_colors} colors)", fontsize=16)
    
    # Save plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plt.close()
    
    # Convert to base64
    base64_img = base64.b64encode(buffer.read()).decode('utf-8')
    
    return base64_img, num_colors

def get_graph_coloring_data(adjacency_matrix, strategy="largest_first"):
    """
    Process graph coloring based on adjacency matrix and strategy.
    
    Parameters:
    - adjacency_matrix: 2D array representing the adjacency matrix
    - strategy: vertex ordering strategy
    
    Returns:
    - Dictionary with graph coloring results
    """
    G = create_graph_from_adjacency_matrix(adjacency_matrix)
    color_map = greedy_coloring(G, strategy)
    
    # Convert color map to node-indexed list for displaying
    node_colors = [color_map[i] for i in range(len(adjacency_matrix))]
    
    # Generate visualization
    base64_img, num_colors = visualize_graph_coloring(G, color_map)
    
    # Prepare results
    results = {
        "graph_img": base64_img,
        "num_colors": num_colors,
        "node_colors": node_colors,
        "strategy": strategy
    }
    
    return results