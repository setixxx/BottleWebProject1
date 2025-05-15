<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Our Awesome App</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/main.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/section.css" />
    % if title == 'Section 4 - Graph Coloring':
        <link rel="stylesheet" type="text/css" href="/static/content/section4_styles.css" />
    % end
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>
<body>
    <div class="container body-content">
        <div class="header">
            <h1>Our Awesome App</h1>
        </div>

        <div class="navbar">
            <a href="/" class="nav-item{{ ' active' if title == 'Home' else '' }}">Home</a>
            <a href="/section1" class="nav-item{{ ' active' if title == 'Section 1' else '' }}">Section 1</a>
            <a href="/section2" class="nav-item{{ ' active' if title == 'Section 2' else '' }}">Section 2</a>
            <a href="/section3" class="nav-item{{ ' active' if title == 'Section 3' else '' }}">Section 3</a>
            <a href="/section4" class="nav-item{{ ' active' if title == 'Section 4 - Graph Coloring' else '' }}">Section 4</a>
        </div>

        {{ !base }}
        <hr />
        <footer>
            <p>&copy; {{ year }} - Our Awesome App</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
    </body>
</html>