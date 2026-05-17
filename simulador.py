import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
TELEFONE_CONSULTOR = "5581982638903" 

# --- FUNÇÃO DE FORMATAÇÃO BRASILEIRA ---
def formatar_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Imobiliário Estratégico", layout="wide")

st.title("🏨 Simulador de Rentabilidade de Investimento")
st.markdown("---")

# --- BARRA LATERAL ---
st.sidebar.header("1. Aquisição na Planta")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0, step=1000.0)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0, step=500.0)
perc_valorizacao = st.sidebar.slider("% Valorização Estimada (Obra)", 0, 100, 35)

st.sidebar.header("2. Operação de Locação")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0, step=10.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("3. Custos Operacionais")
iptu = st.sidebar.number_input("IPTU (R$)", value=70.0)
wifi = st.sidebar.number_input("Wi-Fi (R$)", value=100.0)
energia = st.sidebar.number_input("Energia (R$)", value=150.0)
condominio = st.sidebar.number_input("Condomínio (R$)", value=300.0)
taxa_adm_perc = st.sidebar.slider("% Taxa Administradora", 0, 30, 10)

# --- LÓGICA DE CÁLCULO ---
# Valorização e Investimento
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_capital = valor_pos_obra - preco_planta
investimento_total = preco_planta + custo_mobilia

# Operação Mensal
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)
valor_taxa_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos_mensais = iptu + wifi + energia + condominio + valor_taxa_adm
lucro_liquido_mensal = receita_bruta - total_custos_mensais
projecao_12_meses = lucro_liquido_mensal * 12

# Payback Tradicional (Só aluguel)
payback_tradicional = investimento_total / projecao_12_meses if projecao_12_meses > 0 else 0

# Payback Efetivo (Considerando a Valorização da Obra)
investimento_restante = investimento_total - lucro_capital
if investimento_restante <= 0:
    payback_efetivo = 0.0 # O imóvel se pagou já na entrega
else:
    payback_efetivo = investimento_restante / projecao_12_meses if projecao_12_meses > 0 else 0

# --- EXIBIÇÃO ---
st.header("📈 Valorização de Patrimônio")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Investimento Total", f"R$ {formatar_br(investimento_total)}")
    st.caption("Imóvel + Mobília")
with col2:
    st.metric("Valor na Entrega", f"R$ {formatar_br(valor_pos_obra)}")
    st.write(f"**Ganho na Obra:** R$ {formatar_br(lucro_capital)}")
with col3:
    st.metric("ROI de Valorização", f"{perc_valorizacao}%")

st.divider()

st.header("💰 Rentabilidade e Payback")
r1, r2, r3 = st.columns(3)
with r1:
    st.metric("Lucro Líquido Mensal", f"R$ {formatar_br(lucro_liquido_mensal)}")
    st.write(f"Renda Anual: R$ {formatar_br(projecao_12_meses)}")
with r2:
    st.metric("Payback Tradicional", f"{payback_tradicional:.1f} Anos")
    st.caption("Recuperação apenas via aluguel")
with r3:
    st.metric("Payback Real (Obra + Aluguel)", f"{payback_efetivo:.1f} Anos", delta=f"-{(payback_tradicional - payback_efetivo):.1f} Anos", delta_color="normal")
    st.caption("Considerando lucro da valorização")

st.divider()

# --- BOTÃO DO WHATSAPP ---
msg_whats = (
    f"Olá! Simulei meu investimento e gostei do Payback Real:\n\n"
    f"🏙️ Valor pós-obra: R$ {formatar_br(valor_pos_obra)}\n"
    f"💵 Lucro mensal: R$ {formatar_br(lucro_liquido_mensal)}\n"
    f"⏳ Payback considerando valorização: {payback_efetivo:.1f} anos\n"
    f"Quero saber mais detalhes!"
)
msg_link = urllib.parse.quote(msg_whats)
st.link_button("🟢 Consultar Disponibilidade no WhatsApp", f"https://wa.me/{TELEFONE_CONSULTOR}?text={msg_link}", type="primary")
