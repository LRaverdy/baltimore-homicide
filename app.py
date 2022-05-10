import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly.io as pio

pio.renderers.default = 'svg'  # or 'brower' to display in new window

df = pd.read_csv('data_baltimore.csv')
# -------------------------------------------------

df['age_category'] = df['age'].apply(lambda x: 'Newborns' if (x >= 0) & (x <= 3)
                                    else 'Children' if (x > 3) & (x <= 12)
                                    else 'Youth' if (x > 12) & (x <= 24)
                                    else 'Adults' if (x > 24) & (x <= 64)
                                    else 'Seniors' if x > 64
                                    else x)

# --------------------- Order date ---------------------

months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

days = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]

# In order to sort data by month name
df['dayofweek'] = pd.Categorical(df['dayofweek'], categories=days, ordered=True)

# In order to sort data by month name
df['month'] = pd.Categorical(df['month'], categories=months, ordered=True)

########################################################
###################### Dashboard #######################
########################################################

# Parameters

green = '#5CEDB2'
purple = '#d028fa'
yellow = '#f0ff17'
red = '#d07670'
blue = 'blue'

# Graph colors
colors = ['darkred', green, blue, purple, yellow]

# Hide plotly toolbar options
config={'displaylogo' : False,
        'modeBarButtonsToRemove': ['zoom2d',
                                   'pan2d',
                                   'select2d',
                                   'lasso2d',
                                   'zoomIn2d',
                                   'zoomOut2d',
                                   'toImage',
                                   'resetScale2d']
    }

# --------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1 , maximum-scale=1.9, minimum-scale=.5'}])

server = app.server

########################################################
###################### App Layout ######################
########################################################

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Baltimore Homicides",
                    style={"font-weight":"bold"}),

                  html.H5("Find information about homicides that occured since 2007"),

                  html.Div("Select year, days and hours in which the homicides occurred :",
                           style={
                               "font-weight":"bold",
                               "font-size":"95%",
                               "paddingTop": 20,
                               "paddingBottom": 10,
                                }),

                  dcc.Dropdown(
                        id="slct_year",
                        options=[{
                            "label": f"{x}",
                            "value": x} for x in sorted(df['year'].unique())],
                        multi=False,
                        value=2021,
                        style={
                            'width': "50%",
                            'color': 'black',
                            'font-size':'90%'
                        }),

                  html.Br(),

                  dcc.Checklist(
                      id="select_day",
                      options=df['dayofweek'].sort_values().unique(),
                      value=df['dayofweek'].sort_values().unique(),
                      inline=True,
                      style={
                          'color': 'white',
                          'font-size':'80%'
                      },
                      labelStyle={  # Different padding for the checklist elements
                          'display': 'inline-block',
                          'paddingRight': 10,
                          'paddingLeft': 10,
                          'paddingBottom': 5,
                      },
                  ),

                  html.Br(),

                  dcc.RangeSlider(  # Slider to select the number of hours
                      id="hourSlider",
                      count=1,
                      min=-df['hour'].min(),
                      max=df['hour'].max(),
                      step=1,
                      value=[df['hour'].min(), df['hour'].max()],
                      marks={str(h): str(h) for h in range(df['hour'].min(), df['hour'].max() + 1)}
                  ),

                  html.Div( # Age category
                      '''Age categories :''',
                      style={
                          'paddingTop': 20,
                          'paddingBottom': 10,
                          "font-weight":"bold",
                          "font-size":"95%",
                      }),

                  dcc.Checklist( # Age category check list
                      id="select_age",
                      options=df.sort_values(by='age')['age_category'].unique(),
                      value=df.sort_values(by='age')['age_category'].unique(),
                      inline=True,
                      style={
                          'color': 'white',
                          'font-size':'80%'
                      },
                      labelStyle={  # Different padding for the checklist elements
                          'display': 'inline-block',
                          'paddingRight': 10,
                          'paddingLeft': 10,
                          'paddingBottom': 5,
                      },
                  ),
        ], xl=6, lg=8, md=10, xs=12),

        dbc.Col([ # District
            html.Div(
                "District :", style={  # "text-decoration": "underline",
                    "font-weight": "bold",
                    "font-size":"95%",
                    'paddingTop': 10,
                    'paddingBottom': 10
                }

            ),

            dcc.Checklist( # District check list
                id='check_list',
                options=df['district'].unique(),
                value=df['district'].unique(),
                inline=True,
                labelStyle={  # Different padding for the checklist elements
                  'display': 'inline-block',
                  'paddingRight': 8,
                  'paddingLeft': 8,
                  'paddingBottom': 5,
                },
                style={
                    'width': "100%",
                     'color': 'white',
                     'font-size':'75%'
                }),

            dcc.Graph(
                id='map',
                figure={},
                style={
                    "height": "410px",
                    "width": "100%"
                },
                config=config)
        ], xl=6, lg=8, md=10, xs=12)
    ]),
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Bar plot and Line plot
    dbc.Row([

        # Bar plot
        dbc.Col(dcc.Graph(
            id='bar',
            figure={},
            style={
                "height": "250px",
                "width": "100%"
            },
            config=config
        ), xl=6, lg=8, md=10, xs=12
    ),

        # Line plot
        dbc.Col(
            dcc.Graph('line',
                      figure={},
                      style={
                          "height": "250px",
                          "width": "100%"
                      },
                      config=config
                      ), xl=6, lg=8, md=10, xs=12,
                        style={
                            "maxWidth":"100%",
                            "height":"80%"
                        }
        )
    ])
],fluid = True)

