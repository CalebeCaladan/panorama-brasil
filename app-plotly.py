import yfinance as yf
import streamlit as st
import datetime 
import plotly.express as px
import pandas as pd
from pandas.tseries.offsets import BDay
import requests
yf.pdr_override()

st.write("""
# Panorama de Mercado
Esse WebApp resume o que aconteceu no dia no mercado **Brasileiro** de forma visual. \n
**Ações**, **FFis**, **Renda Fixa**, e outros papeis""")

#st.sidebar.header('Parametros')
today = datetime.date.today()

lista_ativos_ibov = ['WEGE3.SA', 'EMBR3.SA', 'AZUL4.SA', 'CCRO3.SA', 'ECOR3.SA', 'GOLL4.SA', 'RAIL3.SA', 'BRFS3.SA', 'JBSS3.SA', 'MRFG3.SA', 'BEEF3.SA', 'ABEV3.SA', 'ASAI3.SA', 'CRFB3.SA', 'PCAR3.SA', 'NTCO3.SA',
					'BTOW3.SA', 'LAME4.SA', 'LREN3.SA', 'MGLU3.SA', 'VVAR3.SA', 'HGTX3.SA', 'CYRE3.SA', 'EZTC3.SA', 'JHSF3.SA', 'MRVE3.SA', 'CVCB3.SA', 'COGN3.SA', 'RENT3.SA', 'LCAM3.SA', 'YDUQ3.SA', 'BRML3.SA',
					'IGTA3.SA', 'MULT3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BBAS3.SA', 'BPAC11.SA', 'ITSA4.SA', 'ITUB4.SA', 'SANB11.SA', 'BBSE3.SA', 'IRBR3.SA', 'SULA11.SA', 'B3SA3.SA', 'CIEL3.SA', 'KLBN11.SA',
					'SUZB3.SA', 'BRAP4.SA', 'VALE3.SA', 'BRKM5.SA', 'GGBR4.SA', 'GOAU4.SA', 'CSNA3.SA', 'USIM5.SA', 'CSAN3.SA', 'PETR3.SA', 'PETR4.SA', 'BRDT3.SA', 'PRIO3.SA', 'UGPA3.SA', 'HYPE3.SA', 'RADL3.SA',
					'FLRY3.SA', 'HAPV3.SA', 'GNDI3.SA', 'QUAL3.SA', 'TOTS3.SA', 'VIVT3.SA', 'TIMS3.SA', 'SBSP3.SA', 'CMIG4.SA', 'CPLE6.SA', 'CPFE3.SA', 'ELET3.SA', 'ELET6.SA', 'ENBR3.SA', 'ENGI11.SA', 'ENEV3.SA',
					'EGIE3.SA', 'EQTL3.SA', 'TAEE11.SA']

#ibov = yf.download(lista_ativos_ibov, interval='1d', period='5d')['Close']
ibov = yf.download(lista_ativos_ibov, interval='1d', start='2021-03-20', end='2021-03-26')['Close']

ibov_ajustado = pd.DataFrame([])
ibov = ibov.dropna()

for ativo in ibov:
	r = ((ibov[ativo] / ibov[ativo].shift(1)) - 1) #* 100
	ibov_ajustado = ibov_ajustado.append(r)

ibov_ajustado = ibov_ajustado.filter([ibov_ajustado.columns[-1]])
ibov_ajustado = ibov_ajustado.rename(columns={ibov_ajustado.columns[-1]: '%'})
ibov_ajustado = ibov_ajustado.sort_values(by=['%'])
ibov_ajustado.index = ibov_ajustado.index.str.rstrip('.SA')


#grafico_ibov = yf.download('^BVSP', interval='1d', period='1y')['Close']
grafico_ibov = yf.download('^BVSP', interval='1d', start='2019-01-01', end='2021-03-26')['Close']
grafico_ibov = grafico_ibov.rename('Ibov')

fig = px.line(grafico_ibov, 
	x=grafico_ibov.index, 
	y="Ibov",
	width=800, height=350
	)

fig.update_yaxes(automargin=True, title=None)
fig.update_xaxes(title=None)

maiores_altas = ibov_ajustado[-5:]
maiores_altas = maiores_altas.filter([maiores_altas.columns[-1]])
maiores_altas = maiores_altas.rename(columns={maiores_altas.columns[-1]: '%'})
maiores_altas = maiores_altas.sort_values(maiores_altas.columns[-1], ascending=False)
preco_atual = []
for ativo in maiores_altas.index.values:
	preco_atual.append(ibov.filter(like=ativo).tail(1).values[0].item(0))
maiores_altas['Preço'] = preco_atual
maiores_altas = maiores_altas[['Preço' , '%']]

maiores_baixas = ibov_ajustado[0:5]
maiores_baixas = maiores_baixas.filter([maiores_baixas.columns[-1]])
maiores_baixas = maiores_baixas.rename(columns={maiores_baixas.columns[-1]: '%'})
maiores_baixas = maiores_baixas.sort_values(maiores_baixas.columns[-1], ascending=True)
preco_atual = []
for ativo in maiores_baixas.index.values:
	preco_atual.append(ibov.filter(like=ativo).tail(1).values[0].item(0))
maiores_baixas['Preço'] = preco_atual
maiores_baixas = maiores_baixas[['Preço' , '%']]

st.header(f"Desempenho do dia {today.strftime('%d/%m/%Y')}" )

col1, col2 = st.beta_columns([3, 1])

with col1:
	st.plotly_chart(fig, use_container_width=True)

with col2:
	st.subheader('Indice Ibovespa')
	st.write(f'{grafico_ibov.tail(1).round(0).values[0]:.0f} pts | {grafico_ibov.pct_change().tail(1).values[0]:.2%}')
	st.subheader('Maior Alta')
	st.write(f'{maiores_altas.head(1).index.values[0]} | {maiores_altas["%"].head(1).values[0]:.2%}') 
	st.subheader('Maior Baixa')
	st.write(f'{maiores_baixas.head(1).index.values[0]} | {maiores_baixas["%"].head(1).values[0]:.2%}') 
	

col1, col2 = st.beta_columns([2, 2])

with col1:
	st.subheader(f"Maiores Altas")
	st.dataframe(maiores_altas.style.format({'Preço' : "{:.2f}", '%' : "{:.2%}"}))

with col2:
	st.subheader(f"Maiores Baixas")
	st.dataframe(maiores_baixas.style.format({'Preço' : "{:.2f}", '%' : "{:.2%}"}))