import time
import datetime
import requests
import pandas as pd

# PASSAR O CAMINHO DO ARQUIVO
ARQUIVO = "cotacoes.xlsx"

# FUNCAO PARA COLETAR DADOS DA API
def buscar_cotacoes():
    url =  "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,ETH-BRL"
    dados = requests.get(url, timeout=15).json()

    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linhas = []
    for moeda in ["USD", "EUR", "BTC", "ETH"]:
        info = dados[moeda + "BRL"]
        linhas.append({
            "Moeda": moeda,
            "Valor (R$)": round(float(info["bid"]),2),
            "Variação (%)": info["pctChange"],
            "Atualizado em": agora
        })
    return linhas


# LOOP INFINITO DE 1 EM 1 MINUTO
print("Bot iniciado. Atualizando a cada 1 minuto\n")

while True:
    try:
        cotacoes = buscar_cotacoes()
        df = pd.DataFrame(cotacoes)
        df.to_excel(ARQUIVO, index=False)

        print(f"ARQUIVO ATUALIZADO COM SUCESSO - {cotacoes[0]['Atualizado em']}\n ")
        for c in cotacoes:
            print(f" {c['Moeda']} | {c['Valor (R$)']}")
        time.sleep(60)

    except KeyboardInterrupt:
        print("Bot interrompido")
        break

    except Exception as e:
        print(f"Error: \n {e}")