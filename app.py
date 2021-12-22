import base64, json
from datetime import datetime, date
from collections import Counter
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table as dt
import dash_cytoscape as cyto
import dash_daq as daq
import charts, settings, chat_parser
from chatvisualizer import  dfmain

# Boostrap CSS and font awesome . Option 1) Run from codepen directly Option 2) Copy css file to assets folder and run locally
#####################################################################################################################################
external_stylesheets = ['https://codepen.io/unicorndy/pen/GRJXrvP.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

#Insert your javascript here. In this example, addthis.com has been added to the web app for people to share their webpage
external_scripts = [{
        'type': 'text/javascript', #depends on your application
        'src': 'insert your addthis.com js here',
    }]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts = external_scripts)
app.title = 'Whatsapp Instant Visualization App.'

#for heroku to run correctly
server = app.server

# templates used in graphs
graph_template = "plotly_dark"

#Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'whatsapp_txt':'#3CA4FF',
    'day_text':'#f44336',
    'people_text':'#5A9E6F',
    'highest':'#393939'    
}

#Creating custom style for local use
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
    'width': '33%',
    'padding':'2rem', 
    'margin':'1rem', 
    'boxShadow': '#e3e3e3 4px 4px 2px', 
    'border-radius': '10px', 
    'marginTop': '2rem',
    'display': 'inline-block'
}

#Creating custom style for local use
boxBorderStyle = {
    'borderColor' : '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth':2,
}



df = dfmain

def add_help(inside, tooltip_id=None, hide=True):
    """Wrapper html tag to display help tooltips."""
    style = {'display': 'inline-block', 'margin-right': '5px'}
    visibility = 'hidden' if hide else 'visible'
    try:
        inside.style
    except AttributeError:
        inside.style = {}
    inside.style.update(style)
    result = html.Span([
        inside,
        html.I(className='fas fa-question-circle fa-sm text-muted', id='help-' + tooltip_id, style={'visibility': visibility}),
        dbc.Tooltip(settings.TOOLTIPS[tooltip_id], id='tt-' + tooltip_id, target='help-' + tooltip_id, hide_arrow=hide, style={'visibility': visibility, 'z-index': 9999})
    ])
    return result

## App Layout


app.layout = html.Div([
    html.Div([
        html.Header([
            dbc.Navbar([
                dbc.Row([
                    html.A(
                        dbc.Col(html.Img(src=settings.LOGO, height="45px")), href='/'),
                    dbc.Col(dbc.NavbarBrand(id='navbar-brand', className='ml-2'), style={'margin-left': '10px'})],
                    align='center', no_gutters=True)], fixed='top', className='wa-navbar')]),

        dbc.Card(
            dbc.Col([
                dbc.Row([
                    dcc.DatePickerRange(id='date-picker', display_format='DD/MM/YYYY', clearable=True),
                ], align='center')
            ]), className='card-filter'),

        dbc.Card(
            dbc.CardBody([
                dbc.CardHeader(add_help(html.H5('Time Series Chat'), 'time-series')),
                dcc.Graph(id='chart-1', figure=charts.chart1(df))])),

        dbc.Row([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(add_help(html.H5('Emoji Usage'), 'emoji-activity')),
                        dcc.Graph(id='chart-2', figure=charts.chart2(df))]), className='col-md-4'),
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(add_help(html.H5('Chat Activity by Day of Week'), 'Week-day-activity')),
                    dcc.Graph(id='chart-3', figure=charts.chart3(df))]), className='col-md')]),

    
        
        dbc.Card(
            dbc.CardBody([
                dbc.CardHeader(add_help(html.H5('Top 10 Dominance'), 'dominance')),
                dcc.Graph(id='chart-7', figure=charts.chart7(df))])),

        dbc.Row([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(add_help(html.H5('Top 5 Breakdown by Content'), 'breakdown-content')),
                        dcc.Graph(id='chart-5', figure=charts.chart5(df))]), className='col-md-8'),
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(add_help(html.H5('Top 10 Active Times'), 'active-times')),
                    dcc.Graph(id='chart-6', figure=charts.chart6(df))
                    ]), className='col-md')]),

        dbc.Card(
            dbc.CardBody([
                dbc.CardHeader(add_help(html.H5('Word Cloud'), 'word-cloud')),
                html.Img(id='chart-4', dir = charts.chart4(df), style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
        })])),

        dbc.Card(
            dbc.CardBody([
                dbc.CardHeader(add_help(html.H5('Recruitment Genealogy'), 'recruitment-genealogy')),
                dcc.Graph(id='chart-8', figure=charts.chart8(df))]), className='col-md', style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
        }),

        html.Div(id='counter', style={'visibility': 'hidden'})], className='visualize'),

    # html.Div(footer)
], style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
        }, 
        className='row')



        


if __name__ == '__main__':
    app.run_server(debug=True)