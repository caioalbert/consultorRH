# 📊 Métricas e KPIs - Sistema de BI

## Visão Geral

Este documento descreve todas as métricas, KPIs e cálculos utilizados nos dashboards do sistema de BI para inventário de aplicações.

---

## 🏠 Painel Geral

### Métricas Principais

#### 1. Total de Aplicações
- **Fórmula:** COUNT(aplicações)
- **Tipo:** Métrica absoluta
- **Uso:** Visão geral do tamanho do portfólio

#### 2. Produtos Únicos
- **Fórmula:** COUNT(DISTINCT produto)
- **Tipo:** Métrica absoluta
- **Uso:** Quantidade de produtos/squads ativos

#### 3. Ambientes Únicos
- **Fórmula:** COUNT(DISTINCT ambiente)
- **Tipo:** Métrica absoluta
- **Uso:** Diversidade de ambientes

#### 4. Frameworks Únicos
- **Fórmula:** COUNT(DISTINCT framework)
- **Tipo:** Métrica absoluta
- **Uso:** Diversidade tecnológica

### Análises

#### Distribuição por Produto
- **Tipo:** Análise de distribuição
- **Visualização:** Gráfico de barras
- **Insight:** Identificar produtos com maior número de aplicações

#### Distribuição por Ambiente
- **Tipo:** Análise de distribuição percentual
- **Visualização:** Gráfico de pizza
- **Insight:** Proporção de aplicações em cada ambiente

#### Distribuição por Tipo
- **Tipo:** Análise de distribuição
- **Visualização:** Gráfico de barras horizontal
- **Insight:** Tipos de aplicações mais comuns

#### Distribuição por Framework
- **Tipo:** Análise de distribuição (Top 10)
- **Visualização:** Gráfico de barras horizontal
- **Insight:** Frameworks mais utilizados

#### Mapa de Calor: Ambiente x Tipo
- **Tipo:** Análise de correlação
- **Visualização:** Heatmap
- **Insight:** Relação entre ambientes e tipos de aplicação

---

## 🔄 CI/CD

### Métricas Principais

#### 1. Apps com Versionamento
- **Fórmula:** COUNT(apps WHERE ferramenta_versionamento IS NOT NULL)
- **Tipo:** Métrica absoluta
- **Uso:** Controle de versionamento

#### 2. Pipelines YAML
- **Fórmula:** COUNT(apps WHERE tipo_pipeline = 'YAML')
- **Tipo:** Métrica absoluta
- **Uso:** Adoção de práticas modernas

#### 3. Pipelines Classic
- **Fórmula:** COUNT(apps WHERE tipo_pipeline = 'Classic')
- **Tipo:** Métrica absoluta
- **Uso:** Legacy pipelines

#### 4. Tipos de Hospedagem
- **Fórmula:** COUNT(DISTINCT hospedagem)
- **Tipo:** Métrica absoluta
- **Uso:** Diversidade de infraestrutura

### KPIs

#### Taxa de Adoção YAML
- **Fórmula:** (Pipelines YAML / Total Pipelines) × 100
- **Meta:** > 80%
- **Tipo:** KPI percentual
- **Criticidade:** 
  - 🔴 < 30%: Crítico
  - 🟡 30-70%: Atenção
  - 🟢 > 70%: Conforme

### Análises

#### Distribuição de Versionamento
- **Tipo:** Análise de mercado
- **Insight:** Ferramentas de versionamento mais utilizadas

#### Comparação YAML vs Classic
- **Tipo:** Análise comparativa
- **Insight:** Progresso de modernização

#### Análise por Versão
- **Tipo:** Análise de versões (Top 15)
- **Insight:** Controle de versões ativas

#### Distribuição por Hospedagem
- **Tipo:** Análise de infraestrutura
- **Insight:** Onde as aplicações estão hospedadas

---

## 🔒 SecOps

### Métricas Principais

#### 1. Apps com SBOM
- **Fórmula:** COUNT(apps WHERE SBOM = 'Sim')
- **Tipo:** Métrica absoluta
- **Percentual:** (Apps com SBOM / Total Apps) × 100

#### 2. Apps com Scan de Imagens
- **Fórmula:** COUNT(apps WHERE Scan_Imagens = 'Sim')
- **Tipo:** Métrica absoluta
- **Percentual:** (Apps com Scan / Total Apps) × 100

#### 3. Apps com Secret Manager
- **Fórmula:** COUNT(apps WHERE Secret_Manager = 'Sim')
- **Tipo:** Métrica absoluta
- **Percentual:** (Apps com Secret / Total Apps) × 100

#### 4. Apps com SAST
- **Fórmula:** COUNT(apps WHERE SAST_SonarCube = 'Sim')
- **Tipo:** Métrica absoluta
- **Percentual:** (Apps com SAST / Total Apps) × 100

### KPI Principal: Security Score

#### Cálculo do Security Score
```python
score = (
    (SBOM_Sim * 25) +
    (Scan_Imagens_Sim * 25) +
    (Secret_Manager_Sim * 25) +
    (SAST_Sim * 25)
) / 100

# Cada prática vale 25 pontos
# Score total: 0-100
```

#### Faixas de Classificação
- **🔴 0-25%:** Crítico - Ação imediata necessária
- **🟠 25-50%:** Baixo - Melhorias urgentes
- **🟡 50-75%:** Médio - Atenção necessária
- **🟢 75-100%:** Alto - Conforme

#### Metas por Prática
| Prática | Meta |
|---------|------|
| SBOM | > 80% |
| Scan de Imagens | > 90% |
| Secret Manager | > 95% |
| SAST | > 85% |

### Análises

#### Score Médio de Segurança
- **Tipo:** KPI agregado
- **Visualização:** Gauge
- **Meta:** > 75%

