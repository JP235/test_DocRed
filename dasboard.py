import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("MOCK_DATA.csv", header="infer")
df["Total"] = 1   # Dummy var para agrupacions

app = dash.Dash(__name__)

app.layout = html.Div(
    className='main-content',
    style={
    'max-width':"1200px",
    'margin': "0 auto"
    },
    children=[
        html.H1('Reporte Semestre 1 2023', 
                style={
                    'textAlign': 'center', 
                    'color': '#503D36',
                    'font-size': 24}),
        html.Div(
            className='inputs',
            children=[
                html.Div(
                    className='div-user-controls',
                    children=[
                        html.Div(
                            className='div-for-date',
                            children=[
                            html.H4('Fechas'),
                            dcc.DatePickerRange(
                                id="fecha-dropdown",
                                start_date=df["fecha de creacion"].min(),
                                end_date=df["fecha de creacion"].max(),
                            ),       

                        ]        
                        ),
                        html.Div(
                            children=[
                            html.H4('Genero'),
                            dcc.Dropdown(
                            id="genero-dropdown",
                            className="Dropdown1",
                            options=[{"label": i, "value": i} for i in df["genero"].unique()],
                            placeholder="Genero",
                        ),]),

                        html.Div(
                            children=[      
                            html.H4('Pais'),
                            dcc.Checklist(
                            className='div-for-dropdown',
                                id="pais-dropdown",
                                options=[{"label": i, "value": i} for i in df["pais"].unique()],
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                            html.H4('Especialidad'),
                            dcc.Checklist(
                            className='div-for-dropdown',
                                id="especialidad-dropdown",
                                options=[
                                    {"label": i, "value": i} for i in df["especialidad medica"].unique()
                                    ],     
                                ),
                            ]
                        ),
                         
                    ]
                ),
        ]),
        html.Div([],className="plot", id='plot1'),
        html.Div(
            className='distribuciones',
            children=[
            html.Div([],className="plot", id='plot5'),
            html.Div([],className="plot", id='plot3'),
            html.Div([],className="plot", id='plot4'),
            ]
            ),
        html.Div([],className="plot", id='plot2'),
        html.Div([],className="plot", id='plot6'),
    ]
)


@app.callback(
    [Output(component_id='plot1', component_property='children'),
    Output(component_id='plot2', component_property='children'),
    Output(component_id='plot4', component_property='children'),
    Output(component_id='plot5', component_property='children'),
    Output(component_id='plot3', component_property='children'),
    Output(component_id='plot6', component_property='children'),
    ],
    [
        Input("genero-dropdown", "value"),
        Input("pais-dropdown", "value"),
        Input("especialidad-dropdown", "value"),
        Input("fecha-dropdown", "start_date"),
        Input("fecha-dropdown", "end_date"),
    ],
)

def get_graph(genero, pais, especialidad, start_date, end_date):
    dff = df.copy()

    if genero:
        dff = dff[dff["genero"] == genero]

    if pais:
        dff = dff[dff["pais"].isin(pais)]

    if especialidad:
        dff = dff[dff["especialidad medica"].isin(especialidad)]

    if start_date and end_date:
        dff = dff[
            (dff["fecha de creacion"] >= start_date)
            & (dff["fecha de creacion"] <= end_date)
        ]

    data_fecha = dff.groupby('fecha de creacion')['Total'].count().reset_index()
    data_fecha["Acumulado"] = data_fecha["Total"].cumsum()
    data_fecha["Mes"] = pd.to_datetime(data_fecha["fecha de creacion"]).dt.month
    data_fecha["Dia"] = pd.to_datetime(data_fecha["fecha de creacion"]).dt.day
    data_fecha['avg_window = 7'] = data_fecha['Total'].rolling(window=7).mean()
    data_fecha = data_fecha.dropna(subset=['avg_window = 7'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_fecha['fecha de creacion'], y=data_fecha['Acumulado'],name="Acumulado"))
    fig.add_trace(go.Bar(x=data_fecha['fecha de creacion'], y=data_fecha['Total'],name="Nuevos Dia" , yaxis="y2", marker_color=data_fecha['Mes'] ))
    fig.add_trace(go.Scatter(x=data_fecha['fecha de creacion'], y=data_fecha['avg_window = 7'],name="avg_window = 7", yaxis="y2",marker_color="black"))
    # # Add bar plot with dayly records to line plot with axis on the right


    fig.update_layout(
    title_text="Subscripciones por dia",
    yaxis2=dict(
        title="Subs por Día",
        overlaying="y",
        side="right",
        range=[0, data_fecha['Total'].max()+1]  # replace min_value and max_value with your desired values
    ),
    yaxis1 = dict(
        title="Subs Totales",
        side="left",
        showgrid=False
    )
    )
    tree_data = dff.groupby(["pais", "especialidad medica"]).Total.sum().reset_index()
    tree_fig = px.treemap(
                tree_data,
                path=["pais", "especialidad medica"],
                values='Total',
                color='Total',
                color_continuous_scale='RdBu',
            )
    pais_data = dff.groupby(["genero","pais"])["Total"].sum().reset_index(name="Total")
    esp_data = dff.groupby(["genero","especialidad medica"])["Total"].sum().reset_index(name="Total")
    
    pais_pie_fig = px.sunburst(pais_data, values="Total", path=["pais"], title="Distribución según países")
    esp_pie_fig = px.sunburst(esp_data, values="Total", path=["especialidad medica"], title="Distribución según especialidad")
    gen_pie_fig = px.sunburst(esp_data, values="Total", path=["genero"],title="Distribución según género")

    trend_fig = go.Figure()
    # fig.add_trace(go.Scatter(x=data_fecha['fecha de creacion'], y=data_fecha['Acumulado'],name="Acumulado"))
    trend_fig.add_trace(go.Scatter(x=data_fecha['fecha de creacion'], y=data_fecha['avg_window = 7'],name="avg_window = 7", yaxis="y2",marker_color="black"))
    # fig.add_trace(go.Bar(x=data_fecha['fecha de creacion'], y=data_fecha['Total'],name="Nuevos Dia" , yaxis="y2", marker_color=data_fecha['Dia'] ))
    
    model = LinearRegression()
    model = LinearRegression()

    # Reshape index array to 2D for .fit() method
    X = np.array(range(len(data_fecha['avg_window = 7']))).reshape(-1, 1)
    y = data_fecha['avg_window = 7']

    # Fit the model
    model.fit(X, y)

    # Get the linear regression line values
    y_pred = model.predict(X)

    data_fecha['y_pred'] = y_pred
    
    trend_fig.add_trace(go.Scatter(x=data_fecha['fecha de creacion'], y=data_fecha['y_pred'], name='Linear Regression of Moving Average',yaxis="y2", line=dict(color='green')))
    
    return [
        dcc.Graph(figure=tree_fig),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=gen_pie_fig),
        dcc.Graph(figure=pais_pie_fig),
        dcc.Graph(figure=esp_pie_fig),
        dcc.Graph(figure=trend_fig),
        ]


if __name__ == "__main__":
    app.run_server(debug=True)
