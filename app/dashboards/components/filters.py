def add_filters():
    """Agrega filtros al layout del dashboard"""
    return html.Div([
        html.H3("Filtros", className="dashboard-title"),
        html.Div([
            # Filtro de fecha
            html.Div([
                html.Label("Rango de Fechas"),
                dcc.DateRangePickerSingle(
                    id='date-range',
                    start_date=datetime.now() - timedelta(days=30),
                    end_date=datetime.now()
                )
            ], className="filter-item"),
            
            # Filtro de edad
            html.Div([
                html.Label("Rango de Edad"),
                dcc.RangeSlider(
                    id='age-range',
                    min=18,
                    max=100,
                    step=1,
                    marks={18: '18', 40: '40', 60: '60', 80: '80', 100: '100'},
                    value=[18, 100]
                )
            ], className="filter-item"),
            
            # Filtro de trabajo
            html.Div([
                html.Label("Tipo de Trabajo"),
                dcc.Dropdown(
                    id='job-filter',
                    options=[
                        {'label': 'Todos', 'value': 'all'},
                        {'label': 'Management', 'value': 'management'},
                        {'label': 'Technician', 'value': 'technician'},
                        {'label': 'Entrepreneur', 'value': 'entrepreneur'},
                        {'label': 'Blue-collar', 'value': 'blue-collar'}
                    ],
                    value='all',
                    multi=True
                )
            ], className="filter-item")
        ], className="filters-container")
    ], className="filters-section")