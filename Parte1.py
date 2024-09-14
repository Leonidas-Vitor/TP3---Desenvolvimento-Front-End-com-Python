import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import pydeck as pdk
import altair as alt
from geopy.geocoders import Nominatim
import time

st.title("TP3 - Desenvolvimento Front-End com Python")


data_source = 'https://www.data.rio/documents/ad8fb7b4220d4a06b9ee69ca08b57d3c/about'

st.subheader("1 - Objetivo e Motivação:",divider=True)
#Explique o objetivo do dashboard que você está desenvolvendo e a motivação por trás da escolha dos dados e funcionalidades que serão implementados.

st.markdown('''O objetivo desse dashboard é permitir ao usuário visualizar, editar e fazer download dos dados de visitantes em trilhas do Parque Nacional da Tijuca.''')

st.markdown('**Fonte dos dados:**')
st.page_link(data_source, label = 'Número de visitantes por mês em trilhas no Parque Nacional da Tijuca entre 2011-2020',icon='🌳')



st.subheader("2 - Upload de Arquivo CSV:",divider=True)
#Crie uma interface em Streamlit que permita ao usuário fazer o upload de um arquivo CSV contendo dados de turismo do portal Data.Rio

@st.cache_data
def load_data():
    df = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZoMBw66yzAe4JNi16mg/root/content',sep=';')
    df.columns = ['Setor','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    df = df.apply(lambda x: x.str.replace(' ','').astype(int) if x.name != 'Setor' else x)
    return df

@st.cache_data
def upload_data(uploaded_file, sep):
    df = pd.read_csv(uploaded_file, sep=sep)
    df.columns = ['Setor','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    df = df.apply(lambda x: x.str.replace(' ','').astype(int) if x.name != 'Setor' else x)
    return df

st.markdown('Colunas esperadas no arquivo csv: ')
st.info('Setor;Janeiro;Fevereiro;Março;Abril;Maio;Junho;Julho;Agosto;Setembro;Outubro;Novembro;Dezembro', icon="ℹ️")
#st.markdown('*Setor;Janeiro;Fevereiro;Março;Abril;Maio;Junho;Julho;Agosto;Setembro;Outubro;Novembro;Dezembro*')

sep = st.text_input('Separador do arquivo CSV:', value=';', key='sep')

help = 'Faça o upload de um arquivo CSV contendo dados do Número de visitantes por mês em trilhas no Parque Nacional da Tijuca do portal Data.Rio'

uploaded_file =  st.file_uploader("Upload de Arquivo CSV", type=['csv'],accept_multiple_files=False, key='uploader', help=help)

if uploaded_file is not None:
    df = upload_data(uploaded_file,sep)#pd.read_csv(uploaded_file, sep=sep)
    st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')
else:
    df = load_data()
    st.warning('Utilizando os dados de 2019', icon="⚠️")

st.dataframe(df, use_container_width=True)

with st.expander('Código', expanded=False):
    st.code('''
uploaded_file =  st.file_uploader("Upload de Arquivo CSV", type=['csv'],accept_multiple_files=False, key='uploader', help=help)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=sep)
    st.sucess(f'Arquivo {uploaded_file.name} carregado com sucesso!')
else:
    df = load_data()
    st.warning('Utilizando os dados de 2019', icon="⚠️")
    ''')

st.subheader("3 - Filtro de Dados e Seleção:",divider=True)
#Implemente seletores (radio, checkbox, dropdowns) na interface que permitam ao usuário filtrar os dados carregados e selecionar as colunas ou linhas que deseja visualizar.

meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
meses_selecionados = st.multiselect('Selecione os meses:', meses, default=meses, key='meses')

setores = df['Setor'].unique()
setores_selecionados = st.multiselect('Selecione o setor:', setores, default=setores, key='setor')

df = df[['Setor']+meses_selecionados]
df = df[df['Setor'].isin(setores_selecionados)]

st.dataframe(df, use_container_width=True)

st.subheader("4 - Serviço de Download de Arquivos:",divider=True)
#Implemente um serviço que permita ao usuário fazer o download dos dados filtrados em formato CSV diretamente pela interface da aplicação.

if st.button('Download CSV', key='download'):
    with st.spinner('Preparando dados...'):
        time.sleep(2)

    my_bar = st.progress(0, text='Progresso')
    for i in range(100):
        time.sleep(0.01)
        my_bar.progress(i + 1, text='Progresso')
    time.sleep(1)
    my_bar.empty()
    st.success('Download pronto para ser realizado!')
    st.download_button('Clique aqui para baixar o dataset filtrado', df.to_csv(), file_name='data.csv', mime='text/csv')

st.expander('Código', expanded=False).code('''
if st.button('Download CSV', key='download'):
    with st.spinner('Preparando dados...'):
        time.sleep(2)

    my_bar = st.progress(0, text='Progresso')
    for i in range(100):
        time.sleep(0.01)
        my_bar.progress(i + 1, text='Progresso')
    time.sleep(1)
    my_bar.empty()
    st.success('Download pronto para ser realizado!')
    st.download_button('Clique aqui para baixar o dataset filtrado', df.to_csv(), file_name='data.csv', mime='text/csv')
    ''')

st.subheader("5 - Barra de Progresso e Spinner:",divider=True)
#Adicione uma barra de progresso e um spinner para indicar o carregamento dos dados enquanto o arquivo CSV é processado e exibido na interface.
st.expander('Código', expanded=True).code('''
if st.button('Download CSV', key='download'):
    with st.spinner('Preparando dados...'):
        time.sleep(2)

    my_bar = st.progress(0, text='Progresso')
    for i in range(100):
        time.sleep(0.01)
        my_bar.progress(i + 1, text='Progresso')
    time.sleep(1)
    my_bar.empty()
    st.success('Download pronto para ser realizado!')
    st.download_button('Clique aqui para baixar o dataset filtrado', df.to_csv(), file_name='data.csv', mime='text/csv')
    ''')


st.subheader("6 - Color Picker:",divider=True)
#Adicione um color picker à interface que permita ao usuário personalizar a cor de fundo do painel e das fontes exibidas na aplicação.

cols = st.columns(3)

with cols[0]:
    st.subheader('Escolha uma cor primaria:')
    st.session_state['primaryColor'] = st.color_picker('Escolha uma cor', '#00D432', key='highlight_color')

with cols[1]:
    st.subheader('Escolha uma cor de fundo:')
    st.session_state['backgroundColor'] = st.color_picker('Escolha uma cor', '#000', key='bg_color')

with cols[2]:
    st.subheader('Escolha uma cor de fonte:')
    st.session_state['textColor'] = st.color_picker('Escolha uma cor', '#fff', key='text_color')

st.write('')
cols = st.columns([0.45,0.1,0.5])
with cols[1]:
    if st.button('Aplicar'):
        keys = ['primaryColor', 'backgroundColor', 'textColor']
        has_changed = False
        for key in keys:
            st._config.set_option(f'theme.{key}', st.session_state[key])  
        st.rerun()

st.expander('Código', expanded=False).code('''
cols = st.columns(3)

with cols[0]:
    st.subheader('Escolha uma cor primaria:')
    st.session_state['primaryColor'] = st.color_picker('Escolha uma cor', '#00f', key='highlight_color')

with cols[1]:
    st.subheader('Escolha uma cor de fundo:')
    st.session_state['backgroundColor'] = st.color_picker('Escolha uma cor', '#f00', key='bg_color')

with cols[2]:
    st.subheader('Escolha uma cor de fonte:')
    st.session_state['textColor'] = st.color_picker('Escolha uma cor', '#fff', key='text_color')

if st.button('Aplicar'):
    keys = ['primaryColor', 'backgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        st._config.set_option(f'theme.{key}', st.session_state[key])  
    st.rerun()
    ''')

st.subheader("7 - Funcionalidade de Cache:",divider=True)
#Utilize a funcionalidade de cache do Streamlit para armazenar os dados carregados de grandes arquivos CSV, evitando a necessidade de recarregá-los a cada nova interação.

st.expander('Código', expanded=True).code('''
@st.cache_data
def load_data():
    df = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZoMBw66yzAe4JNi16mg/root/content',sep=';')
    return df

@st.cache_data
def upload_data(uploaded_file, sep):
    df = pd.read_csv(uploaded_file, sep=sep)
    return df
    ''')

st.subheader("8 - Persistir Dados Usando Session State",divider=True)
#Implemente a persistência de dados na aplicação utilizando Session State para manter as preferências do usuário (como filtros e seleções) durante a navegação.

st.expander('Código', expanded=True).code('''
cols = st.columns(3)

with cols[0]:
    st.subheader('Escolha uma cor primaria:')
    st.session_state['primaryColor'] = st.color_picker('Escolha uma cor', '#00f', key='highlight_color')

with cols[1]:
    st.subheader('Escolha uma cor de fundo:')
    st.session_state['backgroundColor'] = st.color_picker('Escolha uma cor', '#f00', key='bg_color')

with cols[2]:
    st.subheader('Escolha uma cor de fonte:')
    st.session_state['textColor'] = st.color_picker('Escolha uma cor', '#fff', key='text_color')

if st.button('Aplicar'):
    keys = ['primaryColor', 'backgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        st._config.set_option(f'theme.{key}', st.session_state[key])  
    st.rerun()
    ''')

st.subheader("9 - Visualizações de Dados - Tabelas:",divider=True)
#Crie uma tabela interativa que exiba os dados carregados e permita ao usuário ordenar e filtrar as colunas diretamente pela interface.

st.dataframe(df, use_container_width=True)

st.expander('Código', expanded=False).code('''
st.dataframe(df, use_container_width=True)
    ''')

#st.data_editor(
#    df,
#    column_config={
#        'Setor': st.column_config.Column(),
#        'Janeiro': st.column_config.ListColumn(),
#        'Fevereiro': st.column_config.ListColumn(),
#        'Março': st.column_config.ListColumn(),
#        'Abril': st.column_config.ListColumn(),
#        'Maio': st.column_config.ListColumn(),
#        'Junho': st.column_config.ListColumn(),
#        'Julho': st.column_config.ListColumn(),
#        'Agosto': st.column_config.ListColumn(),
#        'Setembro': st.column_config.ListColumn(),
#        'Outubro': st.column_config.ListColumn(),
#        'Novembro': st.column_config.ListColumn(),
#        'Dezembro': st.column_config.ListColumn(),
#    })


st.subheader("10 - Visualizações de Dados - Gráficos Simples:",divider=True)
#Desenvolva gráficos simples (como barras, linhas, e pie charts) para visualização dos dados carregados, utilizando o Streamlit.

columns = st.columns(4)

with columns[0]:
    first_color = st.color_picker('Gráfico Cor 1', '#FB3838')
with columns[1]:
    second_color = st.color_picker('Gráfico Cor 2', '#007DFF')
with columns[2]:
    third_color = st.color_picker('Gráfico Cor 3', '#48E848')
with columns[3]:
    fourth_color = st.color_picker('Gráfico Cor 4', '#EFEF5A')

st.session_state['plot_colors'] = [first_color, second_color, third_color, fourth_color]


df_melted = df.melt(id_vars='Setor', var_name='Mês', value_name='Visitantes')
df_melted['Mês'] = df_melted['Mês'].apply(lambda x: x[:3])

fig = px.bar(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca', color_discrete_sequence=st.session_state['plot_colors'])
st.plotly_chart(fig)

fig = px.line(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca', color_discrete_sequence=st.session_state['plot_colors'])
st.plotly_chart(fig)

fig = px.pie(values='Visitantes', names='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca', color_discrete_sequence=st.session_state['plot_colors'])
st.plotly_chart(fig)

st.expander('Código', expanded=False).code('''
df_melted = df.melt(id_vars='Setor', var_name='Mês', value_name='Visitantes')
df_melted['Mês'] = df_melted['Mês'].apply(lambda x: x[:3])

fig = px.bar(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca')
st.plotly_chart(fig)

fig = px.line(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca')
st.plotly_chart(fig)

fig = px.pie(values='Visitantes', names='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca')
st.plotly_chart(fig)
''')

st.subheader("11 - Visualizações de Dados - Gráficos Avançados:",divider=True)
#Adicione gráficos mais avançados (como histograma ou scatter plot) para fornecer insights mais profundos sobre os dados.

fig = px.histogram(x='Visitantes', color='Setor', data_frame=df_melted, title='Histograma do número de visitantes por setor', color_discrete_sequence=st.session_state['plot_colors'])
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)

fig = px.scatter(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca', color_discrete_sequence=st.session_state['plot_colors'])
st.plotly_chart(fig)

st.expander('Código', expanded=False).code('''
fig = px.histogram(x='Visitantes', color='Setor', data_frame=df_melted, title='Histograma do número de visitantes por setor')
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)

fig = px.scatter(x='Mês', y='Visitantes', color='Setor', data_frame=df_melted, title='Número de visitantes por mês em trilhas no Parque Nacional da Tijuca')
st.plotly_chart(fig)
''')

st.subheader("12 - Métricas Básicas:",divider=True)
#Implemente a exibição de métricas básicas (como contagem de registros, médias, somas) diretamente na interface para fornecer um resumo rápido dos dados carregados.

columns = st.columns(4)

with columns[0]:
    st.metric('Número de registros', df.shape[0] * (df.shape[1]-1))

with columns[1]:
    st.metric('Média de visitantes', df['Janeiro'].mean())

with columns[2]:
    st.metric('Soma de visitantes', df['Janeiro'].sum())

with columns[3]:
    st.metric('Desvio padrão de visitantes', df['Janeiro'].std().round(2))


st.expander('Código', expanded=False).code('''
columns = st.columns(4)

with columns[0]:
    st.metric('Número de registros', df.shape[0] * (df.shape[1]-1))

with columns[1]:
    st.metric('Média de visitantes', df['Janeiro'].mean())

with columns[2]:
    st.metric('Soma de visitantes', df['Janeiro'].sum())

with columns[3]:
    st.metric('Desvio padrão de visitantes', df['Janeiro'].std().round(2))
''')
