# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
OBJETIVO: PRICING CHALLENGE
EMPRESA:  B2W
AUTOR:    laercio.serra@gmail.com
DATA:     13/10/2016
VERSÃO:   2.0
-------------------------------------------------------------------------------
"""

%matplotlib inline

# CARREGANDO OS PACOTES/BIBLIOTECAS QUE SERÃO USADAS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.pylab import rcParams
from datetime import datetime
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram


# DEFININDO O DIRETORIO DAS BASES PARA ANALISE
s_path = '/home/lserra/Documents/b2w/bases/'

# CARREGANDO OS DADOS DA BASE GERENCIAL - VENDAS POR DIA
# ESTES DADOS FORAM EXTRAIDOS DO DW CONSTRUIDO NO BANCO MYSQL
df_sales = pd.read_csv(s_path + 'vw_ger_sales_month.csv')

# LISTANDO OS 5 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
df_sales.head()

# VERIFICANDO OS TIPOS DE DADOS CARREGADOS
df_sales.dtypes

# FAZENDO A CONVERSAO DA COLUNA DATE DO DATAFRAME 
# DE OBJECT TYPE PARA DATETIME
# df_sales.DATE = df_sales.DATE.apply(lambda d: datetime.strptime(d, "%Y-%m-%d"))
# df_sales.DATE.head()

# INDEXANDO O DATAFRAME PELA COLUNA DATE
# df_sales.index = df_sales.DATE

# LISTANDO OS 10 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
# df_sales.head(10)

# FILTRANDO OS DADOS POR PRODUTOS DE CORRELACAO FORTE [P8, P9]
# ESTA CORRELACAO FOI APURADA NA ANALISE CONSTRUIDA NO R

# df_sales[(df_sales.PRODUCT == "P8") & (df_sales.PRODUCT == "P9")]
freezing_prod = df_sales[df_sales.PRODUCT == 'P8']
freezing_prod.head()

# GERANDO ESTATISTICAS BASICAS DO PRODUTO P8
# EM CIMA DE TODAS AS METRICAS JA CALCULADAS
freezing_prod.describe()

# DEFININDO O TAMANHO DE IMAGEM DO GRÀFICO
rcParams['figure.figsize'] = (15,6)

# GERANDO UM GRAFICO DE HISTOGRAMA DO PRODUTO P8
freezing_prod.QTY_ORDER.hist()

# GERANDO UM GRAFICO DE CURVA S E BARRAS HORIZONTAL DO PRODUTO P8
freezing_prod.QTY_ORDER.tail()

freezing_prod.QTY_ORDER.tail().plot()

freezing_prod.QTY_ORDER.tail().plot(kind="bar", rot=0)

# GERANDO UM GRAFICO COMPARATIVO DE MIN/MAX UNIT PRICES DO PRODUTO P8
ax = freezing_prod.MAX_UNIT_PRICE.plot(title="Min and Max Unit Prices")
freezing_prod.MIN_UNIT_PRICE.plot(style="red", ax=ax)
ax.set_ylabel("Unit Prices ($)")

# GERANDO UM GRAFICO DE TIMES SERIES DO PRODUTO P8
freezing_prod.QTY_ORDER.plot()

"""
Estimando tendência e sazonalidade:
-------------------------------------------------------------------------------
Uma tentativa para reduzir a tendência pode ser a transformação. 
Por exemplo, neste caso podemos claramente ver que existe uma tendência 
positiva significativa. Então nós podemos aplicar a transformação que penaliza
os valores mais alto. Isto pode ser realizado através da aplicação do 
cálculo do log, raiz quadrada, raiz cúbica, etc. 
-------------------------------------------------------------------------------
Neste caso estarei aplicando uma transformação (log), aqui para manter a 
simplicidade e entender o comportamento:
"""
# CRIANDO UMA CÓPIA DO DATAFRAME FILTRADO APLICANDO A FUNCAO DE LOG
# SOBRE A METRICA QTY_ORDER
df_log = np.log(freezing_prod['QTY_ORDER'])

# GERANDO UM GRAFICO PARA AVALIAR O COMPORTAMENTO DA NOVA TENDENCIA
plt.plot(df_log)

"""
-------------------------------------------------------------------------------
Neste caso mais simples, é fácil ver uma tendência para a frente nos dados. 
Mas, acredito que ainda possa existir alguns ruídos. Assim nós podemos usar 
algumas técnicas para estimar ou remodelar esta tendência e depois removê-lo 
da série. E para isso pode haver muitas maneiras de fazê-lo, e alguns dos mais 
comumente usados são:
a)Agregação – aplica-se a média para um período de tempo, como por exemplo
a média mensal/semanal.
b)Alisamento – aplica-se as chamadas média móvel.
c)Ajuste polinomial – podendo-se aplicar um modelo de regressão.
-------------------------------------------------------------------------------
"""
# APLICANDO A MEDIA MOVEL E ANALISANDO O COMPORTAMENTO DA NOVA TENDENCIA
moving_avg = pd.rolling_mean(df_log, 12)

plt.plot(df_log)
plt.plot(moving_avg, color='red')

"""
-------------------------------------------------------------------------------
A linha vermelha mostra a média móvel. Permite que este subtraia a série 
original. Observe que, uma vez que estamos com a média dos últimos 12 valores,
a média móvel não está definido para os primeiros 11 valores. 
Isto pode ser observado com o cálculo abaixo:
-------------------------------------------------------------------------------
"""
log_moving_avg_diff = df_log - moving_avg

log_moving_avg_diff.head(12)

"""
-------------------------------------------------------------------------------
Observe os primeiros 11 valores NaN. Deixa de lado esses valores NaN e vamos
verificar os outros valores para testar a estacionaridade.
-------------------------------------------------------------------------------
"""
log_moving_avg_diff.dropna(inplace=True)

log_moving_avg_diff

"""
-------------------------------------------------------------------------------
Dickey-Fuller Test: 
Este é um dos testes estatísticos para verificar a estacionaridade. 
Aqui, a hipótese nula é que o TS é não-estacionária.
Os resultados do teste são compostos por uma estatística de teste e alguns 
valores críticos para níveis de confiança de diferença. 
Se o "teste estatístico 'é menor do que o "Valor crítico", podemos rejeitar a 
hipótese nula e dizer que a série é estacionária.
-------------------------------------------------------------------------------
"""
from statsmodels.tsa.stattools import adfuller

def test_stationarity(timeseries):
    
    # Determinando rolling estatisticas
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    # Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    # Perform Dickey-Fuller test:
    print ('Resultados do teste Dickey-Fuller:')
    df_test = adfuller(timeseries, autolag='AIC')
    df_output = pd.Series(df_test[0:4], index=['Teste Estatistico','p-value',
    '#Lags Usados','Numero de Observacoes Usados'])
    for key,value in df_test[4].items():
        df_output['Valores Criticos (%s)'%key] = value
    print (df_output)


test_stationarity(log_moving_avg_diff)

"""
-------------------------------------------------------------------------------
Esta parece ser uma série muito melhor. Os valores parecem estar variando
um pouco, mas não há uma tendência específica. Além disso, a estatística de teste 
é menor que os valores críticos 5% para que possamos dizer com 95% de confiança de 
que esta é uma série estacionária.
No entanto, uma desvantagem desta abordagem particular é que o período de tempo 
tenha ser estritamente definidos. Neste caso podemos tomar médias anuais, mas em
situações complexas como previsão de um preço das ações, pode ser difícil chegar
com um número. Então, vamos aplicar uma "média móvel ponderada", onde os valores 
mais recentes é dado um peso maior. Não pode haver muitas técnica para atribuição de pesos.
Um popular é exponencialmente ponderada média móvel, onde os pesos são
atribuídos a todos os valores anteriores, como um factor de deterioração. 
Isto pode ser implementado assim:
-------------------------------------------------------------------------------
"""
expwighted_avg = pd.ewma(df_log, halflife=12)

plt.plot(df_log)
plt.plot(expwighted_avg, color='red')

"""
-------------------------------------------------------------------------------
Note-se que aqui o parâmetro "semi-vida" é utilizado para definir a quantidade de
decaimento exponencial. Esta é apenas uma suposição aqui, que dependem em grande medida
no domínio do negócio. Outros parâmetros de capacidade e de centro de massa também pode
ser utilizado para definir decaimento que são discutidos na ligação partilhada acima. 
Agora, vamos remover esta da série e verificar novamente a estacionaridade:
-------------------------------------------------------------------------------
"""
log_ewma_diff = df_log - expwighted_avg

test_stationarity(log_ewma_diff)

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Essa série tem variações ainda menores em média e desvio padrão em magnitude.
Além disso, o teste estatístico é menor do que o valor crítico de 1%, o que é melhor
do que no caso anterior. 
Então, podemos notar que, neste caso, não haverá valores em falta
já que todos os valores de partida são dados pesos. 
Então, ele vai trabalhar mesmo sem valores anteriores.
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
Eliminando tendencia e sazonalidade:
-------------------------------------------------------------------------------
As técnicas de redução de tendência discutidos anteriormente, não funcionam para
todos os casos, particularmente aqueles com alta sazonalidade. 
Então, agora vamos discutir duas maneiras de remover esta tendência e sazonalidade:

a) Diferenciação - tomando a diferença com um determinado intervalo de tempo
b) Decomposição - modelagem que trata tanto a tendência e sazonalidade e removê-los
do modelo.

Diferenciação: Um dos métodos mais comuns de lidar com ambos (tendência e
sazonalidade) é diferencial. Nesta técnica, tomamos a diferença da
observação num instante particular com que no instante anterior. Isto
funciona bem na maior parte em melhorar a estacionaridade. 
A diferenciação pode ser feito da seguinte forma:
-------------------------------------------------------------------------------
"""
log_diff = df_log - df_log.shift()

