🐍 Python para Finanças
Este diretório contém o motor lógico e os scripts de análise quantitativa do Terminal de Inteligência. Aqui, o Python é utilizado para transformar dados brutos em decisões estratégicas, utilizando bibliotecas de ponta para o mercado financeiro.

🎯 Objetivos da Pasta
O objetivo deste módulo é automatizar tarefas que levariam horas de forma manual, tais como:

Data Wrangling: Limpeza e normalização de dados oficiais da CVM e Banco Central.

Cálculos Quantitativos: Implementação de fórmulas como Graham, Bazin, Sharpe e Volatilidade.

Integração via API: Conexão com Yahoo Finance, SGS (BCB) e bases de dados abertas.

📂 Estrutura de Conteúdo
main.py: Ponto de entrada da aplicação Streamlit.

data_engine.py: Scripts para consumo e tratamento de dados.

metrics.py: Funções puras para cálculos de indicadores financeiros.

utils.py: Funções de suporte (limpeza de strings, formatação de moeda).

Biblioteca,Utilidade principal
Pandas,Manipulação de Séries Temporais e DataFrames Financeiros.
YFinance,Extração de cotações históricas e dividendos (Yahoo Finance).
NumPy,Cálculos matemáticos de alta performance e matrizes de correlação.
Requests/BS4,Web Scraping de portais que não possuem API oficial.
Plotly,Gráficos interactivos de Candlestick e evolução de Património.

📉 Exemplos de Análises Implementadas
Avaliação Fundamentalista: Cálculo automático do Valor Justo com base nos ganhos por acção e valor contabilístico.

Análise de Momentum: Implementação do IFR (RSI) para identificar pontos de sobrecompra e sobrevenda.

Análise de Correlação: Matriz de correlação entre activos para diversificação de carteira.

⚠️ Disclaimer (Aviso Legal)
Os scripts contidos nesta pasta são de carácter puramente educativo e tecnológico. 
Não constituem recomendação de compra ou venda de ativos. 
O uso de algoritmos para decisões de investimento deve ser acompanhado por um profissional certificado.
