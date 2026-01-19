from bcb import sgs
import pandas as pd
import matplotlib.pyplot as plt

# 1. Coleta Individual (mais seguro contra erros de API)
try:
    print("Coletando dados da Selic...")
    selic = sgs.get({'selic': 432}, start='2017-01-01')
    
    print("Coletando dados do IPCA...")
    ipca = sgs.get({'ipca': 433}, start='2017-01-01')

    # 2. Tratamento de Dados (Estatística/Modelagem)
    # Transformamos a Selic diária em média mensal para bater com o IPCA
    selic_mensal = selic.resample('M').mean()

    # Unindo as duas tabelas pela data (Join)
    df = pd.concat([selic_mensal, ipca], axis=1)
    df.columns = ['Selic', 'IPCA']
    
    # Preenche valores vazios se houver (Data Cleaning)
    df = df.fillna(method='ffill')

    print("Dados carregados com sucesso!")

    # 3. Visualização Profissional
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Selic'], label='Selic Meta (% a.a.)', color='#1f77b4', linewidth=2)
    plt.plot(df.index, df['IPCA'], label='IPCA Mensal (%)', color='#d62728', marker='o')

    plt.title('Conjuntura Econômica: Selic vs IPCA', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

except Exception as e:
    print(f"Erro ao capturar dados: {e}")