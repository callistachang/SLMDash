html_layout = """
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%css%}
        </head>

        <body>
            <nav class="navbar navbar-dark bg-primary">
                <a href="/"><i class="fa fa-home fa-lg" style="color: white;"></i></a>
                <span class="navbar-brand my-0 mx-auto h1">Dashboard App</span>
            </nav>
            <header>
                <h2 class="text-center py-3">Data Visualization Dashboard</h1>
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
