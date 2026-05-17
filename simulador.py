import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
TELEFONE_CONSULTOR = "5581982638903" 
NOME_CONSULTOR = "Fábio - Consultor de investimentos imobiliários"

# --- FUNÇÃO DE FORMATAÇÃO BRASILEIRA ---
def formatar_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Imobiliário - Fábio", layout="wide")

# --- CABEÇALHO PERSONALIZADO ---
# Usamos H2 para um título um pouco menor e centralizado
st.markdown(f"<h2 style='text-align: center;'>Simulador de Rentabilidade Imobiliária</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: gray;'>{NOME_CONSULTOR}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- BARRA LATERAL: ENTRADA DE DADOS ---
st.sidebar.header("1. Investimento Inicial")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0, step=1000.0)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0, step=500.0)
perc_valorizacao = st.sidebar.slider("% Valorização Estimada (Obra)", 0, 100, 35)

st.sidebar.header("2. Premissas de Locação")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0, step=10.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("3. Custos Mensais")
iptu = st.sidebar.number_input("IPTU (R$)", value=70.0)
wifi = st.sidebar.number_input("Wi-Fi (R$)", value=100.0)
energia = st.sidebar.number_input("Energia (R$)", value=150.0)
condominio = st.sidebar.number_input("Condomínio (R$)", value=300.0)
taxa_adm_perc = st.sidebar.slider("% Taxa Administradora", 0, 30, 10)

# --- LÓGICA DE CÁLCULO ---
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_capital = valor_pos_obra - preco_planta
investimento_total = preco_planta + custo_mobilia
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)
valor_taxa_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos_mensais = iptu + wifi + energia + condominio + valor_taxa_adm
lucro_liquido_mensal = receita_bruta - total_custos_mensais
rentabilidade_perc = (lucro_liquido_mensal / investimento_total) * 100
projecao_12_meses = lucro_liquido_mensal * 12
payback_tradicional = investimento_total / projecao_12_meses if projecao_12_meses > 0 else 0
investimento_restante = investimento_total - lucro_capital
payback_real = (investimento_restante / projecao_12_meses if projecao_12_meses > 0 else 0) if investimento_restante > 0 else 0

# --- EXIBIÇÃO NO DASHBOARD ---

# SEÇÃO 1: PATRIMÔNIO
st.header("📈 1. Valorização de Patrimônio")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Investimento Total", f"R$ {formatar_br(investimento_total)}")
    st.caption("Imóvel + Mobília")
with c2:
    st.metric("Valor na Entrega", f"R$ {formatar_br(valor_pos_obra)}")
    # Aplicando cor verde e negrito conforme solicitado
    st.markdown(f":green[**Aumento do patrimônio bruto**]: R$ {formatar_br(lucro_capital)}")
with c3:
    # ROI com setinha verde usando o parâmetro 'delta'
    st.metric("ROI de Valorização", f"{perc_valorizacao}%", delta=f"{perc_valorizacao}%", delta_color="normal")

st.divider()

# SEÇÃO 2: OPERAÇÃO MENSAL
st.header("💰 2. Operação Mensal e Custos")
o1, o2, o3 = st.columns(3)
with o1:
    st.metric("Receita Bruta", f"R$ {formatar_br(receita_bruta)}")
    st.write(f"Diária: R$ {formatar_br(valor_diaria)} | Ocupação: {taxa_ocupacao}%")
with o2:
    st.metric("Total Custos", f"R$ {formatar_br(total_custos_mensais)}")
    st.caption(f"Fixos + Taxa Adm ({taxa_adm_perc}%)")
with o3:
    # Lucro Líquido em Negrito
    st.metric("**Lucro Líquido Mensal**", f"R$ {formatar_br(lucro_liquido_mensal)}")
    st.write(f"Rentabilidade: {rentabilidade_perc:.2f}% ao mês".replace(".", ","))

st.divider()

# SEÇÃO 3: PAYBACK
st.header("⏳ 3. Tempo de Retorno (Payback)")
p1, p2, p3 = st.columns(3)
with p1:
    st.metric("Renda Líquida Anual", f"R$ {formatar_br(projecao_12_meses)}")
with p2:
    st.metric("Payback Tradicional", f"{payback_tradicional:.1f} Anos")
with p3:
    dif = payback_tradicional - payback_real
    st.metric("Payback Real", f"{payback_real:.1f} Anos", delta=f"-{dif:.1f} Anos", delta_color="normal")
    # Considerando valorização em negrito
    st.write("**Considerando valorização + aluguel**")

st.divider()

# --- BOTÃO DO WHATSAPP ---
st.subheader("🚀 Quer saber mais sobre estas unidades?")
msg_whats = (
    f"Olá! Usei o Simulador do Fábio e gostei dos resultados:\n\n"
    f"🏙️ Valor pós-obra: R$ {formatar_br(valor_pos_obra)}\n"
    f"💵 Lucro líquido: R$ {formatar_br(lucro_liquido_mensal)}/mês\n"
    f"⏳ Payback Real: {payback_real:.1f} anos\n\n"
    f"Pode me passar mais informações?"
)
msg_link = urllib.parse.quote(msg_whats)
st.link_button(f"🟢 Falar com {NOME_CONSULTOR}", f"https://wa.me/{TELEFONE_CONSULTOR}?text={msg_link}", type="primary")
