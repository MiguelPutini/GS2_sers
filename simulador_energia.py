"""
Módulo de Cálculos e Simulação Energética
Disciplina: Soluções em Energias Renováveis e Sustentáveis
Projeto: Citizen Assist AI - EcoCitizen

Premissas e Referências:
- Tarifa residencial média Brasil/SP (ANEEL/Enel SP 2024): R$ 0,85 por kWh (com impostos PIS/COFINS/ICMS padrão).
- Fator de emissão médio do SIN (MCTI/EPE): 0,085 kg CO2e / kWh (0,000085 tCO2e/kWh).
- Irradiação solar média diária (Atlas Brasileiro de Energia Solar - INPE/CRESESB para região SE): 4,5 kWh/m².dia.
- Performance Ratio (PR) sistema fotovoltaico: 75% (0,75).
- Custo médio instalado microgeração solar residencial (Greener/ABSOLAR 2024): ~R$ 3.800,00 por kWp instalado para sistemas pequenos (1 a 3 kWp).
"""

from dataclasses import dataclass
from typing import Dict, Any, List

TARIFA_PADRAO_KWH = 0.85  # R$/kWh
FATOR_EMISSAO_CO2_KWH = 0.085  # kg CO2 / kWh
IRRADIACAO_MEDIA_SE = 4.5  # kWh/m2.dia
PERFORMANCE_RATIO = 0.75  # 75% eficiência global estimada
CUSTO_POR_KWP_SOLAR = 3800.0  # R$/kWp instalado

# Dados de referência de equipamentos comuns vs eficientes
EQUIPAMENTOS_REF = {
    "geladeira_antiga": {
        "nome": "Geladeira Antiga / Ineficiente (>10 anos)",
        "potencia_w": 180,
        "consumo_mensal_kwh": 65.0,
        "custo_aparelho": 0.0
    },
    "geladeira_inverter_a": {
        "nome": "Geladeira Nova Inverter (Selo Procel A+++)",
        "potencia_w": 110,
        "consumo_mensal_kwh": 26.0,
        "custo_aparelho": 2400.0
    },
    "iluminacao_incandescente_mista": {
        "nome": "Iluminação Mista (Incandescentes/Fluorescentes - 8 lâmpadas)",
        "potencia_w": 480,
        "consumo_mensal_kwh": 72.0,
        "custo_aparelho": 0.0
    },
    "iluminacao_led": {
        "nome": "Iluminação Total LED (8 lâmpadas 9W)",
        "potencia_w": 72,
        "consumo_mensal_kwh": 10.8,
        "custo_aparelho": 120.0  # Kit lâmpadas LED
    },
    "chuveiro_eletrico_inverno": {
        "nome": "Chuveiro Elétrico Comum (5500W, 40 min diários na casa)",
        "potencia_w": 5500,
        "consumo_mensal_kwh": 110.0,
        "custo_aparelho": 0.0
    }
}


def calcular_cenario_base(consumo_mensal_kwh: float, tarifa_kwh: float = TARIFA_PADRAO_KWH) -> Dict[str, Any]:
    """Calcula custos e emissões anuais do cenário atual."""
    custo_mensal = consumo_mensal_kwh * tarifa_kwh
    custo_anual = custo_mensal * 12
    emissao_anual_kg_co2 = (consumo_mensal_kwh * 12) * FATOR_EMISSAO_CO2_KWH

    return {
        "consumo_mensal_kwh": round(consumo_mensal_kwh, 2),
        "consumo_anual_kwh": round(consumo_mensal_kwh * 12, 2),
        "custo_mensal_rs": round(custo_mensal, 2),
        "custo_anual_rs": round(custo_anual, 2),
        "emissao_anual_kg_co2": round(emissao_anual_kg_co2, 2)
    }


