import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
TELEFONE_CONSULTOR = "5581982638903" 
NOME_CONSULTOR = "Fábio - Consultor de investimentos imobiliários"
SITE_CONSULTOR = "https://www.consultorfabiope.com"

# --- FUNÇÃO DE FORMATAÇÃO BRASILEIRA ---
def formatar_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Imobiliário - Fábio", layout="wide")

# --- CABEÇALHO PERSONALIZADO ---
st.markdown(f"<h2 style='text-align: center;'>Simulador de Rentabilidade Imobiliária</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: gray;'>{NOME_CONSULTOR}</p>", unsafe_allow_html=True)

st.info("📲 **Dica:** Se estiver no celular, clique nas **setinhas ( >> )** no canto superior esquerdo para **alterar os valores** da simulação.")
st.markdown("---")

# --- BARRA LATERAL: ENTRADA DE DADOS ---
st.sidebar.header("1. Investimento Inicial")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=260000.0, step=20000.0)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0, step=5000.0)
perc_valorizacao = st.sidebar.slider("% Valorização Estimada (Obra)", 0, 100, 35)

st.sidebar.header("2. Premissas de Locação")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0, step=50.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("3. Custos Mensais")
iptu = st.sidebar.number_input("IPTU (R$)", value=70.0, step=10.0)
wifi = st.sidebar.number_input("Wi-Fi (R$)", value=100.0, step=10.0)
energia = st.sidebar.number_input("Energia (R$)", value=150.0, step=10.0)
condominio = st.sidebar.number_input("Condomínio (R$)", value=300.0, step=10.0)
taxa_adm_perc = st.sidebar.slider("% Taxa Administradora", 0, 30, 10)

# --- LÓGICA DE CÁLCULO ---
valor_pos_obra = preco_planta * (1 + (perc_valorizacao / 100))
lucro_capital = valor_pos_obra - preco_planta
investimento_total = preco_planta + custo_mobilia
receita_bruta = valor_diaria * 30 * (taxa_occupacao / 100) if 'taxa_occupacao' in locals() else valor_diaria * 30 * (taxa_ocupacao / 100)
custos_fixos = iptu + wifi + energia + condominio
valor_taxa_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos_mensais = custos_fixos + valor_taxa_adm
lucro_liquido_mensal = receita_bruta - total_custos_mensais
rentabilidade_perc = (lucro_liquido_mensal / investimento_total) * 100
projecao_12_meses = lucro_liquido_mensal * 12
payback_tradicional = investimento_total / projecao_12_meses if projecao_12_meses > 0 else 0
investimento_restante = investimento_total - lucro_capital
payback_real = (investimento_restante / projecao_12_meses if projecao_12_meses > 0 else 0) if investimento_restante > 0 else 0

# --- EXIBIÇÃO ---

# SEÇÃO 1: PATRIMÔNIO
st.header("📈 1. Valorização de Patrimônio")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Investimento Total", f"R$ {formatar_br(investimento_total)}")
    st.caption("Imóvel + Mobília")
with c2:
    st.metric("Valor na Entrega", f"R$ {formatar_br(valor_pos_obra)}")
    st.markdown(f":green[**Aumento do patrimônio bruto**]: R$ {formatar_br(lucro_capital)}")
with c3:
    st.metric("ROI de Valorização", f"{perc_valorizacao}%", delta=f"{perc_valorizacao}%", delta_color="normal")

st.divider()

# SEÇÃO 2: OPERAÇÃO
st.header("💰 2. Operação Mensal e Custos")
o1, o2, o3, o4 = st.columns(4)
with o1:
    st.metric("Receita Bruta", f"R$ {formatar_br(receita_bruta)}")
    st.write(f"Ocupação: {taxa_ocupacao}%")
with o2:
    st.markdown(f"<p style='font-size:14px; color:gray; margin-bottom:0;'>Custos Fixos</p><h4 style='margin-top:0;'>R$ {formatar_br(custos_fixos)}</h4>", unsafe_allow_html=True)
    st.caption("IPTU, Wi-Fi, Luz, Cond.")
with o3:
    st.markdown(f"<p style='font-size:14px; color:gray; margin-bottom:0;'>Taxa Adm ({taxa_adm_perc}%)</p><h4 style='margin-top:0;'>R$ {formatar_br(valor_taxa_adm)}</h4>", unsafe_allow_html=True)
    st.caption("Sobre receita bruta")
with o4:
    # ROI com seta verde e cor verde
    st.metric(
        "**Lucro Líquido Mensal**", 
        f"R$ {formatar_br(lucro_liquido_mensal)}", 
        delta=f"{rentabilidade_perc:.2f}% ao mês".replace(".", ","),
        delta_color="normal"
    )

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
    st.write("**Considerando valorização + aluguel**")

st.divider()

# --- BOTÃO FINAL ---
st.subheader(f"🚀 Quer avançar com o {NOME_CONSULTOR.split(' - ')[0]}?")
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    msg_whats = (
        f"Olá! Usei o Simulador do Fábio e gostei dos resultados:\n\n"
        f"🏙️ Valor pós-obra: R$ {formatar_br(valor_pos_obra)}\n"
        f"💵 Lucro líquido: R$ {formatar_br(lucro_liquido_mensal)}/mês\n"
        f"⏳ Payback Real: {payback_real:.1f} anos\n\n"
        f"Pode me passar mais informações?"
    )
    msg_link = urllib.parse.quote(msg_whats)
    st.link_button(f"🟢 Falar no WhatsApp", f"https://wa.me/{TELEFONE_CONSULTOR}?text={msg_link}", type="primary", use_container_width=True)

with btn_col2:
    st.link_button("🌐 Visitar meu Site", SITE_CONSULTOR, use_container_width=True)
