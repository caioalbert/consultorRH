# ❓ FAQ - Perguntas Frequentes

## Índice
1. [Instalação e Configuração](#instalação-e-configuração)
2. [Uso do Sistema](#uso-do-sistema)
3. [Dados e Formato](#dados-e-formato)
4. [Dashboards e Métricas](#dashboards-e-métricas)
5. [Problemas Comuns](#problemas-comuns)
6. [Performance e Otimização](#performance-e-otimização)
7. [Segurança e Privacidade](#segurança-e-privacidade)

---

## Instalação e Configuração

### P: Quais são os requisitos mínimos para rodar o sistema?
**R:** 
- Python 3.8 ou superior
- 4GB de RAM (recomendado: 8GB)
- Navegador moderno (Chrome, Firefox, Edge)
- Sistema operacional: Windows, Linux ou macOS

### P: Como instalo o Python?
**R:** 
1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente (3.8+)
3. Execute o instalador
4. **Importante:** Marque a opção "Add Python to PATH"

### P: O arquivo `iniciar.bat` não funciona. O que fazer?
**R:** 
Tente executar manualmente:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### P: Posso rodar em um servidor web?
**R:** Sim! Configure o Streamlit para aceitar conexões externas:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

---

## Uso do Sistema

### P: Como faço para carregar meus dados?
**R:** 
1. Prepare um arquivo CSV ou Excel com as colunas obrigatórias
2. Na sidebar, escolha "Upload de Arquivo" ou "Arquivo Local"
3. Selecione seu arquivo
4. Os dados serão carregados automaticamente

### P: Posso usar o sistema sem fazer upload toda vez?
**R:** 
Sim! Use a opção "Arquivo Local" e mantenha o arquivo no mesmo diretório do app. O sistema lembrará do caminho.

### P: Os filtros aplicam em todos os dashboards?
**R:** 
Sim! Quando você aplica um filtro por Produto ou Ambiente, ele permanece ativo em todos os dashboards durante sua sessão.

### P: Como exporto os gráficos?
**R:** 
Passe o mouse sobre qualquer gráfico e clique no ícone da câmera no canto superior direito para salvar como PNG.

### P: Posso compartilhar minhas visualizações?
**R:** 
Atualmente, você pode compartilhar screenshots. Em versões futuras, teremos compartilhamento de links com filtros aplicados.

---

## Dados e Formato

### P: Quais formatos de arquivo são suportados?
**R:** 
- CSV (UTF-8 recomendado)
- Excel (.xlsx)
- Excel 97-2003 (.xls)

### P: Qual o tamanho máximo de arquivo suportado?
**R:** 
- Recomendado: até 5.000 aplicações
- Máximo testado: 10.000 aplicações
- Para datasets maiores, considere usar filtros ou dividir em múltiplos arquivos

### P: Quais colunas são obrigatórias?
**R:** 
Todas as 15 colunas são obrigatórias:
- Nome_Aplicacao, Produto, Ambiente, Tipo_Aplicacao, Framework
- Ferramenta_Versionamento, Tipo_Pipeline, Versao, Hospedagem
- SBOM, Scan_Imagens, Secret_Manager, SAST_SonarCube
- Data_Ultima_Revisao, Data_Criacao

### P: Como devo formatar as datas?
**R:** 
Use o formato: `YYYY-MM-DD`
Exemplos: `2024-12-04`, `2023-06-15`

### P: Posso deixar células vazias?
**R:** 
Não para campos de texto. Use "Não Especificado" ou similar.
Para práticas de segurança (SBOM, Scan, etc.), use "Não" se não aplicável.

### P: O sistema diferencia maiúsculas de minúsculas?
**R:** 
Não para análises, mas mantenha consistência nos nomes para melhor organização.

---

## Dashboards e Métricas

### P: O que é o Security Score?
**R:** 
É uma pontuação de 0-100 que mede a adoção de práticas de segurança:
- SBOM: 25 pontos
- Scan de Imagens: 25 pontos
- Secret Manager: 25 pontos
- SAST: 25 pontos

### P: Por que devo migrar de Pipeline Classic para YAML?
**R:** 
Pipelines YAML oferecem:
- Versionamento do pipeline junto com o código
- Revisões via Pull Request
- Reutilização de templates
- Melhor rastreabilidade

### P: O que significa "Apps > 3 meses sem revisão"?
**R:** 
São aplicações que não foram revisadas (tecnicamente ou documentalmente) há mais de 3 meses, o que pode indicar falta de manutenção.

### P: Como é calculado "Meses sem Revisão"?
**R:** 
```
Meses = (Data Atual - Data Última Revisão) / 30 dias
```

### P: O que é SBOM?
**R:** 
Software Bill of Materials - lista de todos os componentes de software usados em uma aplicação, importante para gestão de vulnerabilidades.

---

## Problemas Comuns

### P: "Erro ao carregar dados: Arquivo não encontrado"
**R:** 
Verifique:
1. O caminho do arquivo está correto?
2. O arquivo existe no local especificado?
3. Você tem permissão de leitura?

### P: "Erro: Import 'streamlit' could not be resolved"
**R:** 
Instale as dependências:
```bash
pip install -r requirements.txt
```

### P: Os gráficos aparecem vazios ou com erro
**R:** 
Verifique:
1. Se há dados suficientes na coluna
2. Se os valores estão no formato correto
3. Se não há apenas valores nulos

### P: A aplicação está muito lenta
**R:** 
Tente:
1. Aplicar filtros para reduzir o volume de dados
2. Fechar outras abas do navegador
3. Limpar o cache: Settings → Clear Cache
4. Reiniciar a aplicação

### P: "UnicodeDecodeError" ao ler CSV
**R:** 
Salve o CSV com encoding UTF-8:
- Excel: Salvar Como → CSV UTF-8
- Notepad++: Encoding → UTF-8

---

## Performance e Otimização

### P: Quantas aplicações o sistema suporta?
**R:** 
- **Ótimo:** até 1.000 apps
- **Bom:** 1.000-5.000 apps
- **Aceitável:** 5.000-10.000 apps
- **Requer otimização:** >10.000 apps

### P: Como melhorar a performance com muitos dados?
**R:** 
1. Use filtros para visualizar subconjuntos
2. Divida por produto/ambiente em arquivos separados
3. Remova aplicações antigas/descontinuadas
4. Considere upgrade de hardware

### P: O cache é salvo entre sessões?
**R:** 
Não, o cache é por sessão. Quando você fecha o navegador, o cache é perdido.

### P: Posso rodar múltiplas instâncias simultaneamente?
**R:** 
Sim, cada usuário pode ter sua própria sessão independente.

---

## Segurança e Privacidade

### P: Meus dados ficam armazenados no servidor?
**R:** 
Não permanentemente. Os dados são mantidos apenas durante a sessão ativa. Ao fechar o navegador ou após período de inatividade, os dados são descartados.

### P: Posso usar o sistema com dados sensíveis?
**R:** 
Sim, mas recomendamos:
1. Rodar em ambiente local ou rede interna
2. Não usar dados de produção em ambientes públicos
3. Revisar dados antes do upload

### P: O sistema registra logs de atividade?
**R:** 
Por padrão, apenas logs técnicos básicos. Não há auditoria de usuários na v1.0.0 (planejado para v2.2.0).

### P: Como garantir que apenas pessoas autorizadas acessem?
**R:** 
Na v1.0.0, não há sistema de autenticação. Opções:
1. Rodar apenas localmente
2. Usar VPN/rede interna
3. Implementar proxy com autenticação
4. Aguardar v2.2.0 com autenticação nativa

---

## Diversos

### P: Posso customizar as cores e o tema?
**R:** 
Sim, edite o arquivo `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#1f77b4"
backgroundColor="#ffffff"
```

### P: Como adiciono um novo dashboard?
**R:** 
1. Crie um arquivo `dashboard_meu_novo.py`
2. Implemente a função `render_meu_novo_dashboard(df)`
3. Importe e adicione no menu do `app.py`

### P: Posso integrar com outras ferramentas?
**R:** 
Na v1.0.0, não há integrações nativas. Planejado para v2.0.0:
- Azure DevOps API
- GitHub API
- GitLab API
- SonarQube

### P: Há versão mobile?
**R:** 
O sistema é responsivo e funciona em tablets e celulares, mas a experiência é otimizada para desktop.

### P: Preciso de internet para usar?
**R:** 
Não! Após instalar as dependências, o sistema roda completamente offline.

### P: Como faço backup dos meus dados?
**R:** 
Simplesmente mantenha cópias do seu arquivo CSV/Excel em local seguro.

---

## 🆘 Precisa de Mais Ajuda?

### Documentação Completa
- **README.md**: Guia completo do sistema
- **GUIA_RAPIDO.md**: Início rápido
- **TEMPLATE_DADOS.md**: Formato dos dados
- **METRICAS_KPIS.md**: Explicação de todas as métricas

### Suporte
- **Email:** devops@empresa.com
- **Teams:** Canal DevOps
- **Issues:** Repositório do projeto

### Recursos Adicionais
- Arquivo de exemplo: `inventario_aplicacoes.csv`
- Script de início: `iniciar.bat`
- Configuração: `.streamlit/config.toml`

---

**Última Atualização:** Dezembro 2024  
**Versão:** 1.0.0

**Não encontrou sua pergunta?** Entre em contato com a equipe de DevOps!
