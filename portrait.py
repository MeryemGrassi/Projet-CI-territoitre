# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:38:54 2020

PARTIE PORTRAIT du dashboard
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

lien_df_portrait = "https://raw.githubusercontent.com/MeryemGrassi/Projet-CI-territoitre/master/data/df_PORTRAIT.csv"
df = pd.read_csv(lien_df_portrait, index_col = 0)

# dictionnaire des départements pour le dropdown #TODO PB avec accents capital avec accent triés à la fin...
dep = df[['CODE_INSEE', 'COMMUNE']]
dep = dep.sort_values(by='COMMUNE')
dep.columns = ['value', 'label']
dep = dep.to_dict(orient = 'records')

 


app = dash.Dash(__name__)

colors = {
    'background': 'white',
    'text': '#0072bc'
}



app.layout = html.Div(id= 'main',
                      style = {
                          'backgroundColor' : 'white'},
                      children = [
                          html.Div(className = 'one_column', 
                                   children = [
                                     html.H1(children = "Carte d'identité Territoriale - REGION SUD",
                                     ),
                             
                                    html.H3(children = "Prototype d'application de l'utilisation des données OpenSource de la région SUD. Projet REGION SUD by WILD CODE SCHOOL", 
                                     ),
                             
                                    dcc.Dropdown(
                                        id = 'cityChoice',
                                        options = dep,
                                        multi=False,
                                        value = 4001,
                                        placeholder="sélectionnez une ville",
                                        style = {
                                            'width' : 500,
                                            'textAlign' : 'left'
                                            }),
                             
                                    html.P(id = 'display_name_of_city')                                                
                                 ]),
        
                            html.Div(className = 'two_columns',
                                     children = [
                                         html.Div(id = 'portrait'),
                                         html.Div(className = 'bloc2', children = [
                                             dcc.Graph(id = 'mapOfCity', figure = {}),
                                             html.Div(id = 'PNR')
                                             ])
                                         ]),
                            
                            html.Div(className = 'one_column',
                                     children = [
                                         dash_table.DataTable(
                                            id='table',
                                            columns=[{"name": i, "id": i} for i in df.columns],
                                            data=df.to_dict('records')),
                                         
                                         dcc.Graph(),
                                         
                                         dash_table.DataTable()
                                         ])
                            ])

# MAJ du portrait
@app.callback(
    Output('portrait', 'children'),
    [Input('cityChoice', 'value')])
def update_output_div(input_value):
    ville = df[df['CODE_INSEE'] == input_value]['COMMUNE'].values[0]
    nbreHabitant = df[df['CODE_INSEE'] == input_value]['POPULATION_2016'].values[0]
    superficie = df[df['CODE_INSEE'] == input_value]['SUPERFICIE_2016'].values[0]
    densitePop = df[df['CODE_INSEE'] == input_value]['DENSITE_POP_2016'].values[0]
    return f"Votre commune : {ville} a {nbreHabitant} habitants, pour une surface totale de {superficie} km² \
            soit une densité de population de {densitePop} habitants par km². (source : INSEE 2016)"


# MAJ nom de la ville
@app.callback(
    Output('display_name_of_city', 'children'),
    [Input('cityChoice', 'value')])
def update_ville(input_value):
    ville = df[df['CODE_INSEE'] == input_value]['COMMUNE']
    return ville


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

