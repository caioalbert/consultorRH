"""
Dashboard - CI/CD com Apache ECharts
Visualizações de métricas de CI/CD
"""
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd


def render_cicd_dashboard(df: pd.DataFrame):
    """
    Renderiza o dashboard de CI/CD com ECharts
    
    Args:
        df: DataFrame com os dados do inventário
    """
    # Paleta de cores Fitbank
    fitbank_colors = ["#323751", "#5F82A6", "#FCD669", "#4A5F7A", "#7B9BB8", "#FFE399", "#3D4A63", "#6A8DB5"]
    
    # 4 gráficos em 1 linha
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Ferramenta de Versionamento**")
        version_counts = df['Ferramenta_Versionamento'].value_counts()
        if len(version_counts) == 0:
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
                    "radius": "65%",
                    "center": ["50%", "50%"],
                    "data": [
                        {"value": int(v), "name": k, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, (k, v) in enumerate(version_counts.items())
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.2)"
                        }
                    },
                    "label": {
                        "fontSize": 11,
                        "color": "#323751",
                        "fontWeight": "bold",
                        "formatter": "{b}: {c}"
                    }
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_versionamento", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_versionamento:
                st.session_state.filter_versionamento = clicked
    
    with col2:
        st.markdown("**Tipo de Pipeline**")
        pipeline_counts = df['Tipo_Pipeline'].value_counts()
        if len(pipeline_counts) == 0:
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
                    "data": pipeline_counts.index.tolist(),
                    "axisLabel": {"fontSize": 11, "color": "#5A6C7D"},
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
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, (k, v) in enumerate(pipeline_counts.items())
                    ],
                    "type": "bar",
                    "label": {
                        "show": True,
                        "position": "top",
                        "fontSize": 12,
                        "fontWeight": "bold",
                        "color": "#323751"
                    },
                    "barWidth": "50%",
                    "itemStyle": {"borderRadius": [4, 4, 0, 0]}
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_pipeline", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_tipo_pipeline:
                st.session_state.filter_tipo_pipeline = clicked
    
    with col3:
        st.markdown("**Aplicações por Versão**")
        versao_counts = df['Versao'].value_counts().head(10)
        if len(versao_counts) == 0:
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
                    "data": versao_counts.index.tolist(),
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
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, v in enumerate(versao_counts.values.tolist())
                    ],
                    "type": "bar",
                    "itemStyle": {"borderRadius": [4, 4, 0, 0]},
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
            clicked = st_echarts(options=option, height="280px", key="chart_versao", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_versao:
                st.session_state.filter_versao = clicked
    
    with col4:
        st.markdown("**Aplicações por Hospedagem**")
        hosp_counts = df['Hospedagem'].value_counts()
        if len(hosp_counts) == 0:
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
                    "data": hosp_counts.index.tolist(),
                    "axisLabel": {"rotate": 30, "fontSize": 10, "color": "#5A6C7D"},
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
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, v in enumerate(hosp_counts.values.tolist())
                    ],
                    "type": "bar",
                    "itemStyle": {"borderRadius": [4, 4, 0, 0]},
                    "label": {
                        "show": True,
                        "position": "top",
                        "fontSize": 11,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "50%"
                }]
            }
            events = {
                "click": "function(params) { return params.name }"
            }
            clicked = st_echarts(options=option, height="280px", key="chart_hospedagem", events=events)
            if clicked and clicked != "" and clicked != st.session_state.filter_hospedagem:
                st.session_state.filter_hospedagem = clicked
