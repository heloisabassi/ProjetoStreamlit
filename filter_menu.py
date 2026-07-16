import streamlit as st
import pandas as pd

class FilterMenu:
    def __init__(self, final_data: pd.DataFrame):
        """
        Inicializa o menu de filtros com o DataFrame fornecido, criando colunas adicionais para Ano, Mês, Primeiro Dia do Mês e Gross Margin.
        """
        self.final_data = final_data.copy()

        # Garantir que a coluna 'Ano-mes' exista no formato datetime
        if "Ano-mes" not in self.final_data.columns:
            self.final_data["Ano-mes"] = pd.to_datetime(self.final_data["Sales Date"])

        # Criar as colunas 'Ano' e 'Mês' com base na coluna 'Ano-mes'
        self.final_data["Ano"] = self.final_data["Ano-mes"].dt.year
        self.final_data["Mês"] = self.final_data["Ano-mes"].dt.month

        # Criar a coluna 'Primeiro Dia do Mês' baseado na coluna 'Ano-mes'
        self.final_data["Primeiro Dia do Mês"] = self.final_data["Ano-mes"].dt.to_period("M").dt.start_time

        # Calcular e adicionar a coluna 'Gross Margin' (diferença entre Receita e Custo)
        if 'Revenue' in self.final_data.columns and 'Total Cost' in self.final_data.columns:
            self.final_data["Gross Margin"] = self.final_data["Revenue"] - self.final_data["Total Cost"]
        else:
            self.final_data["Gross Margin"] = None  # Caso as colunas não existam

    def render(self):
        """
        Renderiza o menu de filtros na barra lateral do Streamlit, aplica os filtros selecionados,
        e retorna os dados filtrados e sumarizados.
        """
        st.sidebar.title("Filtros")

        # Filtro: Ano
        anos_disponiveis = sorted(self.final_data["Ano"].unique().tolist())
        ano_mais_recente = max(anos_disponiveis)

        ano = st.sidebar.selectbox(
            "Selecione o Ano Atual", 
            options=anos_disponiveis,
            index=anos_disponiveis.index(ano_mais_recente)
        )
        
        #apenas para teste
        if not ano:
            ano = 2022

        # Filtro: Mês
        meses_disponiveis = sorted(self.final_data["Mês"].unique().tolist())
        mes = st.sidebar.multiselect(
            "Mês",
            options=meses_disponiveis,
            default=[]
        )

        # Filtro: BL_Desc
        bl_desc = st.sidebar.multiselect(
            "Business Line", 
            options=sorted(self.final_data["BL_DESC"].unique().tolist()),
            default=[]
        )

        # Filtro: Division
        division = st.sidebar.multiselect(
            "Divisão", 
            options=sorted(self.final_data["Division"].unique().tolist()),
            default=[]
        )

        # Filtro: Geo Zone
        geo_zone = st.sidebar.multiselect(
            "Zona Geográfica", 
            options=sorted(self.final_data["GEO ZONE"].unique().tolist()),
            default=[]
        )

        # Filtro: CAT_ID
        cat_id = st.sidebar.multiselect(
            "Categoria", 
            options=sorted(self.final_data["CAT_ID"].unique().tolist()),
            default=[]
        )

        # Filtro: Estado da Planta
        plant_state = st.sidebar.multiselect(
            "Estado da Planta", 
            options=sorted(self.final_data["Plant_State"].unique().tolist()),
            default=[]
        )

        # Filtro: Gerente da Planta
        filtered_managers = self.final_data[ 
            self.final_data["Plant_State"].isin(plant_state)
        ]["Plant Manager"].unique() if plant_state else self.final_data["Plant Manager"].unique()

        plant_manager = st.sidebar.multiselect(
            "Plant Manager", 
            options=sorted(filtered_managers.tolist()),
            default=[]
        )

        # Filtro: Nome da Planta
        filtered_plant_names = self.final_data[ 
            self.final_data["Plant Manager"].isin(plant_manager)
        ]["Plant Name"].unique() if plant_manager else self.final_data["Plant Name"].unique()

        plant_name = st.sidebar.multiselect(
            "Planta", 
            options=sorted(filtered_plant_names.tolist()),
            default=[]
        )

        # Criar dados sumarizados para os cartões (ano atual e anterior)
        anos_para_somar = [ano - 1, ano]  # Ano atual e anterior

        # Aplicar os filtros para dados filtrados e sumarizados
        filtered_data = self.final_data[self.final_data["Ano"].isin(anos_para_somar)].copy()

        if mes:
            filtered_data = filtered_data[filtered_data["Mês"].isin(mes)]

        if bl_desc:
            filtered_data = filtered_data[filtered_data["BL_DESC"].isin(bl_desc)]

        if division:
            filtered_data = filtered_data[filtered_data["Division"].isin(division)]

        if geo_zone:
            filtered_data = filtered_data[filtered_data["GEO ZONE"].isin(geo_zone)]

        if cat_id:
            filtered_data = filtered_data[filtered_data["CAT_ID"].isin(cat_id)]

        if plant_state:
            filtered_data = filtered_data[filtered_data["Plant_State"].isin(plant_state)]

        if plant_manager:
            filtered_data = filtered_data[filtered_data["Plant Manager"].isin(plant_manager)]

        if plant_name:
            filtered_data = filtered_data[filtered_data["Plant Name"].isin(plant_name)]

        
        cards_data = filtered_data.groupby("Ano")[["Revenue", "Total Cost", "Gross Margin"]].sum().reset_index()
        filtered_data = filtered_data[filtered_data["Ano"]== ano]

        return filtered_data, cards_data
    




