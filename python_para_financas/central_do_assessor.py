import pandas as pd
import numpy as np
import yfinance as yf
from bcb import sgs
from automacao_notion import enviar_indicador_notion

def buscar_dados_mercado():
    print("🔍 Capturando dados oficiais e limpando o terminal...")
    
    try:
        # 1. TAXA DI ANUALIZADA (Série 4389)
        di_df = sgs.get(4389, last=1)
        taxa_di = float(di_df.iloc[-1].iloc[0]) # Correção para pegar o número puro

        # 2. SELIC META ANUALIZADA (Série 432)
        selic_df = sgs.get(432, last=1)
        selic_real = float(selic_df.iloc[-1].iloc[0]) # Correção para pegar o número puro

        # 3. IPCA ACUMULADO 12 MESES (Série 433)
        # Buscamos os dados de 2025 para acumular
        ipca_bruto = sgs.get(433, start='2025-01-01')
        # Calculamos o acumulado e extraímos apenas o valor numérico final (.iloc[0])
        ipca_acumulado = float(((np.prod(1 + ipca_bruto/100, axis=0) - 1) * 100).iloc[0])
        
        # 4. DÓLAR (USDBRL=X)
        dolar_data = yf.download('USDBRL=X', period='1d', interval='1m', progress=False)
        # Pegamos o último fechamento de forma segura
        cotacao_dolar = float(dolar_data['Close'].iloc[-1])

        print("-" * 50)
        print(f"📊 RESULTADOS CAPTURADOS:")
        print(f"DI: {taxa_di}% | Selic: {selic_real}%")
        print(f"IPCA 12m: {ipca_acumulado:.2f}% | Dólar: R${cotacao_dolar:.2f}")
        print("-" * 50)

        # Lista para o Notion
        indicadores = [
            ("Taxa DI", round(taxa_di, 2), "Benchmark CDI anualizado."),
            ("Selic Meta", round(selic_real, 2), "Taxa básica definida pelo COPOM."),
            ("IPCA (12 meses)", round(ipca_acumulado, 2), "Inflação acumulada (Matemática Financeira)."),
            ("Dólar PTAX", round(cotacao_dolar, 2), "Cotação atualizada USD/BRL.")
        ]

        print("📤 Sincronizando com o Notion do Fernando...")
        for nome, valor, insight in indicadores:
            sucesso = enviar_indicador_notion(nome, valor, insight)
            if sucesso:
                print(f"✔️ {nome} atualizado!")
            else:
                print(f"❌ Erro em {nome}")

    except Exception as e:
        print(f"⚠️ Erro técnico na captura: {e}")

if __name__ == "__main__":
    buscar_dados_mercado()