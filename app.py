import streamlit as st

# Simulador de IRPF 2024 com base na tabela progressiva atualizada (com dependentes, educação e PGBL)
def calcular_irpf_2024(rendimentos, inss, despesas_medicas, despesas_educacao=0, pgbp=0, num_dependentes=0, irrf=0):
    limite_dependente = 2275.08 * num_dependentes
    limite_educacao = min(despesas_educacao, 3561.50 * num_dependentes)
    limite_pgbp = min(pgbp, rendimentos * 0.12)

    base_calculo = rendimentos - inss - despesas_medicas - limite_educacao - limite_pgbp - limite_dependente

    aliquota = 0.275
    parcela_deduzir = 10740.98

    imposto_devido = base_calculo * aliquota - parcela_deduzir
    imposto_devido = max(imposto_devido, 0)

    diferenca = imposto_devido - irrf

    return {
        "Base de Cálculo": round(base_calculo, 2),
        "Imposto Devido": round(imposto_devido, 2),
        "IRRF Pago": round(irrf, 2),
        "Diferença (a pagar ou restituir)": round(diferenca, 2)
    }

# Interface com Streamlit
st.title("Simulador IRPF 2024")

rendimentos = st.number_input("Rendimentos Tributáveis (R$)", min_value=0.0, value=0.0, step=100.0)
inss = st.number_input("Contribuição ao INSS (R$)", min_value=0.0, value=0.0, step=100.0)
despesas_medicas = st.number_input("Despesas Médicas (R$)", min_value=0.0, value=0.0, step=100.0)
despesas_educacao = st.number_input("Despesas com Educação (R$)", min_value=0.0, value=0.0, step=100.0)
pgbp = st.number_input("Contribuições PGBL (R$)", min_value=0.0, value=0.0, step=100.0)
num_dependentes = st.number_input("Número de Dependentes", min_value=0, value=0, step=1)
irrf = st.number_input("IRRF Pago (R$)", min_value=0.0, value=0.0, step=100.0)

if st.button("Calcular IRPF"):
    resultado = calcular_irpf_2024(
        rendimentos=rendimentos,
        inss=inss,
        despesas_medicas=despesas_medicas,
        despesas_educacao=despesas_educacao,
        pgbp=pgbp,
        num_dependentes=num_dependentes,
        irrf=irrf
    )

    st.subheader("Resultado da Simulação")
    for chave, valor in resultado.items():
        st.write(f"{chave}: R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
