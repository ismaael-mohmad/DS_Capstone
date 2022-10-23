# Import required libraries
from codecs import unicode_escape_decode, unicode_escape_encode, utf_8_encode
from gc import callbacks
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\Ismail\My Drive\Colab Notebooks\IBM DataScience\10 - Capstone Project\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    ],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                     ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df[['Launch Site','class']].groupby('Launch Site').mean().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        data1 = filtered_df[filtered_df['Launch Site']==entered_site]
        data = data1[['class','Launch Site']].groupby('class').count().reset_index()
        fig = px.pie(data, values='Launch Site', 
        names='class', 
        title='Total Success Launches for Site '+entered_site)
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='slider', component_property='value')])
def get_scatter_chart(entered_site, pay_load):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df[(filtered_df['Payload Mass (kg)']>=pay_load[0]) & (filtered_df['Payload Mass (kg)']<=pay_load[1])]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='Correlation between Success and Mass for All Sites')
        return fig
    else:
        data = filtered_df[(filtered_df['Payload Mass (kg)']>=pay_load[0]) & (filtered_df['Payload Mass (kg)']<=pay_load[1]) & (filtered_df['Launch Site']==entered_site)]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='Correlation between Success and Mass for '+entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
