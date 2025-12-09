import pandas as pd
import plotly.express as px

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_attendances_by_region(df):
    """
    Bar chart of total attendances by Health Region.
    """
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    df['Total_Atendimentos'] = df[conditions].sum(axis=1)
    
    region_data = df.groupby('Região de Saúde')['Total_Atendimentos'].sum().reset_index()
    
    fig = px.bar(region_data, x='Região de Saúde', y='Total_Atendimentos',
                 title='Total de Atendimentos por Região de Saúde',
                 color='Região de Saúde')
    return fig

def plot_attendances_by_establishment(df):
    """
    Bar chart of total attendances by Establishment.
    """
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    df['Total_Atendimentos'] = df[conditions].sum(axis=1)
    
    est_data = df.groupby('Estabelecimento')['Total_Atendimentos'].sum().reset_index().sort_values('Total_Atendimentos', ascending=True)
    
    fig = px.bar(est_data, y='Estabelecimento', x='Total_Atendimentos',
                 title='Total de Atendimentos por Estabelecimento',
                 orientation='h')
    return fig

if __name__ == "__main__":
    file_path = 'atendimentos_aps_brasilia.csv'
    try:
        df = load_data(file_path)
        fig1 = plot_attendances_by_region(df)
        fig1.show()
        fig2 = plot_attendances_by_establishment(df)
        fig2.show()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
