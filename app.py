import streamlit as st
from theme_manager import ThemeManager  # Classe para carregar o tema
from data_loader import DataLoader  # Classe para carregar os dados
from filter_menu import FilterMenu  # Classe para renderizar o menu de filtros
from dashboard import Dashboard  # Classe para gerar os gráficos do dashboard

# Configuração da página deve ser o primeiro comando Streamlit
st.set_page_config(
    page_title="BF LUBS - Lubrificantes e Aditivos",
    page_icon="📊",  
    layout="wide"
)

# Inicializar o gerenciador de temas
theme_manager = ThemeManager(theme="dark")  # Escolha "dark" ou "light"
theme_manager.apply_theme()  # Aplica o tema escolhido

# Inicialização das classes e carregamento de dados
try:
    st.title("Sales Overview")

    # Carregando os dados
    data_loader = DataLoader('Dataset')
    final_data = data_loader.final_data

    if final_data.empty:
        st.error("O dataset está vazio. Verifique os dados fornecidos.")
        st.stop()

    # Renderização do menu de filtros
    filter_menu = FilterMenu(final_data)
    filtered_data, cards_data = filter_menu.render()

    if filtered_data.empty:
        st.warning("Nenhum dado foi encontrado após aplicar os filtros. Ajuste os filtros e tente novamente.")
        st.stop()

    # Inicialização do Dashboard
    dashboard = Dashboard(filtered_data, cards_data)

    # Gerando os gráficos
    bar_chart = dashboard.plot_bar_chart()
    division_chart = dashboard.plot_division_chart()
    plant_chart = dashboard.plot_plant_chart()
    monthly_sales = dashboard.plot_sales_by_month()

    # Calculando a variação anual para cada métrica
    revenue_variation = dashboard.calculate_annual_variation('Revenue')
    total_cost_variation = dashboard.calculate_annual_variation('Total Cost')
    gross_margin_variation = dashboard.calculate_annual_variation('Gross Margin')

    # Exibindo os cards no Streamlit na primeira linha (superior)
    col1, col2, col3 = st.columns(3)  # Dividindo em 3 colunas

    with col1:
        st.metric(label="Variação de Revenue (%)", value=f"{revenue_variation:.2f}%" if revenue_variation is not None else "N/A")

    with col2:
        st.metric(label="Variação de Total Cost (%)", value=f"{total_cost_variation:.2f}%" if total_cost_variation is not None else "N/A")

    with col3:
        st.metric(label="Variação de Gross Margin (%)", value=f"{gross_margin_variation:.2f}%" if gross_margin_variation is not None else "N/A")

    # Exibindo os gráficos no Streamlit na segunda linha (inferior)
    col1, col2 = st.columns(2)  # Dividindo em 2 colunas para os gráficos

    with col1:
        st.altair_chart(bar_chart, use_container_width=True)
        st.altair_chart(division_chart, use_container_width=True)

    with col2:
        st.altair_chart(plant_chart, use_container_width=True)
        st.altair_chart(monthly_sales, use_container_width=True)
    

except Exception as e:
    st.error(f"Ocorreu um erro: {e}")
