import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
# Note que adicionamos o 55 para o link funcionar corretamente
TELEFONE_CONSULTOR = "5581982638903" 

st.set_page_config(page_title="Simulador Imobiliário Pro", layout="wide")

# --- CABEÇALHO ---
st.title("📊 Simulador de Rentabilidade Imobiliária")
st.markdown("Calcule a valorização e a rentabilidade mensal do seu novo investimento.")

# --- BARRA LATERAL (ENTRADA DE DADOS) ---
st.sidebar.header("Dados da Compra")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0)
perc_valorizacao = st.sidebar.slider("% Valorização na Obra", 0, 100, 35)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0)

st.sidebar.header("Premissas de Aluguel")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Estimada", 0, 100, 65)

# --- LÓGICA DE CÁLCULO ---
# 1. Valorização de Capital
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_obra = valor_pos_obra - preco_planta

# 2. Investimento Total (CapEx)
investimento_total = preco_planta + custo_mobilia

# 3. Operação Mensal (Receita e Custos fixos da sua planilha)
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)
# Custos baseados na sua planilha: IPTU(70) + Wi-Fi(100) + Energia(150) + Condomínio(300) + Adm(10%)
taxa_adm = receita_bruta * 0.10
total_custos = 70 + 100 + 150 + 300 + taxa_adm

# 4. Rentabilidade Líquida
lucro_liquido_mensal = receita_bruta - total_custos
roi_mensal_perc = (lucro_liquido_mensal / investimento_total) * 100
payback_anos = investimento_total / (lucro_liquido_mensal * 12) if lucro_liquido_mensal > 0 else 0

# --- EXIBIÇÃO DOS RESULTADOS ---
st.header("📈 Projeção de Resultados")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Valor Pós-Entrega", f"R$ {valor_pos_obra:,.2f}")
    st.write(f"**Lucro na Obra:** R$ {lucro_obra:,.2f}")

with col2:
    st.metric("Lucro Líquido Mensal", f"R$ {lucro_liquido_mensal:,.2f}")
    st.write(f"**ROI Mensal:** {roi_mensal_perc:.2f}%")

with col3:
    st.metric("Tempo de Retorno", f"{payback_anos:.2f} Anos")
    st.write(f"**Renda Anual:** R$ {lucro_liquido_mensal * 12:,.2f}")

st.divider()

# --- SEÇÃO DE FECHAMENTO (CALL TO ACTION) ---
st.subheader("🚀 Gostou dos números?")
st.write("Clique abaixo para receber a tabela completa e verificar as unidades disponíveis.")

# Preparação da mensagem do WhatsApp
texto_whats = (
    f"Olá! Usei seu Simulador e gostei dos números:\n\n"
    f"📍 Imóvel Planta: R$ {preco_planta:,.2f}\n"
    f"💰 Lucro Mensal: R$ {lucro_liquido_mensal:,.2f}\n"
    f"📈 ROI: {roi_mensal_perc:.2f}% ao mês.\n\n"
    f"Pode me enviar mais detalhes?"
)
mensagem_url = urllib.parse.quote(texto_whats)
link_final = f"https://wa.me/{TELEFONE_CONSULTOR}?text={mensagem_url}"

st.link_button("🟢 Falar com Consultor no WhatsApp", link_final, type="primary")
