import streamlit as st
import pandas as pd
import analysis_temporal
import analysis_geo_establishment
import analysis_conditions
import analysis_forecast

# Page Config
st.set_page_config(page_title="Análise APS Brasília", layout="wide")

# Title
st.title("📊 Painel de Análise de Dados APS - Brasília")
st.markdown("Este painel permite explorar os dados de atendimentos individuais na Atenção Primária à Saúde.")

# Load Data
@st.cache_data
def get_data():
    try:
        return pd.read_csv('atendimentos_aps_brasilia.csv')
    except FileNotFoundError:
        st.error("Arquivo 'atendimentos_aps_brasilia.csv' não encontrado.")
        return None

df = get_data()

if df is not None:
    # Sidebar
    st.sidebar.header("Navegação")
    page = st.sidebar.radio("Escolha a Análise:", 
                            ["Visão Geral", "Análise Temporal", "Geografia e Estabelecimentos", "Condições de Saúde", "Previsão"])

    # Global Filters (Optional, applied to dataframe copy)
    st.sidebar.header("Filtros Globais")
    
    all_years = sorted(df['Ano de Competência'].unique())
    selected_years = st.sidebar.multiselect("Selecione os Anos:", all_years, default=all_years)
    
    all_regions = sorted(df['Região de Saúde'].unique())
    selected_regions = st.sidebar.multiselect("Selecione as Regiões:", all_regions, default=all_regions)

    # Apply filters
    df_filtered = df[df['Ano de Competência'].isin(selected_years) & df['Região de Saúde'].isin(selected_regions)]

    if df_filtered.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
    else:
        # Pages
        if page == "Visão Geral":
            st.header("Visão Geral dos Dados")
            
            # KPI Cards
            col1, col2, col3 = st.columns(3)
            
            conditions = [
                'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
                'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
                'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
                'Usuário de outras drogas'
            ]
            total_attendances = df_filtered[conditions].sum().sum()
            total_establishments = df_filtered['Estabelecimento'].nunique()
            total_months = df_filtered.groupby(['Ano de Competência', 'Mês de Competência']).ngroups
            
            col1.metric("Total de Atendimentos", f"{total_attendances:,.0f}")
            col2.metric("Estabelecimentos Ativos", total_establishments)
            col3.metric("Meses Monitorados", total_months)
            
            st.subheader("Amostra dos Dados")
            st.dataframe(df_filtered.head())
            
            st.markdown("---")
            st.markdown("### Resumo da Documentação")
            st.markdown("""
            - **Fonte**: Painel Power BI "Atendimentos Individuais na APS".
            - **Período**: 2019 a 2025.
            - **Cobertura**: 20 UBS em 3 Regiões de Saúde.
            """)

        elif page == "Análise Temporal":
            st.header("📈 Análise Temporal")
            
            st.subheader("Evolução Total")
            fig_total = analysis_temporal.plot_total_attendances_over_time(df_filtered)
            st.plotly_chart(fig_total, use_container_width=True)
            
            st.subheader("Tendências por Condição")
            conditions = [
                'Asma', 'DPOC', 'Pré-natal', 'Puericultura', 'Puerpério (até 42 dias)',
                'Rast. risco cardiovascular', 'Reabilitação', 'Saúde mental',
                'Saúde sexual e reprodutiva', 'Tabagismo', 'Usuário de álcool',
                'Usuário de outras drogas'
            ]
            selected_conditions = st.multiselect("Selecione as condições para visualizar:", conditions, default=conditions[:3])
            
            if selected_conditions:
                fig_trends = analysis_temporal.plot_condition_trends(df_filtered, selected_conditions)
                st.plotly_chart(fig_trends, use_container_width=True)
            else:
                st.info("Selecione pelo menos uma condição.")

        elif page == "Geografia e Estabelecimentos":
            st.header("🗺️ Geografia e Estabelecimentos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Por Região")
                fig_region = analysis_geo_establishment.plot_attendances_by_region(df_filtered)
                st.plotly_chart(fig_region, use_container_width=True)
                
            with col2:
                st.subheader("Por Estabelecimento")
                fig_est = analysis_geo_establishment.plot_attendances_by_establishment(df_filtered)
                st.plotly_chart(fig_est, use_container_width=True)

        elif page == "Condições de Saúde":
            st.header("🩺 Condições de Saúde")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribuição")
                fig_pie = analysis_conditions.plot_conditions_distribution(df_filtered)
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with col2:
                st.subheader("Correlação")
                fig_corr = analysis_conditions.plot_heatmap_conditions(df_filtered)
                st.plotly_chart(fig_corr, use_container_width=True)

        elif page == "Previsão":
            st.header("🔮 Previsão de Demanda")
            st.markdown("Previsão baseada no histórico total de atendimentos usando o modelo Holt-Winters.")
            
            periods = st.slider("Meses para prever:", min_value=1, max_value=24, value=12)
            
            # Note: Forecasting usually needs the full time series structure, so we might want to use the unfiltered df 
            # or be careful if the filtered df has gaps. For simplicity, we use df_filtered but warn if it's too small.
            if len(df_filtered) < 24:
                st.warning("Dados insuficientes para uma previsão confiável com os filtros atuais. Tente selecionar mais anos/regiões.")
            else:
                fig_forecast = analysis_forecast.forecast_total_attendances(df_filtered, periods)
                st.plotly_chart(fig_forecast, use_container_width=True)

else:
    st.stop()