def calcular_alternativa_eficiencia(
    consumo_mensal_base: float,
    tarifa_kwh: float = TARIFA_PADRAO_KWH,
    trocar_geladeira: bool = True,
    trocar_iluminacao: bool = True
) -> Dict[str, Any]:
    """
    Alternativa 1: Eficiência Energética e Redução de Desperdício (Selo Procel A+++ / LED).
    """
    investimento_total = 0.0
    reducao_mensal_kwh = 0.0
    detalhes = []

    if trocar_iluminacao:
        red_led = EQUIPAMENTOS_REF["iluminacao_incandescente_mista"]["consumo_mensal_kwh"] - EQUIPAMENTOS_REF["iluminacao_led"]["consumo_mensal_kwh"]
        reducao_mensal_kwh += red_led
        investimento_total += EQUIPAMENTOS_REF["iluminacao_led"]["custo_aparelho"]
        detalhes.append(f"Substituição de lâmpadas incandescentes/fluorescentes por LED (Economia de ~{red_led:.1f} kWh/mês)")

    if trocar_geladeira:
        red_gel = EQUIPAMENTOS_REF["geladeira_antiga"]["consumo_mensal_kwh"] - EQUIPAMENTOS_REF["geladeira_inverter_a"]["consumo_mensal_kwh"]
        reducao_mensal_kwh += red_gel
        investimento_total += EQUIPAMENTOS_REF["geladeira_inverter_a"]["custo_aparelho"]
        detalhes.append(f"Substituição de refrigerador antigo por modelo Inverter Procel A+++ (Economia de ~{red_gel:.1f} kWh/mês)")

    # Se o consumo base for menor que a redução calculada, limita a 60% do consumo base
    if reducao_mensal_kwh > (consumo_mensal_base * 0.7):
        reducao_mensal_kwh = consumo_mensal_base * 0.45

    novo_consumo_mensal = max(consumo_mensal_base - reducao_mensal_kwh, 0.0)
    economia_mensal_kwh = consumo_mensal_base - novo_consumo_mensal
    economia_mensal_rs = economia_mensal_kwh * tarifa_kwh
    economia_anual_rs = economia_mensal_rs * 12
    emissao_evitada_anual_kg = (economia_mensal_kwh * 12) * FATOR_EMISSAO_CO2_KWH

    payback_anos = (investimento_total / economia_anual_rs) if economia_anual_rs > 0 else 0.0

    return {
        "tipo": "Eficiência Energética (Equipamentos Selo Procel A+++ e LEDs)",
        "investimento_inicial_rs": round(investimento_total, 2),
        "consumo_restante_mensal_kwh": round(novo_consumo_mensal, 2),
        "economia_mensal_kwh": round(economia_mensal_kwh, 2),
        "economia_mensal_rs": round(economia_mensal_rs, 2),
        "economia_anual_rs": round(economia_anual_rs, 2),
        "payback_estimado_anos": round(payback_anos, 1),
        "emissao_evitada_anual_kg_co2": round(emissao_evitada_anual_kg, 2),
        "detalhes": detalhes,
        "viabilidade": "Alta. Fácil implementação gradual sem necessidade de obras estruturais ou aprovação da concessionária.",
        "impacto_ambiental": "Médio-Alto: redução direta de demanda no Sistema Interligado Nacional (SIN), menor acionamento de termoelétricas poluentes.",
        "limitacoes": "A economia real varia com hábitos de uso (frequência de abertura da porta da geladeira, tempo de luz acesa)."
    }