#### Distribuição de Scores
- **Tipo:** Análise de distribuição
- **Visualização:** Gráfico de barras
- **Insight:** Quantas apps em cada faixa

#### Práticas de Segurança
- **Tipo:** Análise comparativa
- **Visualização:** Barras empilhadas
- **Insight:** Adoção de cada prática

#### Radar Comparativo
- **Tipo:** Análise multidimensional
- **Visualização:** Gráfico radar
- **Insight:** Visão holística das práticas

#### Análise por Produto
- **Tipo:** Análise segmentada
- **Insight:** Score de segurança por produto

#### Top 20 Maior Risco
- **Tipo:** Análise de risco
- **Insight:** Aplicações que precisam de atenção imediata

---

## ⚖️ Governança

### Métricas Principais

#### 1. Apps Sem Data de Revisão
- **Fórmula:** COUNT(apps WHERE Data_Ultima_Revisao IS NULL)
- **Tipo:** Métrica absoluta
- **Criticidade:** 🔴 Alta

#### 2. Apps > 3 Meses Sem Revisão
- **Fórmula:** COUNT(apps WHERE meses_sem_revisao > 3)
- **Tipo:** Métrica absoluta
- **Percentual:** (Apps > 3m / Total Apps) × 100

#### 3. Apps > 6 Meses Sem Revisão
- **Fórmula:** COUNT(apps WHERE meses_sem_revisao > 6)
- **Tipo:** Métrica absoluta
- **Criticidade:** 🟠 Média

#### 4. Apps > 12 Meses Sem Revisão
- **Fórmula:** COUNT(apps WHERE meses_sem_revisao > 12)
- **Tipo:** Métrica absoluta
- **Criticidade:** 🔴 Alta

### Cálculo de Meses Sem Revisão

```python
meses_sem_revisao = (data_hoje - data_ultima_revisao).days / 30
```

### Classificação de Conformidade

#### Status de Conformidade
| Status | Critério | Cor |
|--------|----------|-----|
| Conforme | ≤ 3 meses | 🟢 Verde |
| Atenção | 3-6 meses | 🟡 Amarelo |
| Alerta | 6-12 meses | 🟠 Laranja |
| Crítico | > 12 meses | 🔴 Vermelho |

### Políticas de Governança

#### Política de Revisão
- **Frequência Mínima:** A cada 3 meses
- **Frequência Recomendada:** Mensal
- **Ação:** Revisão técnica e atualização de documentação

#### SLA de Revisão
- **Apps Produção:** Máximo 3 meses
- **Apps Homologação:** Máximo 6 meses
- **Apps Desenvolvimento:** Máximo 12 meses

### Análises

#### Distribuição por Período
- **Tipo:** Análise temporal
- **Categorias:**
  - 0-1 mês: 🟢 Recente
  - 1-3 meses: 🔵 Conforme
  - 3-6 meses: 🟡 Atenção
  - 6-12 meses: 🟠 Alerta
  - > 12 meses: 🔴 Crítico

#### Status de Conformidade
- **Tipo:** Análise de conformidade
- **Visualização:** Gráfico de pizza
- **Meta:** > 80% conforme

#### Análise por Produto
- **Tipo:** Análise segmentada
- **Métricas:**
  - Total de apps
  - Apps sem data
  - Apps > 3 meses
  - Apps > 6 meses
  - Média de meses sem revisão

#### Top 20 Revisão Mais Antiga
- **Tipo:** Análise de risco
- **Ordenação:** Por data mais antiga
- **Uso:** Priorização de revisões

#### Timeline de Aplicações
- **Tipo:** Análise visual temporal
- **Visualização:** Timeline gráfica
- **Insight:** Evolução temporal das revisões

---

## 🎯 Indicadores Estratégicos

### Maturidade DevOps
```
Score = (
    (% YAML × 0.3) +
    (Security Score × 0.4) +
    (% Conforme Governança × 0.3)
)
```

### Nível de Maturidade
- **Nível 1 (0-25%):** Inicial
- **Nível 2 (25-50%):** Gerenciado
- **Nível 3 (50-75%):** Definido
- **Nível 4 (75-90%):** Quantitativamente Gerenciado
- **Nível 5 (90-100%):** Otimizado

### Debt Score (Dívida Técnica)
```
Debt_Score = (
    (% Pipelines Classic × 0.3) +
    ((100 - Security Score) × 0.4) +
    (% Apps > 6m sem revisão × 0.3)
)
```

**Interpretação:**
- Quanto menor, melhor
- > 60%: Dívida técnica alta
- 30-60%: Dívida técnica moderada
- < 30%: Dívida técnica controlada

---

## 📈 Tendências e Previsões

### Métricas de Tendência (Futuro)
- Taxa de crescimento de aplicações
- Velocidade de adoção de YAML
- Melhoria do Security Score
- Redução de aplicações desatualizadas

### Alertas Automáticos (Futuro)
- Apps com score < 25%
- Apps > 6 meses sem revisão
- Novos gaps de segurança
- Ambientes sem conformidade

---

## 💡 Como Usar Estes KPIs

### Para Gestores
1. Monitore o Security Score geral
2. Acompanhe a taxa de adoção YAML
3. Revise aplicações críticas mensalmente
4. Estabeleça metas por produto

### Para Times de DevOps
1. Priorize apps com score baixo
2. Migre pipelines Classic para YAML
3. Implemente práticas de segurança faltantes
4. Mantenha revisões em dia

### Para Auditoria/Compliance
1. Verifique conformidade de governança
2. Audite práticas de segurança
3. Valide SLAs de revisão
4. Gere relatórios periódicos

---

**Versão:** 1.0.0  
**Última Atualização:** Dezembro 2024
