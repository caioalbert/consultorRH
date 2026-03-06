import express from 'express';
import cors from 'cors';
import multer from 'multer';
import Papa from 'papaparse';
import { PrismaClient } from '@prisma/client';

const app = express();
const globalForPrisma = globalThis;
const prisma = globalForPrisma.__prisma ?? new PrismaClient();
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

if (!globalForPrisma.__prisma) {
  globalForPrisma.__prisma = prisma;
}

const upload = multer({ storage: multer.memoryStorage() });

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ ok: true });
});

app.get('/api/colaboradores', asyncHandler(async (req, res) => {
  const data = await prisma.colaborador.findMany();
  res.json(data);
}));

app.get('/api/ferias', asyncHandler(async (req, res) => {
  const data = await prisma.ferias.findMany();
  res.json(data);
}));

app.get('/api/exames', asyncHandler(async (req, res) => {
  const data = await prisma.exame.findMany();
  res.json(data);
}));

app.get('/api/esocial', asyncHandler(async (req, res) => {
  const data = await prisma.eSocial.findMany();
  res.json(data);
}));

app.get('/api/history', asyncHandler(async (req, res) => {
  const data = await prisma.importHistory.findMany({
    orderBy: { createdAt: 'desc' }
  });
  res.json(data);
}));

app.post('/api/upload/:type', upload.single('file'), asyncHandler(async (req, res) => {
  const { type } = req.params;
  const { file } = req;

  if (!file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const csvData = file.buffer.toString('utf8');
  const parsed = Papa.parse(csvData, { header: true, skipEmptyLines: true });

  if (parsed.errors.length > 0) {
    return res.status(400).json({ error: `Invalid CSV: ${parsed.errors[0].message}` });
  }

  try {
    let count = 0;

    if (type === 'colaboradores') {
      await prisma.colaborador.deleteMany();
      for (const row of parsed.data) {
        await prisma.colaborador.create({
          data: {
            nome: row.nome || '',
            cpf: row.cpf || `${Date.now()}-${Math.random()}`,
            cargo: row.cargo,
            filial: row.filial,
            setor: row.setor,
            dataAdmissao: row.data_admissao,
            status: row.status,
            risco: row.risco
          }
        });
        count++;
      }
    } else if (type === 'ferias') {
      await prisma.ferias.deleteMany();
      for (const row of parsed.data) {
        await prisma.ferias.create({
          data: {
            nome: row.nome || '',
            filial: row.filial,
            periodoAquisitivo: row.periodo_aquisitivo,
            diasDevidos: parseInt(row.dias_devidos, 10) || 0,
            vencimento: row.vencimento,
            emDobro: row.em_dobro,
            passivo: row.passivo,
            status: row.status
          }
        });
        count++;
      }
    } else if (type === 'exames') {
      await prisma.exame.deleteMany();
      for (const row of parsed.data) {
        await prisma.exame.create({
          data: {
            nome: row.nome || '',
            filial: row.filial,
            tipoExame: row.tipo_exame,
            ultimoExame: row.ultimo_exame,
            vencimento: row.vencimento,
            diasAtraso: parseInt(row.dias_atraso, 10) || 0,
            passivo: row.passivo,
            status: row.status
          }
        });
        count++;
      }
    } else if (type === 'esocial') {
      await prisma.eSocial.deleteMany();
      for (const row of parsed.data) {
        await prisma.eSocial.create({
          data: {
            evento: row.evento || '',
            descricao: row.descricao,
            pendencias: parseInt(row.pendencias, 10) || 0,
            passivo: row.passivo,
            criticidade: row.criticidade
          }
        });
        count++;
      }
    } else {
      return res.status(400).json({ error: 'Invalid type' });
    }

    await prisma.importHistory.create({
      data: {
        tipo: type,
        arquivo: file.originalname,
        registros: count
      }
    });

    return res.json({ success: true, count });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}));

app.delete('/api/:type', asyncHandler(async (req, res) => {
  const { type } = req.params;
  const models = {
    colaboradores: prisma.colaborador,
    ferias: prisma.ferias,
    exames: prisma.exame,
    esocial: prisma.eSocial
  };

  if (!models[type]) {
    return res.status(404).json({ error: 'Invalid type' });
  }

  await models[type].deleteMany();
  return res.json({ success: true });
}));

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: err.message || 'Internal server error' });
});

export default app;
