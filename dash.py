#pip install streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# ** PRIMEIRA CONSULTA/ ATUALIZACOES DE DADOS
query = "SELECT * FROM tb_carros"

# Carregar os dados
df = conexao(query)

#Botao para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)


# ********* ESTRUTURA LATERAL DE FILTROS *****

st.sidebar.header("Selecione o filtro: ")

marca = st.sidebar.multiselect("Marca Selecionada", 
                               options = df["marca"].unique(),
                                 default=df["marca"].unique() 
                                   )

modelo= st.sidebar.multiselect("Modelo Selecionado", 
                               options = df["modelo"].unique(),
                                 default=df["modelo"].unique() 
                                   )

ano = st.sidebar.multiselect("Ano Selecionado", 
                               options = df["ano"].unique(),
                                 default=df["ano"].unique() 
                                   )

valor = st.sidebar.multiselect(" Valor Selecionado", 
                               options = df["valor"].unique(),
                                 default=df["valor"].unique() 
                                   )

cor = st.sidebar.multiselect(" Cor Selecionada", 
                               options = df["cor"].unique(),
                                 default=df["cor"].unique() 
                                   )

numero_vendas = st.sidebar.multiselect(" Numero de Vendas Selecionada", 
                               options = df["numero_vendas"].unique(),
                                 default=df["numero_vendas"].unique() 
                                   )


# Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca))&
    (df["modelo"].isin(modelo))&
    (df["ano"].isin(ano))&
    (df["cor"].isin(cor))&
    (df["numero_vendas"].isin(numero_vendas))
    
]

# **** EXIBIR VALORES MÉDIOS - ESTÍSTICA
def Home():
    with st.expander("Tabela"): #Cria uma caixa expansivel com um titulo
        mostrardados = st.multiselect("Filter: ", df_selecionado.columns, default=[])

        #Verifica se o usuario selecionou colunas para exiir
        if mostrardados:
        #Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrardados])

# ***** VERIFICA SE O DATAFRAME filtrado (df_selecionado) nao esta vazio
if not df_selecionado.empty:
  venda_total = df_selecionado["numero_vendas"].sum()
  venda_media = df_selecionado["numero_vendas"].mean()
  venda_mediana = df_selecionado["numero_vendas"].median()

  # Cria tres colunas para exibir os totais calculados
  total1, total2, total3 = st.columns(3, gap="large")

  with total1:
      st.info("Valor total de Vendas dos Carros", icon="📌")
      st.metric(label="Total", value=f"{venda_total:,.0f}")

  with total2:
      st.info("Valor Medio das vendas", icon="📌")
      st.metric(label="Media", value=f"{venda_media:,.0f}")

  with total3:
      st.info("Valor Mediano das vendas", icon="📌")
      st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

else:
  st.warning("Nenhum dado disponivel com os filtros selecionados")

  st.markdown("""*********""")


#*****************GRAFICOS****************************

def graficos (df_selecionado):
  if df_selecionado.empty:
      st.warning("Nenhum dado disponível para gerar gráficos")
      #Interrompe a funcao, pq nao tem motivo para continuar executando se n tem dado
      return
  

  # Criacao dps graficos

  # 4 abas -> Graficos de Barra, Grafico de linha, Grafico de pizza e Grafico de dispersao
  graf1, graf2, graf3, graf4,graf5, graf6 = st.tabs(["Grafico de Barras","Grafico de Linhas", "Grafico de Pizza", "Grafico de Dispersao","Gráfico de Histograma", "Gráfico de Box-Plot" ])
 

    # Gráfico de Barras
  with graf1:
      st.header("Gráfico de Barras")
      fig_bar = px.bar(df_selecionado, 
                        x='marca', 
                        y='numero_vendas', 
                        color='marca', 
                        title="Número de Vendas por Marca", 
                        labels={"numero_vendas": "Número de Vendas", "marca": "Marca"}, 
                        color_discrete_sequence=px.colors.qualitative.Pastel)
      st.plotly_chart(fig_bar)



#Grafico de Linhas
  with graf2:
    st.header("Gráfico de Linhas")
    fig_line = px.line(df_selecionado,
                        x='ano',
                        y='numero_vendas',
                        title= 'Número de Vendas por Ano',
                        markers= True,
                        color='modelo',
                        labels={'número_vendas': 'Número de Vendas', 'ano':'Ano'}, color_discrete_sequence= px.colors.sequential.Viridis)
    st.plotly_chart(fig_line)



#Grafico de Pizza
  with graf3:
      st.header("Gráfico de Pizza")
      fig_pie = px.pie(df_selecionado,
                        names = 'cor',
                        values='numero_vendas',
                        title= 'Distribuicao de Vendas por Cor', color_discrete_sequence= px.colors.sequential.Plasma)
      st.plotly_chart(fig_pie)


#Grafico de Dispersao
  with graf4:
      st.header("Gráfico de Dispersao")
      fig_scatter = px.scatter(df_selecionado,
                                x = 'valor',
                                y = 'numero_vendas',
                                size= 'numero_vendas',
                                color= 'marca',
                                title= 'Dispersao de Vendas por Valor de Carros',
                                labels={'numero_vendas':'Numero de Vendas', 'valor':'Valor do Carro'}, color_discrete_sequence= px.colors.qualitative.Set1)
      st.plotly_chart(fig_scatter)

#Grafico de Histograma
  with graf5:
     st.header("Gráfico de Histograma")
     fig_histogram = px.histogram(df_selecionado,
                                  x = 'valor',
                                  nbins = 30,
                                  title = 'Distribuicao de Vendas por Faixa Valor',
                                  labels={'valor': 'Valor do Carro' }, color_discrete_sequence=px.colors.sequential.Sunset)
     st.plotly_chart(fig_histogram) 

#Grafico de Box-Plot
  with graf6:
     st.header("Gráfico de Box-Plot")
     fig_box = px.box(df_selecionado,
                      x= 'marca',
                      y= 'valor',
                      title = 'Distribuicao de Valores de Carros por Marca',
                      labels={'valor': 'Valor do Carro', 'marca': 'Marca'},
                      color = 'marca', color_discrete_sequence=px.colors.qualitative.T10)
     st.plotly_chart(fig_box)
        

def barraprogresso():
  valorAtual = df_selecionado["numero_vendas"].sum()
  objetivo = 20000
  percentual = round(valorAtual / objetivo * 100)

  if percentual > 100:
    st.subheader('Valores Atingidos!!!')
  else:
    st.write(f"Voce tem {percentual}% de {objetivo}. Corra atrás filhao!")

    mybar= st.progress(0)
    for percentualCompleto in range(percentual):
      mybar.progress(percentualCompleto +1, text ='Alvo %')

# ********** MENU LATERAL ************

def menuLateral():
  with st.sidebar:
      selecionado = option_menu(menu_title='Menu', options=["Home", "Progresso"],
      icons= ['house', 'eye'], menu_icon='cast', default_index=0)

  if selecionado == "Home":
      st.subheader(f'Página: {selecionado}') 
       
      Home()
      graficos(df_selecionado)
  elif selecionado == "Progresso":
      st.subheader(f'Página: {selecionado}')
      barraprogresso()
      graficos(df_selecionado)

menuLateral()

