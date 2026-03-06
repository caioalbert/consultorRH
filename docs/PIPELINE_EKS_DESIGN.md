# Pipeline CI/CD - Deploy EKS (Amazon Elastic Kubernetes Service)

> **📌 Versão Simplificada e Otimizada**  
> Esta pipeline foi otimizada para simplicidade operacional, removendo complexidade desnecessária enquanto mantém as melhores práticas essenciais.

## 🔄 Mudanças Principais

### ✅ Removido (Simplificação)
- ❌ Service Mesh (Istio) - Complexidade desnecessária para aplicação stateless
- ❌ Prometheus/Grafana - Substituído por CloudWatch Container Insights (nativo)
- ❌ SAST/DAST scanning - Removido da pipeline (pode ser feito separadamente)
- ❌ Testes unitários/integração automáticos - Foco em smoke tests
- ❌ Canary/Blue-Green deployment - Substituído por Rolling Update
- ❌ Redis - Não necessário para esta aplicação
- ❌ Performance tests (K6) - Desnecessário para BI dashboard interno

### ✅ Mantido (Essencial)
- ✅ Linting informativo (YAML, Python, Dockerfile) - Non-blocking
- ✅ Trivy scanning - Apenas vulnerabilidades CRITICAL
- ✅ Rolling Update deployment - Zero downtime garantido
- ✅ Auto-scaling (HPA) - Escalabilidade automática
- ✅ CloudWatch monitoring - Nativo e integrado
- ✅ Smoke tests - Validação básica pós-deploy
- ✅ Health checks - Liveness e Readiness probes
- ✅ Secrets management - AWS Secrets Manager

### 🎯 Estratégia de Deploy Escolhida

**Rolling Update** foi selecionado após análise da aplicação:

**Justificativa:**
1. **Aplicação Stateless**: Streamlit dashboard sem sessões persistentes
2. **Leitura de dados**: CSV/Excel (sem transações críticas)
3. **Simplicidade**: Menos componentes para gerenciar
4. **Custo-benefício**: Sem infraestrutura duplicada
5. **Zero downtime**: `maxUnavailable: 0` garante disponibilidade

**Configuração:**
- `maxSurge: 1` - Permite 1 pod extra durante update
- `maxUnavailable: 0` - Zero pods indisponíveis
- Health checks rigorosos - Garante pods saudáveis

