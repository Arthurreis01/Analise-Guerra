import pandas as pd
import streamlit as st
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
# PUxar uma base de dados de compras de imoveis
st.header('Falaties in conflite Palestine x Israel 2000 to 2023')


df = pd.read_csv("analysis_conflit_Israel.csv", sep=",")

df['date_of_event'] = pd.to_datetime(df['date_of_event'])

#análise 1: Número de mortos entre Israeli e Palestina (piechart)
# Função para contar mortes por país
def contar_mortes(df):
    mortes_em_israel = (df['citizenship'] == 'Israeli').sum()
    mortes_na_palestina = (df['citizenship'] == 'Palestinian').sum()
    return mortes_em_israel, mortes_na_palestina

# Chame a função e obtenha os resultados
mortes_em_israel, mortes_na_palestina = contar_mortes(df)

# Crie um DataFrame para o gráfico de pizza
df_pizza = pd.DataFrame({'País': ['Israel', 'Palestina'], 'Mortes': [mortes_em_israel, mortes_na_palestina]})
# Crie o gráfico de pizza com Plotly Express

col1, col2 = st.columns (2)

fig = px.pie(df_pizza, names='País', values='Mortes', title='Mortes em Israel vs. Palestina', color= 'País')
col1.plotly_chart(fig, use_container_width=True)
### transformar porcentagem em valor

#análise 2: Event location district (maps com bolhas de maiores ataques - filtro por anos)

#criar sidebar com selectslider com anos



#análise 3: Analise de mortes (idade x anos) quantidade de ocorrências por idade em cada ano
#colocar datas em formato de periodo mensal
df["Year"] = df["date_of_event"].apply(lambda x: str(x.year))

def contar_mortes_por_idade(df):
    # Agrupe os dados por idade e conte o número de mortes em cada grupo
    mortes_por_idade = df.groupby('age').size().reset_index(name='Quantidade de Mortes')

    # Classifique os dados por idade em ordem crescente
    mortes_por_idade = mortes_por_idade.sort_values(by='age')

    return mortes_por_idade

# Chame a função para obter o DataFrame com as mortes por idade
mortes_por_idade_df = contar_mortes_por_idade(df)

fig_age = px.bar(mortes_por_idade_df, x='age', y='Quantidade de Mortes', title= "Mortes por idade de 1990 a 2023")
col2.plotly_chart(fig_age, use_container_width=True)




# plotador de noticias em tempo real
import requests
from bs4 import BeautifulSoup

# Defina o User-Agent no cabeçalho
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'"
}

def get_news(keyword='Israel'):
    url = 'https://www.globo.com/'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    noticias = soup.find_all('a')
    tgt_class1 = 'post__title'
    tgt_class2 = 'post-multcontent__link--title__text'

    news_dict = {}

    for noticia in noticias:
        if (noticia.h2 is not None) and (tgt_class1 in noticia.h2.get('class', [])) and keyword in noticia.h2.text:
            news_dict[noticia.h2.text] = noticia['href']
        if (noticia.h2 is not None) and (tgt_class2 in noticia.h2.get('class', [])) and keyword in noticia.h2.text:
            news_dict[noticia.h2.text] = noticia['href']

    return news_dict

keyword = 'Israel'
news = get_news(keyword)
len(news)

# Para imprimir as notícias no Streamlit
st.write(f"Acompanhe as últimas notícias do site globo em '{keyword}':")
for title, link in news.items():
    st.write(f"[{title}]({link})")

