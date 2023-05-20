import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

# Leitura do arquivo CSV
df = pd.read_csv('Space_Corrected.csv')

# Limpeza dos dados para remover valores ausentes
df_cleaned = df.dropna()

# Criação do aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1('Lançamentos Espaciais'),
    
    # Input numérico para selecionar um ano
    dcc.Input(
        id='input-year',
        type='number',
        placeholder='Digite um ano'
    ),
    
    # Gráfico de barras reativo
    dcc.Graph(id='launches-bar-chart'),
    
    # Tabela reativa
    html.H2('Detalhes dos Lançamentos'),
    html.Div(id='launches-table')
])

# Callback para atualizar o gráfico de barras
@app.callback(
    dash.dependencies.Output('launches-bar-chart', 'figure'),
    [dash.dependencies.Input('input-year', 'value')]
)
def update_bar_chart(year):
    if year:
        # Filtrar os lançamentos pelo ano selecionado
        filtered_df = df_cleaned[df_cleaned['Datum'].str.contains(str(year))]
        
        # Contagem dos lançamentos bem sucedidos e mal sucedidos
        success_count = filtered_df[filtered_df['Status Mission'] == 'Success'].shape[0]
        failure_count = filtered_df[filtered_df['Status Mission'] != 'Success'].shape[0]
        
        # Criação do gráfico de barras
        data = [
            go.Bar(x=['Bem Sucedidos', 'Mal Sucedidos'], y=[success_count, failure_count])
        ]
        
        layout = go.Layout(title=f'Lançamentos Espaciais - {year}', yaxis_title='Quantidade')
        
        return {'data': data, 'layout': layout}
    else:
        return {}

# Callback para atualizar a tabela
@app.callback(
    dash.dependencies.Output('launches-table', 'children'),
    [dash.dependencies.Input('input-year', 'value')]
)
def update_table(year):
    if year:
        # Filtrar os lançamentos pelo ano selecionado
        filtered_df = df_cleaned[df_cleaned['Datum'].str.contains(str(year))]
        
        # Criação da tabela HTML
        table = html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in filtered_df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns
                ]) for i in range(len(filtered_df))
            ])
        ])
        
        return table
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
