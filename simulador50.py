import streamlit as st
import pandas as pd
import datetime
import io
import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
install("openpyxl")

# Define as cores da página
st.set_page_config(
    page_title='Simulador TOP50',
    page_icon=':bar_chart:',
    layout='wide'
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('<div style="position: fixed; bottom: 0; right: 20px;"><p style="color: white;"><span style="color:black;font-size: 21px;font-family: Barlow;">MADE BY </span><span style="color:#9966FF;font-size: 21px; font-family: Arial, sans-serif;">PERFORMANCE</span></p></div>', unsafe_allow_html=True)
st.markdown('<div style="position: fixed; bottom: 0; right: 1360px;"><p style="color: grey; font-size: 14px;font-family: Barlow;">Criado por Pedro Dantas</p></div>', unsafe_allow_html=True)

def link():
    st.sidebar.markdown("<a href='https://madebyperformance-simuladoraai-simulador-0pnd67.streamlit.app/' target='_blank' style='text-decoration: none; font-family: Barlow; font-weight: bold; font-size: 20px; color: white;'>Simulador do Partnership.</a>", unsafe_allow_html=True)
    st.sidebar.markdown('<div style="position: fixed; bottom: 0; right: 10px;"><p style="color: grey; font-size: 14px;font-family: Barlow;">Clique acima para ser redirecionado ao Simulador do Partnership do Assessor 2023.</p></div>', unsafe_allow_html=True)
link()

#df = pd.read_excel('Base Simulador Top50.xlsx')
df = pd.read_csv('Base Simulador Top50.csv',delimiter=';',encoding='latin-1')
df['KPI5'] = df['KPI5'].astype('float64')
df = df.fillna(0)
df = df.rename(columns={df.columns[0]:'KPI1'})

# Título do aplicativo
st.title('Simulador TOP50')

# Descrição do aplicativo
st.write("<span style='font-family: Barlow; font-size: 24px;'>Este aplicativo recalcula o ranking com base em uma média escolhida pelo usuário.</span>", unsafe_allow_html=True)
# Menu de medidas

ranking = st.number_input("Sua posição atual",format="%.0f")
fat = st.number_input("Seu Faturamento no proximo mês",format="%.0f")
fxp="{:,.0f}".format(fat) 
fxp = fxp.replace(",",".")
st.write(f"<span style='font-family: Barlow; color: grey;font-size: 14px;'>Faturamento Selecionado: R${fxp}</span>", unsafe_allow_html=True)
inc = st.number_input("Seu Incremento no proximo mês",format="%.0f")
fxp3="{:,.0f}".format(inc) 
fxp3 = fxp3.replace(",",".")
st.write(f"<span style='font-family: Barlow; color: grey;font-size: 14px;'>Incremento Selecionado: R$ {fxp3}</span>", unsafe_allow_html=True)


if st.button('Calcular nova posição'):
    if ranking == 0:
      st.write("<span style='font-family: Barlow; color: rgb(255, 0, 0);font-size: 24px;'>Por favor, insira sua posição atual para começar a simulação.</span>", unsafe_allow_html=True) 
    if ranking > 0:
        mes_anterior = df['KPI5'].max()
        df['KPI4'] = df['KPI4'].astype(int)
        df['Fat esperado'] = df['KPI2'] / mes_anterior
        df['Fat esperado'] = df['KPI2'] + df['Fat esperado']
        df['Inc esperado'] = df['KPI1'] / mes_anterior
        df['Inc esperado'] = df['KPI1'] + df['Inc esperado']
        df['NPS esperado'] = df['KPI3']
        df.loc[df['KPI4'] == ranking, 'Fat esperado'] = df.loc[df['KPI4'] == ranking, 'KPI2'] + fat
        df.loc[df['KPI4'] == ranking, 'Inc esperado'] = df.loc[df['KPI4'] == ranking, 'KPI1'] + inc
        df['KPI5'] = df['NPS esperado'].apply(lambda x: 0.05 if x >= 90 else 0)

        # Criar a coluna com os rankings
        df['Ranking INC2'] = df['Inc esperado'].rank(ascending=True)
        df['Ranking FAT2'] = df['Fat esperado'].rank(ascending=True)
        df['Desempate Fat2'] = df['Fat esperado']/10000000

        #KPI4
        df['Nota Final2'] = ((df['Ranking INC2']+df['Ranking FAT2'])/2)
        df['KPI6'] = df['Nota Final2']*df['KPI5']
        df['Nota Final2'] = df['Nota Final2'] + df['KPI6'] + df['Desempate Fat2']
        df['KPI42'] = df['Nota Final2'].rank(ascending=False)
        df = df.sort_values('KPI42', ascending=True)
        
        df['KPI42'] = df['KPI42'].astype(int)
        df['KPI4'] = df['KPI4'].astype(int)
        rank_antigo = df.loc[df['KPI4'] == ranking, 'KPI4'].iloc[0]
        rank_atual = df.loc[df['KPI4'] == ranking, 'KPI42'].iloc[0] # Selecionando o primeiro valor retornado
        st.write("<span style='font-family: Barlow; color: grey;font-size: 14px;'>As posições são calculadas levando em conta que todos os Assessores manterão e média de Incremento, Faturamento e NPS. É natural que a projeção não bata na vírgula mas trará uma posição bem aproximada..</span>", unsafe_allow_html=True) 
        st.write(f"<span style='font-family: Barlow; color: black;font-size: 25px;'>Sua posição antiga era: {rank_antigo}</span>", unsafe_allow_html=True) 
        st.write(f"<span style='font-family: Barlow; color: black;font-size: 25px;'>Sua nova posição será: {rank_atual}</span>", unsafe_allow_html=True) 
        if rank_antigo <=50:
            if rank_atual > 50:
                st.write("<span style='font-family: Barlow; color: red;font-size: 24px;'>Cuidado! Com essa Performance você pode perder sua colocação na zona de premiação no mês que vem.</span>", unsafe_allow_html=True)
            if rank_atual <= 50:
                st.write("<span style='font-family: Barlow; color: green;font-size: 24px;'>Com essa Performance você se mantém no TOP50 mas continue melhorando para alcançar prêmios ainda melhores!</span>", unsafe_allow_html=True)
        if rank_antigo >50:
            if rank_atual > 50:
                st.write("<span style='font-family: Barlow; color: black;font-size: 24px;'>Com essa performance você ainda não entra no TOP50 mas continue melhorando para alcançar a zona de premiação!</span>", unsafe_allow_html=True)
            if rank_atual <= 50:
                st.write("<span style='font-family: Barlow; color: green;font-size: 24px;'>Parabens! Com essa Performance você pode entrar na zona de premiação no próximo mês! </span>", unsafe_allow_html=True)
