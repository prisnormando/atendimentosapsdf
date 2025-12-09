import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def load_data(filepath):
    return pd.read_csv(filepath)

def forecast_total_attendances(df, periods=12):
    """
    Forecasts total attendances for the next 'periods' months using Holt-Winters.
    """
    conditions = [
        'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
        'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
        'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
        'Usuário de outras drogas'
    ]
    
    # Prepare time series
    df['Date'] = pd.to_datetime(df['Ano de Competência'].astype(str) + '-' + df['Mês de Competência'].astype(str).str.zfill(2) + '-01')
    df['Total_Atendimentos'] = df[conditions].sum(axis=1)
    
    # Aggregate by month
    monthly_ts = df.groupby('Date')['Total_Atendimentos'].sum()
    
    # Train model
    # Using 'add' trend and seasonality if enough data, otherwise simple
    try:
        model = ExponentialSmoothing(monthly_ts, trend='add', seasonal='add', seasonal_periods=12).fit()
    except:
        # Fallback for less data or errors
        model = ExponentialSmoothing(monthly_ts, trend='add').fit()
        
    forecast = model.forecast(periods)
    
    # Plotting
    fig = go.Figure()
    
    # Historical Data
    fig.add_trace(go.Scatter(x=monthly_ts.index, y=monthly_ts.values, mode='lines', name='Histórico'))
    
    # Forecast Data
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast.values, mode='lines+markers', name='Previsão', line=dict(dash='dash', color='red')))
    
    fig.update_layout(title=f'Previsão de Atendimentos Totais (Próximos {periods} Meses)',
                      xaxis_title='Data', yaxis_title='Total de Atendimentos')
    
    return fig

if __name__ == "__main__":
    file_path = 'atendimentos_aps_brasilia.csv'
    try:
        df = load_data(file_path)
        fig = forecast_total_attendances(df)
        fig.show()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