########################################################
###################### Callbacks #######################
########################################################

# --------------------- Map -----------------------------
@app.callback(
    Output('map', 'figure'),
    Input('slct_year', 'value'),
    Input('check_list', 'value'),
    Input('select_day', 'value'),
    Input('hourSlider', 'value'),
    Input('select_age', 'value')
)
def update_graph(year, district, day, time, age):
    hours = [i for i in range(time[0], time[1] + 1)]

    data = df[df['district'].isin(district)]
    data = data[data['dayofweek'].isin(day)]
    data = data[data['year'] == year]
    data = data[data['hour'].isin(hours)]
    data = data[data['age_category'].isin(age)]
    mapbox_access_token = 'pk.eyJ1IjoibGV3aXN3ZXJuZWNrIiwiYSI6ImNsMnMzYnA1OTA5dXgza25yazhhajh3NGsifQ.Z3CrpQqY0Xj_ZH3spiAiYQ'

    fig = px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        color="cause",
        hover_data=df.columns,
        size_max=15,
        zoom=10,
        color_discrete_sequence=colors
    )

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        template='plotly_dark',
        mapbox_style="dark",
        mapbox=dict(
            accesstoken=mapbox_access_token),
        legend_orientation='h',
        legend_valign='middle',
        legend_x=-0.05,
        legend_y=1.15,
        legend_title=None,
        margin=dict(t=60, b=60, l=0, r=0)
    )

    fig.update_xaxes(color='white')
    fig.update_yaxes(color='white')

    return fig

# ------------------- Line plot -------------------------
@app.callback(
    Output('line', 'figure'),
    Input('slct_year', 'value'),
    Input('check_list', 'value'),
    Input('select_day', 'value'),
    Input('hourSlider', 'value'),
    Input('select_age', 'value')
)
def update_graph(year, district, day, time, age):
    hours = [i for i in range(time[0], time[1] + 1)]
    data = df[df['hour'].isin(hours)]
    data = data[data['district'].isin(district)]
    data = data[data['dayofweek'].isin(day)]
    data = data[data['age_category'].isin(age)]
    data = data[(data['year'] <= year) & (data['year'] > (year - 2))].groupby(['year', 'month'])['cause'].agg(
        ['count']).reset_index()

    line = px.line(
        data.sort_values(by='month'),
        x='month',
        y='count',
        color='year'
    )

    line.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title_font_color='white',
        title='Total number of homicide by month',
        title_x=0.5,
        title_y=.99,
        xaxis_title=None,
        yaxis_title=None,
        legend_traceorder="reversed",
        margin=dict(t=50, b=50, l=0, r=0)
    )

    line.update_xaxes(color='white')
    line.update_yaxes(color='white')

    return line

# =============================================================================

# ------------------- Bar plot --------------------------
@app.callback(
    Output('bar', 'figure'),
    Input('slct_year', 'value'),
    Input('check_list', 'value'),
    Input('select_day', 'value'),
    Input('hourSlider', 'value'),
    Input('select_age', 'value')
)
def update_graph(year, district, day, time, age):
    hours = [i for i in range(time[0], time[1] + 1)]
    data = df[df['hour'].isin(hours)]
    data = data[data['dayofweek'].isin(day)]
    data = data[data['district'].isin(district)]
    data = data[data['age_category'].isin(age)]
    data = data[(data['year'] <= year) & (data['year'] > (year - 2))].groupby(['year', 'cause'])['cause'].agg(
        ['count']).reset_index()
    data['year'] = data['year'].astype(str)

    bar = px.bar(
        data.sort_values(by='count', ascending=False),
        x='year',
        y='count',
        color='cause',
        barmode='group',
        text='count',
        color_discrete_sequence=colors
    )

    bar.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        template='plotly_dark',
        title='Total number of homicide by cause',
        title_x=.5,
        #legend_orientation='h',
        #legend_valign='middle',
        #legend_x=-0.05,
        #legend_y=1.2,
        legend_title=None,
        xaxis_title=None,
        margin=dict(t=50, b=50, l=0, r=0)
    )

    return bar

# =============================================================================
# # ------------------- Pie plot --------------------------
#
# @app.callback(
#     Output('pie', 'figure'),
#     Input('slct_year', 'value'),
#     Input('check_list', 'value'),
#     Input('select_day', 'value'),
#     Input('hourSlider', 'value'),
#     Input('select_age', 'value')
# )
#
# def update_graph(year, district, day, time, age):
#
#     hours = [i for i in range(time[0], time[1]+1)]
#     data = df[df['hour'].isin(hours)]
#     data = data[data['district'].isin(district)]
#     data = data[data['year'] == year]
#     data = data[data['age_category'].isin(age)]
#     data = data['cause'].value_counts()
#
#     pie_fig = px.pie(
#         data,
#         values=data.values,
#         names=data.index,
#         color_discrete_sequence=colors
#     )
#
#     pie_fig.update_layout(
#         legend_font_color='white',
#         title='Methods used to commit homicides',
#         title_font_color='white',
#         title_x=.5,
#         title_y=.99,
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(t=0, b=150, l=0, r=0),
#         showlegend=False
#     )
#
#     pie_fig.update_traces(
#         textfont_color='white',
#         textposition='outside',
#         textinfo='percent+label',
#         pull=[0, 0, .1, .2, .4],
#         hole=.4,
#         rotation = 125
# )
#
#     return pie_fig

# ------------------- Run server -----------------------

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)