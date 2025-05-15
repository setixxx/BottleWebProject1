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
                            <div class="matrix-controls">
                                <button type="button" class="btn btn-secondary" onclick="makeMatrixSymmetric()">Make Symmetric</button>
                                <button type="button" class="btn btn-secondary" onclick="fillRandomValues()">Random Values</button>
                            </div>
                            <div class="matrix-container">
                                <div class="matrix-corner-placeholder"></div>
                                <div class="matrix-header-row" id="matrix_header_row">
                                    <!-- Column headers will be added by JavaScript -->
                                </div>
                                <div id="matrix_input_container" class="matrix-input-grid">
                                    % if defined('adjacency_matrix_values') and adjacency_matrix_values:
                                        % for r in range(len(adjacency_matrix_values)):
                                            <div class="matrix-row">
                                            <div class="matrix-row-index">{{ r }}</div>
                                            % for c in range(len(adjacency_matrix_values[r])):
                                                <input type="number" name="adj_matrix_{{r}}_{{c}}" class="matrix-cell" min="0" max="1" value="{{ adjacency_matrix_values[r][c] }}" {{ 'readonly' if r == c else '' }}>
                                            % end
                                            </div>
                                        % end
                                    % else:
                                        % default_matrix_size = 6
                                        % for r in range(default_matrix_size):
                                            <div class="matrix-row">
                                            <div class="matrix-row-index">{{ r }}</div>
                                            % for c in range(default_matrix_size):
                                                <input type="number" name="adj_matrix_{{r}}_{{c}}" class="matrix-cell" min="0" max="1" value="{{ '0' if r == c else '1' if (r==0 and c in (1,2,3)) or (r==1 and c in (0,2,4)) or (r==2 and c in (0,1,3,4,5)) or (r==3 and c in (0,2,5)) or (r==4 and c in (1,2,5)) or (r==5 and c in (2,3,4)) else '0' }}" {{ 'readonly' if r == c else '' }}>
                                            % end
                                            </div>
                                        % end
                                    % end
                                </div>
                            </div>
                            <small class="form-text text-muted">Matrix is symmetric. Diagonal elements are 0.</small>
                        </div>
                        <input type="hidden" name="strategy" value="largest_first">
                        <button type="submit" class="btn btn-primary">Color Graph</button>
                    </form>
                </div>

                <div class="results-area" id="results_area">
                    <div class="results-section">
                        <h3>Coloring Results</h3>
                        % if defined('graph_img') and graph_img:
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
                        % else:
                            <p>Graph coloring results will be displayed here after submitting the form.</p>
                            <div class="loading-area">
                                <p>Loading test graph...</p>
                            </div>
                        % end
                    </div>
                </div>
            </div>
        </div>
    </div>

    <a href="/" class="back-button">Back to Home</a>
</div>

<script>
// Function to generate matrix inputs
function generateMatrixInputs(size) {
    const container = document.getElementById('matrix_input_container');
    const headerRow = document.getElementById('matrix_header_row');

    container.innerHTML = ''; // Clear previous inputs
    headerRow.innerHTML = ''; // Clear previous headers

    size = parseInt(size);
    if (isNaN(size) || size < 1 || size > 15) {
        container.innerHTML = '<p class="error-message">Please enter a number between 1 and 15.</p>';
        return;
    }

    // Create column headers
    for (let j = 0; j < size; j++) {
        const headerCell = document.createElement('div');
        headerCell.className = 'matrix-header-cell';
        headerCell.textContent = j;
        headerRow.appendChild(headerCell);
    }

    for (let i = 0; i < size; i++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'matrix-row';

        // Add row index
        const rowIndex = document.createElement('div');
        rowIndex.className = 'matrix-row-index';
        rowIndex.textContent = i;
        rowDiv.appendChild(rowIndex);

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
                input.value = '0'; // Default to 0
            }

            // Ensure symmetry when changing values
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

// Function to make matrix symmetric
function makeMatrixSymmetric() {
    const size = parseInt(document.getElementById('num_vertices').value);

    for (let i = 0; i < size; i++) {
        for (let j = i+1; j < size; j++) {
            const cell1 = document.getElementsByName(`adj_matrix_${i}_${j}`)[0];
            const cell2 = document.getElementsByName(`adj_matrix_${j}_${i}`)[0];

            if (cell1 && cell2) {
                cell2.value = cell1.value;
            }
        }
    }
}

// Function to fill with random values
function fillRandomValues() {
    const size = parseInt(document.getElementById('num_vertices').value);

    for (let i = 0; i < size; i++) {
        for (let j = i+1; j < size; j++) { // Only upper triangle (i < j)
            const cell1 = document.getElementsByName(`adj_matrix_${i}_${j}`)[0];
            const cell2 = document.getElementsByName(`adj_matrix_${j}_${i}`)[0];

            if (cell1 && cell2) {
                // Generate random 0 or 1
                const randomValue = Math.round(Math.random());
                cell1.value = randomValue;
                cell2.value = randomValue; // Keep symmetry
            }
        }
    }
}

// Load test data and submit form automatically on page load
document.addEventListener('DOMContentLoaded', function() {
    const numVerticesInput = document.getElementById('num_vertices');

    // If the matrix is not already rendered by python (e.g. on error)
    if (!document.getElementsByName('adj_matrix_0_0').length) {
        generateMatrixInputs(numVerticesInput.value || 6);
    } else {
        // Update column headers if matrix already exists
        const headerRow = document.getElementById('matrix_header_row');
        headerRow.innerHTML = '';
        const size = parseInt(numVerticesInput.value || 6);

        for (let j = 0; j < size; j++) {
            const headerCell = document.createElement('div');
            headerCell.className = 'matrix-header-cell';
            headerCell.textContent = j;
            headerRow.appendChild(headerCell);
        }
    }

    // Auto-submit the form if there's no graph image already displayed
    if (!document.querySelector('.graph-visualization img')) {
        // Small delay to ensure UI is ready
        setTimeout(function() {
            document.querySelector('.graph-form').submit();
        }, 500);
    }
});
</script>