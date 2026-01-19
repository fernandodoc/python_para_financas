from bcb import sgs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração visual
plt.style.use('seaborn-v0_8-whitegrid')

def gerar_analise_macro():
    try:
        print("Acessando API do Banco Central...")
        
        # 1. Coleta de dados (Janela de 7 anos para evitar erro de limite da API)
        # 432: Selic Meta, 433: IPCA Mensal
        dados = sgs.get({'selic': 432, 'ipca': 433}, start='2017-01-01')
        
        # 2. Tratamento de Dados
        # A Selic vem diária, vamos pegar a última taxa de cada mês
        df = dados.resample('M').last()
        
        # Cálculo do IPCA acumulado 12 meses (Lógica de Matemática Financeira)
        # Aplicamos o produto de (1 + taxa) para os últimos 12 meses
        df['IPCA_12m'] = df['ipca'].rolling(window=12).apply(
            lambda x: (np.prod(1 + x/100) - 1) * 100
        )

        # 3. Cálculo do Juro Real Ex-post (Selic - IPCA 12m)
        # Simplificado para análise de conjuntura: (1+i)/(1+inf) - 1
        df['Juro_Real'] = ((1 + df['selic']/100) / (1 + df['IPCA_12m']/100) - 1) * 100

        print("Dados processados com sucesso!")

        # 4. Visualização Profissional
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Eixo principal: Selic e IPCA
        ax1.plot(df.index, df['selic'], label='Selic Meta (% a.a.)', color='#1f77b4', linewidth=2)
        ax1.plot(df.index, df['IPCA_12m'], label='IPCA Acum. 12m (% a.a.)', color='#d62728', linestyle='--')
        
        # Preenchimento para destacar o Juro Real Positivo
        ax1.fill_between(df.index, df['selic'], df['IPCA_12m'], 
                         where=(df['selic'] > df['IPCA_12m']), 
                         color='green', alpha=0.1, label='Juro Real')

        ax1.set_title('Análise de Conjuntura: Política Monetária vs Inflação', fontsize=14)
        ax1.set_ylabel('Taxa % ao ano')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    gerar_analise_macro()