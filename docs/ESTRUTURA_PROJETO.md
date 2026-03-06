# Estrutura do Projeto - Sistema de BI para Inventário de Aplicações

```
Inventory - DevOps/
│
├── app.py                      # Arquivo principal da aplicação
├── iniciar.bat                 # Script para iniciar a aplicação
├── requirements.txt            # Dependências do projeto
│
├── src/                        # Código fonte
│   ├── __init__.py
│   ├── dashboards/             # Módulos de dashboards
│   │   ├── __init__.py
│   │   ├── dashboard_painel_geral.py
│   │   ├── dashboard_cicd.py
│   │   ├── dashboard_governanca.py
│   │   └── dashboard_secops.py
│   │
│   └── utils/                  # Utilitários
│       ├── __init__.py
│       └── data_loader.py      # Carregador de dados
│
├── assets/                     # Recursos estáticos
│   └── logo.png                # Logo da aplicação
│
├── config/                     # Configurações
│   └── settings.py             # Arquivo de configurações
│
├── data/                       # Dados da aplicação
│   ├── inventario_aplicacoes.csv
│   └── temp_inventory_data.csv
│
└── docs/                       # Documentação
    ├── README.md
    ├── CHANGELOG.md
    ├── FAQ.md
    ├── GUIA_RAPIDO.md
    ├── INDEX.md
    ├── METRICAS_KPIS.md
    ├── RESUMO_PROJETO.md
    └── TEMPLATE_DADOS.md
```

## Descrição das Pastas

### `/src`
Contém todo o código fonte da aplicação organizado em módulos.

### `/src/dashboards`
Módulos responsáveis pela renderização dos diferentes dashboards da aplicação.

### `/src/utils`
Utilitários e funções auxiliares, como carregamento de dados.

### `/assets`
Recursos estáticos como imagens, ícones e arquivos de mídia.

### `/config`
Arquivos de configuração da aplicação.

### `/data`
Arquivos de dados CSV e temporários.

### `/docs`
Toda a documentação do projeto em formato Markdown.

## Benefícios desta Estrutura

1. **Organização**: Separação clara entre código, dados, assets e documentação
2. **Manutenibilidade**: Fácil localização e modificação de componentes
3. **Escalabilidade**: Estrutura preparada para crescimento do projeto
4. **Boas Práticas**: Segue padrões da comunidade Python
5. **Modularidade**: Componentes independentes e reutilizáveis
