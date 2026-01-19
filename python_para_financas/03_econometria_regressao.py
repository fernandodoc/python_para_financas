import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from bcb import sgs

# Configuração visual para seus relatórios de assessor
plt.style.use('seaborn-v0_8-whitegrid')

def realizar_analise_econometrica():
    try:
        print("Coletando dados separadamente para evitar erro de conexão...")
        
        # Coleta individual (Mais estável que pedir as duas juntas)
        selic_bruta = sgs.get(432, start='2017-01-01') # Selic Meta
        ipca_bruto = sgs.get(433, start='2017-01-01')  # IPCA Mensal
        
        print("Tratando e alinhando as séries históricas...")
        # Unindo as tabelas pelo índice de data
        df = pd.concat([selic_bruta, ipca_bruto], axis=1)
        df.columns = ['selic', 'ipca']
        
        # Ajustando para fechamento mensal
        df = df.resample('ME').last()
        
        # Cálculo do IPCA acumulado 12 meses (Fundamental para a Regressão)
        df['IPCA_12m'] = df['ipca'].rolling(window=12).apply(
            lambda x: (np.prod(1 + x/100) - 1) * 100
        )
        
        # Removendo valores nulos (os primeiros 11 meses)
        df_limpo = df.dropna().copy()

        # --- MODELAGEM ECONOMÉTRICA ---
        # Y (Dependente): Selic | X (Independente): Inflação
        Y = df_limpo['selic']
        X = df_limpo['IPCA_12m']
        X = sm.add_constant(X) # Adiciona a constante (Beta 0)
        
        modelo = sm.OLS(Y, X).fit()

        print("\n" + "="*55)
        print("      INTERPRETAÇÃO TÉCNICA (GUIA DO FERNANDO)")
        print("="*55)
        
        # 1. R-Squared: O termômetro da relação
        # Se for alto (ex: 0.75), significa que a Selic segue muito de perto a inflação.
        # É um ótimo argumento para mostrar ao cliente a previsibilidade do BC.
        print(f"-> Poder de Explicação (R²): {modelo.rsquared:.2f}")
        
        # 2. Beta (Coeficiente do IPCA): A força da reação
        # Mostra quanto o BC sobe de juros para cada 1% de inflação adicional.
        # Útil para prever o teto da Selic em ciclos de alta.
        coef = modelo.params['IPCA_12m']
        print(f"-> Sensibilidade (Beta): {coef:.2f}")
        
        # 3. P-Value: A validação estatística
        # Menor que 0.05 significa que a relação NÃO é coincidência.
        p_valor = modelo.pvalues['IPCA_12m']
        status = "CONFIÁVEL" if p_valor < 0.05 else "NÃO CONFIÁVEL"
        print(f"-> Confiança Estatística: {status} (p-value: {p_valor:.4f})")

        # --- GRÁFICO DE DISPERSÃO E TENDÊNCIA ---
        plt.figure(figsize=(10, 6))
        plt.scatter(df_limpo['IPCA_12m'], df_limpo['selic'], color='#1f77b4', alpha=0.5, label='Dados Históricos')
        plt.plot(df_limpo['IPCA_12m'], modelo.predict(X), color='red', linewidth=2, label='Modelo de Reação')
        
        plt.title('Econometria: Relação Histórica Inflação vs. Selic', fontsize=14)
        plt.xlabel('IPCA Acumulado 12 meses (%)')
        plt.ylabel('Taxa Selic (% a.a.)')
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Erro na análise: {e}")

if __name__ == "__main__":
    realizar_analise_econometrica()