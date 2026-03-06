#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para carregar dados dos CSVs no banco de dados PostgreSQL
Utiliza as funções fn_* criadas na migration 003
"""

import os
import sys
import csv
from datetime import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carrega variáveis de ambiente
load_dotenv()


class DataLoader:
    """Classe para carregar dados dos CSVs no banco"""
    
    def __init__(self):
        self.conn = None
        self.data_dir = root_dir / "data"
        
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT', 5432),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            print("✓ Conexão estabelecida com sucesso!")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar: {e}")
            return False
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
            print("✓ Conexão fechada")
    
    def parse_bool(self, value):
        """Converte string para booleano"""
        if not value or value.upper() in ['N/A', 'NULL', '']:
            return None
        return value.upper() == 'SIM'
    
    def parse_date(self, value):
        """Converte string para data"""
        if not value or value.upper() in ['N/A', 'NULL', '']:
            return None
        
        # Tenta vários formatos de data
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None
    
    def load_aplicacoes(self):
        """Carrega dados do inventário de aplicações"""
        csv_file = self.data_dir / "inventario_aplicacoes.csv"
        
        if not csv_file.exists():
            print(f"✗ Arquivo não encontrado: {csv_file}")
            return
        
        print(f"\nℹ Carregando aplicações de {csv_file}...")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            cursor = self.conn.cursor()
            
            count = 0
            errors = 0
            
            for row in reader:
                try:
                    # Primeiro, garante que o produto existe
                    produto_nome = row['Produto'].strip()
                    cursor.execute(
                        "SELECT * FROM fn_get_or_create_produto(%s)",
                        (produto_nome,)
                    )
                    produto = cursor.fetchone()
                    produto_id = produto[0]
                    
                    # Converte campos booleanos
                    sbom = self.parse_bool(row.get('SBOM'))
                    scan_imagens = self.parse_bool(row.get('Scan_Imagens'))
                    secret_manager = self.parse_bool(row.get('Secret_Manager'))
                    sast_sonarcube = self.parse_bool(row.get('SAST_SonarCube'))
                    
                    # Converte datas
                    data_ultima_revisao = self.parse_date(row.get('Data_Ultima_Revisao'))
                    data_criacao = self.parse_date(row.get('Data_Criacao'))
                    
                    # Insere aplicação
                    cursor.execute("""
                        SELECT * FROM fn_criar_aplicacao(
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        row['Nome_Aplicacao'].strip(),
                        produto_id,
                        row['Ambiente'].strip() if row['Ambiente'].strip() not in ['N/A', ''] else None,
                        row['Tipo_Aplicacao'].strip() if row['Tipo_Aplicacao'].strip() else None,
                        row['Framework'].strip() if row['Framework'].strip() else None,
                        row['Ferramenta_Versionamento'].strip() if row['Ferramenta_Versionamento'].strip() else None,
                        row['Tipo_Pipeline'].strip() if row['Tipo_Pipeline'].strip() else None,
                        row['Versao'].strip() if row['Versao'].strip() else None,
                        row['Hospedagem'].strip() if row['Hospedagem'].strip() else None,
                        sbom,
                        scan_imagens,
                        secret_manager,
                        sast_sonarcube,
                        data_ultima_revisao,
                        data_criacao
                    ))
                    
                    count += 1
                    
                    if count % 10 == 0:
                        print(f"  Processadas: {count} aplicações")
                        self.conn.commit()
                    
                except Exception as e:
                    errors += 1
                    print(f"✗ Erro ao processar aplicação {row.get('Nome_Aplicacao', 'N/A')}: {e}")
                    self.conn.rollback()
            
            # Commit final
            self.conn.commit()
            cursor.close()
            
            print(f"✓ Aplicações carregadas: {count}")
            if errors > 0:
                print(f"✗ Erros encontrados: {errors}")
    
    def load_gmuds(self):
        """Carrega dados de GMUDs"""
        csv_file = self.data_dir / "gmud_dados.csv"
        
        if not csv_file.exists():
            print(f"✗ Arquivo não encontrado: {csv_file}")
            return
        
        print(f"\nℹ Carregando GMUDs de {csv_file}...")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            cursor = self.conn.cursor()
            
            count = 0
            errors = 0
            
            for row in reader:
                try:
                    # Parse data prevista
                    data_prevista_str = row.get('Data/hora Prevista', '').strip()
                    data_prevista = None
                    
                    if data_prevista_str and data_prevista_str not in ['N/A', '', 'NULL']:
                        # Tenta vários formatos
                        for fmt in ['%d/%m/%y %H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M']:
                            try:
                                data_prevista = datetime.strptime(data_prevista_str, fmt)
                                break
                            except ValueError:
                                continue
                    
                    # Normaliza risco
                    risco = row.get('Risco a Operação', '').strip()
                    risco_map = {
                        'BAIXO': 'Baixo', 'BAIXA': 'Baixo',
                        'MÉDIO': 'Médio', 'MEDIA': 'Médio',
                        'ALTO': 'Alto', 'ALTA': 'Alto',
                        'ALTISSIMO': 'Altíssimo', 'ALTISSIMA': 'Altíssimo'
                    }
                    risco = risco_map.get(risco.upper(), risco) if risco else None
                    
                    # Busca aplicação pelo nome
                    nome_aplicacao = row.get('Nome da Aplicação', '').strip()
                    aplicacao_id = None
                    
                    if nome_aplicacao:
                        cursor.execute(
                            "SELECT id FROM aplicacoes WHERE nome = %s LIMIT 1",
                            (nome_aplicacao,)
                        )
                        result = cursor.fetchone()
                        if result:
                            aplicacao_id = result[0]
                    
                    # Insere GMUD (sem nome_aplicacao, apenas aplicacao_id)
                    cursor.execute("""
                        SELECT * FROM fn_criar_gmud(
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        row.get('ID do Item', '').strip() or None,
                        data_prevista,
                        row.get('Responsável / Executor', '').strip() or None,
                        row.get('Tempo Estimado', '').strip() or None,
                        row.get('Solicitante / área de atuação', '').strip() or None,
                        aplicacao_id,
                        row.get('Ambiente', '').strip() or None,
                        row.get('hostname/namespace', '').strip() or None,
                        row.get('Local de Implantação', '').strip() or None,
                        row.get('Build/Release', '').strip() or None,
                        row.get('Configurações alteradas', '').strip() or None,
                        row.get('Tempo Realizado', '').strip() or None,
                        row.get('Ocorrências', '').strip() or None,
                        row.get('Soluções Atribuídas', '').strip() or None,
                        row.get('Validações Realizadas', '').strip() or None,
                        risco,
                        row.get('Impacto', '').strip() or None,
                        row.get('RCA', '').strip() or None,
                        row.get('Controle', '').strip() or None
                    ))
                    
                    count += 1
                    
                    if count % 10 == 0:
                        print(f"  Processadas: {count} GMUDs")
                        self.conn.commit()
                    
                except Exception as e:
                    errors += 1
                    print(f"✗ Erro ao processar GMUD {row.get('ID do Item', 'N/A')}: {e}")
                    self.conn.rollback()
            
            # Commit final
            self.conn.commit()
            cursor.close()
            
            print(f"✓ GMUDs carregadas: {count}")
            if errors > 0:
                print(f"✗ Erros encontrados: {errors}")
    
    def get_stats(self):
        """Exibe estatísticas do banco"""
        print("\n" + "=" * 70)
        print("  ESTATÍSTICAS DO BANCO DE DADOS")
        print("=" * 70)
        
        cursor = self.conn.cursor()
        
        # Produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        print(f"\n✓ Produtos: {cursor.fetchone()[0]}")
        
        # Aplicações
        cursor.execute("SELECT COUNT(*) FROM aplicacoes")
        print(f"✓ Aplicações: {cursor.fetchone()[0]}")
        
        # Aplicações por ambiente
        cursor.execute("""
            SELECT ambiente, COUNT(*) 
            FROM aplicacoes 
            WHERE ambiente IS NOT NULL
            GROUP BY ambiente 
            ORDER BY COUNT(*) DESC
        """)
        print("\n  Aplicações por ambiente:")
        for row in cursor.fetchall():
            print(f"    - {row[0]}: {row[1]}")
        
        # GMUDs
        cursor.execute("SELECT COUNT(*) FROM gmuds")
        print(f"\n✓ GMUDs: {cursor.fetchone()[0]}")
        
        # GMUDs por risco
        cursor.execute("""
            SELECT risco, COUNT(*) 
            FROM gmuds 
            WHERE risco IS NOT NULL
            GROUP BY risco 
            ORDER BY COUNT(*) DESC
        """)
        print("\n  GMUDs por risco:")
        for row in cursor.fetchall():
            print(f"    - {row[0]}: {row[1]}")
        
        cursor.close()
        print("\n" + "=" * 70)


def main():
    """Função principal"""
    print("=" * 70)
    print("  CARREGAMENTO DE DADOS - PostgreSQL AWS RDS")
    print("=" * 70)
    
    loader = DataLoader()
    
    # Conecta ao banco
    if not loader.connect():
        return
    
    try:
        # Carrega aplicações (que também cria produtos)
        loader.load_aplicacoes()
        
        # Carrega GMUDs
        loader.load_gmuds()
        
        # Exibe estatísticas
        loader.get_stats()
        
        print("\n✓ PROCESSO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"\n✗ Erro durante o processo: {e}")
        
    finally:
        loader.close()


if __name__ == "__main__":
    main()
