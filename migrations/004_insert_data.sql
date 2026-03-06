-- Migration 004: Inserção de dados iniciais do inventário
-- Data: 2025-12-08
-- Descrição: Carrega dados dos CSVs de aplicações e GMUDs

BEGIN;

-- Inserir produtos únicos
INSERT INTO produtos (nome, descricao) 
VALUES 
    ('TOPUP', 'Sistema de recarga e top-up'),
    ('SPB', 'Sistema de Pagamentos Brasileiro'),
    ('Rutas', 'Sistema de rotas e logística')
ON CONFLICT (nome) DO NOTHING;

-- Inserir aplicações do inventário
INSERT INTO aplicacoes (
    nome_aplicacao, produto_id, ambiente, tipo_aplicacao, framework, 
    ferramenta_versionamento, tipo_pipeline, versao, hospedagem,
    sbom, scan_imagens, secret_manager, sast_sonarqube,
    data_ultima_revisao, data_criacao
)
SELECT 
    nome_app, 
    p.id,
    CASE WHEN amb IN ('N/A', '') THEN NULL ELSE amb END,
    CASE WHEN tipo IN ('N/A', '') THEN NULL ELSE tipo END,
    CASE WHEN fw IN ('N/A', '') THEN NULL ELSE fw END,
    CASE WHEN fv IN ('N/A', '') THEN NULL ELSE fv END,
    CASE WHEN tp IN ('N/A', '') THEN NULL ELSE tp END,
    CASE WHEN ver IN ('N/A', '') THEN NULL ELSE ver END,
    CASE WHEN hosp IN ('N/A', '') THEN NULL ELSE hosp END,
    CASE WHEN sb = 'Sim' THEN TRUE WHEN sb = 'Não' THEN FALSE ELSE NULL END,
    CASE WHEN si = 'Sim' THEN TRUE WHEN si = 'Não' THEN FALSE ELSE NULL END,
    CASE WHEN sm = 'Sim' THEN TRUE WHEN sm = 'Não' THEN FALSE ELSE NULL END,
    CASE WHEN sast = 'Sim' THEN TRUE WHEN sast = 'Não' THEN FALSE ELSE NULL END,
    dur::date,
    dc::date
