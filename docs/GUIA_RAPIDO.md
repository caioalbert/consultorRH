# 🚀 Guia Rápido de Uso

## Iniciando a Aplicação

### Opção 1: Script Automático (Recomendado)
1. Dê duplo clique no arquivo `iniciar.bat`
2. Aguarde a instalação das dependências
3. A aplicação abrirá automaticamente no navegador

### Opção 2: Manual
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
streamlit run app.py
```

## 📊 Usando os Dashboards

### 1. Carregar Dados
**Sidebar → Configuração**
- **Upload de Arquivo**: Faça upload do seu CSV/Excel
- **Arquivo Local**: Digite o caminho do arquivo

Exemplo: `inventario_aplicacoes.csv` (arquivo de exemplo incluído)

### 2. Navegação
**Sidebar → Dashboards**
- 🏠 **Painel Geral**: Visão geral e distribuições
- 🔄 **CI/CD**: Análise de pipelines e versionamento
- 🔒 **SecOps**: Métricas de segurança
- ⚖️ **Governança**: Controle de revisões

### 3. Filtros
**Sidebar → Filtros**
- **Produto**: Filtra aplicações de um produto específico
- **Ambiente**: Filtra por Produção, Homologação ou Desenvolvimento

### 4. Interação com Gráficos
- **Hover**: Passe o mouse para ver detalhes
- **Zoom**: Use o mouse para dar zoom em áreas
- **Download**: Clique no ícone da câmera para salvar o gráfico
- **Pan**: Arraste para mover a visualização

## 📋 Formato dos Dados

### Colunas Obrigatórias

```csv
Nome_Aplicacao,Produto,Ambiente,Tipo_Aplicacao,Framework,
Ferramenta_Versionamento,Tipo_Pipeline,Versao,Hospedagem,
SBOM,Scan_Imagens,Secret_Manager,SAST_SonarCube,
Data_Ultima_Revisao,Data_Criacao
```

### Valores Aceitos

**Ambiente:**
- Produção
- Homologação
- Desenvolvimento

**Tipo_Pipeline:**
- YAML
- Classic

**SBOM, Scan_Imagens, Secret_Manager, SAST_SonarCube:**
- Sim
- Não

**Datas:**
- Formato: YYYY-MM-DD
- Exemplo: 2024-11-15

## 💡 Dicas e Truques

### 1. Análise Rápida
- Use o **Painel Geral** para ter uma visão rápida do inventário
- Verifique o **SecOps** para identificar gaps de segurança
- Consulte **Governança** para aplicações que precisam de revisão

### 2. Exportar Dados
- Clique nos gráficos para baixar como PNG
- Use os filtros para focar em produtos específicos

### 3. Performance
- Para arquivos grandes (>1000 apps), use filtros
- Os dados são cacheados automaticamente

### 4. Atualização de Dados
- Sempre que atualizar o CSV, faça novo upload
- O sistema detecta automaticamente mudanças

## 🎯 Principais Métricas

### Painel Geral
- ✅ Total de aplicações
- ✅ Distribuição por produto
- ✅ Frameworks mais utilizados
- ✅ Ambientes disponíveis

### CI/CD
- ✅ % de adoção de Pipeline YAML
- ✅ Ferramentas de versionamento
- ✅ Tipos de hospedagem
- ✅ Versões por aplicação

### SecOps
- ✅ Score de segurança (0-100)
- ✅ Aplicações com SBOM
- ✅ Cobertura de Scan de imagens
- ✅ Uso de Secret Manager
- ✅ Análise SAST

### Governança
- ✅ Apps sem revisão > 3 meses
- ✅ Top 20 aplicações mais antigas
- ✅ Status de conformidade
- ✅ Timeline de revisões

## ⚠️ Solução de Problemas

### Erro ao carregar dados
**Problema:** "Arquivo não encontrado"
**Solução:** Verifique se o caminho está correto e o arquivo existe

**Problema:** "Formato não suportado"
**Solução:** Use apenas arquivos CSV ou Excel (.xlsx, .xls)

### Gráficos não aparecem
**Problema:** Página em branco
**Solução:** 
```bash
# Reinstale as dependências
pip install --force-reinstall -r requirements.txt
```

### Aplicação lenta
**Problema:** Demora para carregar
**Solução:**
- Use filtros para reduzir o volume de dados
- Feche outras abas do navegador
- Limpe o cache: Settings → Clear Cache

## 📞 Precisa de Ajuda?

1. Consulte o **README.md** completo
2. Verifique se todas as dependências estão instaladas
3. Confirme que o arquivo de dados está no formato correto
4. Entre em contato com o time de DevOps

## 🔄 Atualizações Futuras

### Em Desenvolvimento
- [ ] Filtro por framework
- [ ] Exportação de relatórios em PDF
- [ ] Alertas automáticos para aplicações críticas
- [ ] Integração com Azure DevOps API
- [ ] Dashboard de tendências temporais

### Sugestões
Envie suas sugestões para a equipe de desenvolvimento!

---

**Versão:** 1.0.0  
**Última Atualização:** Dezembro 2024
