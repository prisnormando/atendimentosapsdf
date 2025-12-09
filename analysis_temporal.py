import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data(filepath):
    """Loads the dataset."""
    return pd.read_csv(filepath)

def plot_total_attendances_over_time(df):
    """
    Plots the total number of attendances (sum of all conditions) over time.
    """
    # List of condition columns
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    
    # Create a date column for sorting
    df['Date'] = pd.to_datetime(df['Ano de Competência'].astype(str) + '-' + df['Mês de Competência'].astype(str).str.zfill(2) + '-01')
    
    # Calculate total attendances per row
    df['Total_Atendimentos'] = df[conditions].sum(axis=1)
    
    # Group by Date
    monthly_data = df.groupby('Date')['Total_Atendimentos'].sum().reset_index()
    
    fig = px.line(monthly_data, x='Date', y='Total_Atendimentos', 
                  title='Evolução Temporal do Total de Atendimentos',
                  labels={'Total_Atendimentos': 'Total de Atendimentos', 'Date': 'Data'})
    return fig

def plot_condition_trends(df, selected_conditions=None):
    """
    Plots trends for specific conditions over time.
    """
    if selected_conditions is None:
        selected_conditions = [
            'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
            'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
            'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
            'Usuário de outras drogas'
        ]
        
    df['Date'] = pd.to_datetime(df['Ano de Competência'].astype(str) + '-' + df['Mês de Competência'].astype(str).str.zfill(2) + '-01')
    
    monthly_conditions = df.groupby('Date')[selected_conditions].sum().reset_index()
    
    # Melt for plotly
    melted = monthly_conditions.melt(id_vars=['Date'], value_vars=selected_conditions, 
                                     var_name='Condição', value_name='Atendimentos')
    
    fig = px.line(melted, x='Date', y='Atendimentos', color='Condição',
                  title='Tendência por Condição de Saúde')
    return fig

if __name__ == "__main__":
    # Example usage
    file_path = 'atendimentos_aps_brasilia.csv'
    try:
        df = load_data(file_path)
        print("Dados carregados com sucesso!")
        
        fig1 = plot_total_attendances_over_time(df)
        fig1.show()
        
        fig2 = plot_condition_trends(df)
        fig2.show()
        
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Certifique-se de estar na pasta correta.")
