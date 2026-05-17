import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
TELEFONE_CONSULTOR = "5581982638903" 

# --- FUNÇÃO DE FORMATAÇÃO BRASILEIRA ---
def formatar_br(valor):
    """Transforma 1234.56 em 1.234,56"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Imobiliário Profissional", layout="wide")

st.title("🏨 Simulador de Rentabilidade Estimada")
st.markdown("---")

# --- BARRA LATERAL ---
st.sidebar.header("1. Investimento Inicial")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0, step=1000.0)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0, step=500.0)
perc_valorizacao = st.sidebar.slider("% Valorização Média Esperada", 0, 100, 35)

st.sidebar.header("2. Premissas de Ocupação")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0, step=10.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("3. Custos Mensais")
iptu = st.sidebar.number_input("IPTU (R$)", value=70.0)
wifi = st.sidebar.number_input("Wi-Fi (R$)", value=100.0)
energia = st.sidebar.number_input("Energia (R$)", value=150.0)
condominio = st.sidebar.number_input("Condomínio (R$)", value=300.0)
taxa_adm_perc = st.sidebar.slider("% Taxa Administradora", 0, 30, 10)

# --- CÁLCULOS ---
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_capital = valor_pos_obra - preco_planta
investimento_total = preco_planta + custo_mobilia
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)
valor_taxa_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos_mensais = iptu + wifi + energia + condominio + valor_taxa_adm
lucro_liquido_mensal = receita_bruta - total_custos_mensais
rentabilidade_perc = (lucro_liquido_mensal / investimento_total) * 100
projecao_12_meses = lucro_liquido_mensal * 12
payback_anos = investimento_total / projecao_12_meses if projecao_12_meses > 0 else 0

# --- EXIBIÇÃO (USANDO A FUNÇÃO DE FORMATAÇÃO) ---

st.header("📈 Resumo do Investimento")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Investimento Total", f"R$ {formatar_br(investimento_total)}")
    st.write(f"Imóvel: R$ {formatar_br(preco_planta)}")
    st.write(f"Mobília: R$ {formatar_br(custo_mobilia)}")

with col2:
    st.metric("Valor Pós-Obra", f"R$ {formatar_br(valor_pos_obra)}")
    st.write(f"**Ganho:** R$ {formatar_br(lucro_capital)} ({perc_valorizacao}%)")

with col3:
    st.metric("Receita Bruta Mensal", f"R$ {formatar_br(receita_bruta)}")
    st.write(f"Ocupação: {taxa_ocupacao}%")

st.divider()

st.header("💰 Rentabilidade Líquida")
r1, r2, r3, r4 = st.columns(4)
r1.metric("Lucro Líquido", f"R$ {formatar_br(lucro_liquido_mensal)}")
r2.metric("ROI Mensal", f"{rentabilidade_perc:.2f}%".replace(".", ","))
r3.metric("Renda em 12 meses", f"R$ {formatar_br(projecao_12_meses)}")
r4.metric("Payback (Anos)", f"{payback_anos:.2f}".replace(".", ","))

st.divider()

# --- BOTÃO DO WHATSAPP ---
st.subheader("📲 Gostou desta projeção?")
msg_whats = (
    f"Olá! Usei o Simulador e quero detalhes desta unidade:\n\n"
    f"💰 Preço na Planta: R$ {formatar_br(preco_planta)}\n"
    f"🛋️ Mobília: R$ {formatar_br(custo_mobilia)}\n"
    f"📊 ROI: {rentabilidade_perc:.2f}% ao mês\n".replace(".", ",") +
    f"💵 Lucro Líquido: R$ {formatar_br(lucro_liquido_mensal)}/mês\n"
    f"⏳ Payback: {payback_anos:.2f} anos".replace(".", ",")
)
msg_link = urllib.parse.quote(msg_whats)
st.link_button("🟢 Falar com Consultor no WhatsApp", f"https://wa.me/{TELEFONE_CONSULTOR}?text={msg_link}", type="primary")
