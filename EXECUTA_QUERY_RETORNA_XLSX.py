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

import getpass
import os
import platform
import oracledb

#apontamento para usar o Think Mod
d = None                               # On Linux, no directory should be passed
if platform.system() == "Darwin":      # macOS
  d = os.environ.get("HOME")+("/Downloads/instantclient_23_3")
elif platform.system() == "Windows":   # Windows
  d = r'C:\oracle\instantclient_23_6'
oracledb.init_oracle_client(lib_dir=d)


#============================================================ EXECUCAO ============================================================
if __name__ == "__main__":
    print("\n============================== inicio ========================\n")
    
    try:
        un = 'PIETRO'
        cs = '192.168.5.9:1521/TASYHOM'
        pw = ''

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
            with connection.cursor() as cursor:
                sql = """ 
                        SELECT 
                            TO_CHAR(DT_ENTRADA,'dd/mm/yyyy hh24:mi:ss') DT_ENTRADA,
                            NR_ATENDIMENTO,
                            NM_PACIENTE
                        FROM ATENDIMENTO_PACIENTE_V
                        ORDER BY DT_ENTRADA DESC
                        FETCH FIRST 10 ROWS ONLY
                    """
                for r in cursor.execute(sql):
                    print(r)
    except Exception as erro:
        print(f"Erro Inexperado: {erro}")
    
    print("\n============================== fim ========================\n")