FROM (VALUES
    ('PreparePixIn', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '2.1', 'EKS', 'Sim', 'Sim', 'Sim', 'Não', '2025-11-27', '2024-01-15'),
    ('TopUpPreAuthorization', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-04', '2023-06-10'),
    ('CancelTopUpWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.4.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-04', '2023-08-22'),
    ('ConsultExternalTokenWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.1', 'EC2', 'Sim', 'Não', 'Sim', 'Não', '2025-12-03', '2023-09-05'),
    ('SettleTopUpFeeWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.4', 'EC2', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2023-07-18'),
    ('GetTopUpProducts', 'TOPUP', 'Produção', 'API', 'NET 6', 'Azure Repos', 'Classic', '1.0.1', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2023-05-12'),
    ('CheckConfirmationTopUpV2Worker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.1', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2024-02-20'),
    ('GenerateTopUp', 'TOPUP', 'Produção', 'API', 'NET 6', 'Azure Repos', 'YAML', '1.2.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2023-04-08'),
    ('UpdateTopUpProducts', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.0', 'EC2', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2023-10-30'),
    ('topupauthorizationv2', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '2.0.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2024-03-15'),
    ('CheckConfirmationTopUpWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.0.4.0', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2023-06-25'),
    ('AuthorizationTopUpWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.5.2', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2023-11-08'),
    ('ConfirmTopUp', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.3.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2023-12-01'),
    ('ProcessTopUpWorker', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '2.1.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2024-01-20'),
    ('GetTopUpById', 'TOPUP', 'Produção', 'API', 'NET 6', 'Azure Repos', 'YAML', '1.0.1.0', 'EC2', 'Sim', 'Não', 'Sim', 'Não', '2025-12-03', '2023-07-05'),
    ('ConsultExternalTokenWorkerV2', 'TOPUP', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.0', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2024-04-12'),
    ('SettleTopUpFeeV2Worker', 'SPB', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.0', 'EC2', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2024-05-08'),
    ('GetTopUpProductsByPhone', 'SPB', 'Produção', 'API', 'NET 6', 'Azure Repos', 'YAML', '1.0', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2023-08-15'),
    ('SendXMLMessage', 'SPB', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.0.0', 'EKS', 'Não', 'Não', 'Sim', 'Não', '2025-12-02', '2023-09-20'),
    ('ReceiveMessageWorker', 'SPB', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'EC2', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2023-10-05'),
    ('app-qaops-rutas-prod', 'Rutas', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2024-01-30'),
    ('app-rutas-prod', 'Rutas', 'Produção', 'Web Application', 'React', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2024-02-15'),
    ('rutas-api-prod', 'Rutas', 'Produção', 'API', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Sim', 'Não', 'Sim', 'Não', '2025-12-03', '2024-03-01'),
    ('rutas-webhook-prod', 'Rutas', 'Produção', 'API', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2024-03-20'),
    ('rutas-worker-api-elasticlogger-prod', 'Rutas', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2024-04-01'),
    ('rutas-worker-api-mailnotification-prod', 'Rutas', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2024-04-15'),
    ('rutas-worker-api-smsnotification-prod', 'Rutas', 'Produção', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2024-05-01'),
    -- Aplicações Sandbox
    ('PreparePixIn', 'TOPUP', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '2.1', 'EKS', 'Sim', 'Sim', 'Sim', 'Não', '2025-11-27', '2024-01-15'),
    ('TopUpPreAuthorization', 'TOPUP', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-04', '2023-06-10'),
    ('GetTopUpProducts', 'TOPUP', 'Sandbox', 'API', 'NET 6', 'Azure Repos', 'Classic', '1.0.1', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2023-05-12'),
    ('UpdateTopUpProducts', 'TOPUP', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0.0', 'EC2', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2023-10-30'),
    ('ConfirmTopUp', 'TOPUP', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.3.0', 'EKS', 'Sim', 'Sim', 'Sim', 'Sim', '2025-12-03', '2023-12-01'),
    ('ConsultExternalTokenWorkerV2', 'TOPUP', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'YAML', '1.0', 'EC2', 'Sim', 'Sim', 'Sim', 'Não', '2025-12-03', '2024-04-12'),
    ('app-qaops-rutas-prod', 'Rutas', 'Sandbox', 'Worker', 'NET 6', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2024-01-30'),
    ('app-rutas-prod', 'Rutas', 'Sandbox', 'Web Application', 'React', 'Azure Repos', 'Classic', '1.0', 'Cloud Run', 'Não', 'Não', 'Sim', 'Não', '2025-12-03', '2024-02-15')
) AS data(nome_app, prod, amb, tipo, fw, fv, tp, ver, hosp, sb, si, sm, sast, dur, dc)
JOIN produtos p ON p.nome = data.prod;

-- Inserir GMUDs (amostra dos principais registros)
-- Nota: nome_aplicacao é armazenado na tabela mas não usado nas funções
INSERT INTO gmuds (
    id_item, data_hora_prevista, responsavel_executor, tempo_estimado,
    solicitante_area, nome_aplicacao, aplicacao_id, ambiente, hostname_namespace,
    local_implantacao, build_release, configuracoes_alteradas,
    tempo_realizado, ocorrencias, solucoes_atribuidas, validacoes_realizadas,
    risco_operacao, impacto, rca, controle
)
SELECT 
    id_item,
    CASE 
        WHEN data_prev ~ '^\d{2}/\d{2}/\d{2} \d{1,2}:\d{2}$' 
        THEN TO_TIMESTAMP(data_prev, 'DD/MM/YY HH24:MI')
        ELSE NULL 
    END,
    resp,
    tempo_est,
    solic,
    app_nome,
    a.id,
    CASE WHEN amb IN ('N/A', '') THEN NULL ELSE amb END,
    CASE WHEN host IN ('N/A', '') THEN NULL ELSE host END,
    CASE WHEN local IN ('N/A', '') THEN NULL ELSE local END,
    CASE WHEN build IN ('N/A', '') THEN NULL ELSE build END,
    CASE WHEN configs IN ('N/A', '') THEN NULL ELSE configs END,
    CASE WHEN tempo_real IN ('N/A', '') THEN NULL ELSE tempo_real END,
    CASE WHEN ocorr IN ('N/A', '') THEN NULL ELSE ocorr END,
    CASE WHEN soluc IN ('N/A', '') THEN NULL ELSE soluc END,
    CASE WHEN valid IN ('N/A', '') THEN NULL ELSE valid END,
    CASE 
        WHEN UPPER(risco_val) IN ('BAIXO', 'BAIXA') THEN 'Baixo'
        WHEN UPPER(risco_val) IN ('MÉDIO', 'MEDIA') THEN 'Médio'
        WHEN UPPER(risco_val) IN ('ALTO', 'ALTA') THEN 'Alto'
        WHEN UPPER(risco_val) IN ('ALTISSIMO', 'ALTISSIMA') THEN 'Altíssimo'
        ELSE NULL
    END,
    CASE WHEN imp IN ('N/A', '') THEN NULL ELSE imp END,
    CASE WHEN rca_val IN ('N/A', '') THEN NULL ELSE rca_val END,
    CASE WHEN ctrl IN ('N/A', '') THEN NULL ELSE ctrl END
FROM (VALUES
    ('238173', '25/11/25 7:00', 'Daiana Lima', '20min', 'Osmar Graner', 'PreparePixIn', 'Sandbox', NULL, 'EKS', 'Link do Build e Link do Release', 'Chave adicionada ao config: AddDays', '30min', 'N/A', 'N/A', '1) Configs validados no repositório e no servidor 2) Execução de logs do pipeline conferida', 'Alto', 'Janela cancelada devido a extensão do horário', NULL, 'Conferido por (nome da pessoa)'),
    ('745641', '25/11/25 7:00', 'Gustavo Miguel Brandão', '1h', 'Natanael Vieira Barboza', 'ADMIN', 'Sandbox', 'Sandboxsites', 'Windows', 'https://dev.azure.com/fitbank/Fit/_build?definitionId=133&_a=summary', 'N/A', '1h', 'N/A', 'N/A', '1) Configs validados no repositório e no servidor', 'Alto', 'N/A', NULL, 'Conferido por Daiana Menezes Lima'),
    ('347187', '25/11/25 11:21', 'Gustavo Miguel Brandão', '1h', 'Alimpio Brito Rodrigues', 'GenerateBoletoOut', 'Produção', 'PRD-SRV-SP1A-01', 'Windows', 'https://dev.azure.com/fitbank/Fit/_build/results?buildId=171491&view=results', 'RunThreadSantander=false SantanderMaxThreads=10', '1h', 'Motivo: Devido a alta volumetria de pagamentos. Impacto: Aumento no tempo de SLA do cliente', 'Serviço duplicado no servidor PRD-SRV-SP1A-02', '1) Configs validados no repositório e no servidor', 'Alto', 'Diminuição no tempo de SLA do cliente', NULL, 'Conferido por Daiana Menezes Lima'),
    ('743206', '25/11/25 14:10', 'Antonia Micaele Tomaz Silva', '20min', 'Francisco Alex Sousa Anchiêta', 'GenerateBoletoOutItau', 'Sandbox', 'payments-sbx', 'EKS', 'https://dev.azure.com/fitbank/Fit/_releaseProgress?_a=release-pipeline-progress&releaseId=291497', 'Chaves alteradas: CertificatePath e PrivateKeyFile', '1min', 'N/A', 'N/A', '1) Configs validados no repositório e no servidor', 'Baixo', 'N/A pois ainda não tem nenhum cliente configurado', NULL, 'Conferido por Daiana Menezes Lima'),
    ('745005', '25/11/25 16:19', 'Antonio Cavalcante de Macedo Neto', '5min', 'Thiago Costa Barros', 'GenericSendWebhookPaymentsBoletoOutStatusClient', 'Produção', 'payments', 'EKS', 'https://dev.azure.com/fitbank/Fit/_releaseProgress?_a=release-pipeline-progress&releaseId=291556', 'Chave adicionada ao config: OSBEndpoint', '1min', 'Motivo: Cliente começou a operar com OSB e precisa da dupla URL nos envios de webhook', 'N/A', '1) Configs validados no repositório e no servidor', 'Baixo', 'N/A', NULL, 'Conferido por Daiana Menezes Lima'),
    ('347227', '25/11/25 16:04', 'Caio Alberto Ferreira', '1min', 'Francisco Litien Alexandre Bezerra', 'ConsultOfStatusAutomaticPixMQ', 'Sandbox', 'core-sbx', 'EKS', 'https://dev.azure.com/fitbank/Fit/_releaseProgress?_a=release-pipeline-progress&releaseId=291504', 'Chaves alteradas: DefaultUserId', '1min', 'Motivo: Valor antigo da chave DefaultUserId estava errado na config', '1) Troca do valor da chave para o valor correto', '1) Configs Validados no repositorio e no cluster', 'Baixo', 'N/A', NULL, 'Conferido por Daiana Menezes Lima'),
    ('347231', '25/11/25 18:27', 'Caio Alberto Ferreira', '5min', 'Francisco Alex Sousa Anchiêta', 'GenerateBoletoOutItau', 'Produção', 'payments', 'EKS', 'https://dev.azure.com/fitbank/Fit/_releaseProgress?releaseId=291944&_a=release-pipeline-progress', 'Configs PVC adicionadas', '1min', 'Motivo: a aplicação tem necessidade de utilizar um certificado para funcionar corretamente', '1) adicionar configurações PVC e PVC com o caminho indicado do arquivo', '1) validação da config no cluster 2) validação se o serviço está executando corretamente', 'Baixo', 'N/A', NULL, 'Conferido por Daiana Menezes Lima'),
    ('347232', '25/11/25 15:52', 'Witalo Vieira Melo', '5min', 'Antonio Cavalcante de Macedo Neto', 'ValidateCnab', 'Produção', 'CnabIO', 'Windows', 'https://dev.azure.com/fitbank/Infra/_git/Fit.Configs/commit/047de8672ac06b337526252137221eaeb167ad6c', 'Chaves alteradas: RunWorkerService e PrivateKeyFile', '5min', 'Motivo: Outlayers SLA Operação JPM - CNAB', 'N/A', '1) Configs validados no repositório e no servidor', 'Alto', 'Melhorar os tempos do processamento dos arquivos do Cnab', NULL, 'Conferido por Daiana Menezes Lima'),
    ('745826', '26/11/25 10:02', 'João Paulo Ribeiro Coelho', '1h', 'Antonia Micaele Tomaz Silva', 'ADMIN', 'Preprodução', 'FITSITES1C2', 'Windows', 'Pipelines - Run 20251126.1', 'N/A', '1h', 'JANELA', 'https://dev.azure.com/fitbank/d3cf5213-5493-4696-b832-b11318d2a72d/_git/bf8bd5fa-8356-4ab0-b390-ce7112de208c/pullrequest/61292', 'Config: OK Não alterado', 'Alto', 'N/A', NULL, 'Conferido por Daiana Menezes Lima'),
    ('745130', '26/11/25 8:12', 'João Paulo Ribeiro Coelho', '1h', 'Francisco Litien alexandre Bezerra', 'APIREST [PIX]', 'Produção', 'PRD-ST-SP1A-08', 'Windows', 'Pipelines - Run 20251126.2', 'N/A', '1h', 'JANELA', 'https://dev.azure.com/fitbank/d3cf5213-5493-4696-b832-b11318d2a72d/_git/bf8bd5fa-8356-4ab0-b390-ce7112de208c/pullrequest/61273', 'Config: OK Não alterado', 'Alto', 'Parada operacional ao Cliente', NULL, 'Conferido por Daiana Menezes Lima')
) AS data(id_item, data_prev, resp, tempo_est, solic, app_nome, amb, host, local, build, configs, tempo_real, ocorr, soluc, valid, risco_val, imp, rca_val, ctrl)
LEFT JOIN aplicacoes a ON a.nome_aplicacao = data.app_nome AND a.ambiente = data.amb;

COMMIT;

-- Verificar dados inseridos
SELECT 'Produtos inseridos:' AS info, COUNT(*) AS total FROM produtos
UNION ALL
SELECT 'Aplicações inseridas:', COUNT(*) FROM aplicacoes
UNION ALL
SELECT 'GMUDs inseridas:', COUNT(*) FROM gmuds;
