#importando a biblioteca streamlit como st, para criação de dashboard
import streamlit as st
#importando a biblioteca pandas como pd, para tratamento de dados
import pandas as pd
#importando a biblioteca matplotlib e sua sub biblioteca/módulo pyplot como plt, para geração de gráficos
import matplotlib.pyplot as plt
#importando a biblioteca seaborn como sns, para geração de gráficos mais estatísticos de alta qualidade e mais fáceis de usar
import seaborn as sns

# Título do Dashboard
st.title('Meu Dashboard Interativo')


#carregando a planilha "data_imdb1000.csv" devidamente separada em colunas anteriormente.
#Após a separação em colunas no excel, o sistema python entendeu que seus separadores passaram a ser ";", então foi indicado no código (sep = ";")
#indiquei no código também para que fosse pulado os espaços iniciais
#padronizei a base de dados na planilha no padrão utf-8 para não haver incompatibilidade
df = pd.read_csv('data_imdb1000.csv' , sep= ";", skipinitialspace=True , encoding='utf-8')


#Verifiquei os tipos de caracteres em cada coluna
#print(df.dtypes)

#Verifiquei quantos espaços vazios há na base de dados
# Convertendo 'numVotes' para float, tratando 'VAZIO' para que não cause erro
df['numVotes'] = pd.to_numeric(df['numVotes'], errors='coerce').fillna(0)  # Preencher NaNs com 0

df['averageRating'] = pd.to_numeric(df['averageRating'], errors='coerce')  # Converter para numérico
df['averageRating'] = df['averageRating'].fillna(0)  # Preencher NaNs com 0


#tratei os espaços vazios como preenchimento com "Vazio" para nao perder o resto das informações da linha
df = df.fillna("VAZIO")
#print(df.fillna("VAZIO"))

# Preencher NaNs resultantes de averageRating com um valor adequado (por exemplo, 0 ou um valor médio)
df['averageRating'] = df['averageRating'].fillna(0)  # Atribuir o resultado de volta à coluna


#verifiquei apenas as 10 primeiras linhas para ver se as formatações estavam corretas
#n = 10
#print(df.head(n))

#exibir o DF original
#print("DataFrame original:")
#print(df)

# Separar os gêneros em colunas diferentes usando get_dummies (eles estão misturados dentro da coluna genres, separados por vírgula)
generos_dummies = df['genres'].str.get_dummies(sep=', ')

# Somar as colunas para contar a frequência de cada gênero
frequencia_genres = generos_dummies.sum()

# Exibindo a frequência de gêneros
#print("\nFrequência de gêneros:")
#print(frequencia_genres)

# Criando um gráfico de barras para frequência de gêneros
plt.figure(figsize=(8, 6))
frequencia_genres.plot(kind='bar', color='skyblue')
plt.title('Frequência de Gêneros')
plt.xlabel('')
plt.ylabel('Frequência')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()  # Ajusta o layout para não cortar os rótulos
plt.show()
st.pyplot(plt)

# Ordenar o DataFrame pelos números de votos em ordem decrescente e mostrar os 10 primeiros
top_votados = df.sort_values(by='numVotes', ascending=False)

top_votados10 = top_votados.head(10)

# Exibindo os 10 títulos mais votados
#print("\n10 Títulos mais votados:")
#print(top_votados[['title', 'numVotes']])

#Série mais votada
# Encontrar o título mais votado e o número de votos correspondente
titulo_mais = df['title'][df['numVotes'].idxmax()]  # Obter o título correspondente ao menor número de votos
votos_mais = df['numVotes'].max()  # Obter o menor número de votos diretamente do DataFrame original

# Criar uma figura para a caixa de informação
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')  # Oculta os eixos

# Adicionar a caixa de texto com as informações do título mais votado
info_text = f"Título mais votado:\n{titulo_mais}\nNúmero de votos: {votos_mais}"
plt.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=12, color='black',
         bbox=dict(facecolor='lightblue', edgecolor='gray', boxstyle='round,pad=0.5'))

plt.title(" ", fontsize=14)
plt.tight_layout()
plt.show()
st.pyplot(plt)

#Série menos votada
# Encontrar o título menos votado e o número de votos correspondente
df['numVotes'].gt(0).any()
min_idx = df['numVotes'][df['numVotes'] > 0].idxmin()  #Índice do menor número de votos onde numVotes > 0
titulo_menos = df.loc[min_idx, 'title']
votos_menos = df.loc[min_idx, 'numVotes']

# Criar uma figura para a caixa de informação
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')  # Oculta os eixos

# Adicionar a caixa de texto com as informações do título mais votado
info_text = f"Título menos votado:\n{titulo_menos}\nNúmero de votos: {votos_menos}"
plt.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=12, color='black',
         bbox=dict(facecolor='lightblue', edgecolor='gray', boxstyle='round,pad=0.5'))

plt.title(" ", fontsize=14)
plt.tight_layout()
plt.show()
st.pyplot(plt)

# Criando o gráfico de barras de 10 títulos mais votados
plt.figure(figsize=(8, 6))
plt.bar(top_votados10['title'], top_votados10['numVotes'], color='skyblue')
plt.title('10 Títulos Mais Votados')
plt.xlabel('')
plt.ylabel('Número de Votos')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()  # Ajusta o layout para evitar cortes
plt.show()
st.pyplot(plt)

# Ordenar o DataFrame pelas pontuações em ordem decrescente
top_pontuados = df.sort_values(by='averageRating', ascending=False).head(10)

# Exibindo os 10 com as melhores pontuações em títulos
#print("\n10 anos com as melhores pontuações em títulos:")
#print(top_pontuados[['releaseYear', 'averageRating']])

# Criando o gráfico de barras de 10 anos de lançamento mais pontuados
plt.figure(figsize=(8, 6))
plt.bar(top_pontuados['releaseYear'], top_pontuados['averageRating'], color='skyblue')  # **Alterado para top_pontuados**
plt.title('10 anos de lançamento Mais pontuados')
plt.xlabel('')
plt.ylabel('Pontuação')
plt.xticks(ticks=top_pontuados['releaseYear'], labels=top_pontuados['releaseYear'], rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()  # Ajusta o layout para evitar cortes
plt.show()
st.pyplot(plt)

# Ordenar o DataFrame pelos números de votos em ordem decrescente
top_genresvot = df.sort_values(by='numVotes', ascending=False).head(10)

# Exibindo os 10 gêneros mais votados
#print("\n10 Gêneros mais votados:")
#print(top_genresvot[['genres', 'numVotes']])

# Criando o gráfico de barras de 10 grupos de gêneros mais votados
plt.figure(figsize=(8, 6))
plt.bar(top_genresvot['genres'], top_genresvot['numVotes'], color='skyblue')
plt.title('10 grupo de gêneros mais votados')
plt.xlabel('')
plt.ylabel('Número de Votos')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()  # Ajusta o layout para evitar cortes
plt.show()
st.pyplot(plt)

