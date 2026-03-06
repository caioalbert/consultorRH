# Consultor RH - Sistema de Compliance Trabalhista

Sistema web para gestão de compliance trabalhista com upload de CSV e dashboard de indicadores.

## Stack

- Frontend: React + Vite + TailwindCSS
- Backend: Node.js + Express (rodando como Function na Vercel em `/api`)
- Banco: PostgreSQL + Prisma ORM

## Rodando localmente

### 1) Backend

```bash
cd backend
cp .env.example .env
# ajuste DATABASE_URL
npm install
npm run db:push
npm run dev
```

Backend em `http://localhost:3001`

### 2) Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend em `http://localhost:5173` (com proxy para `/api` -> `localhost:3001`).

## Deploy na Vercel

### Pré-requisitos

- Banco PostgreSQL acessível pela internet (ex: Vercel Postgres, Neon, Supabase)
- `DATABASE_URL` do banco

### Variáveis de ambiente na Vercel

- `DATABASE_URL` (obrigatória)
- `VITE_API_URL=/api` (recomendado)

### Sincronizar schema (primeira vez)

```bash
cd backend
DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/DB_NAME?sslmode=require" npm run db:push
```

### Build

A Vercel usa:

- `buildCommand`: `npm run build`
- `outputDirectory`: `frontend/dist`
- API Function: `api/[...path].js`

## Funcionalidades

- Upload de CSV para 4 tipos:
  - Colaboradores
  - Férias
  - Exames ASO
  - eSocial
- Dashboard com KPIs
- Histórico de importações

## Formato dos CSVs

### Colaboradores
```csv
nome,cpf,cargo,filial,setor,data_admissao,status,risco
Ana Lima,123.456.789-00,Analista RH,São Paulo,RH,2020-03-15,Ativo,Normal
```

### Férias
```csv
nome,filial,periodo_aquisitivo,dias_devidos,vencimento,em_dobro,passivo,status
Ana Lima,São Paulo,2022/2023,30,2023-11-01,Não,R$ 5000,Vencida
```

### Exames
```csv
nome,filial,tipo_exame,ultimo_exame,vencimento,dias_atraso,passivo,status
Ana Lima,São Paulo,Periódico,2022-01-10,2023-01-10,320,R$ 500,Atrasado
```

### eSocial
```csv
evento,descricao,pendencias,passivo,criticidade
S-1200,Remuneração do Trabalhador,87,R$ 157719,Crítico
```

## API Endpoints

- `GET /api/health`
- `GET /api/colaboradores`
- `GET /api/ferias`
- `GET /api/exames`
- `GET /api/esocial`
- `GET /api/history`
- `POST /api/upload/:type`
- `DELETE /api/:type`

## Prisma Studio

```bash
cd backend
npm run studio
```
