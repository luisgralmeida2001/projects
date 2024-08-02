"""
WebScrapping - Relatório Semanal
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def web_scraping(x, x_dias):
    # Ajusta a data para X dias atrás
    x_dias = str(format(x_dias, "%Y-%m-%d"))
    data_obj = datetime.strptime(x_dias, "%Y-%m-%d")
    dia = x_dias[8:10]
    mes = x_dias[5:7]
    ano = data_obj.year  

    # URL do site
    url = f"https://sdro.ons.org.br/SDRO/DIARIO/{ano}_{mes}_{dia}/HTML/02_BalancoEnergeticoAcumuloDia.html"
    print(url)
    headers = {"User-Agent": "Mozilla/5.0"}

    # Endereços dos valores que extraímos do site
    selector = {
        "SE/CO "+ str(x): [
            "#lbl_hidr_SE_V",
            "#lbl_gerTermSE_V",
            "#lbl_geracaoNuclearSE",
            "#lbl_GeracaoSolarSE",
        ],
        "SUL "+ str(x): [
            "#lbl_gerhidrS_V",
            "#lbl_gerTermS_V",
            "#lbl_geracaoEolicaS",
            "#lbl_geracaoSolarS",
        ],
        "NORTE "+ str(x): [
            "#lbl_hidr_N_V",
            "#lbl_geracaoTermicaN",
            "#lbl_geracaoEolicaN_V",
            "#lbl_geracaoSolarN",
        ],
        "NORDESTE "+ str(x): [
            "#lbl_geracaoHidraulicaNE",
            "#lbl_geracaoTermicaNE",
            "#lbl_GeracaoEolicaNE",
            "#lbl_GeracaoSolarNE",
        ],
        "ENA "+ str(x): ["#lbl_MltSE", 
                "#lbl_mltS", 
                "#lbl_MltN", 
                "#lbl_mltNE"],

        "EAR "+ str(x): [
            "#lbl_EaDiaPercSE",
            "#lbl_eaDiaPercS",
            "#lbl_eaDiaPercN",
            "#lbl_eaDiaPercNE",
        ],
        "CARGA "+ str(x): [
            "#lbl_cargaSE_V",
            "#lbl_cargaS_V",
            "#lbl_cargaPropriaN",
            "#lbl_cargaPropriaNE",
        ],
    }

    # Cria uma lista com os valores das chaves do dicionário (Submercados)
    nome = list(selector.keys())
    n = 0

    # Extraio o código HTML do site
    requisicao = requests.get(url, headers=headers)
    raw_html = requisicao.text
    site = BeautifulSoup(raw_html, "html.parser")
    valores = []

    # FOR responsável pela leitura e armazenamento dos dados do site
    for n in range(len(selector)):
        for i in range(len(selector[nome[n]])):
            pesquisa = site.select_one(selector[nome[n]][i])
            # if type(pesquisa) != "NoneType":
            if type(pesquisa) is not type(None):
                pesquisa = pesquisa.text
            valores.append(pesquisa)

    # Transforma a lista de dados em um dicionário
    dicionario_valores = {nome[i]: valores[i * 4 : i * 4 + 4] for i in range(len(nome))}

    # FOR para remover o "%" da EAR e ENA
    for i in range(4, 6, 1):
        dicionario_valores[nome[i]] = [
            valor.replace("%", "") for valor in dicionario_valores[nome[i]]
        ]
    return dicionario_valores


def valor_mes_passado(i, data_principal):
    z = f"M. Passado -{i}"
    dia_mes_passado = data_principal - relativedelta(months=i)
    dicionario_valores = web_scraping(z, dia_mes_passado)  
    return dicionario_valores

# Semana atual
x = "S. Atual"
dois_dias_atras = datetime.now() - timedelta(days=4)
dicionario_valores1 = web_scraping(x, dois_dias_atras)

# Semana passada
y = "S. Passada"
dia_semana_passada = dois_dias_atras - timedelta(days=7)
dicionario_valores2 = web_scraping(y, dia_semana_passada)


dicionario_valores3 = valor_mes_passado(1,dois_dias_atras)
dicionario_valores4 = valor_mes_passado(2,dois_dias_atras)
dicionario_valores5 = valor_mes_passado(3,dois_dias_atras)
dicionario_valores6 = valor_mes_passado(4,dois_dias_atras)
dicionario_valores7 = valor_mes_passado(5,dois_dias_atras)
dicionario_valores8 = valor_mes_passado(6,dois_dias_atras)
dicionario_valores9 = valor_mes_passado(7,dois_dias_atras)
dicionario_valores10 = valor_mes_passado(8,dois_dias_atras)
dicionario_valores11 = valor_mes_passado(9,dois_dias_atras)
dicionario_valores12 = valor_mes_passado(10,dois_dias_atras)
dicionario_valores13 = valor_mes_passado(11,dois_dias_atras)
dicionario_valores14 = valor_mes_passado(12,dois_dias_atras)


# # Mês passado -1
# z = "M. Passado -1"
# dia_mes_passado = dois_dias_atras - relativedelta(months=1)
# dicionario_valores3 = web_scraping(z, dia_mes_passado)

# # Ano passado
# k = "M. Passado -12"
# dia_ano_passado = dois_dias_atras - relativedelta(months=12)
# dicionario_valores4 = web_scraping(k, dia_ano_passado)

# Juntar tudo
dicionario_valores = {**dicionario_valores1, **dicionario_valores2, **dicionario_valores3, **dicionario_valores4,
                      **dicionario_valores5, **dicionario_valores6, **dicionario_valores7, **dicionario_valores8,
                      **dicionario_valores9, **dicionario_valores10, **dicionario_valores11, **dicionario_valores12,
                      **dicionario_valores13, **dicionario_valores14 }

# Cria uma tabela com os dados e coloca-os em uma planilha
df = pd.DataFrame(dicionario_valores)
df.to_excel(
    r"G:\Drives compartilhados\USINAS\USINAS GESTAO\- Relatorio Semanal\ws\wsdbRelatorio_Semanal.xlsx",
    startrow = 0,
    startcol = 0,
    index = False,
    sheet_name = "Base de Dados",
    float_format = True,
)
print(df)