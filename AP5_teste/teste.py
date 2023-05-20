import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

dados = pd.read_csv('Space_Corrected.csv')

dados['Ano'] = pd.to_datetime(dados['Datum'], format="%a %b %d, %Y %H:%M %Z", errors='coerce').dt.year

por_ano = dados['Ano'].value_counts().sort_index(ascending=False)

por_ano.head(10).plot.bar()

app_ui = ui.page_fixed(
    ui.h2("Lançamentos Espaciais"),
    ui.markdown("""
        Vamos analisar os dados dos lançamentos espaciais desde o primeiro lançamento em 1957 até 2020.
    """),
    ui.panel_main(
        ui.output_table("text_data"),
        ui.output_plot("plot")
    )
)

def server(input, output, session):
    @output
    @render.plot
    def plot():
        fig = plt.figure(figsize=(6,6))
        ax = sns.countplot(y="Status Mission", data=dados, order=dados["Status Mission"].value_counts().index, palette="Set2")
        ax.set_xscale("log")
        ax.axes.set_title("Mission Status vs. Count",fontsize=18)
        ax.set_xlabel("Count",fontsize=16)
        ax.set_ylabel("Mission Status",fontsize=16)
        ax.tick_params(labelsize=12)

        return fig
    
    @output
    @render.table
    def text_data():
        return dados.head()

app = App(app_ui, server=server)
app.run()
