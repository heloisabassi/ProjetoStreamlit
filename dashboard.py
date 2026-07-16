import pandas as pd
import streamlit as st
import altair as alt

class Dashboard:
    def __init__(self, data, cards_data):
        """
        Inicializa o Dashboard com o DataFrame filtrado.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("O parâmetro 'data' deve ser um DataFrame do pandas.")
        self.data = data.copy()

        if not isinstance(cards_data, pd.DataFrame):
            raise ValueError("O parâmetro 'data' deve ser um DataFrame do pandas.")
        self.cards_data = cards_data.copy()

    @staticmethod
    def format_dynamic(value):
        """
        Formata o valor de forma dinâmica:
        - Para valores até 999.000, usa 'k' com separador de milhar e sem casas decimais.
        - Para valores a partir de 1.000.000, usa 'mi' com separador de milhar e uma casa decimal.
        """
        if value >= 1_000_000:
            return f"{value / 1_000_000:,.1f} mi"
        elif value >= 1_000:
            return f"{value / 1_000:,.0f} k"
        return f"{value:,.0f}"

    def validate_columns(self, required_columns):
        """
        Valida se as colunas necessárias estão presentes no DataFrame.
        """
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"As colunas necessárias estão faltando no DataFrame: {', '.join(missing_columns)}")

    def plot_bar_chart(self):
        """
        Cria um gráfico de barras de Revenue por Business Line (BL_DESC).
        """
        self.validate_columns(['BL_DESC', 'Revenue'])

        grouped_data = (
            self.data[['BL_DESC', 'Revenue']]
            .dropna(subset=['Revenue'])
            .groupby('BL_DESC', as_index=False)
            .sum()
        )

        # Ordenar os dados do maior para o menor valor de receita (baseado no eixo Y)
        grouped_data = grouped_data.sort_values(by='Revenue', ascending=False)
        grouped_data['RevenueFormatted'] = grouped_data['Revenue'].apply(self.format_dynamic)

        bars = (
            alt.Chart(grouped_data)
            .mark_bar()
            .encode(
                x=alt.X('BL_DESC:N', title=None, axis=alt.Axis(grid=False, labelAngle=0)),
                y=alt.Y('Revenue:Q', title=None, axis=alt.Axis(grid=False, tickCount=0)),
                tooltip=['BL_DESC', 'RevenueFormatted']
            )
            .properties(
                title="Revenue by Business Line",
                # width=400,
                # height=400
            )
        )
        labels = (
            alt.Chart(grouped_data)
            .mark_text(dy=-10)
            .encode(
                x=alt.X('BL_DESC:N'),
                y=alt.Y('Revenue:Q'),
                text='RevenueFormatted:N'
            )
        )
        return bars + labels

    def plot_division_chart(self):
        """
        Cria um gráfico de colunas de Revenue por divisão (Division).
        """
        self.validate_columns(['Division', 'Revenue'])

        grouped_data = (
            self.data[['Division', 'Revenue']]
            .dropna(subset=['Revenue'])
            .groupby('Division', as_index=False)
            .sum()
        )
        # Ordenar os dados do maior para o menor valor de receita (baseado no eixo Y)
        grouped_data = grouped_data.sort_values(by='Revenue', ascending=False)
        grouped_data['RevenueFormatted'] = grouped_data['Revenue'].apply(self.format_dynamic)

        bars = (
            alt.Chart(grouped_data)
            .mark_bar()
            .encode(
                x=alt.X('Division:N', title=None, axis=alt.Axis(grid=False, labelAngle=0)),
                y=alt.Y('Revenue:Q', title=None, axis=alt.Axis(grid=False, tickCount=0)),
                tooltip=['Division', 'RevenueFormatted']
            )
            .properties(
                title="Revenue by Division",
                # width=400,
                # height=400
            )
        )
        labels = (
            alt.Chart(grouped_data)
            .mark_text(dy=-10)
            .encode(
                x=alt.X('Division:N'),
                y=alt.Y('Revenue:Q'),
                text='RevenueFormatted:N'
            )
        )
        return bars + labels

    def plot_plant_chart(self):
        """
        Cria um gráfico de colunas de Revenue por planta (Plant), ordenando pelo valor de Revenue.
        """
        self.validate_columns(['Plant Name', 'Revenue'])

        # Agrupar os dados por planta e somar a receita
        grouped_data = (
            self.data[['Plant Name', 'Revenue']]
            .dropna(subset=['Revenue'])
            .groupby('Plant Name', as_index=False)
            .sum()
        )

        # Ordenar os dados pelo valor de Revenue
        grouped_data = grouped_data.sort_values(by='Revenue', ascending=False)

        # Formatar a coluna de receita
        grouped_data['RevenueFormatted'] = grouped_data['Revenue'].apply(self.format_dynamic)

        # Criar o gráfico de barras com ordenação
        bars = (
            alt.Chart(grouped_data)
            .mark_bar()
            .encode(
                x=alt.X(
                    'Plant Name:N',
                    title=None,
                    axis=alt.Axis(grid=False, labelAngle=0),
                    sort=alt.EncodingSortField(
                        field='Revenue',  # Campo pelo qual ordenar
                        op='sum',         # Operação de agregação
                        order='descending'  # Ordem decrescente
                    )
                ),
                y=alt.Y(
                    'Revenue:Q',
                    title=None,
                    axis=alt.Axis(grid=False, tickCount=0)
                ),
                tooltip=['Plant Name', 'RevenueFormatted']
            )
            .properties(
                title="Revenue by Plant"
            )
        )

        # Adicionar os rótulos de receita
        labels = (
            alt.Chart(grouped_data)
            .mark_text(dy=-10)
            .encode(
                x=alt.X('Plant Name:N'),
                y=alt.Y('Revenue:Q'),
                text='RevenueFormatted:N'
            )
        )

        return bars + labels


    
    def plot_sales_by_month(self):
        """
        Cria um gráfico de área em camadas para mostrar as receitas por mês,
        com a área sob cada linha preenchida, sem empilhamento.
        """
        self.validate_columns(['Primeiro Dia do Mês', 'Revenue', 'BL_DESC'])

        # Garantir que 'Primeiro Dia do Mês' esteja no formato datetime
        self.data['Primeiro Dia do Mês'] = pd.to_datetime(self.data['Primeiro Dia do Mês'])

        # Agrupar os dados por 'Primeiro Dia do Mês' e 'BL_DESC', somando as receitas
        grouped_data = (
            self.data.groupby(['Primeiro Dia do Mês', 'BL_DESC'], as_index=False)['Revenue'].sum()
        )

        # Criar o gráfico de área em camadas
        area_chart = (
            alt.Chart(grouped_data)
            .mark_area(opacity=0.6, line=True)  # Define a transparência e exibe a linha
            .encode(
                x=alt.X(
                    'Primeiro Dia do Mês:T',
                    axis=alt.Axis(
                        format='%b %Y',
                        labelAngle=0,  # Etiquetas do eixo X na horizontal
                        labelFontSize=12
                    ),
                    title=None  # Remove o título do eixo x
                ),
                y=alt.Y(
                    'Revenue:Q',
                    axis=alt.Axis(
                        format='$.2s',
                        labelFontSize=12,
                        labels=False  # Remove os valores dos rótulos do eixo Y
                    ),
                    title=None  # Remove o título do eixo y
                ),
                color=alt.Color(
                    'BL_DESC:N',
                    title='Business Line',
                    scale=alt.Scale(scheme='category10')  # Define um esquema de cores
                ),
                tooltip=[ 
                    alt.Tooltip('Primeiro Dia do Mês:T', title='Mês', format='%b %Y'),
                    alt.Tooltip('BL_DESC:N', title='Business Line'),
                    alt.Tooltip('Revenue:Q', title='Receita', format='$.0f')
                ]
            )
            .properties(
                title="Revenue by Month",
                # width=700,
                # height=400
            )
            .configure_axis(
                grid=False
            )
            .configure_legend(
                title=None,
                titleFontSize=0,
                labelFontSize=12,
                orient='top'
            )
        )
        return area_chart


    def calculate_annual_variation(self, metric):
        """
        Calcula a variação anual de uma métrica (por exemplo, Receita, Custo ou Margem).
        
        Parâmetros:
        - metric: o nome da coluna para a qual calcular a variação anual.
        
        Retorna:
        - A variação anual em percentual.
        """
        # Verificar se o DataFrame contém os dados necessários
        if metric not in self.cards_data.columns:
            st.error(f"Coluna '{metric}' não encontrada no DataFrame.")
            return None
        
        # Agrupar os dados por ano e somar os valores da métrica
        yearly_data = self.cards_data.groupby('Ano').agg({metric: 'sum'}).reset_index()
        
        # Ordenar os dados por ano
        yearly_data = yearly_data.sort_values('Ano')
        
        # Garantir que há pelo menos dois anos de dados
        if len(yearly_data) < 2:
            st.warning("Não há dados suficientes para calcular a variação anual.")
            return None
        
        # Calcular a variação entre o último ano e o ano anterior
        last_year_value = yearly_data.iloc[-1][metric]
        previous_year_value = yearly_data.iloc[-2][metric]
        
        # Evitar divisão por zero
        if previous_year_value == 0:
            return None
        
        # Calcular a variação percentual
        variation = ((last_year_value - previous_year_value) / previous_year_value) * 100
        
        return variation