import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DO CONSULTOR ---
TELEFONE_CONSULTOR = "5581982638903" 

# --- FUNÇÃO DE FORMATAÇÃO BRASILEIRA ---
def formatar_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Imobiliário Completo", layout="wide")

st.title("🏨 Simulador de Rentabilidade de Investimento")
st.markdown("---")

# --- BARRA LATERAL: ENTRADA DE DADOS ---
st.sidebar.header("1. Aquisição e Obra")
preco_planta = st.sidebar.number_input("Preço na Planta (R$)", value=269000.0, step=1000.0)
custo_mobilia = st.sidebar.number_input("Investimento em Mobília (R$)", value=35000.0, step=500.0)
perc_valorizacao = st.sidebar.slider("% Valorização Estimada (Obra)", 0, 100, 35)

st.sidebar.header("2. Operação (Airbnb/Aluguel)")
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", value=350.0, step=10.0)
taxa_ocupacao = st.sidebar.slider("% Ocupação Mensal", 0, 100, 65)

st.sidebar.header("3. Custos Fixos e Variáveis")
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

# Operação Mensal Detalhada
receita_bruta = valor_diaria * 30 * (taxa_ocupacao / 100)
valor_taxa_adm = receita_bruta * (taxa_adm_perc / 100)
total_custos_mensais = iptu + wifi + energia + condominio + valor_taxa_adm
lucro_liquido_mensal = receita_bruta - total_custos_mensais
rentabilidade_mensal_perc = (lucro_liquido_mensal / investimento_total) * 100
projecao_12_meses = lucro_liquido_mensal * 12

# Paybacks
payback_tradicional = investimento_total / projecao_12_meses if projecao_12_meses > 0 else 0
investimento_restante = investimento_total - lucro_capital
payback_real = (investimento_restante / projecao_12_meses if projecao_12_meses > 0 else 0) if investimento_restante > 0 else 0

# --- EXIBIÇÃO NO DASHBOARD ---

# SEÇÃO 1: PATRIMÔNIO E VALORIZAÇÃO
st.header("📈 1. Valorização de Patrimônio")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Investimento Total", f"R$ {formatar_br(investimento_total)}")
    st.write(f"Imóvel: R$ {formatar_br(preco_planta)}")
    st.write(f"Mobília: R$ {formatar_br(custo_mobilia)}")
with c2:
    st.metric("Valor na Entrega", f"R$ {formatar_br(valor_pos_obra)}")
    st.write(f"**Ganho na Obra:** R$ {formatar_br(lucro_capital)}")
with c3:
    st.metric("ROI de Valorização", f"{perc_valorizacao}%")
    st.caption("Aumento do patrimônio bruto")

st.divider()

# SEÇÃO 2: OPERAÇÃO MENSAL (Lucro Bruto e Custos)
st.header("💰 2. Operação Mensal e Custos")
o1, o2, o3 = st.columns(3)
with o1:
    st.metric("Receita Bruta", f"R$ {formatar_br(receita_bruta)}")
    st.write(f"Diária: R$ {formatar_br(valor_diaria)}")
    st.write(f"Ocupação: {taxa_ocupacao}%")
with o2:
    st.metric("Total Custos", f"R$ {formatar_br(total_custos_mensais)}")
    st.write(f"Custos Fixos: R$ {formatar_br(iptu + wifi + energia + condominio)}")
    st.write(f"Taxa Adm ({taxa_adm_perc}%): R$ {formatar_br(valor_taxa_adm)}")
with o3:
    st.metric("Lucro Líquido Mensal", f"R$ {formatar_br(lucro_liquido_mensal)}", f"{rentabilidade_mensal_perc:.2f}%")
    st.caption("Retorno líquido sobre investimento total")

st.divider()

# SEÇÃO 3: MÉTRICAS DE RETORNO (PAYBACK)
st.header("⏳ 3. Tempo de Retorno (Payback)")
p1, p2, p3 = st.columns(3)
with p1:
    st.metric("Renda Líquida Anual", f"R$ {formatar_br(projecao_12_meses)}")
    st.caption("Projeção de 12 meses de operação")
with p2:
    st.metric("Payback Tradicional", f"{payback_tradicional:.1f} Anos")
    st.caption("Considerando apenas aluguel")
with p3:
    dif = payback_tradicional - payback_real
    st.metric("Payback Real", f"{payback_real:.1f} Anos", delta=f"-{dif:.1f} Anos", delta_color="normal")
    st.caption("Considerando Valorização + Aluguel")

st.divider()

# --- BOTÃO DO WHATSAPP ---
st.subheader("🚀 Gostou desta projeção?")
msg_whats = (
    f"Olá! Simulei meu investimento e gostei dos números:\n\n"
    f"🏙️ Imóvel pós-obra: R$ {formatar_br(valor_pos_obra)}\n"
    f"💵 Lucro líquido: R$ {formatar_br(lucro_liquido_mensal)}/mês\n"
    f"⏳ Payback Real: {payback_real:.1f} anos\n\n"
    f"Quero detalhes sobre as unidades!"
)
msg_link = urllib.parse.quote(msg_whats)
st.link_button("🟢 Consultar Disponibilidade no WhatsApp", f"https://wa.me/{TELEFONE_CONSULTOR}?text={msg_link}", type="primary")
