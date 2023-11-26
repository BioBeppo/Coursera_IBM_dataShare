
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

#Read data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#print(spacex_df.head())

# Create a dash app
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard by SWE',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                     {'label': 'All Launch sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder='Select a Launch Site or All',
                                             searchable=True
                                             # style={'width':'60%','padding':'3px','font-size':'20px','text-align-last':'center'}
                                             ),
                                html.Br(),

                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]
                                                ),

                              
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
# First Callback: Success Pie Chart / Individual vs All
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    """
    Generate a pie chart based on the selected launch site.

    Parameters:
    - entered_site (str): The selected launch site.

    Returns:
    - fig (plotly.graph_objs.Figure): The generated pie chart.
    """
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Success Count for All Launch Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', names='class', title=f"Total Success Launches for {entered_site}")
        return fig

# Second Callback: Success Payload Scatter Chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def scatter(entered_site, payload):
    """
    Generate a scatter chart based on the selected launch site and payload range.

    Parameters:
    - entered_site (str): The selected launch site.
    - payload (list): The selected payload range.

    Returns:
    - fig (plotly.graph_objs.Figure): The generated scatter chart.
    """
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Success count on Payload mass for All Sites')
        return fig
    else:
        filtered_df_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_site, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f"Success count on Payload mass for {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


#Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:

#Which site has the largest successful launches?
    #Answer: VAFB SLC-4E
#Which site has the highest launch success rate?
    #Answer: KSC LC-39A
#Which payload range(s) has the highest launch success rate?
    #Answer: 3000-4000 kg
#Which payload range(s) has the lowest launch success rate?
    #Answer: 6000-7000 kg
#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
    #Answer: B5