# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Unique site list
sites = []
sites.append({'label': 'All Sites', 'value': 'ALL'})
for s in spacex_df['Launch Site'].unique():
    sites.append({'label': s, 'value': s})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.Div([
            html.Label("Launch Sites:"),
            dcc.Dropdown(
                id = 'site-dropdown',
                options = sites,
                placeholder='Select a Launch Site here',
                value='ALL',
                searchable=True,
                style={'width': '50%', 'padding': '3px', 'font-size': '20px'})]),
        
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
                id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0', 100: '100'},
                value=[1000, 5000]),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart'))
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='class', names='Launch Site',
                     title='Toal Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='Launch Site', names='class',
                     title='Total Success Launches for site {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, entered_payload):
    print(entered_payload[0], entered_payload[1], entered_site)
    # Filter by payload
    df_filter_1 = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]

    if entered_site == 'ALL':
        fig = px.scatter(df_filter_1, 
                     x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = df_filter_1[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation between Payload and Success for the Site {}'.format(entered_site))
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
