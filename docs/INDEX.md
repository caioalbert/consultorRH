# 📚 Índice Geral da Documentação

Sistema de BI para Controle de Inventário de Aplicações - Documentação Completa

---

## 🚀 Início Rápido

### Para Começar Imediatamente
1. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** ⚡
   - Como iniciar a aplicação
   - Primeiros passos
   - Dicas essenciais

### Para Instalação Detalhada
2. **[README.md](README.md)** 📖
   - Visão geral completa
   - Instalação passo a passo
   - Estrutura do projeto
   - Exemplos de uso

---

## 📊 Usando o Sistema

### Carregamento de Dados
3. **[TEMPLATE_DADOS.md](TEMPLATE_DADOS.md)** 📋
   - Estrutura do arquivo CSV/Excel
   - Colunas obrigatórias
   - Valores aceitos
   - Validação de dados
   - Como exportar do Excel

### Entendendo as Métricas
4. **[METRICAS_KPIS.md](METRICAS_KPIS.md)** 📈
   - Todas as métricas explicadas
   - Cálculo dos KPIs
   - Security Score
   - Fórmulas e interpretações
   - Como usar cada métrica

---

## 📖 Referência

### Perguntas Frequentes
5. **[FAQ.md](FAQ.md)** ❓
   - Instalação e configuração
   - Uso do sistema
   - Problemas comuns
   - Soluções de troubleshooting
   - Performance

### Histórico e Roadmap
6. **[CHANGELOG.md](CHANGELOG.md)** 📝
   - Versão atual (v1.0.0)
   - Funcionalidades implementadas
   - Roadmap futuro
   - Bugs conhecidos
   - Como contribuir

---

## 🎯 Por Tipo de Usuário

### 👨‍💼 Gestores e Líderes
**Leia primeiro:**
1. README.md - Seção "Visão Geral"
2. METRICAS_KPIS.md - Seção "Indicadores Estratégicos"
3. GUIA_RAPIDO.md - Seção "Principais Métricas"

**Foco em:**
- Security Score geral
- Taxa de adoção de práticas modernas
- Conformidade de governança
- Top 20 aplicações críticas

### 👨‍💻 Desenvolvedores e DevOps
**Leia primeiro:**
1. README.md - Seção "Instalação"
2. TEMPLATE_DADOS.md - Estrutura completa
3. METRICAS_KPIS.md - Todos os cálculos

**Foco em:**
- CI/CD metrics
- Migração para YAML
- Práticas de segurança
- Revisões técnicas

### 🔒 Segurança e Compliance
**Leia primeiro:**
1. METRICAS_KPIS.md - Seção "SecOps"
2. README.md - Dashboard SecOps
3. FAQ.md - Seção "Segurança e Privacidade"

**Foco em:**
- Security Score
- SBOM, Scan, Secret Manager, SAST
- Aplicações de alto risco
- Conformidade

### 📊 Analistas de BI
**Leia primeiro:**
1. TEMPLATE_DADOS.md - Estrutura dos dados
2. METRICAS_KPIS.md - Todas as métricas
3. CHANGELOG.md - Funcionalidades disponíveis

**Foco em:**
- Todos os dashboards
- Filtros e segmentações
- Exportação de dados
- Análises personalizadas

---

## 📁 Estrutura de Arquivos

### Aplicação Principal
```
app.py                          # Aplicação Streamlit principal
data_loader.py                  # Carregador de dados
```

### Dashboards
```
dashboard_painel_geral.py       # Dashboard: Painel Geral
dashboard_cicd.py               # Dashboard: CI/CD
dashboard_secops.py             # Dashboard: SecOps
dashboard_governanca.py         # Dashboard: Governança
```

### Dados e Configuração
```
inventario_aplicacoes.csv       # Dados de exemplo (50 apps)
requirements.txt                # Dependências Python
.streamlit/config.toml          # Configuração Streamlit
.gitignore                      # Arquivos ignorados pelo Git
```

### Scripts e Utilitários
```
iniciar.bat                     # Script de inicialização Windows
```

### Documentação
```
README.md                       # Documentação principal
GUIA_RAPIDO.md                  # Guia rápido de uso
TEMPLATE_DADOS.md               # Template e formato de dados
METRICAS_KPIS.md                # Métricas e KPIs detalhados
CHANGELOG.md                    # Histórico e roadmap
FAQ.md                          # Perguntas frequentes
INDEX.md                        # Este arquivo (índice geral)
```

---

## 🎓 Trilhas de Aprendizado

### Trilha 1: Usuário Básico (30 minutos)
1. ✅ Ler GUIA_RAPIDO.md (10 min)
2. ✅ Executar iniciar.bat (2 min)
3. ✅ Carregar dados de exemplo (2 min)
4. ✅ Explorar Painel Geral (5 min)
5. ✅ Aplicar filtros (5 min)
6. ✅ Visualizar outros dashboards (6 min)

