# DevOpsHub - Pipeline

Pipeline CI/CD para a aplicação DevOpsHub usando Azure DevOps e Argo Rollouts.

## 📁 Estrutura

```
pipeline/
├── azure-pipelines.yml          # Pipeline CI/CD completa
├── Dockerfile                   # Build da imagem Docker
├── .dockerignore               # Exclusões para build
└── rollouts/
    ├── core-sbx/               # Rollout para Sandbox
    │   ├── devops-devopshub-web.yaml
    │   ├── service.yaml
    │   └── kustomization.yaml
    └── core-prod/              # Rollout para Produção
        ├── devops-devopshub-web.yaml
        ├── service.yaml
        └── kustomization.yaml
```

## 🚀 Estratégia de Deploy

### **Sandbox (core-sbx)**
- **Strategy**: Canary simples
- **Replicas**: 1
- **maxUnavailable**: 1, **maxSurge**: 0
- **NodeSelector**: `sandbox: "yes"`

### **Produção (core-prod)**  
- **Strategy**: Canary com steps (20% → 60% → 100%)
- **Replicas**: 3
- **maxUnavailable**: 1, **maxSurge**: 0  
- **NodeSelector**: `production: "yes"`
- **Manual Approval**: Pause entre cada step

## 🔧 Pipeline Stages

1. **BUILD** - Build e push da imagem Docker para ECR
2. **SANDBOX** - Deploy automático no ambiente sandbox
3. **PRODUCTION** - Deploy com aprovação manual (somente branch `main`)

## ⚙️ Como Configurar

### 1. Azure DevOps
- Aponte a pipeline para: `pipeline/azure-pipelines.yml`
- Configure Service Connection: `AWS.EKS`
- Configure Environment: `production` (para aprovações)

### 2. Variáveis Necessárias
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
- `registry`: `676949161726.dkr.ecr.sa-east-1.amazonaws.com`
- `eks_cluster`: `EKS-PROD-01`

### 3. Pré-requisitos Cluster
- Argo Rollouts Controller instalado
- Namespaces: `core-sbx`, `core-prod` 
- Node selectors configurados

## 📊 Monitoramento

```bash
# Status dos rollouts
kubectl argo rollouts get rollout devops-devopshub-web -n core-sbx
kubectl argo rollouts get rollout devops-devopshub-web -n core-prod

# Status dos services
kubectl get svc devops-devopshub-web-service -n core-sbx
kubectl get svc devops-devopshub-web-service -n core-prod

# Promote manual (produção)
kubectl argo rollouts promote devops-devopshub-web -n core-prod
```

Simples e focado! 🎯