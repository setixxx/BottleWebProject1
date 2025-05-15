# Graph Theory: Graph Coloring

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

This provides a theoretical upper bound for graph coloring algorithms.