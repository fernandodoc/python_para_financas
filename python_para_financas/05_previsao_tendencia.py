import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Configuração visual profissional
plt.style.use('seaborn-v0_8-whitegrid')

def realizar_previsao_ibov():
    try:
        print("1/3 - Coletando histórico longo do Ibovespa para aprendizado do modelo...")
        ticker = yf.Ticker('^BVSP')
        # Buscamos desde 2015 para que o modelo entenda diferentes ciclos de mercado
        df = ticker.history(start='2015-01-01')['Close']
        df.index = df.index.tz_localize(None)
        
        # Resample para mensal (ME) para reduzir ruídos diários e focar na tendência
        df_m = df.resample('ME').last()

        print("2/3 - Treinando modelo Holt-Winters (Tendência + Sazonalidade)...")
        # Ajustamos o modelo considerando tendência aditiva e sazonalidade de 12 meses
        modelo = ExponentialSmoothing(
            df_m, 
            trend='add', 
            seasonal='add', 
            seasonal_periods=12
        ).fit()

        # Projetando os próximos 6 meses
        previsao = modelo.forecast(6)

        print("\n" + "="*60)
        print("      PROJEÇÃO DE TENDÊNCIA: IBOVESPA (GUIA DO FERNANDO)")
        print("="*60)
        
        # INTERPRETAÇÃO PARA O ASSESSOR:
        
        ultimo_preco = df_m.iloc[-1]
        preco_alvo = previsao.iloc[-1]
        upside = ((preco_alvo / ultimo_preco) - 1) * 100

        print(f"-> Último Fechamento: {ultimo_preco:.0f} pontos")
        print(f"-> Projeção para 6 meses: {preco_alvo:.0f} pontos")
        print(f"-> Upside Projetado (Tendência): {upside:.2f}%")

        print("-" * 60)
        # Comentário Ético e Técnico:
        # Lembre-se, Fernando: modelos estatísticos projetam a CONTINUIDADE do padrão atual.
        # Use isso para mostrar ao cliente se o "momentum" do mercado é favorável.
        if upside > 0:
            print("INSIGHT: O modelo identifica uma inércia de ALTA. Estrutura gráfica favorável.")
        else:
            print("INSIGHT: O modelo identifica uma inércia de BAIXA ou lateralização.")

        print("\n3/3 - Gerando Gráfico de Projeção...")
        plt.figure(figsize=(12, 6))
        # Mostramos apenas os últimos 3 anos no gráfico para não esmagar a visualização
        plt.plot(df_m.iloc[-36:], label='Histórico Real', color='#1f77b4', linewidth=2)
        plt.plot(previsao, label='Projeção (6 meses)', color='red', linestyle='--', marker='o')
        
        plt.title('Modelo de Previsão: Tendência Estocástica do Ibovespa', fontsize=14)
        plt.ylabel('Pontos')
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Erro na modelagem de previsão: {e}")

if __name__ == "__main__":
    realizar_previsao_ibov()