plt.plot(log_diff)

# Isto parece ter reduzido a tendência consideravelmente.
# Vamos verificar usando estes valores:
log_diff.dropna(inplace=True)
log_diff

test_stationarity(log_diff)

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Podemos ver que as variações médias e de desvio padrão, têm pequenas variações 
com o tempo.
Além disso, a estatística de teste Dickey-Fuller é menor do que o valor crítico de 10%,
assim, o TS é estacionário com 90% de confiança. Também, pode tomar o segundo ou
diferenças de terceira ordem que poderia obter resultados ainda melhores em certas
aplicações.
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
Decomposição: Nesta abordagem, tanto tendência e sazonalidade são modelados
separadamente, e a parte restante da série é devolvido.
-------------------------------------------------------------------------------
"""
# ESTE TRECHO DO CODIGO ESTÁ COM PROBLEMAS.
# ValueError: freq D not understood. Please report if you think this in error.
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(df_log, freq=61320)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(df_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Tendência')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Sazonalidae')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Resíduos')
plt.legend(loc='best')
plt.tight_layout()

ts_log_decompose = residual
ts_log_decompose.dropna(inplace=True)
test_stationarity(ts_log_decompose)

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Sem conclusão
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
Clustering Analysis - Dendograma
-------------------------------------------------------------------------------
"""
# CRIANDO UM NOVO DATAFRAME DE VENDAS A PARTIR DO DATAFRAME EXISTENTE
# SELECIONANDO SOMENTE AS COLUNAS PRODUCT, QTY_ORDER
new_df = df_sales[['PRODUCT', 'QTY_ORDER']]
# LISTANDO OS 5 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
new_df.head()
# AGRUPANDO O NOVO DATAFRAME POR PRODUTO
new_df = new_df.groupby(['PRODUCT']).aggregate(np.sum)
# LISTANDO OS 15 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
new_df.head(15)
# CALCULANDO OS DADOS PARA A CRIACAO DE UM GRAFICO DO TIPO DENDOGRAMA
data_dist = pdist(new_df)  # calculando as distâncias
data_link = linkage(data_dist)  # calculando as relações
# CRIANDO UM GRAFICO DO TIPO DENDOGRAMA
dendrogram(data_link)
plt.xlabel('Products')
plt.ylabel('Orders')
plt.suptitle('Orders Cluster Analysis', fontweight='bold', fontsize=14);

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Sem conclusão
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
Clustering Analysis - Orders by Workdays
-------------------------------------------------------------------------------
"""
# CRIANDO UM NOVO DATAFRAME DE VENDAS A PARTIR DE UM NOVO ARQUIVO
new_df = pd.read_csv(s_path + 'sel_sales_day_wo_events.csv')
# SELECIONANDO SOMENTE AS COLUNAS PRODUCT, QTY_ORDER
new_df = new_df[['WEEKDAY', 'PRODUCT', 'QTY_ORDER']]
# VERIFICANDO OS TIPOS DE DADOS CARREGADOS
new_df.dtypes
# LISTANDO OS 15 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
new_df.head(15)
# DEFININDO O TAMANHO DE IMAGEM DO GRÀFICO
rcParams['figure.figsize'] = (14,12)
rcParams['font.size'] = 14
# GERANDO O GRÁFICO
sns.set_style("whitegrid")
g=sns.swarmplot(x='WEEKDAY',y='QTY_ORDER',hue='PRODUCT',data=new_df)
g.set(xlabel="Weekday", ylabel="Number of Orders")

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Sem conclusão
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
Clustering Analysis - Orders by Events
-------------------------------------------------------------------------------
"""
# CRIANDO UM NOVO DATAFRAME DE VENDAS A PARTIR DE UM NOVO ARQUIVO
new_df = pd.read_csv(s_path + 'sel_sales_day_w_events.csv')
# SELECIONANDO SOMENTE AS COLUNAS PRODUCT, QTY_ORDER
new_df = new_df[['WEEKDAY', 'PRODUCT', 'QTY_ORDER']]
# VERIFICANDO OS TIPOS DE DADOS CARREGADOS
new_df.dtypes
# LISTANDO OS 15 PRIMEIROS REGISTROS PARA SIMPLES CONFERENCIA
new_df.head(15)
# DEFININDO O TAMANHO DE IMAGEM DO GRÀFICO
rcParams['figure.figsize'] = (14,12)
rcParams['font.size'] = 14
# GERANDO O GRÁFICO
sns.set_style("whitegrid")
g=sns.swarmplot(x='WEEKDAY',y='QTY_ORDER',hue='PRODUCT',data=new_df)
g.set(xlabel="Weekday", ylabel="Number of Orders")

"""
-------------------------------------------------------------------------------
>> CONCLUSÃO:
Sem conclusão
-------------------------------------------------------------------------------
"""