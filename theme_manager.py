import streamlit as st
import altair as alt

class ThemeManager:
    def __init__(self, theme="dark"):
        """
        Inicializa o gerenciador de temas com validação para evitar valores inválidos.
        Valores aceitos: "light" ou "dark".
        """
        self.valid_themes = ["light", "dark"]
        if theme not in self.valid_themes:
            raise ValueError(f"Tema inválido. Escolha entre {self.valid_themes}.")
        
        self.theme = theme
        self.theme_config = self._load_theme_config()

    def _load_theme_config(self):
        """
        Carrega a configuração de cores para o tema selecionado.
        """
        themes = {
            "light": {
                "background_color": "white",
                "title_font_color": "black",
                "axis_color": "black",
                "label_color": "black",
                "text_color": "black",
                "border_color": "#e0e0e0",
                "sidebar_background_color": "#f8f9fa",
                "sidebar_text_color": "black",
                "button_color": "#ffffff",
                "button_text_color": "black",
                "button_hover_color": "#0056b3"
            },
            "dark": {
                "background_color": "#1e1e1e",
                "title_font_color": "white",
                "axis_color": "white",
                "label_color": "white",
                "text_color": "white",
                "border_color": "#333333",
                "sidebar_background_color": "#2b2b2b",
                "sidebar_text_color": "white",
                "button_color": "#444444",
                "button_text_color": "white",
                "button_hover_color": "#666666"
            }
        }
        return themes[self.theme]

    def _apply_altair_theme(self):
        """
        Configura o tema do Altair com base nas configurações atuais.
        """
        config = self.theme_config
        alt.themes.register('custom_theme', lambda: {
            'config': {
                'background': config['background_color'],
                'title': {'color': config['title_font_color']},
                'axis': {
                    'labelColor': config['axis_color'],
                    'titleColor': config['axis_color'],
                    'gridColor': config['border_color']
                }, 
                'legend': {
                    'labelColor': config['label_color'],
                    'titleColor': config['title_font_color']
                },
                "text": {
                    "color": config["text_color"],
                    "fontSize": 12,
                    "font": "Arial"
                }
            }
        })
        alt.themes.enable('custom_theme')

    def apply_theme(self):
        """
        Aplica o tema ao ambiente do Streamlit e configurações de gráficos.
        """
        # Configurações do Altair
        self._apply_altair_theme()

        # Configurações de cores gerais do Streamlit
        config = self.theme_config
        st.markdown(
            f"""
            <style>
                /* Fundo da página */
                .stApp .stMainBlockContainer {{
                    background-color: {config["background_color"]};
                    color: {config["title_font_color"]};
                }}

                /* Barra lateral */
                section[data-testid="stSidebar"] {{
                    background-color: {config["sidebar_background_color"]};
                    color: {config["sidebar_text_color"]};
                }}

                /* Texto da barra lateral */
                section[data-testid="stSidebar"] .css-1v3fvcr {{
                    color: {config["sidebar_text_color"]};
                }}

                /*texto dentro do bot~ao*/
                .st-f0.st-c6.st-cu.st-dp.st-dq.st-f1.st-f2{{
                    color: {config["button_text_color"]};
                }}

                /*etiquetas dos botões*/
                .st-emotion-cache-ue6h4q.e1y5xkzn3{{
                    color: {config["sidebar_text_color"]};
                }}

                /*Botoes BG*/
                .st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-ct.st-aw.st-bq .st-ak.st-an.st-al.st-am.st-ct.st-cu.st-bq.st-bn.st-cv.st-cw.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-d5.st-d6.st-ar.st-av.st-eu.st-ev.st-ew.st-ex.st-aj.st-ey,
                .st-cd.st-ck.st-cl.st-cs.st-cn.st-co.st-ct.st-aw.st-bq .st-ak.st-an.st-al.st-am.st-ct.st-cu.st-bq.st-bn.st-cv.st-cw.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-d5.st-d6.st-ar.st-av.st-eu.st-ev.st-ew.st-ex.st-aj.st-dc{{
                    background-color: {config["button_color"]};
                    color: {config["label_color"]};
                    border: 1px solid {config["border_color"]};
                }}

                /* Bordas para cada gráfico */
                div.stColumn.st-emotion-cache-1r6slb0.e1f1d6gn3,
                .st-emotion-cache-1wmy9hl.e1f1d6gn1 div div .chart-wrapper {{
                    border: 1px solid {config["border_color"]};
                    border-radius: 5px;
                    padding: 5px;
                }}

                /* Cards */
                .stMetric .st-emotion-cache-17c4ue.e1i5pmia2,
                .stMetric .st-emotion-cache-1wivap2.e1i5pmia3 {{
                    color: {config["label_color"]};
                }}
                
                /* Ajustando o tamanho do canvas (gráfico)*/
                canvas.marks {{
                    width: 100%;
                    max-width: 100%;
                    margin: 0 auto;
                }}

                /*Header*/
                .stAppHeader.st-emotion-cache-12fmjuu.ezrtsby2{{
                    background-color: {config["background_color"]};
                    color: {config["label_color"]};
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