def calcular_alternativa_solar_fotovoltaica(
    consumo_mensal_base: float,
    tarifa_kwh: float = TARIFA_PADRAO_KWH,
    cobertura_desejada: float = 0.85
) -> Dict[str, Any]:
    """
    Alternativa 2: Fonte Renovável (Microgeração Solar Fotovoltaica Conectada à Rede - On-Grid).
    Fórmula de dimensionamento:
    Geração mensal (kWh) = Potência_kWp * Irradiação_média * PR (0.75) * 30 dias
    Potência_kWp necessária = Geração_desejada / (Irradiação_média * PR * 30)
    """
    meta_geracao_mensal = consumo_mensal_base * cobertura_desejada
    fator_geracao_mensal_por_kwp = IRRADIACAO_MEDIA_SE * PERFORMANCE_RATIO * 30  # ~101.25 kWh por mês por kWp
    potencia_kwp_necessaria = meta_geracao_mensal / fator_geracao_mensal_por_kwp

    # Ajustando para módulos comerciais típicos de ~550W (0.55 kWp)
    num_paineis = max(1, round(potencia_kwp_necessaria / 0.55))
    potencia_instalada_kwp = num_paineis * 0.55
    geracao_mensal_estimada_kwh = potencia_instalada_kwp * fator_geracao_mensal_por_kwp

    investimento_total = potencia_instalada_kwp * CUSTO_POR_KWP_SOLAR

    # Considerando taxa mínima de disponibilidade da rede monofásica/bifásica (aprox 30-50 kWh/mês de taxa mínima)
    economia_efetiva_mensal_kwh = min(geracao_mensal_estimada_kwh, consumo_mensal_base * 0.90)
    economia_mensal_rs = economia_efetiva_mensal_kwh * tarifa_kwh
    economia_anual_rs = economia_mensal_rs * 12
    emissao_evitada_anual_kg = (economia_efetiva_mensal_kwh * 12) * FATOR_EMISSAO_CO2_KWH

    payback_anos = (investimento_total / economia_anual_rs) if economia_anual_rs > 0 else 0.0

    return {
        "tipo": "Fonte Renovável (Sistema Solar Fotovoltaico On-Grid)",
        "potencia_instalada_kwp": round(potencia_instalada_kwp, 2),
        "quantidade_paineis_550w": num_paineis,
        "area_estimada_m2": round(num_paineis * 2.6, 1),
        "geracao_mensal_estimada_kwh": round(geracao_mensal_estimada_kwh, 2),
        "investimento_inicial_rs": round(investimento_total, 2),
        "economia_mensal_rs": round(economia_mensal_rs, 2),
        "economia_anual_rs": round(economia_anual_rs, 2),
        "payback_estimado_anos": round(payback_anos, 1),
        "emissao_evitada_anual_kg_co2": round(emissao_evitada_anual_kg, 2),
        "viabilidade": "Média-Alta para quem tem telhado próprio e desimpedido; para aluguel ou apartamentos exige energia solar por assinatura/consórcio.",
        "impacto_ambiental": "Excelente: energia 100% limpa, renovável, zero emissões locais de gases de efeito estufa e vida útil superior a 25 anos.",
        "limitacoes": "Custo inicial de instalação (Capex); dependência de espaço físico ensolarado; regras de compensação da Lei 14.300/2022 (taxação do fio B); taxa mínima da distribuidora."
    }


def comparar_todas_alternativas(consumo_mensal_kwh: float, tarifa_kwh: float = TARIFA_PADRAO_KWH) -> Dict[str, Any]:
    """Retorna o estudo comparativo completo exigido pelo edital."""
    cenario_base = calcular_cenario_base(consumo_mensal_kwh, tarifa_kwh)
    alt_eficiencia = calcular_alternativa_eficiencia(consumo_mensal_kwh, tarifa_kwh)
    alt_solar = calcular_alternativa_solar_fotovoltaica(consumo_mensal_kwh, tarifa_kwh)

    # Proposta híbrida/recomendada
    investimento_combinado = alt_eficiencia["investimento_inicial_rs"] + alt_solar["investimento_inicial_rs"]
    economia_combinada_anual = alt_eficiencia["economia_anual_rs"] + alt_solar["economia_anual_rs"]
    payback_combinado = (investimento_combinado / economia_combinada_anual) if economia_combinada_anual > 0 else 0.0

    return {
        "cenario_atual": cenario_base,
        "alternativa_1_eficiencia": alt_eficiencia,
        "alternativa_2_solar_renovavel": alt_solar,
        "sintese_hibrida": {
            "estrategia_recomendada": "Passo 1: Redução de desperdício e troca de lâmpadas/geladeira (baixo investimento, retorno imediato) -> Passo 2: Dimensionar sistema solar menor e mais barato para cobrir a carga otimizada.",
            "investimento_total_rs": round(investimento_combinado, 2),
            "economia_anual_total_rs": round(economia_combinada_anual, 2),
            "payback_medio_anos": round(payback_combinado, 1)
        },
        "referencias": [
            "ANEEL - Agência Nacional de Energia Elétrica (Tarifas Homologadas das Distribuidoras)",
            "INPE / CRESESB - Atlas Brasileiro de Energia Solar (2ª Edição)",
            "MCTI - Fatores de Emissão de CO2 do Sistema Interligado Nacional (SIN)",
            "PROCEL / Eletrobras - Programa Nacional de Conservação de Energia Elétrica",
            "Lei nº 14.300/2022 - Marco Legal da Micro e Minigeração Distribuída"
        ]
    }


if __name__ == "__main__":
    import json
    resultado = comparar_todas_alternativas(250.0)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