### Trilha 2: Usuário Intermediário (1 hora)
1. ✅ Completar Trilha 1
2. ✅ Ler TEMPLATE_DADOS.md (15 min)
3. ✅ Preparar seu próprio CSV (20 min)
4. ✅ Carregar dados reais (5 min)
5. ✅ Explorar todos os dashboards (20 min)

### Trilha 3: Usuário Avançado (2 horas)
1. ✅ Completar Trilha 2
2. ✅ Ler METRICAS_KPIS.md completo (30 min)
3. ✅ Entender cálculos dos KPIs (20 min)
4. ✅ Análise profunda dos dados (40 min)
5. ✅ Gerar insights e relatórios (30 min)

### Trilha 4: Desenvolvedor (3 horas)
1. ✅ Ler README.md completo (30 min)
2. ✅ Entender arquitetura (20 min)
3. ✅ Estudar código-fonte (60 min)
4. ✅ Ler CHANGELOG.md (20 min)
5. ✅ Customizar dashboards (50 min)

---

## 🔍 Busca Rápida

### Por Funcionalidade

| Funcionalidade | Documento | Seção |
|----------------|-----------|-------|
| Instalar sistema | README.md | Instalação |
| Iniciar aplicação | GUIA_RAPIDO.md | Início |
| Formato CSV | TEMPLATE_DADOS.md | Estrutura |
| Security Score | METRICAS_KPIS.md | SecOps |
| Filtros | README.md | Navegação |
| Exportar gráficos | GUIA_RAPIDO.md | Dicas |
| Erro ao carregar | FAQ.md | Problemas Comuns |
| Roadmap | CHANGELOG.md | Versões Futuras |

### Por Problema

| Problema | Documento | Solução |
|----------|-----------|---------|
| Não inicia | FAQ.md | Instalação |
| Erro de dados | TEMPLATE_DADOS.md | Validação |
| Gráfico vazio | FAQ.md | Problemas Comuns |
| Sistema lento | FAQ.md | Performance |
| Encoding erro | FAQ.md | Problemas Comuns |

---

## 📞 Suporte e Contato

### Onde Encontrar Ajuda
1. **Primeira opção:** [FAQ.md](FAQ.md)
2. **Segunda opção:** README.md e documentação específica
3. **Terceira opção:** Contatar equipe DevOps

### Canais de Suporte
- **Email:** devops@empresa.com
- **Teams:** Canal DevOps
- **Wiki:** Confluence (interno)

---

## 🔄 Atualizações

### Como Saber de Novas Versões
- Consulte [CHANGELOG.md](CHANGELOG.md) regularmente
- Inscreva-se nas notificações do repositório
- Acompanhe o canal de DevOps

### Como Atualizar
```bash
# Baixe a nova versão
git pull

# Atualize dependências
pip install --upgrade -r requirements.txt

# Reinicie a aplicação
streamlit run app.py
```

---

## ✅ Checklist de Documentos

Use este checklist para garantir que leu toda documentação necessária:

### Obrigatório para Todos
- [ ] README.md
- [ ] GUIA_RAPIDO.md
- [ ] FAQ.md (pelo menos skimming)

### Para Uso Diário
- [ ] TEMPLATE_DADOS.md
- [ ] METRICAS_KPIS.md (sua área)

### Para Desenvolvedores
- [ ] README.md completo
- [ ] CHANGELOG.md
- [ ] TEMPLATE_DADOS.md
- [ ] METRICAS_KPIS.md completo

### Opcional mas Recomendado
- [ ] INDEX.md (este arquivo)
- [ ] CHANGELOG.md (seção Roadmap)

---

## 📝 Notas

### Convenções Usadas na Documentação
- ✅ Item completo/disponível
- [ ] Item pendente/futuro
- 🔴 Crítico/Urgente
- 🟡 Atenção
- 🟢 OK/Conforme
- ⚡ Rápido/Importante
- 💡 Dica
- ⚠️ Aviso

### Formatos de Código
```bash
# Comandos de terminal
```

```python
# Código Python
```

```csv
# Formato CSV
```

---

## 🎉 Conclusão

Você agora tem acesso completo a toda documentação do sistema!

### Próximos Passos
1. Escolha sua trilha de aprendizado acima
2. Comece pelo GUIA_RAPIDO.md
3. Execute o sistema com dados de exemplo
4. Explore e aprenda!

### Lembre-se
- A documentação é viva e está em constante atualização
- Suas sugestões são bem-vindas
- Em caso de dúvida, consulte o FAQ primeiro

---

**Sistema de BI - Inventário de Aplicações**  
**Versão:** 1.0.0  
**Última Atualização:** Dezembro 2024  
**Mantido por:** Equipe DevOps

---

**Feliz análise! 📊🚀**