---

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura da Pipeline](#arquitetura-da-pipeline)
3. [Requisitos e Pré-requisitos](#requisitos-e-pré-requisitos)
4. [Estrutura de Arquivos](#estrutura-de-arquivos)
5. [Stages da Pipeline](#stages-da-pipeline)
6. [Configurações Kubernetes](#configurações-kubernetes)
7. [Estratégia de Deploy](#estratégia-de-deploy)
8. [Segurança e Secrets](#segurança-e-secrets)
9. [Monitoramento e Observabilidade](#monitoramento-e-observabilidade)
10. [Rollback e Disaster Recovery](#rollback-e-disaster-recovery)
11. [Checklist de Implementação](#checklist-de-implementação)
12. [Melhores Práticas](#melhores-práticas-implementadas)

---

## 🎯 Visão Geral

Pipeline CI/CD completa para deploy da aplicação **Sistema de BI - Inventário de Aplicações** no Amazon EKS, implementando:

- ✅ Build multi-stage otimizado
- ✅ Validação de código (linting informativo)
- ✅ Deploy progressivo (Rolling Update com validação)
- ✅ Auto-scaling horizontal e vertical
- ✅ Gestão de secrets com AWS Secrets Manager
- ✅ Monitoramento nativo do EKS/CloudWatch

---

## 🏗️ Arquitetura da Pipeline

### Fluxo de Stages

```mermaid
graph LR
    A[Code Checkout] --> B[Validation/Lint]
    B --> C[Build]
    C --> D[Push Image]
    D --> E[Deploy Dev]
    E --> F[Smoke Tests]
    F --> G[Deploy Staging]
    G --> H[Smoke Tests]
    H --> I[Deploy Production]
    I --> J[Health Check]
```

### Componentes da Aplicação

- **Frontend**: Streamlit (Python) - Dashboard interativo
- **Backend**: Python (Pandas, Plotly, ECharts)
- **Database**: PostgreSQL (opcional - para persistência futura)
- **Storage**: S3 para arquivos CSV/Excel
- **Load Balancer**: AWS ALB

---

## 📦 Requisitos e Pré-requisitos

### Ferramentas Necessárias

| Ferramenta | Versão Mínima | Propósito |
|------------|---------------|-----------|
| Docker | 24.0+ | Build de imagens |
| Kustomize | 5.0+ | Deploy Kubernetes (já incluso no kubectl 1.14+) |
| kubectl | 1.28+ | Gerenciamento K8s |
| AWS CLI | 2.x | Integração AWS |
| eksctl | 0.160+ | Gerenciamento EKS |
| Trivy | 0.48+ | Security scanning (imagens) |
| Hadolint | 2.12+ | Dockerfile linting |
| yamllint | 1.33+ | YAML validation |
| kubeconform | 0.6+ | Kubernetes manifest validation |

### Permissões AWS IAM

```yaml
# Permissões necessárias para a pipeline
Policies:
  - ECR: 
      - ecr:GetAuthorizationToken
      - ecr:BatchCheckLayerAvailability
      - ecr:PutImage
      - ecr:InitiateLayerUpload
      - ecr:UploadLayerPart
      - ecr:CompleteLayerUpload
  
  - EKS:
      - eks:DescribeCluster
      - eks:ListClusters
      - eks:UpdateClusterConfig
  
  - SecretsManager:
      - secretsmanager:GetSecretValue
      - secretsmanager:DescribeSecret
  
  - S3:
      - s3:PutObject
      - s3:GetObject
      - s3:ListBucket
```

### Secrets Requeridos

```yaml
# Azure DevOps Library Secrets
AWS_ACCESS_KEY_ID: "AKIAXXXXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY: "secret-key"
AWS_REGION: "sa-east-1"
ECR_REGISTRY: "676949161726.dkr.ecr.sa-east-1.amazonaws.com"
EKS_CLUSTER_NAME: "EKS-STAGE-01"
DOCKER_HUB_USERNAME: "optional-for-caching"
DOCKER_HUB_TOKEN: "optional-for-caching"
SLACK_WEBHOOK: "for-notifications"
```

---

## 📁 Estrutura de Arquivos

### Estrutura Completa do Projeto

```
DevOpsHub/
├── .azure-pipelines/
│   ├── azure-pipelines.yml              # Pipeline principal
│   ├── templates/
│   │   ├── build-stage.yml              # Stage de build
│   │   ├── test-stage.yml               # Stage de testes
│   │   ├── security-stage.yml           # Stage de segurança
│   │   ├── deploy-stage.yml             # Stage de deploy
│   │   └── rollback-stage.yml           # Stage de rollback
│   └── variables/
│       ├── common.yml                   # Variáveis comuns
│       ├── dev.yml                      # Variáveis dev
│       ├── staging.yml                  # Variáveis staging
│       └── production.yml               # Variáveis produção
│
├── k8s/
│   ├── base/                            # Configurações base (Kustomize)
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── ingress.yaml
│   │   ├── hpa.yaml
│   │   ├── pdb.yaml
│   │   ├── serviceaccount.yaml
│   │   ├── rbac.yaml
│   │   ├── networkpolicy.yaml
│   │   └── external-secrets.yaml
│   │
│   └── overlays/                        # Overlays por ambiente
│       ├── dev/
│       │   ├── kustomization.yaml
│       │   ├── configmap-patch.yaml
│       │   ├── deployment-patch.yaml
│       │   └── namespace-patch.yaml
│       ├── staging/
│       │   ├── kustomization.yaml
│       │   ├── configmap-patch.yaml
│       │   ├── deployment-patch.yaml
│       │   ├── ingress-patch.yaml
│       │   └── namespace-patch.yaml
│       └── production/
│           ├── kustomization.yaml
│           ├── configmap-patch.yaml
│           ├── deployment-patch.yaml
│           ├── ingress-patch.yaml
│           ├── hpa-patch.yaml
│           └── namespace-patch.yaml
│
├── docker/
│   ├── Dockerfile                    # Multi-stage production
│   ├── Dockerfile.dev                # Development
│   ├── .dockerignore
│   └── healthcheck.sh                # Health check script
│
├── scripts/
│   ├── deploy/
│   │   ├── pre-deploy.sh             # Validações pré-deploy
│   │   ├── post-deploy.sh            # Validações pós-deploy
│   │   ├── rollback.sh               # Script de rollback
│   │   └── smoke-tests.sh            # Smoke tests
│   ├── security/
│   │   ├── scan-image.sh             # Trivy scan
│   │   └── check-secrets.sh          # Secret detection
│   └── utils/
│       ├── cleanup.sh                # Limpeza
│       └── notify.sh                 # Notificações
│
├── tests/
│   ├── unit/                         # Testes unitários (futuros)
│   └── smoke/                        # Smoke tests básicos
│       └── health-check.sh
│
└── monitoring/
    └── cloudwatch/
        └── dashboard.json
```

---

## 🔄 Stages da Pipeline

### Pipeline Principal (azure-pipelines.yml)

```yaml
name: $(Build.BuildId)-$(Date:yyyyMMdd)$(Rev:.r)

trigger:
  branches:
    include:
      - main
      - develop
      - release/*
  paths:
    exclude:
      - docs/**
      - README.md

pr:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/**

pool:
  name: Self-HostedARM64v8

variables:
  - template: variables/common.yml
  - name: isMain
    value: $[eq(variables['Build.SourceBranch'], 'refs/heads/main')]
  - name: isDevelop
    value: $[eq(variables['Build.SourceBranch'], 'refs/heads/develop')]

stages:
  # ========================================
  # STAGE 1: VALIDATION & LINTING (NON-BLOCKING)
  # ========================================
  - stage: Validation
    displayName: '🔍 Code Validation & Linting'
    jobs:
      - job: LintYAML
        displayName: 'Lint YAML Files'
        continueOnError: true  # Non-blocking
        steps:
          - checkout: self
          
          - script: |
              pip install yamllint
              yamllint -c .yamllint.yml k8s/ helm/ || echo "⚠️ YAML lint issues found (non-blocking)"
            displayName: 'YAML Lint Check (Informational)'
          
          - script: |
              # Install kubeconform
              wget https://github.com/yannh/kubeconform/releases/latest/download/kubeconform-linux-arm64.tar.gz
              tar xf kubeconform-linux-arm64.tar.gz
              sudo mv kubeconform /usr/local/bin/
              
              # Validate Kubernetes manifests
              kubeconform -summary -output json k8s/base/*.yaml || echo "⚠️ Kubernetes manifest issues found (non-blocking)"
            displayName: 'Kubernetes Manifest Validation (Informational)'
      
      - job: LintDockerfile
        displayName: 'Lint Dockerfile'
        continueOnError: true  # Non-blocking
        steps:
          - checkout: self
          
          - script: |
              docker run --rm -i hadolint/hadolint < docker/Dockerfile || echo "⚠️ Dockerfile lint issues found (non-blocking)"
            displayName: 'Hadolint - Dockerfile Best Practices (Informational)'
      
      - job: LintPython
        displayName: 'Lint Python Code'
        continueOnError: true  # Non-blocking
        steps:
          - checkout: self
          
          - script: |
              pip install flake8 black
              echo "🔍 Running flake8..."
              flake8 app.py src/ --max-line-length=120 --extend-ignore=E501,W503 || echo "⚠️ flake8 issues found"
              
              echo "🔍 Running black check..."
              black --check app.py src/ || echo "⚠️ black formatting issues found"
            displayName: 'Python Code Quality Check (Informational)'

  # ========================================
  # STAGE 2: BUILD & PUSH
  # ========================================
  - stage: Build
    displayName: '🏗️ Build & Push'
    dependsOn: []  # Run in parallel with Validation
    jobs:
      - job: BuildImage
        displayName: 'Build Docker Image'
        steps:
          - checkout: self
          
          - script: |
              # Build multi-stage Docker image
              docker build \
                --platform=linux/arm64 \
                --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
                --build-arg VCS_REF=$(Build.SourceVersion) \
                --build-arg VERSION=$(Build.BuildId) \
                --cache-from $(registry)/$(imageName):cache \
                --tag $(imageName):$(Build.BuildId) \
                --tag $(imageName):latest \
                -f docker/Dockerfile \
                .
            displayName: 'Docker Build with Cache'
            env:
              DOCKER_BUILDKIT: 1
          
          - script: |
              # Trivy Image Scan - Only fail on CRITICAL vulnerabilities
              trivy image \
                --severity CRITICAL \
                --exit-code 1 \
                --no-progress \
                --format json \
                --output trivy-report.json \
                $(imageName):$(Build.BuildId) || echo "⚠️ Vulnerabilities found - review trivy-report.json"
            displayName: 'Trivy - Container Image Scan (Critical Only)'
            continueOnError: true
          
          - task: PublishBuildArtifacts@1
            inputs:
              PathtoPublish: 'trivy-report.json'
              ArtifactName: 'security-reports'
            displayName: 'Publish Security Reports'
            condition: always()
          
          - script: |
              # Push to ECR
              aws ecr get-login-password --region $(awsRegion) | \
                docker login --username AWS --password-stdin $(registry)
              
              docker tag $(imageName):$(Build.BuildId) $(registry)/$(imageName):$(Build.BuildId)
              docker tag $(imageName):$(Build.BuildId) $(registry)/$(imageName):latest
              
              docker push $(registry)/$(imageName):$(Build.BuildId)
              docker push $(registry)/$(imageName):latest
            displayName: 'Push Image to ECR'
            env:
              AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
          
          - script: |
              # Cleanup
              docker rmi $(imageName):$(Build.BuildId) || true
              docker rmi $(imageName):latest || true
              docker rmi $(registry)/$(imageName):$(Build.BuildId) || true
              docker rmi $(registry)/$(imageName):latest || true
              docker system prune -af --volumes
            displayName: 'Docker Cleanup'
            condition: always()

  # ========================================
  # STAGE 3: DEPLOY TO DEV
  # ========================================
  - stage: DeployDev
    displayName: '🚀 Deploy to Development'
    dependsOn: Build
    condition: and(succeeded(), eq(variables.isDevelop, true))
    jobs:
      - deployment: DeployDev
        displayName: 'Deploy to Dev Environment'
        environment: 'development'
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/deploy-stage.yml
                  parameters:
                    environment: 'dev'
                    cluster: 'EKS-DEV-01'
                    namespace: 'devopshub-dev'
                    overlay: 'dev'
                    imageTag: '$(Build.BuildId)'
      
      - job: SmokeTestDev
        displayName: 'Smoke Tests - Dev'
        dependsOn: DeployDev
        steps:
          - checkout: self
          
          - script: |
              # Wait for deployment to stabilize
              sleep 30
              
              # Basic health check
              bash scripts/deploy/smoke-tests.sh $(devAppUrl)
            displayName: 'Run Smoke Tests'

  # ========================================
  # STAGE 4: DEPLOY TO STAGING
  # ========================================
  - stage: DeployStaging
    displayName: '🚀 Deploy to Staging'
    dependsOn: DeployDev
    condition: and(succeeded(), eq(variables.isMain, true))
    jobs:
      - deployment: DeployStaging
        displayName: 'Deploy to Staging Environment'
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/deploy-stage.yml
                  parameters:
                    environment: 'staging'
                    cluster: 'EKS-STAGE-01'
                    namespace: 'devopshub-staging'
                    overlay: 'staging'
                    imageTag: '$(Build.BuildId)'
      
      - job: SmokeTestStaging
        displayName: 'Smoke Tests - Staging'
        dependsOn: DeployStaging
        steps:
          - checkout: self
          
          - script: |
              # Wait for deployment to stabilize
              sleep 30
              
              # Basic health check
              bash scripts/deploy/smoke-tests.sh $(stagingAppUrl)
            displayName: 'Run Smoke Tests'

  # ========================================
  # STAGE 5: DEPLOY TO PRODUCTION (ROLLING UPDATE)
  # ========================================
  - stage: DeployProduction
    displayName: '🚀 Deploy to Production'
    dependsOn: DeployStaging
    condition: and(succeeded(), eq(variables.isMain, true))
    jobs:
      - deployment: DeployProduction
        displayName: 'Production Deployment (Rolling Update)'
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/deploy-stage.yml
                  parameters:
                    environment: 'production'
                    cluster: 'EKS-PROD-01'
                    namespace: 'devopshub-prod'
                    overlay: 'production'
                    imageTag: '$(Build.BuildId)'
                    deploymentStrategy: 'rollingupdate'
                    
                - script: |
                    # Monitor rollout
                    kubectl rollout status deployment/devopshub \
                      -n devopshub-prod \
                      --timeout=10m
                  displayName: 'Monitor Deployment Rollout'
                  env:
                    AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
                    AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
      
      - job: PostDeployValidation
        displayName: 'Post-Deploy Validation'
        dependsOn: DeployProduction
        steps:
          - checkout: self
          
          - script: |
              # Wait for pods to be ready
              sleep 60
              
              # Health check
              bash scripts/deploy/post-deploy.sh $(productionAppUrl)
            displayName: 'Post-Deploy Health Check'
          
          - script: |
              # Verify all pods are running
              kubectl get pods -n devopshub-prod -l app=devopshub
              
              # Check deployment status
              kubectl get deployment devopshub -n devopshub-prod -o wide
            displayName: 'Verify Deployment Status'
            env:
              AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
          
          - script: |
              # Send success notification
              bash scripts/utils/notify.sh "✅ Production deployment successful - Build $(Build.BuildId)"
            displayName: 'Send Success Notification'
```

---

## ☸️ Configurações Kubernetes

### Por que Kustomize ao invés de Helm?

**Vantagens do Kustomize:**
- ✅ **Nativo do Kubernetes**: Integrado no kubectl (1.14+)
- ✅ **Declarativo puro**: YAML puro, sem templates complexos
- ✅ **Patches simples**: Sobrescreve apenas o necessário por ambiente
- ✅ **Sem dependências**: Não precisa instalar ferramentas extras
- ✅ **Fácil debugging**: `kubectl kustomize` mostra o resultado final
- ✅ **GitOps friendly**: Perfeito para ArgoCD/Flux

**Estrutura Kustomize:**
```
k8s/
├── base/              # Configurações comuns a todos os ambientes
└── overlays/          # Customizações específicas por ambiente
    ├── dev/
    ├── staging/
    └── production/
```

### Base Kustomization (k8s/base/kustomization.yaml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: devopshub

# Common labels para todos os recursos
commonLabels:
  app: devopshub
  managed-by: kustomize

# Common annotations
commonAnnotations:
  documentation: "https://github.com/org/devopshub"

# Recursos base
resources:
  - namespace.yaml
  - serviceaccount.yaml
  - rbac.yaml
  - configmap.yaml
  - external-secrets.yaml
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - hpa.yaml
  - pdb.yaml
  - networkpolicy.yaml

# ConfigMap generator (opcional)
configMapGenerator:
  - name: nginx-config
    files:
      - configs/nginx.conf

# Images (será sobrescrito pelos overlays)
images:
  - name: devopshub
    newName: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub
    newTag: latest
```

### Overlay Development (k8s/overlays/dev/kustomization.yaml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: devopshub-dev

# Referência à base
bases:
  - ../../base

# Nome prefix para evitar conflitos
namePrefix: dev-

# Labels adicionais
commonLabels:
  environment: dev

# Patch de namespace
patchesStrategicMerge:
  - namespace-patch.yaml
  - deployment-patch.yaml
  - configmap-patch.yaml

# Sobrescrever imagem
images:
  - name: devopshub
    newName: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub
    newTag: dev-latest

# Replicas para dev
replicas:
  - name: devopshub
    count: 2
```

### Deployment Patch Dev (k8s/overlays/dev/deployment-patch.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devopshub
spec:
  template:
    spec:
      containers:
        - name: devopshub
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "1Gi"
              cpu: "500m"
          env:
            - name: ENVIRONMENT
              value: "development"
            - name: LOG_LEVEL
              value: "DEBUG"
```

### ConfigMap Patch Dev (k8s/overlays/dev/configmap-patch.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: devopshub-config
data:
  LOG_LEVEL: "DEBUG"
  FEATURE_CICD_DASHBOARD: "true"
  FEATURE_SECOPS_DASHBOARD: "false"
  FEATURE_GOVERNANCA_DASHBOARD: "true"
  FEATURE_GMUD_DASHBOARD: "true"
```

### Namespace Patch Dev (k8s/overlays/dev/namespace-patch.yaml)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: devopshub-dev
  labels:
    environment: dev
```

### Overlay Staging (k8s/overlays/staging/kustomization.yaml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: devopshub-staging

bases:
  - ../../base

namePrefix: staging-

commonLabels:
  environment: staging

patchesStrategicMerge:
  - namespace-patch.yaml
  - deployment-patch.yaml
  - configmap-patch.yaml
  - ingress-patch.yaml

images:
  - name: devopshub
    newName: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub
    newTag: staging-latest

replicas:
  - name: devopshub
    count: 3
```

### Overlay Production (k8s/overlays/production/kustomization.yaml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: devopshub-prod

bases:
  - ../../base

# Sem prefix em produção
namePrefix: ""

commonLabels:
  environment: production

patchesStrategicMerge:
  - namespace-patch.yaml
  - deployment-patch.yaml
  - configmap-patch.yaml
  - ingress-patch.yaml
  - hpa-patch.yaml

images:
  - name: devopshub
    newName: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub
    # Tag será definido pela pipeline

replicas:
  - name: devopshub
    count: 5
```

### Deployment Patch Production (k8s/overlays/production/deployment-patch.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devopshub
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  
  template:
    spec:
      containers:
        - name: devopshub
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          env:
            - name: ENVIRONMENT
              value: "production"
            - name: LOG_LEVEL
              value: "INFO"
      
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - devopshub
              topologyKey: kubernetes.io/hostname
```

### HPA Patch Production (k8s/overlays/production/hpa-patch.yaml)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: devopshub-hpa
spec:
  minReplicas: 5
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Ingress Patch Production (k8s/overlays/production/ingress-patch.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: devopshub
  annotations:
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:sa-east-1:676949161726:certificate/prod-cert-xxx
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:sa-east-1:676949161726:regional/webacl/prod-waf-xxx
spec:
  rules:
    - host: devopshub.producao.com.br
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: devopshub
                port:
                  number: 80
```

### Template de Deploy Stage (templates/deploy-stage.yml)

```yaml
# Azure DevOps Pipeline Template for Kustomize Deploy
parameters:
  - name: environment
    type: string
  - name: cluster
    type: string
  - name: namespace
    type: string
  - name: overlay
    type: string
  - name: imageTag
    type: string
  - name: deploymentStrategy
    type: string
    default: 'rollingupdate'

steps:
  - checkout: self
  
  - script: |
      aws sts get-caller-identity
    displayName: 'Verify AWS Identity'
    env:
      AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
      AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
      AWS_DEFAULT_REGION: sa-east-1
  
  - script: |
      aws eks update-kubeconfig --region sa-east-1 --name ${{ parameters.cluster }}
    displayName: 'Configure kubeconfig for EKS'
    env:
      AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
      AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
      AWS_DEFAULT_REGION: sa-east-1
  
  - script: |
      kubectl version --client
      kubectl get nodes
    displayName: 'Verify kubectl connectivity'
  
  - script: |
      # Build kustomization with image tag
      cd k8s/overlays/${{ parameters.overlay }}
      
      # Update image tag in kustomization
      kustomize edit set image devopshub=$(registry)/$(imageName):${{ parameters.imageTag }}
      
      # Verify what will be deployed
      echo "=== Generated manifests preview ==="
      kubectl kustomize .
      
      # Apply to cluster
      echo "=== Applying to cluster ==="
      kubectl apply -k . --dry-run=client -o yaml
      kubectl apply -k .
    displayName: 'Deploy with Kustomize'
  
  - script: |
      # Wait for rollout to complete
      kubectl rollout status deployment/devopshub \
        -n ${{ parameters.namespace }} \
        --timeout=10m
    displayName: 'Wait for Rollout'
  
  - script: |
      # Verify deployment
      kubectl get pods -n ${{ parameters.namespace }} -l app=devopshub
      kubectl get deployment devopshub -n ${{ parameters.namespace }} -o wide
      kubectl get svc devopshub -n ${{ parameters.namespace }}
    displayName: 'Verify Deployment'
  
  - script: |
      echo "Deployment to ${{ parameters.environment }} completed successfully"
    displayName: 'Deploy Success'
```

### Comandos Úteis Kustomize

```bash
# Preview das mudanças (sem aplicar)
kubectl kustomize k8s/overlays/dev

# Preview com saída formatada
kubectl kustomize k8s/overlays/production | less

# Aplicar diretamente
kubectl apply -k k8s/overlays/dev

# Aplicar com validação
kubectl apply -k k8s/overlays/production --dry-run=server

# Deletar recursos
kubectl delete -k k8s/overlays/dev

# Diff antes de aplicar (requer kubectl diff plugin)
kubectl diff -k k8s/overlays/staging

# Build e salvar em arquivo
kubectl kustomize k8s/overlays/production > manifest.yaml

# Validar sintaxe
kubectl kustomize k8s/overlays/dev --enable-alpha-plugins

# Atualizar imagem dinamicamente
cd k8s/overlays/production
kustomize edit set image devopshub=registry/image:v1.2.3
kubectl apply -k .
```

---

## ☸️ Recursos Kubernetes Base

### 1. Namespace (k8s/base/namespace.yaml)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: devopshub
  labels:
    name: devopshub
    environment: base
    monitoring: enabled
  annotations:
    description: "Sistema de BI - Inventário de Aplicações DevOps"
```

### 2. ConfigMap Global (k8s/base/configmap.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: devopshub-config
  namespace: devopshub
  labels:
    app: devopshub
    component: config
data:
  # Application Settings
  APP_NAME: "DevOpsHub BI System"
  APP_VERSION: "1.0.0"
  LOG_LEVEL: "INFO"
  
  # Streamlit Settings
  STREAMLIT_SERVER_PORT: "8501"
  STREAMLIT_SERVER_ADDRESS: "0.0.0.0"
  STREAMLIT_SERVER_HEADLESS: "true"
  STREAMLIT_BROWSER_GATHER_USAGE_STATS: "false"
  STREAMLIT_SERVER_MAX_UPLOAD_SIZE: "200"
  STREAMLIT_SERVER_ENABLE_CORS: "false"
  
  # Database Settings (non-sensitive) - Optional for future use
  DB_HOST: "devopshub-postgres.devopshub.svc.cluster.local"
  DB_PORT: "5432"
  DB_NAME: "devopshub"
  DB_SSL_MODE: "require"
  
  # AWS Settings
  AWS_REGION: "sa-east-1"
  S3_BUCKET: "devopshub-data"
  S3_DATA_PATH: "inventory/"
  
  # Feature Flags
  FEATURE_CICD_DASHBOARD: "true"
  FEATURE_SECOPS_DASHBOARD: "true"
  FEATURE_GOVERNANCA_DASHBOARD: "true"
  FEATURE_GMUD_DASHBOARD: "true"
  
  # Monitoring
  HEALTH_CHECK_PATH: "/health"
  READINESS_CHECK_PATH: "/ready"
  
  # Data Files
  INVENTORY_FILE: "data/inventario_aplicacoes.csv"
  GMUD_FILE: "data/gmud_dados.csv"

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: devopshub
data:
  nginx.conf: |
    server {
        listen 80;
        server_name _;
        
        client_max_body_size 100M;
        
        location / {
            proxy_pass http://localhost:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }
        
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        location /ready {
            access_log off;
            return 200 "ready\n";
            add_header Content-Type text/plain;
        }
    }
```

### 3. External Secrets (k8s/base/external-secrets.yaml)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: devopshub
spec:
  provider:
    aws:
      service: SecretsManager
      region: sa-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: devopshub-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: devopshub-secrets
  namespace: devopshub
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  
  target:
    name: devopshub-secrets
    creationPolicy: Owner
  
  data:
    # Database Credentials (Optional - for future use)
    - secretKey: DB_USERNAME
      remoteRef:
        key: devopshub/database
        property: username
    
    - secretKey: DB_PASSWORD
      remoteRef:
        key: devopshub/database
        property: password
    
    # AWS Credentials
    - secretKey: AWS_ACCESS_KEY_ID
      remoteRef:
        key: devopshub/aws
        property: access_key_id
    
    - secretKey: AWS_SECRET_ACCESS_KEY
      remoteRef:
        key: devopshub/aws
        property: secret_access_key
    
    # API Keys (if needed)
    - secretKey: API_KEY
      remoteRef:
        key: devopshub/api
        property: key
```

### 4. Deployment com Best Practices (k8s/base/deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devopshub
  namespace: devopshub
  labels:
    app: devopshub
    version: v1
    tier: frontend
  annotations:
    kubernetes.io/change-cause: "Initial deployment"
spec:
  replicas: 3
  
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  
  revisionHistoryLimit: 10
  
  selector:
    matchLabels:
      app: devopshub
      version: v1
  
  template:
    metadata:
      labels:
        app: devopshub
        version: v1
        tier: frontend
    
    spec:
      serviceAccountName: devopshub-sa
      
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      
      # Anti-affinity para distribuir pods
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - devopshub
                topologyKey: kubernetes.io/hostname
      
      # Topology Spread
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: devopshub
      
      initContainers:
        # Migration init container
        - name: migration
          image: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub:latest
          command: ['python', 'migrations/migrate.py']
          envFrom:
            - configMapRef:
                name: devopshub-config
            - secretRef:
                name: devopshub-secrets
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
      
      containers:
        # Main application container
        - name: devopshub
          image: 676949161726.dkr.ecr.sa-east-1.amazonaws.com/devopshub:latest
          imagePullPolicy: Always
          
          ports:
            - name: http
              containerPort: 8501
              protocol: TCP
          
          envFrom:
            - configMapRef:
                name: devopshub-config
            - secretRef:
                name: devopshub-secrets
          
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
              ephemeral-storage: "1Gi"
            limits:
              memory: "2Gi"
              cpu: "1000m"
              ephemeral-storage: "2Gi"
          
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            successThreshold: 1
            failureThreshold: 3
          
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 15
            periodSeconds: 5
            timeoutSeconds: 3
            successThreshold: 1
            failureThreshold: 3
          
          startupProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 0
            periodSeconds: 5
            timeoutSeconds: 3
            successThreshold: 1
            failureThreshold: 30
          
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
            capabilities:
              drop:
                - ALL
          
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /.cache
            - name: config
              mountPath: /app/config
              readOnly: true
        
        # Sidecar: NGINX reverse proxy
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - name: http-proxy
              containerPort: 80
          resources:
            requests:
              memory: "64Mi"
              cpu: "50m"
            limits:
              memory: "128Mi"
              cpu: "100m"
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/conf.d
      
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
        - name: config
          configMap:
            name: devopshub-config
        - name: nginx-config
          configMap:
            name: nginx-config
      
      # DNS Config
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
          - name: ndots
            value: "2"
      
      # Termination grace period
      terminationGracePeriodSeconds: 30
```

### 11. Service (k8s/base/service.yaml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: devopshub
  namespace: devopshub
  labels:
    app: devopshub
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "tcp"
spec:
  type: ClusterIP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  
  ports:
    - name: http
      port: 80
      targetPort: http-proxy
      protocol: TCP
  
  selector:
    app: devopshub
    version: v1

---
apiVersion: v1
kind: Service
metadata:
  name: devopshub-headless
  namespace: devopshub
  labels:
    app: devopshub
spec:
  clusterIP: None
  ports:
    - name: http
      port: 8501
      targetPort: http
  selector:
    app: devopshub
```

### 12. Ingress com ALB (k8s/base/ingress.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: devopshub
  namespace: devopshub
  annotations:
    # AWS Load Balancer Controller
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    
    # Certificate Manager
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:sa-east-1:676949161726:certificate/xxx
    
    # Health Check
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
    
    # Security
    alb.ingress.kubernetes.io/security-groups: sg-xxxxx
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS-1-2-2017-01
    
    # Tags
    alb.ingress.kubernetes.io/tags: Environment=production,Application=devopshub
    
    # WAF
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:sa-east-1:676949161726:regional/webacl/xxx
spec:
  rules:
    - host: devopshub.exemplo.com.br
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: devopshub
                port:
                  number: 80
```

### 13. HPA - Horizontal Pod Autoscaler (k8s/base/hpa.yaml)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: devopshub-hpa
  namespace: devopshub
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: devopshub
  
  minReplicas: 3
  maxReplicas: 20
  
  metrics:
    # CPU Utilization
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    
    # Memory Utilization
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    
    # Custom Metric: Requests per second
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Min
    
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
        - type: Pods
          value: 4
          periodSeconds: 30
      selectPolicy: Max

---
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: devopshub-vpa
  namespace: devopshub
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: devopshub
  
  updatePolicy:
    updateMode: "Auto"
  
  resourcePolicy:
    containerPolicies:
      - containerName: devopshub
        minAllowed:
          cpu: 250m
          memory: 512Mi
        maxAllowed:
          cpu: 2000m
          memory: 4Gi
        controlledResources:
          - cpu
          - memory
```

### 14. PDB - Pod Disruption Budget (k8s/base/pdb.yaml)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: devopshub-pdb
  namespace: devopshub
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: devopshub
  unhealthyPodEvictionPolicy: AlwaysAllow
```

### 15. Network Policy (k8s/base/networkpolicy.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: devopshub-network-policy
  namespace: devopshub
spec:
  podSelector:
    matchLabels:
      app: devopshub
  
  policyTypes:
    - Ingress
    - Egress
  
  ingress:
    # Allow from ALB/Ingress
    - from:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: TCP
          port: 8501
        - protocol: TCP
          port: 80
  
  egress:
    # Allow DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
    
    # Allow PostgreSQL (optional - for future use)
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    
    # Allow HTTPS to external services (S3, AWS APIs)
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 443
```

### 16. Service Account & RBAC (k8s/base/serviceaccount.yaml)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: devopshub-sa
  namespace: devopshub
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::676949161726:role/DevOpsHubEKSRole

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: devopshub-role
  namespace: devopshub
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
  
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devopshub-rolebinding
  namespace: devopshub
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: devopshub-role
subjects:
  - kind: ServiceAccount
    name: devopshub-sa
    namespace: devopshub
```

---

## 🎯 Estratégia de Deploy

### Estratégia Recomendada: Rolling Update

**Análise da Aplicação:**
- **Tipo**: Aplicação Streamlit stateless (dashboard de visualização)
- **Estado**: Sem sessões críticas ou transações longas
- **Dados**: Leitura de CSV/Excel (sem escrita em tempo real)
- **Usuários**: Acesso para visualização de dashboards
- **Complexidade**: Baixa a média

**Por que Rolling Update?**

✅ **Simplicidade**: Menos complexidade operacional que Blue/Green ou Canary  
✅ **Zero Downtime**: Com `maxUnavailable: 0`, sempre há pods disponíveis  
✅ **Rollback Rápido**: `kubectl rollout undo` em caso de problemas  
✅ **Adequado para Stateless**: Perfeito para aplicações sem estado  
✅ **Menor Custo**: Não requer infraestrutura duplicada

**Configuração Recomendada:**

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Permite 1 pod adicional durante o update
    maxUnavailable: 0  # Zero pods indisponíveis (zero downtime garantido)

# Com 5 réplicas em produção:
# 1. Cria 1 novo pod (total: 6 pods)
# 2. Aguarda o novo pod ficar ready
# 3. Remove 1 pod antigo (total: 5 pods)
# 4. Repete até todos serem atualizados
```

**Health Checks para Garantir Segurança:**

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8501
  initialDelaySeconds: 15
  periodSeconds: 5
  failureThreshold: 3

livenessProbe:
  httpGet:
    path: /health
    port: 8501
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

**Quando NÃO usar Rolling Update:**

❌ Mudanças de schema de banco incompatíveis  
❌ Necessidade de testes A/B em produção  
❌ Requisitos regulatórios de validação prévia  
❌ Aplicações com estado crítico

**Alternativa para Casos Críticos: Blue/Green Simplificado**

Se precisar de validação mais rigorosa, use Blue/Green apenas em produção:

```bash
# 1. Deploy da versão green com Kustomize
kustomize build k8s/overlays/production | \
  sed 's/app: devopshub/app: devopshub-green/g' | \
  sed "s|image:.*|image: $(registry)/$(imageName):NEW_VERSION|g" | \
  kubectl apply -f -

# 2. Teste a versão green internamente
kubectl port-forward svc/devopshub-green 8501:80 -n devopshub-prod

# 3. Switch do Service para green
kubectl patch service devopshub -n devopshub-prod \
  -p '{"spec":{"selector":{"version":"green"}}}'

# 4. Após validação, remover blue
kubectl delete deployment devopshub-blue -n devopshub-prod
```

---

## 🔐 Segurança e Secrets

### AWS Secrets Manager Structure

```json
{
  "devopshub/database": {
    "username": "devopshub_user",
    "password": "SuperSecurePassword123!",
    "host": "devopshub-db.cluster-xxxxx.sa-east-1.rds.amazonaws.com",
    "port": "5432",
    "database": "devopshub"
  },
  "devopshub/aws": {
    "access_key_id": "AKIAXXXXXXXXXXXXXXXX",
    "secret_access_key": "secret-access-key-here",
    "region": "sa-east-1"
  },
  "devopshub/api": {
    "key": "api-key-here"
  }
}
```

### Security Scanning Tools Configuration

```yaml
# .trivyignore - Ignore known false positives
# CVE-2023-xxxxx

# .hadolint.yaml - Dockerfile linting rules
ignored:
  - DL3008  # Pin versions in apt-get install
  - DL3009  # Delete apt cache

trustedRegistries:
  - docker.io
  - gcr.io
  - 676949161726.dkr.ecr.sa-east-1.amazonaws.com

# .yamllint.yml
extends: default
rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

---

## 📊 Monitoramento e Observabilidade

### CloudWatch Container Insights

O monitoramento será realizado nativamente usando **AWS CloudWatch Container Insights**, eliminando a necessidade de Prometheus/Grafana.

**Vantagens:**
- ✅ Integração nativa com EKS
- ✅ Sem gerenciamento de infraestrutura adicional
- ✅ Métricas automáticas de pods, nodes, namespaces
- ✅ Logs centralizados
- ✅ Alarmes integrados com SNS

### Habilitando Container Insights

```bash
# Enable Container Insights no cluster EKS
aws eks update-cluster-config \
  --name EKS-PROD-01 \
  --region sa-east-1 \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# Install CloudWatch agent via Helm
helm repo add aws https://aws.github.io/eks-charts
helm install aws-cloudwatch-metrics aws/aws-cloudwatch-metrics \
  --namespace amazon-cloudwatch \
  --create-namespace \
  --set clusterName=EKS-PROD-01
```

### CloudWatch Dashboard JSON

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["ContainerInsights", "pod_cpu_utilization", {"stat": "Average"}],
          [".", "pod_memory_utilization", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "sa-east-1",
        "title": "DevOpsHub - Resource Utilization"
      }
    },
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ApplicationELB", "TargetResponseTime", {"stat": "Average"}],
          [".", "RequestCount", {"stat": "Sum"}],
          [".", "HTTPCode_Target_5XX_Count", {"stat": "Sum"}]
        ],
        "period": 60,
        "stat": "Sum",
        "region": "sa-east-1",
        "title": "DevOpsHub - Application Performance"
      }
    },
    {
      "type": "log",
      "properties": {
        "query": "SOURCE '/aws/containerinsights/EKS-PROD-01/application'\n| fields @timestamp, log\n| filter kubernetes.namespace_name = 'devopshub-prod'\n| sort @timestamp desc\n| limit 100",
        "region": "sa-east-1",
        "title": "DevOpsHub - Application Logs"
      }
    }
  ]
}
```

### CloudWatch Alarms

```yaml
# CloudWatch Alarms via Terraform/CloudFormation
alarms:
  - name: DevOpsHub-HighCPU
    metric: pod_cpu_utilization
    threshold: 80
    evaluation_periods: 2
    period: 300
    comparison: GreaterThanThreshold
    
  - name: DevOpsHub-HighMemory
    metric: pod_memory_utilization
    threshold: 85
    evaluation_periods: 2
    period: 300
    comparison: GreaterThanThreshold
  
  - name: DevOpsHub-PodRestarts
    metric: pod_number_of_container_restarts
    threshold: 3
    evaluation_periods: 1
    period: 60
    comparison: GreaterThanThreshold
  
  - name: DevOpsHub-TargetResponseTime
    namespace: AWS/ApplicationELB
    metric: TargetResponseTime
    threshold: 2
    evaluation_periods: 2
    period: 60
    comparison: GreaterThanThreshold
  
  - name: DevOpsHub-5XXErrors
    namespace: AWS/ApplicationELB
    metric: HTTPCode_Target_5XX_Count
    threshold: 10
    evaluation_periods: 1
    period: 60
    comparison: GreaterThanThreshold
```

### Application Logging

```yaml
# FluentBit DaemonSet for log forwarding (já incluído no Container Insights)
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: amazon-cloudwatch
data:
  output.conf: |
    [OUTPUT]
        Name cloudwatch_logs
        Match *
        region sa-east-1
        log_group_name /aws/containerinsights/EKS-PROD-01/application
        log_stream_prefix devopshub-
        auto_create_group true
```

### Health Check Endpoints

Adicionar ao `app.py` para monitoramento:

```python
# Health check endpoint
@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}

@app.route('/ready')
def ready():
    # Check data files exist
    if os.path.exists('data/inventario_aplicacoes.csv'):
        return {'status': 'ready'}
    return {'status': 'not_ready'}, 503
```

---

## 🔄 Rollback e Disaster Recovery

### Rollback Script

```bash
#!/bin/bash
# scripts/deploy/rollback.sh

NAMESPACE=${1:-devopshub}
REVISION=${2:-0}  # 0 = previous revision

echo "Rolling back deployment in namespace: $NAMESPACE"

if [ "$REVISION" -eq 0 ]; then
    # Rollback to previous revision
    kubectl rollout undo deployment/devopshub -n $NAMESPACE
else
    # Rollback to specific revision
    kubectl rollout undo deployment/devopshub -n $NAMESPACE --to-revision=$REVISION
fi

# Wait for rollback to complete
kubectl rollout status deployment/devopshub -n $NAMESPACE --timeout=5m

# Verify health
bash scripts/deploy/post-deploy.sh

echo "Rollback completed successfully"
```

### Backup Strategy

```yaml
# Velero Backup Schedule
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: devopshub-daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  template:
    includedNamespaces:
      - devopshub
    includedResources:
      - '*'
    storageLocation: aws-s3
    ttl: 720h  # 30 days
```

---

## 📝 Checklist de Implementação

### Fase 1: Preparação
- [ ] Criar repositório Git
- [ ] Configurar Azure DevOps project
- [ ] Provisionar EKS cluster
- [ ] Configurar AWS Secrets Manager
- [ ] Configurar ECR repository
- [ ] Instalar External Secrets Operator
- [ ] Instalar AWS Load Balancer Controller
- [ ] Instalar Metrics Server
- [ ] Habilitar CloudWatch Container Insights

### Fase 2: Desenvolvimento
- [ ] Criar Dockerfile multi-stage
- [ ] Criar health check endpoints (`/health`, `/ready`)
- [ ] Configurar linters (Python, YAML, Docker)
- [ ] Testar aplicação localmente

### Fase 3: Kubernetes
- [ ] Criar namespace
- [ ] Criar ConfigMaps
- [ ] Configurar External Secrets
- [ ] Criar Deployment
- [ ] Criar Services
- [ ] Configurar Ingress/ALB
- [ ] Configurar HPA
- [ ] Configurar VPA (opcional)
- [ ] Criar PDB
- [ ] Configurar Network Policies
- [ ] Configurar RBAC

### Fase 4: Pipeline
- [ ] Criar pipeline YAML
- [ ] Configurar stages (Lint, Build, Deploy)
- [ ] Adicionar Trivy scanning (non-blocking)
- [ ] Configurar smoke tests
- [ ] Configurar notificações
- [ ] Testar rollback

### Fase 5: Monitoramento
- [ ] Habilitar Container Insights
- [ ] Criar CloudWatch Dashboard
- [ ] Criar CloudWatch Alarms
- [ ] Configurar SNS para notificações
- [ ] Testar alertas

### Fase 6: Produção
- [ ] Deploy em DEV
- [ ] Testes em DEV
- [ ] Deploy em STAGING
- [ ] Smoke tests em STAGING
- [ ] Deploy em PRODUCTION (Rolling Update)
- [ ] Monitoramento 24/7
- [ ] Documentação

---

## 🎓 Melhores Práticas Implementadas

### ✅ Segurança
- Container image scanning (Trivy - informativo)
- Secret management (AWS Secrets Manager)
- RBAC mínimo necessário
- Network Policies
- Non-root containers
- Read-only filesystem
- Security contexts

### ✅ Confiabilidade
- Health checks (liveness, readiness, startup)
- Rolling updates com zero downtime
- Pod Disruption Budget
- Anti-affinity rules
- Topology spread constraints
- Resource limits
- Auto-scaling (HPA)

### ✅ Observabilidade
- CloudWatch Container Insights
- Centralized logging
- Custom CloudWatch alarms
- Application health endpoints

### ✅ Performance
- Resource optimization
- Multi-stage Docker builds
- Efficient data loading
- Horizontal scaling

### ✅ DevOps
- Infrastructure as Code
- Automated deployment
- Progressive delivery (Rolling Update)
- Automated rollback capability
- Linting informativo (non-blocking)
- Simple monitoring stack

---

## 📚 Referências

- [AWS EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
- [Kubernetes Production Best Practices](https://learnk8s.io/production-best-practices)
- [OWASP Kubernetes Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
- [12 Factor App](https://12factor.net/)
- [Azure DevOps Pipelines Documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/)

---

## 📞 Suporte

Para dúvidas ou problemas:
- **Equipe DevOps**: devops@empresa.com.br
- **Slack**: #devops-support
- **Jira**: Projeto DEVOPS

---

**Versão do Documento:** 1.0.0  
**Data:** Dezembro 2025  
**Autor:** Equipe DevOps  
**Status:** ✅ Pronto para Implementação
