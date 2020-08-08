html_layout = """
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%css%}
            {%favicon%}
        </head>

        <body>
            <nav class="navbar navbar-dark bg-primary">
                <a href="/"><i class="fa fa-home fa-lg" style="color: white;"></i></a>
                <span class="navbar-brand my-0 mx-auto h1">Dashboard App</span>
            </nav>
            <header class="text-center py-3">
                <h2>Data Visualization Dashboard</h2>
            </header>

            {%app_entry%}
            
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
