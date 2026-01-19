from bcb import sgs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Estilo para relatórios profissionais
plt.style.use('seaborn-v0_8-whitegrid')

def calcular_metricas_estatisticas():
    try:
        print("Coletando dados para processamento estatístico...")
        # 432: Selic Meta | 433: IPCA Mensal
        dados = sgs.get({'selic': 432, 'ipca': 433}, start='2018-01-01')
        
        # 1. Alinhamento de frequências (Mensal)
        df = dados.resample('ME').last()

        # 2. Cálculo do IPCA Acumulado 12 meses (Matemática Financeira)
        # Equivalente a (1+i1)*(1+i2)...(1+i12) - 1 na HP 12C
        df['IPCA_12m'] = df['ipca'].rolling(window=12).apply(
            lambda x: (np.prod(1 + x/100) - 1) * 100
        )

        # 3. Cálculo do Juro Real (Equação de Fisher)
        # Fórmula: [(1 + Juro Nominal) / (1 + Inflação)] - 1
        df['Juro_Real'] = ((1 + df['selic']/100) / (1 + df['IPCA_12m']/100) - 1) * 100

        # Limpando valores nulos gerados pelo cálculo de 12 meses
        df_analise = df.dropna()

        print("\n--- RESUMO ESTATÍSTICO (ÚLTIMO MÊS) ---")
        ultimo = df_analise.iloc[-1]
        print(f"IPCA Acumulado: {ultimo['IPCA_12m']:.2f}%")
        print(f"Selic Nominal: {ultimo['selic']:.2f}%")
        print(f"Juro Real Líquido: {ultimo['Juro_Real']:.2f}%")

        # Visualização da evolução do Juro Real
        plt.figure(figsize=(10, 5))
        plt.fill_between(df_analise.index, df_analise['Juro_Real'], color='lightgreen', alpha=0.4)
        plt.plot(df_analise.index, df_analise['Juro_Real'], color='green', label='Juro Real (% a.a.)')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        
        plt.title('Estatística Aplicada: Evolução do Juro Real no Brasil')
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Erro no processamento: {e}")

if __name__ == "__main__":
    calcular_metricas_estatisticas()