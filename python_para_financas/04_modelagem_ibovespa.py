import yfinance as yf
from bcb import sgs
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Estilo visual profissional
plt.style.use('seaborn-v0_8-whitegrid')

def realizar_modelagem_ibov():
    try:
        print("1/4 - Coletando Ibovespa (Yahoo) e Selic (BCB)...")
        
        # Coleta Ibovespa e limpa o fuso horário para permitir o cruzamento de dados
        ticker = yf.Ticker('^BVSP')
        ibov = ticker.history(start='2017-01-01', interval='1d')['Close']
        ibov.index = ibov.index.tz_localize(None) 
        
        # Coleta Selic individualizada para evitar erros de servidor
        selic = sgs.get(432, start='2017-01-01')

        print("2/4 - Alinhando dados mensais...")
        # 'ME' garante o fechamento do último dia do mês
        ibov_m = ibov.resample('ME').last()
        selic_m = selic.resample('ME').last()

        # Criando DataFrame único
        df = pd.DataFrame({
            'Ibov_Preco': ibov_m,
            'Selic': selic_m.iloc[:, 0]
        }).dropna()

        # Cálculo do Retorno Mensal (%) - Essencial para análise de volatilidade
        df['Retorno_Ibov'] = df['Ibov_Preco'].pct_change() * 100
        df = df.dropna()

        print("3/4 - Executando Econometria (Bolsa vs Juros)...")
        Y = df['Retorno_Ibov']
        X = sm.add_constant(df['Selic'])
        modelo = sm.OLS(Y, X).fit()

        print("\n" + "="*60)
        print("      ANÁLISE DE ATIVOS: IBOVESPA vs SELIC (GUIA DO FERNANDO)")
        print("="*60)

        # INTERPRETAÇÃO TÉCNICA PARA O ASSESSOR:
        
        # 1. R-Squared: O quanto o juro explica a variação da bolsa?
        # Nota: Geralmente é baixo (0.10 a 0.20), pois a bolsa depende de lucro e exterior,
        # não apenas da Selic. Use isso para explicar Diversificação.
        print(f"-> R-Squared: {modelo.rsquared:.2f}")
        
        # 2. Beta (Sensibilidade): Se a Selic sobe 1%, o que acontece com o Ibov?
        # Interpretação: Se for -0.8, a bolsa tende a cair 0.8% no mês da alta.
        coef = modelo.params['Selic']
        print(f"-> Sensibilidade (Beta): {coef:.2f}")
        
        p_valor = modelo.pvalues['Selic']
        print(f"-> Significância: {'RELEVANTE' if p_valor < 0.05 else 'POUCO RELEVANTE'}")

        print("-" * 60)
        if coef < 0:
            print("INSIGHT: Relação INVERSA. Ótimo momento para explicar que juro alto esmaga o múltiplo das ações.")

        print("\n4/4 - Gerando Gráfico de Dois Eixos...")
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Eixo 1: Ibovespa (Azul)
        ax1.plot(df.index, df['Ibov_Preco'], color='#1f77b4', linewidth=2, label='Ibovespa')
        ax1.set_ylabel('Pontos Ibovespa', color='#1f77b4', fontsize=12, fontweight='bold')
        
        # Eixo 2: Selic (Vermelho)
        ax2 = ax1.twinx()
        ax2.plot(df.index, df['Selic'], color='#d62728', linestyle='--', linewidth=2, label='Selic')
        ax2.set_ylabel('Selic % a.a.', color='#d62728', fontsize=12, fontweight='bold')

        plt.title('Relacionamento Histórico: Ativos de Risco vs Taxa de Juros', fontsize=14)
        plt.show()

    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    realizar_modelagem_ibov()