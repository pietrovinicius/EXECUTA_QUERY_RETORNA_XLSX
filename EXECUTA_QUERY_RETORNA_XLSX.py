"""
22/11/2024
@PLima

APP PARA EXECUTAR QUERY DENTRO DO BANCO DE DADOS TASY DO HSF

passos:

#Como importar oracledb:
# python -m pip install oracledb


página Habilitando o modo Python-oracledb Thick:
https://python-oracledb.readthedocs.io/en/latest/user_guide/initialization.html#enablingthick


Instalando o banco de dados para ativar o modo Think
página download: https://www.oracle.com/database/technologies/xe-downloads.html

banco de dados 21c
banco de dados instalado:
1) contêiner multitenant: localhost:1522
2) plugável: localhost:1522/XEPDB1
3) url do EM Express: https//localhost:5500/em


Importando a lib oracledb:
1) python -m pip install oracledb

2) Seu aplicativo deve chamar a função oracledb.init_oracle_client()para carregar as 
bibliotecas do cliente

3) Download do instantclient_23_5:

instantclient-basiclite-windows.x64-23.6.0.24.10.zip
extraido em: C:\oracle

ficando com o endereço: 'C:\oracle\instantclient_23_6'
extração do arquivo heim: C:\oracle\instantclient_23_6




"""

import os
import platform
import oracledb
import pandas as pd

#apontamento para usar o Think Mod
"""
d = None                               # On Linux, no directory should be passed
if platform.system() == "Darwin":      # macOS
  d = os.environ.get("HOME")+("/Downloads/instantclient_23_3")
elif platform.system() == "Windows":   # Windows
  d = r'C:\oracle\instantclient_23_6'
oracledb.init_oracle_client(lib_dir=d)
"""
def encontrar_diretorio_instantclient(nome_pasta="instantclient-basiclite-windows.x64-23.6.0.24.10\instantclient_23_6"):
  """
  Localiza o diretório do Instant Client dentro da pasta raiz do aplicativo.
    a pasta é C:\Pietro\Projetos\EXECUTA_QUERY_RETORNA_XLSX\instantclient-basiclite-windows.x64-23.6.0.24.10\instantclient_23_6
  Args:
    nome_pasta: Nome da pasta do Instant Client.

  Returns:
    Caminho completo para a pasta do Instant Client, ou None se não encontrada.
  """
  # Obtém o diretório do script atual
  diretorio_atual = os.path.dirname(os.path.abspath(__file__))

  # Constrói o caminho completo para a pasta do Instant Client
  caminho_instantclient = os.path.join(diretorio_atual, nome_pasta)

  # Verifica se a pasta existe
  if os.path.exists(caminho_instantclient):
    return caminho_instantclient
  else:
    print(f"A pasta '{nome_pasta}' não foi encontrada na raiz do aplicativo.")
    return None





#============================================================ EXECUCAO ============================================================
if __name__ == "__main__":
    print("\n============================== inicio ========================\n")

    try:
        un = 'PIETRO'
        cs = '192.168.5.9:1521/TASYHOM'
        
        # Chamar a função para obter o caminho do Instant Client
        caminho_instantclient = encontrar_diretorio_instantclient()

        # Usar o caminho encontrado para inicializar o Oracle Client
        if caminho_instantclient:
            print(f'if caminho_instantclient:\n')
            print(f'oracledb.init_oracle_client(lib_dir=caminho_instantclient)\n')
            oracledb.init_oracle_client(lib_dir=caminho_instantclient)
        else:
            print("Erro ao localizar o Instant Client. Verifique o nome da pasta e o caminho.")
        

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
            print(f'with oracledb.connect(user=un, password=pw, dsn=cs) as connection\n')
            with connection.cursor() as cursor:
                print(f'with connection.cursor() as cursor:\n')
                sql = """ 
                        SELECT 
                            TO_CHAR(DT_ENTRADA,'dd/mm/yyyy hh24:mi:ss') DT_ENTRADA,
                            NR_ATENDIMENTO,
                            NM_PACIENTE
                        FROM ATENDIMENTO_PACIENTE_V
                        ORDER BY DT_ENTRADA DESC
                        FETCH FIRST 10 ROWS ONLY
                    """
                #Executando a query:
                print(f'cursor.execute(sql)\n{sql}')
                cursor.execute(sql)
                
                # Imprimir os resultados da consulta para verificar
                print(f'results = cursor.fetchall()\n')
                results = cursor.fetchall()
        
                #Exibindo redultado no console:
                #print(f'Exibindo redultado no console:\n')    
                #for r in cursor.execute(sql):
                #    print(r)
                
                #Inserindo resultado em um data frame:
                #df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                
                print(f'df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])')
                df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
                

        print('\n\n')
        
        # Visualizar os primeiros 5 registros
        print(f'data_frame:\n{df.head()}')

    except Exception as erro:
        print(f"Erro Inexperado:\n{erro}")
    
    print("\n============================== fim ========================\n")