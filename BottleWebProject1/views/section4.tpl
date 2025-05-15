% rebase('layout.tpl', title='Section 4 - Graph Coloring', year=year)
<link rel="stylesheet" type="text/css" href="/static/content/section4_styles.css" />

<div class="section-container">
    <div class="section-content section4-content">
        <h2>Graph Coloring with Greedy Algorithm (Largest First Strategy)</h2>

        <details class="theory-section collapsible">
            <summary class="collapsible-header">View/Hide Theory</summary>
            <div class="collapsible-content">
                {{ !theory_content }}
            </div>
        </details>

        <div class="practical-section">
            <h3>Practical Implementation</h3>
            <p>Enter the number of vertices to generate an adjacency matrix for an undirected graph. Then, input the matrix values (0 for no edge, 1 for an edge).</p>

            % if defined('error') and error:
            <div class="error-message">
                <p>{{ error }}</p>
            </div>
            % end

            <div class="practical-flex-container">
                <div class="input-area">
                    <form method="post" action="/section4" class="graph-form">
                        <div class="form-group">
                            <label for="num_vertices">Number of Vertices:</label>
                            <input type="number" id="num_vertices" name="num_vertices" class="form-control" min="1" max="15" value="{{ num_vertices if defined('num_vertices') else 6 }}" onchange="generateMatrixInputs(this.value)">
                        </div>

                        <div class="form-group">
                            <label>Adjacency Matrix:</label>
                            <div id="matrix_input_container" class="matrix-input-grid">
                                % if defined('adjacency_matrix_values') and adjacency_matrix_values:
                                    % for r in range(len(adjacency_matrix_values)):
                                        <div class="matrix-row">
                                        % for c in range(len(adjacency_matrix_values[r])):
                                            <input type="number" name="adj_matrix_{{r}}_{{c}}" class="matrix-cell" min="0" max="1" value="{{ adjacency_matrix_values[r][c] }}" {{ 'readonly' if r == c else '' }}>
                                        % end
                                        </div>
                                    % end
                                % else:
                                    % default_matrix_size = 6
                                    % for r in range(default_matrix_size):
                                        <div class="matrix-row">
                                        % for c in range(default_matrix_size):
                                            <input type="number" name="adj_matrix_{{r}}_{{c}}" class="matrix-cell" min="0" max="1" value="{{ '0' if r == c else '1' if (r==0 and c in (1,2,3)) or (r==1 and c in (0,2,4)) or (r==2 and c in (0,1,3,4,5)) or (r==3 and c in (0,2,5)) or (r==4 and c in (1,2,5)) or (r==5 and c in (2,3,4)) else '0' }}" {{ 'readonly' if r == c else '' }}>
                                        % end
                                        </div>
                                    % end
                                % end
                            </div>
                            <small class="form-text text-muted">Matrix is symmetric. Diagonal elements are 0.</small>
                        </div>
                        <input type="hidden" name="strategy" value="largest_first">
                        <button type="submit" class="btn btn-primary">Color Graph</button>
                    </form>
                </div>

                % if defined('graph_img') and graph_img:
                <div class="results-area">
                    <div class="results-section">
                        <h3>Coloring Results</h3>
                        <p>The graph has been colored using <strong>{{ num_colors }}</strong> colors with the <strong>Largest First</strong> strategy.</p>

                        <div class="color-map">
                            <h4>Color Assignment (Horizontal):</h4>
                            <table class="table table-horizontal">
                                <thead>
                                    <tr>
                                        <th>Vertex</th>
                                        % for i in range(len(node_colors)):
                                        <th>{{ i }}</th>
                                        % end
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Color</td>
                                        % for color in node_colors:
                                        <td>{{ color }}</td>
                                        % end
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="graph-visualization">
                            <h4>Graph Visualization:</h4>
                            <img src="data:image/png;base64,{{ graph_img }}" alt="Graph Coloring Visualization" class="img-fluid">
                        </div>
                    </div>
                </div>
                % end
            </div>
        </div>
    </div>

    <a href="/" class="back-button">Back to Home</a>
</div>

<script>
function generateMatrixInputs(size) {
    const container = document.getElementById('matrix_input_container');
    container.innerHTML = ''; // Clear previous inputs
    size = parseInt(size);
    if (isNaN(size) || size < 1 || size > 15) {
        container.innerHTML = '<p class="error-message">Please enter a number between 1 and 15.</p>';
        return;
    }

    for (let i = 0; i < size; i++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'matrix-row';
        for (let j = 0; j < size; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `adj_matrix_${i}_${j}`;
            input.className = 'matrix-cell';
            input.min = '0';
            input.max = '1';
            if (i === j) {
                input.value = '0';
                input.readOnly = true;
            } else {
                // For demonstration, prefill some values - this part can be improved
                // input.value = (i < j) ? '0' : '0'; // Default to 0
            }
            // Ensure symmetry by linking inputs
            input.onchange = function(event) {
                if (i !== j) {
                    const symmetric_input = document.getElementsByName(`adj_matrix_${j}_${i}`)[0];
                    if (symmetric_input) {
                        symmetric_input.value = event.target.value;
                    }
                }
            };
            rowDiv.appendChild(input);
        }
        container.appendChild(rowDiv);
    }
}

// Initial generation if num_vertices is pre-filled (e.g., on error or reload)
document.addEventListener('DOMContentLoaded', function() {
    const numVerticesInput = document.getElementById('num_vertices');
    if (numVerticesInput.value && !document.querySelector('#matrix_input_container .matrix-row')) {
         // if the matrix is not already rendered by python (e.g. on error)
        if (!document.getElementsByName('adj_matrix_0_0').length) {
            generateMatrixInputs(numVerticesInput.value);
        }
    } else if (!numVerticesInput.value) {
         generateMatrixInputs(6); // Default to 6 if nothing is set
    }
});
</script>