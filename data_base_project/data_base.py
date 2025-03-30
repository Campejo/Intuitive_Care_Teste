from db_connection import abrir_conexao, fechar_conexao
import os
import io
import pandas as pd

path_contabeis = r'data_base_project\dados_abertos_gov\demonstracoes_contabeis'
csv_operadoras = r'data_base_project\dados_abertos_gov\operadoras_ativas\Relatorio_cadop.csv'

conexao = abrir_conexao()

def criar_tabelas_se_nao_existirem(conexao):
    sql_criar_operadoras = """
    CREATE TABLE IF NOT EXISTS operadoras_ativas (
        Registro_ANS VARCHAR(20) PRIMARY KEY,
        CNPJ VARCHAR(14) NOT NULL,
        Razao_Social VARCHAR(255) NOT NULL,
        Nome_Fantasia VARCHAR(255),
        Modalidade VARCHAR(100),
        Logradouro VARCHAR(255),
        Numero VARCHAR(20),
        Complemento VARCHAR(255),
        Bairro VARCHAR(100),
        Cidade VARCHAR(100),
        UF CHAR(2),
        CEP VARCHAR(8),
        DDD CHAR(2),
        Telefone VARCHAR(20),
        Fax VARCHAR(20),
        Endereco_eletronico VARCHAR(255),
        Representante VARCHAR(255),
        Cargo_Representante VARCHAR(100),
        Regiao_de_Comercializacao SMALLINT,
        Data_Registro_ANS DATE
    );
    """
    sql_criar_dados_financeiros = """
    CREATE TABLE IF NOT EXISTS dados_financeiros (
        id_financeiro SERIAL PRIMARY KEY,
        Data DATE NOT NULL,
        Reg_ANS VARCHAR(20) NOT NULL,
        CD_Conta_Contabil VARCHAR(14) NOT NULL,
        Descricao VARCHAR(255),
        VL_Saldo_Inicial NUMERIC(15, 2) DEFAULT 0,
        VL_Saldo_Final NUMERIC(15, 2) DEFAULT 0
    );
    """

    try:
        cursor = conexao.cursor()

        cursor.execute(sql_criar_operadoras)
        conexao.commit()
        print('Tabela operadoras_ativas criada ou já existente.')

        cursor.execute(sql_criar_dados_financeiros)
        conexao.commit()
        print('Tabela dados_financeiros criada ou já existente')

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao criar tabelas: {e}')

    finally:
        cursor.close()


def importar_operadoras(conexao):
    try:
        cursor = conexao.cursor()
        print('Importando Relatorio_cadop.csv ...')

        with open(csv_operadoras, 'r', encoding='utf-8', errors='replace') as file:
            data = io.StringIO(file.read())
            cursor.copy_expert("COPY operadoras_ativas FROM STDIN WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8'", data)

        conexao.commit()
        print('Relatorio_cadop.csv importado com sucesso!')
        
    except Exception as e:
        conexao.rollback()
        print(f'Falha ao importar Relatorio_cadop.csv: {e}')

    finally:
        cursor.close()




def importar_dados_financeiros(conexao):
    try:
        cursor = conexao.cursor()

        try:
            for csv in os.listdir(path_contabeis):
                path_file = os.path.join(path_contabeis, csv)

                print(f'Importando {csv}')


                df = pd.read_csv(path_file, delimiter=';', encoding='utf-8', dtype=str)

                df['VL_SALDO_INICIAL'] = df['VL_SALDO_INICIAL'].str.replace(',', '.')
                df['VL_SALDO_FINAL'] = df['VL_SALDO_FINAL'].str.replace(',', '.')

                
                data = io.StringIO()
                df.to_csv(data, index=False, header=True, sep=';')
                data.seek(0)

                cursor.copy_expert("COPY dados_financeiros(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) FROM STDIN WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8'", data)

                conexao.commit()
                print(f'{csv} importado com sucesso!')
    
        except Exception as e:
            conexao.rollback()
            print(f'Falha ao importar {csv}: {e}')

    except Exception as e:
        print(f'Erro ao listar arquivos CSV: {e}')

    finally:
        cursor.close()


def buscar_maiores_despesas(conexao):
    sql_operadoras_ultimo_trimestre = """
    SELECT
        oa.razao_social,
        SUM(df.VL_Saldo_Final - df.VL_Saldo_Inicial) AS total_despesas
    FROM
        dados_financeiros df
    JOIN
        operadoras_ativas oa ON df.Reg_ANS = oa.Registro_ANS
    WHERE
        df.Descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
        AND df.Data >= '2024-10-01' AND df.Data <= '2024-12-31'
    GROUP BY
        oa.razao_social
    ORDER BY
        total_despesas DESC
    LIMIT 10;
    """

    sql_operadoras_ultimo_ano = """
    SELECT
        oa.razao_social,
        SUM(df.VL_Saldo_Final - df.VL_Saldo_Inicial) AS total_despesas
    FROM
        dados_financeiros df
    JOIN
        operadoras_ativas oa ON df.Reg_ANS = oa.Registro_ANS
    WHERE
        df.Descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
        AND df.Data >= '2024-01-01' AND df.Data <= '2024-12-31'
    GROUP BY
        oa.razao_social
    ORDER BY
        total_despesas DESC
    LIMIT 10;
    """
    cursor = conexao.cursor()

    try:
        cursor.execute(sql_operadoras_ultimo_trimestre)
        resultados_trimestre = cursor.fetchall()
        print('Consulta do último trimestre realizada com sucesso!')

        if resultados_trimestre:
            print('\nAs 10 operadoras com maiores despesas no ÚLTIMO TRIMESTRE:')

            for operadora, despesa in resultados_trimestre:
                print(f'- {operadora}: {despesa}')

        else:
            print('Nenhuma operadora encontrada com despesas no último trimestre.')

    except Exception as e:
        print(f'Erro ao realizar consulta do último trimestre: {e}')
            
    try:
        cursor.execute(sql_operadoras_ultimo_ano)
        resultados_ano = cursor.fetchall()
        print('Consulta do último ano realizada com sucesso!')
            
        if resultados_ano:
            print('\nAs 10 operadoras com maiores despesas no ÚLTIMO ANO:')

            for operadora, despesa in resultados_ano:
                print(f'- {operadora}: {despesa:}')

        else:
            print('Nenhuma operadora encontrada com despesas no último ano.')

    except Exception as e:
        print(f'Erro ao realizar consulta: {e}')
    
    finally:
        cursor.close()




try:
    criar_tabelas_se_nao_existirem(conexao) # Item 3.3
    #importar_operadoras(conexao) # Item 3.4
    #importar_dados_financeiros(conexao) # Item 3.4
    buscar_maiores_despesas(conexao)

except Exception as e:
    print(f'Erro ao processar querys: {e}')

finally:
    fechar_conexao(conexao)