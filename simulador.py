import streamlit as st

# Configuração da página para aproveitar melhor o espaço
st.set_page_config(page_title="Simulador de Investimento Pro", layout="wide")

st.title("🏨 Simulador de Rentabilidade Imobiliária Avançado")
st.markdown("Baseado na sua planilha de projeção de lucros.")

# --- BARRA LATERAL: ENTRADA DE DADOS ---
st.sidebar.header("1. Aquisição e Valorização")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0)
perc_valorizacao = st.sidebar.slider("% Valorização Estimada", 0, 100, 35)

st.sidebar.header("2. Investimento Inicial (Setup)")
custo_mobilia = st.sidebar.number_input("Custo de Mobília (R$)", value=35000.0)

st.sidebar.header("3. Premissas de Locação")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("4. Custos Mensais (OpEx)")
condominio = st.sidebar.number_input("Condomínio (R$)", value=300.0)
iptu = st.sidebar.number_input("IPTU Mensal (R$)", value=70.0)
energia = st.sidebar.number_input("Energia (R$)", value=150.0)
internet = st.sidebar.number_input("Wi-Fi (R$)", value=100.0)
taxa_adm_perc = st.sidebar.slider("% Taxa Administradora", 0, 30, 10)

# --- LÓGICA DE PROGRAMAÇÃO (CÁLCULOS) ---

# A. Valorização
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_valorizacao = valor_pos_obra - preco_planta

# B. Investimento Total
investimento_total = preco_planta + custo_mobilia

# C. Receita de Locação
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)

# D. Custos Variáveis e Fixos
custo_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos = condominio + iptu + energia + internet + custo_adm

# E. Rentabilidade Final
lucro_liquido_mensal = receita_bruta - total_custos
rentabilidade_mensal_perc = (lucro_liquido_mensal / investimento_total) * 100
payback_anos = investimento_total / (lucro_liquido_mensal * 12) if lucro_liquido_mensal > 0 else 0

# --- EXIBIÇÃO NA TELA ---

# Seção 1: Patrimônio
st.header("📈 Valorização de Patrimônio")
c1, c2, c3 = st.columns(3)
c1.metric("Preço na Planta", f"R$ {preco_planta:,.2f}")
c2.metric("Valorização Média", f"R$ {lucro_valorizacao:,.2f}", f"{perc_valorizacao}%")
c3.metric("Valor Pós-Entrega", f"R$ {valor_pos_obra:,.2f}")

st.divider()

# Seção 2: Rentabilidade de Aluguel
st.header("💰 Rentabilidade Líquida (Mensal)")
r1, r2, r3, r4 = st.columns(4)
r1.metric("Receita Bruta", f"R$ {receita_bruta:,.2f}")
r2.metric("Custos Operais", f"R$ {total_custos:,.2f}")
r3.metric("Lucro Líquido", f"R$ {lucro_liquido_mensal:,.2f}")
r4.metric("ROI Mensal", f"{rentabilidade_mensal_perc:.2f}%")

st.divider()

# Seção 3: Payback e Retorno
st.header("⏳ Tempo de Retorno")
p1, p2 = st.columns(2)
p1.metric("Projeção 12 meses", f"R$ {lucro_liquido_mensal * 12:,.2f}")
p2.metric("Imóvel Pago em (Anos)", f"{payback_anos:.2f} Anos")

st.info(f"O investimento total foi de **R$ {investimento_total:,.2f}** (Imóvel + Mobília).")