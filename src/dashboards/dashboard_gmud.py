"""
Dashboard de GMUDs (Gestão de Mudanças)
Visualização e gestão de GMUDs realizadas
"""
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from datetime import datetime
import os

def render_gmud_dashboard(df_gmud):
    """
    Renderiza o dashboard de GMUDs
    
    Args:
        df_gmud: DataFrame com dados de GMUDs
    """
    st.markdown('<div class="main-header">GMUDs - Gestão de Mudanças</div>', unsafe_allow_html=True)
    
    # Carregar inventário de aplicações para obter produtos
    try:
        inv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'inventario_aplicacoes.csv')
        df_inventario = pd.read_csv(inv_path, encoding='utf-8')
        # Criar mapeamento Nome_Aplicacao -> Produto
        app_to_produto = dict(zip(df_inventario['Nome_Aplicacao'], df_inventario['Produto']))
    except:
        app_to_produto = {}
    
    if df_gmud is None or len(df_gmud) == 0:
        st.warning("Nenhum dado de GMUD encontrado.")
        return
    
    # Paleta de cores Fitbank
    fitbank_colors = ["#323751", "#5F82A6", "#FCD669", "#4A5F7A", "#7B9BB8", "#FFE399", "#3D4A63", "#6A8DB5"]
    
    # Métricas gerais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_gmuds = len(df_gmud)
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-box-label">Total de GMUDs</div>
            <div class="metric-box-value">{total_gmuds}</div>
            <div class="metric-box-subtitle">Registradas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        ambientes = df_gmud['Ambiente'].nunique()
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-box-label">Ambientes</div>
            <div class="metric-box-value">{ambientes}</div>
            <div class="metric-box-subtitle">Diferentes</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        aplicacoes = df_gmud['Nome_Aplicacao'].nunique()
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-box-label">Aplicações</div>
            <div class="metric-box-value">{aplicacoes}</div>
            <div class="metric-box-subtitle">Impactadas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        responsaveis = df_gmud['Responsavel'].nunique()
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-box-label">Responsáveis</div>
            <div class="metric-box-value">{responsaveis}</div>
            <div class="metric-box-subtitle">Envolvidos</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        prod_count = len(df_gmud[df_gmud['Ambiente'] == 'Produção'])
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-box-label">Produção</div>
            <div class="metric-box-value">{prod_count}</div>
            <div class="metric-box-subtitle">GMUDs em PROD</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filtros
    st.markdown("### Filtros")
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
    
    with col_f1:
        ambientes_list = ['Todos'] + sorted(df_gmud['Ambiente'].unique().tolist())
        selected_ambiente = st.selectbox("Ambiente", ambientes_list, key="gmud_ambiente")
    
    with col_f2:
        aplicacoes_list = ['Todos'] + sorted(df_gmud['Nome_Aplicacao'].unique().tolist())
        selected_aplicacao = st.selectbox("Aplicação", aplicacoes_list, key="gmud_aplicacao")
    
    with col_f3:
        responsaveis_list = ['Todos'] + sorted(df_gmud['Responsavel'].unique().tolist())
        selected_responsavel = st.selectbox("Responsável", responsaveis_list, key="gmud_responsavel")
    
    with col_f4:
        riscos_list = ['Todos'] + sorted(df_gmud['Risco_Operacao'].dropna().unique().tolist())
        selected_risco = st.selectbox("Risco", riscos_list, key="gmud_risco")
    
    with col_f5:
        locais_list = ['Todos'] + sorted(df_gmud['Local_Implantacao'].dropna().unique().tolist())
        selected_local = st.selectbox("Local Implantação", locais_list, key="gmud_local")
    
    # Aplicar filtros
    filtered_df = df_gmud.copy()
    
    if selected_ambiente != 'Todos':
        filtered_df = filtered_df[filtered_df['Ambiente'] == selected_ambiente]
    
    if selected_aplicacao != 'Todos':
        filtered_df = filtered_df[filtered_df['Nome_Aplicacao'] == selected_aplicacao]
    
    if selected_responsavel != 'Todos':
        filtered_df = filtered_df[filtered_df['Responsavel'] == selected_responsavel]
    
    if selected_risco != 'Todos':
        filtered_df = filtered_df[filtered_df['Risco_Operacao'] == selected_risco]
    
    if selected_local != 'Todos':
        filtered_df = filtered_df[filtered_df['Local_Implantacao'] == selected_local]
    
    # Filtrar últimos 30 dias para os gráficos
    if 'Data_Prevista' in filtered_df.columns:
        filtered_df['Data_Prevista_dt'] = pd.to_datetime(filtered_df['Data_Prevista'], errors='coerce')
        data_limite = pd.Timestamp.now() - pd.Timedelta(days=30)
        filtered_df_30dias = filtered_df[filtered_df['Data_Prevista_dt'] >= data_limite].copy()
    else:
        filtered_df_30dias = filtered_df.copy()
    
    if len(filtered_df) != len(df_gmud):
        st.info(f"Exibindo {len(filtered_df)} de {len(df_gmud)} GMUDs | Últimos 30 dias: {len(filtered_df_30dias)} GMUDs")
    
    st.markdown("---")
    
    # Expander 1: Distribuição de GMUDs
    with st.expander("Distribuição de GMUDs (30d)", expanded=True):
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    
    with col_g1:
        st.markdown("**GMUDs por Ambiente (30d)**")
        env_counts = filtered_df_30dias['Ambiente'].value_counts().head(10)
        if len(env_counts) > 0:
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
                    "data": env_counts.index.tolist(),
                    "axisLabel": {
                        "rotate": 45,
                        "fontSize": 9,
                        "color": "#323751",
                        "interval": 0
                    },
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "axisTick": {"show": False}
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 9,
                        "color": "#323751"
                    },
                    "axisLine": {"show": False},
                    "splitLine": {
                        "lineStyle": {
                            "color": "#D1D9E6",
                            "type": "dashed"
                        }
                    }
                },
                "series": [{
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, v in enumerate(env_counts.values.tolist())
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
                    "barWidth": "60%"
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_ambiente")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    with col_g2:
        st.markdown("**GMUDs por Risco (30d)**")
        risk_counts = filtered_df_30dias['Risco_Operacao'].value_counts()
        if len(risk_counts) > 0:
            option = {
                "tooltip": {
                    "trigger": "item",
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "legend": {
                    "orient": "vertical",
                    "right": "5%",
                    "top": "center",
                    "textStyle": {
                        "fontSize": 9,
                        "color": "#323751"
                    }
                },
                "series": [{
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "center": ["35%", "50%"],
                    "avoidLabelOverlap": True,
                    "itemStyle": {
                        "borderRadius": 4,
                        "borderColor": "#fff",
                        "borderWidth": 2
                    },
                    "label": {
                        "show": False
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": 11,
                            "fontWeight": "bold",
                            "color": "#323751"
                        }
                    },
                    "labelLine": {"show": False},
                    "data": [
                        {"value": int(risk_counts.get(cat, 0)), "name": cat, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, cat in enumerate(risk_counts.index)
                    ]
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_risco")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    with col_g3:
        st.markdown("**Top 10 Aplicações (30d)**")
        app_counts = filtered_df_30dias['Nome_Aplicacao'].value_counts().head(10)
        if len(app_counts) > 0:
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
                    "containLabel": True
                },
                "yAxis": {
                    "type": "category",
                    "data": app_counts.index.tolist(),
                    "axisLabel": {
                        "fontSize": 8,
                        "color": "#323751"
                    },
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "axisTick": {"show": False}
                },
                "xAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 9,
                        "color": "#323751"
                    },
                    "axisLine": {"show": False},
                    "splitLine": {
                        "lineStyle": {
                            "color": "#D1D9E6",
                            "type": "dashed"
                        }
                    }
                },
                "series": [{
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, v in enumerate(app_counts.values.tolist())
                    ],
                    "type": "bar",
                    "itemStyle": {"borderRadius": [0, 4, 4, 0]},
                    "label": {
                        "show": True,
                        "position": "right",
                        "fontSize": 9,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "60%"
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_top_apps")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    with col_g4:
        st.markdown("**GMUDs por Local (30d)**")
        local_counts = filtered_df_30dias['Local_Implantacao'].value_counts().head(5)
        if len(local_counts) > 0:
            option = {
                "tooltip": {
                    "trigger": "item",
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "series": [{
                    "type": "pie",
                    "radius": "70%",
                    "center": ["50%", "50%"],
                    "itemStyle": {
                        "borderRadius": 4,
                        "borderColor": "#fff",
                        "borderWidth": 2
                    },
                    "label": {
                        "fontSize": 9,
                        "color": "#323751",
                        "formatter": "{b}\n{d}%"
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": 11,
                            "fontWeight": "bold"
                        }
                    },
                    "data": [
                        {"value": int(local_counts.get(cat, 0)), "name": cat, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, cat in enumerate(local_counts.index)
                    ]
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_local")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    st.markdown("---")
    
    # Expander 2: Análise de Responsáveis e Impactos
    with st.expander("Análise de Responsáveis e Impactos (30d)", expanded=True):
        col_g5, col_g6, col_g7 = st.columns(3)
    
    with col_g5:
        st.markdown("**GMUDs por Responsável (30d)**")
        resp_counts = filtered_df_30dias['Responsavel'].value_counts().head(10).sort_values(ascending=True)
        if len(resp_counts) > 0:
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
                    "containLabel": True
                },
                "yAxis": {
                    "type": "category",
                    "data": resp_counts.index.tolist(),
                    "axisLabel": {
                        "fontSize": 8,
                        "color": "#323751"
                    },
                    "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                    "axisTick": {"show": False}
                },
                "xAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 9,
                        "color": "#323751"
                    },
                    "axisLine": {"show": False},
                    "splitLine": {
                        "lineStyle": {
                            "color": "#D1D9E6",
                            "type": "dashed"
                        }
                    }
                },
                "series": [{
                    "data": [
                        {"value": v, "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                        for i, v in enumerate(resp_counts.values.tolist())
                    ],
                    "type": "bar",
                    "itemStyle": {"borderRadius": [0, 4, 4, 0]},
                    "label": {
                        "show": True,
                        "position": "right",
                        "fontSize": 9,
                        "color": "#323751",
                        "fontWeight": "bold"
                    },
                    "barWidth": "60%"
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_responsavel")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    with col_g6:
        st.markdown("**Demandas Impactadas (30d)**")
        if 'Impacto' in filtered_df_30dias.columns:
            total_30d = len(filtered_df_30dias)
            impactadas = len(filtered_df_30dias[filtered_df_30dias['Impacto'].notna() & (filtered_df_30dias['Impacto'] != 'N/A')])
            percentual = (impactadas / total_30d * 100) if total_30d > 0 else 0
            
            option = {
                "tooltip": {
                    "trigger": "item",
                    "backgroundColor": "#FFF",
                    "borderColor": "#323751",
                    "textStyle": {"color": "#323751"}
                },
                "series": [{
                    "type": "pie",
                    "radius": ["50%", "75%"],
                    "center": ["50%", "50%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 4,
                        "borderColor": "#fff",
                        "borderWidth": 2
                    },
                    "label": {
                        "show": True,
                        "fontSize": 11,
                        "fontWeight": "bold",
                        "color": "#323751",
                        "formatter": "{b}\n{c}\n({d}%)"
                    },
                    "data": [
                        {"value": impactadas, "name": "Impactadas", "itemStyle": {"color": fitbank_colors[1]}},
                        {"value": total_30d - impactadas, "name": "Sem Impacto", "itemStyle": {"color": fitbank_colors[4]}}
                    ]
                }]
            }
            st_echarts(options=option, height="200px", key="chart_gmud_demandas")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    with col_g7:
        st.markdown("**Tempo Médio Deploy (30d)**")
        if 'Tempo_Estimado' in filtered_df_30dias.columns and 'Nome_Aplicacao' in filtered_df_30dias.columns:
            # Converter tempo estimado para numérico
            filtered_df_30dias['Tempo_Estimado_num'] = pd.to_numeric(
                filtered_df_30dias['Tempo_Estimado'].str.extract(r'(\d+)')[0], 
                errors='coerce'
            )
            
            # Inferir tipo de aplicação baseado no nome
            def classificar_app(nome):
                nome_lower = str(nome).lower()
                if 'api' in nome_lower or 'service' in nome_lower or 'svc' in nome_lower:
                    return 'API'
                elif 'worker' in nome_lower or 'mq' in nome_lower or 'process' in nome_lower:
                    return 'Worker'
                else:
                    return 'Outros'
            
            filtered_df_30dias['Tipo_Aplicacao'] = filtered_df_30dias['Nome_Aplicacao'].apply(classificar_app)
            tempo_medio = filtered_df_30dias.groupby('Tipo_Aplicacao')['Tempo_Estimado_num'].mean().dropna()
            
            if len(tempo_medio) > 0:
                option = {
                    "tooltip": {
                        "trigger": "axis",
                        "axisPointer": {"type": "shadow"},
                        "backgroundColor": "#FFF",
                        "borderColor": "#323751",
                        "textStyle": {"color": "#323751"},
                        "formatter": "{b}: {c} min"
                    },
                    "grid": {
                        "left": "5%",
                        "right": "5%",
                        "bottom": "3%",
                        "top": "3%",
                        "containLabel": True
                    },
                    "xAxis": {
                        "type": "category",
                        "data": tempo_medio.index.tolist(),
                        "axisLabel": {
                            "fontSize": 9,
                            "color": "#323751"
                        },
                        "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                        "axisTick": {"show": False}
                    },
                    "yAxis": {
                        "type": "value",
                        "name": "Minutos",
                        "axisLabel": {
                            "fontSize": 9,
                            "color": "#323751"
                        },
                        "axisLine": {"show": False},
                        "splitLine": {
                            "lineStyle": {
                                "color": "#D1D9E6",
                                "type": "dashed"
                            }
                        }
                    },
                    "series": [{
                        "data": [
                            {"value": round(v, 1), "itemStyle": {"color": fitbank_colors[i % len(fitbank_colors)]}}
                            for i, v in enumerate(tempo_medio.values.tolist())
                        ],
                        "type": "bar",
                        "itemStyle": {"borderRadius": [4, 4, 0, 0]},
                        "label": {
                            "show": True,
                            "position": "top",
                            "fontSize": 10,
                            "color": "#323751",
                            "fontWeight": "bold",
                            "formatter": "{c}min"
                        },
                        "barWidth": "60%"
                    }]
                }
                st_echarts(options=option, height="200px", key="chart_gmud_tempo_deploy")
            else:
                st.info("⚠️ Nenhum dado disponível")
        else:
            st.info("⚠️ Nenhum dado disponível")
    
    st.markdown("---")
    
    # Expander 3: Análise Temporal de Implantações
    with st.expander("Análise Temporal de Implantações (30d)", expanded=True):
        col_g8, col_g9, col_g10 = st.columns(3)
        
        with col_g8:
            st.markdown("**Implantações por Dia (30d)**")
            if 'Data_Prevista_dt' in filtered_df_30dias.columns:
                daily_counts = filtered_df_30dias['Data_Prevista_dt'].dt.date.value_counts().sort_index()
                
                if len(daily_counts) > 0:
                    # Criar labels com dia da semana
                    dias_semana = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'}
                    labels_com_dia = []
                    for d in daily_counts.index:
                        dia_semana = dias_semana[pd.Timestamp(d).dayofweek]
                        labels_com_dia.append(f"{str(d)}\n{dia_semana}")
                    
                    option = {
                        "tooltip": {
                            "trigger": "axis",
                            "backgroundColor": "#FFF",
                            "borderColor": "#323751",
                            "textStyle": {"color": "#323751"}
                        },
                        "grid": {
                            "left": "5%",
                            "right": "5%",
                            "bottom": "10%",
                            "top": "5%",
                            "containLabel": True
                        },
                        "xAxis": {
                            "type": "category",
                            "data": labels_com_dia,
                            "axisLabel": {
                                "rotate": 45,
                                "fontSize": 8,
                                "color": "#323751"
                            },
                            "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                            "axisTick": {"show": False}
                        },
                        "yAxis": {
                            "type": "value",
                            "axisLabel": {
                                "fontSize": 9,
                                "color": "#323751"
                            },
                            "axisLine": {"show": False},
                            "splitLine": {
                                "lineStyle": {
                                    "color": "#D1D9E6",
                                    "type": "dashed"
                                }
                            }
                        },
                        "series": [{
                            "data": daily_counts.values.tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"color": fitbank_colors[0], "width": 2},
                            "areaStyle": {"color": fitbank_colors[0], "opacity": 0.3},
                            "itemStyle": {"color": fitbank_colors[0]}
                        }]
                    }
                    st_echarts(options=option, height="200px", key="chart_gmud_implantacoes_dia")
                else:
                    st.info("⚠️ Nenhum dado disponível")
            else:
                st.info("⚠️ Nenhum dado disponível")
        
        with col_g9:
            st.markdown("**Implantações por Semana (30d)**")
            if 'Data_Prevista_dt' in filtered_df_30dias.columns:
                weekly_counts = filtered_df_30dias['Data_Prevista_dt'].dt.isocalendar().week.value_counts().sort_index()
                
                if len(weekly_counts) > 0:
                    option = {
                        "tooltip": {
                            "trigger": "axis",
                            "backgroundColor": "#FFF",
                            "borderColor": "#323751",
                            "textStyle": {"color": "#323751"}
                        },
                        "grid": {
                            "left": "5%",
                            "right": "5%",
                            "bottom": "5%",
                            "top": "5%",
                            "containLabel": True
                        },
                        "xAxis": {
                            "type": "category",
                            "data": [f"Sem {w}" for w in weekly_counts.index],
                            "axisLabel": {
                                "fontSize": 9,
                                "color": "#323751"
                            },
                            "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                            "axisTick": {"show": False}
                        },
                        "yAxis": {
                            "type": "value",
                            "axisLabel": {
                                "fontSize": 9,
                                "color": "#323751"
                            },
                            "axisLine": {"show": False},
                            "splitLine": {
                                "lineStyle": {
                                    "color": "#D1D9E6",
                                    "type": "dashed"
                                }
                            }
                        },
                        "series": [{
                            "data": weekly_counts.values.tolist(),
                            "type": "bar",
                            "itemStyle": {"color": fitbank_colors[1], "borderRadius": [4, 4, 0, 0]},
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
                    st_echarts(options=option, height="200px", key="chart_gmud_implantacoes_semana")
                else:
                    st.info("⚠️ Nenhum dado disponível")
            else:
                st.info("⚠️ Nenhum dado disponível")
        
        with col_g10:
            st.markdown("**Implantações por Mês (30d)**")
            if 'Data_Prevista_dt' in filtered_df_30dias.columns:
                monthly_counts = filtered_df_30dias['Data_Prevista_dt'].dt.to_period('M').value_counts().sort_index()
                
                if len(monthly_counts) > 0:
                    meses = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                             7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
                    labels_meses = [f"{meses[p.month]}/{str(p.year)[-2:]}" for p in monthly_counts.index]
                    
                    option = {
                        "tooltip": {
                            "trigger": "axis",
                            "backgroundColor": "#FFF",
                            "borderColor": "#323751",
                            "textStyle": {"color": "#323751"}
                        },
                        "grid": {
                            "left": "5%",
                            "right": "5%",
                            "bottom": "5%",
                            "top": "5%",
                            "containLabel": True
                        },
                        "xAxis": {
                            "type": "category",
                            "data": labels_meses,
                            "axisLabel": {
                                "fontSize": 9,
                                "color": "#323751"
                            },
                            "axisLine": {"lineStyle": {"color": "#D1D9E6"}},
                            "axisTick": {"show": False}
                        },
                        "yAxis": {
                            "type": "value",
                            "axisLabel": {
                                "fontSize": 9,
                                "color": "#323751"
                            },
                            "axisLine": {"show": False},
                            "splitLine": {
                                "lineStyle": {
                                    "color": "#D1D9E6",
                                    "type": "dashed"
                                }
                            }
                        },
                        "series": [{
                            "data": monthly_counts.values.tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"color": fitbank_colors[2], "width": 3},
                            "areaStyle": {"color": fitbank_colors[2], "opacity": 0.4},
                            "itemStyle": {"color": fitbank_colors[2]},
                            "label": {
                                "show": True,
                                "position": "top",
                                "fontSize": 10,
                                "color": "#323751",
                                "fontWeight": "bold"
                            }
                        }]
                    }
                    st_echarts(options=option, height="200px", key="chart_gmud_implantacoes_mes")
                else:
                    st.info("⚠️ Nenhum dado disponível")
            else:
                st.info("⚠️ Nenhum dado disponível")
    
    st.markdown("---")
    
    # Expander para Lista e Detalhes
    with st.expander("Lista Completa e Detalhes de GMUDs", expanded=True):
        # Tabela completa de GMUDs
        st.markdown("**Lista Completa de GMUDs**")
        display_cols = ['ID_Item', 'Data_Prevista', 'Nome_Aplicacao', 'Ambiente', 
                        'Responsavel', 'Risco_Operacao', 'Local_Implantacao']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        df_display = filtered_df[available_cols].copy()
        
        # Renomear colunas
        rename_map = {
            'ID_Item': 'ID',
            'Data_Prevista': 'Data',
            'Nome_Aplicacao': 'Aplicação',
            'Ambiente': 'Ambiente',
            'Responsavel': 'Responsável',
            'Risco_Operacao': 'Risco',
            'Local_Implantacao': 'Local'
        }
        df_display = df_display.rename(columns=rename_map)
        
        # Filtro de texto
        search_term = st.text_input("Pesquisar na tabela", placeholder="Digite para filtrar...")
        
        # Aplicar filtro de texto no dataframe original
        df_filtered_by_search = filtered_df.copy()
        if search_term:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            df_filtered_by_search = filtered_df[mask]
        
        # Preparar dataframe para exibição
        available_cols = [col for col in display_cols if col in df_filtered_by_search.columns]
        df_display = df_filtered_by_search[available_cols].copy()
        df_display = df_display.rename(columns=rename_map)
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Download CSV
        csv_data = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="gmuds_completo.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Detalhes das últimas 5 GMUDs (usando o dataframe filtrado por texto)
        st.markdown("**Detalhes das Últimas 5 GMUDs**")
        last_5 = df_filtered_by_search.tail(5).iloc[::-1]
        
        for idx, row in last_5.iterrows():
            st.markdown(f"**GMUD: {row['ID_Item']}**")
            
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.markdown(f"**Aplicação:** {row['Nome_Aplicacao']}")
                st.markdown(f"**Ambiente:** {row['Ambiente']}")
                st.markdown(f"**Responsável:** {row['Responsavel']}")
            
            with col_d2:
                st.markdown(f"**Solicitante:** {row.get('Solicitante', 'N/A')}")
                st.markdown(f"**Hostname:** {row.get('Hostname', 'N/A')}")
                st.markdown(f"**Local:** {row.get('Local_Implantacao', 'N/A')}")
            
            with col_d3:
                st.markdown(f"**Risco:** {row.get('Risco_Operacao', 'N/A')}")
                st.markdown(f"**Tempo Estimado:** {row.get('Tempo_Estimado', 'N/A')}")
                st.markdown(f"**Tempo Realizado:** {row.get('Tempo_Realizado', 'N/A')}")
            
            if pd.notna(row.get('Configuracoes_Alteradas')):
                st.markdown(f"**Configurações Alteradas:**")
                st.code(row['Configuracoes_Alteradas'])
            
            if pd.notna(row.get('Ocorrencias')) and row.get('Ocorrencias') != 'N/A':
                st.markdown(f"**Ocorrências:** {row['Ocorrencias']}")
            
            if pd.notna(row.get('Validacoes_Realizadas')):
                st.markdown(f"**Validações:** {row['Validacoes_Realizadas']}")
            
            if pd.notna(row.get('Impacto')):
                st.markdown(f"**Impacto:** {row['Impacto']}")
            
            st.markdown("---")
