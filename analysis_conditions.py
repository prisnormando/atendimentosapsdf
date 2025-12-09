import pandas as pd
import plotly.express as px

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_conditions_distribution(df):
    """
    Pie chart or Bar chart showing the distribution of different conditions.
    """
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    
    total_per_condition = df[conditions].sum().reset_index()
    total_per_condition.columns = ['Condição', 'Total']
    
    fig = px.pie(total_per_condition, names='Condição', values='Total',
                 title='Distribuição dos Tipos de Atendimento')
    return fig

def plot_heatmap_conditions(df):
    """
    Heatmap of conditions correlation or co-occurrence (simplified as aggregate comparison).
    Since we don't have patient-level data, we can correlate the monthly counts across all establishments.
    """
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    
    corr = df[conditions].corr()
    
    fig = px.imshow(corr, text_auto=True, aspect="auto",
                    title='Correlação entre Volumes de Atendimento por Condição',
                    color_continuous_scale='RdBu_r')
    return fig

if __name__ == "__main__":
    file_path = 'atendimentos_aps_brasilia.csv'
    try:
        df = load_data(file_path)
        fig1 = plot_conditions_distribution(df)
        fig1.show()
        fig2 = plot_heatmap_conditions(df)
        fig2.show()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
