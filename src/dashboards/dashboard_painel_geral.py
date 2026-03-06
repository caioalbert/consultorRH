"""
Dashboard - Painel Geral com Apache ECharts
Visualizações gerais do inventário de aplicações
"""
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd


def render_painel_geral(df: pd.DataFrame):
    """
    Renderiza o dashboard do Painel Geral com ECharts
    
    Args:
        df: DataFrame com os dados do inventário
    """
    # Paleta de cores Fitbank
    fitbank_colors = ["#323751", "#5F82A6", "#FCD669", "#4A5F7A", "#7B9BB8", "#FFE399", "#3D4A63", "#6A8DB5"]
    
    # 4 gráficos em 1 linha
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Aplicações por Produto**")
        produto_counts = df['Produto'].value_counts().head(10)
        if len(produto_counts) == 0:
            st.info("⚠️ Nenhum dado disponível")
        else:
            option = {
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "grid": {
                    "left": "5%",
                    "right": "5%",
                    "bottom": "3%",
                    "top": "3%",
                    "containLabel": True,
                    "show": False
                },
                "xAxis": {
                    "type": "category",
                    "data": produto_counts.index.tolist(),
                    "axisLabel": {
                        "rotate": 45,
                        "fontSize": 9,
                        "color": "#5A6C7D"
                    },
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "splitLine": {"show": False}
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {"fontSize": 10, "color": "#5A6C7D"},
                    "axisLine": {"show": False},
                    "splitLine": {"show": False}
                },
                "series": [{
                    "data": produto_counts.values.tolist(),
                    "type": "bar",
                    "itemStyle": {"color": "#5F82A6", "borderRadius": [4, 4, 0, 0]},
                    "label": {
                        "show": True,
                        "position": "top",
                        "fontSize": 10,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "60%"
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_produto", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_produto:
                st.session_state.filter_produto = clicked
    
    with col2:
        st.markdown("**Aplicações por Ambiente**")
        ambiente_counts = df['Ambiente'].value_counts()
        if len(ambiente_counts) == 0:
            st.info("⚠️ Nenhum dado disponível")
        else:
            option = {
                "tooltip": {
                    "trigger": "item",
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "legend": {"show": False},
                "series": [{
                    "type": "pie",
                    "radius": ["45%", "75%"],
                    "avoidLabelOverlap": False,
                    "label": {
                        "show": True,
                        "fontSize": 11,
                        "color": "#323751",
                        "fontWeight": "bold",
                        "formatter": "{b}: {c}"
                    },
                    "labelLine": {"show": True, "lineStyle": {"color": "#5F82A6"}},
                    "data": [
                        {"value": int(v), "name": k, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, (k, v) in enumerate(ambiente_counts.items())
                    ]
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_ambiente", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_ambiente:
                st.session_state.filter_ambiente = clicked
    
    with col3:
        st.markdown("**Aplicações por Tipo**")
        tipo_counts = df['Tipo_Aplicacao'].value_counts()
        if len(tipo_counts) == 0:
            st.info("⚠️ Nenhum dado disponível")
        else:
            option = {
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "grid": {
                    "left": "5%",
                    "right": "5%",
                    "bottom": "3%",
                    "top": "3%",
                    "containLabel": True,
                    "show": False
                },
                "xAxis": {
                    "type": "category",
                    "data": tipo_counts.index.tolist(),
                    "axisLabel": {"fontSize": 9, "color": "#5A6C7D", "rotate": 30},
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "splitLine": {"show": False}
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {"fontSize": 10, "color": "#5A6C7D"},
                    "axisLine": {"show": False},
                    "splitLine": {"show": False}
                },
                "series": [{
                    "data": tipo_counts.values.tolist(),
                    "type": "bar",
                    "itemStyle": {"color": "#FCD669", "borderRadius": [4, 4, 0, 0]},
                    "label": {
                        "show": True,
                        "position": "top",
                        "fontSize": 10,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "60%"
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_tipo", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_tipo_aplicacao:
                st.session_state.filter_tipo_aplicacao = clicked
    
    with col4:
        st.markdown("**Aplicações por Framework**")
        framework_counts = df['Framework'].value_counts().head(8)
        if len(framework_counts) == 0:
            st.info("⚠️ Nenhum dado disponível")
        else:
            option = {
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "grid": {
                    "left": "5%",
                    "right": "5%",
                    "bottom": "3%",
                    "top": "3%",
                    "containLabel": True,
                    "show": False
                },
                "xAxis": {
                    "type": "category",
                    "data": framework_counts.index.tolist(),
                    "axisLabel": {"fontSize": 9, "color": "#5A6C7D", "rotate": 30},
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "splitLine": {"show": False}
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {"fontSize": 10, "color": "#5A6C7D"},
                    "axisLine": {"show": False},
                    "splitLine": {"show": False}
                },
                "series": [{
                    "data": framework_counts.values.tolist(),
                    "type": "bar",
                    "itemStyle": {"color": "#323751", "borderRadius": [4, 4, 0, 0]},
                    "label": {
                        "show": True,
                        "position": "top",
                        "fontSize": 10,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "50%"
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_framework", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_framework:
                st.session_state.filter_framework = clicked
