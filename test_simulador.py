"""
Testes Unitários Automatizados - Motor de Simulação Energética
Disciplina: Soluções em Energias Renováveis e Sustentáveis
Projeto: Citizen Assist AI - EcoCitizen
"""

import unittest
from simulador_energia import (
    calcular_cenario_base,
    calcular_alternativa_eficiencia,
    calcular_alternativa_solar_fotovoltaica,
    comparar_todas_alternativas,
    TARIFA_PADRAO_KWH,
    FATOR_EMISSAO_CO2_KWH,
    EQUIPAMENTOS_REF
)


class TestSimuladorEnergia(unittest.TestCase):

    def setUp(self):
        self.consumo_padrao = 250.0  # kWh/mês (casa urbana média)
        self.tarifa_padrao = TARIFA_PADRAO_KWH  # R$ 0.85/kWh

    def test_calcular_cenario_base(self):
        """Valida se os cálculos do cenário de consumo atual estão exatos."""
        resultado = calcular_cenario_base(self.consumo_padrao, self.tarifa_padrao)

        esperado_custo_mensal = round(self.consumo_padrao * self.tarifa_padrao, 2)
        esperado_custo_anual = round(esperado_custo_mensal * 12, 2)
        esperado_emissao = round((self.consumo_padrao * 12) * FATOR_EMISSAO_CO2_KWH, 2)

        self.assertEqual(resultado["consumo_mensal_kwh"], 250.0)
        self.assertEqual(resultado["consumo_anual_kwh"], 3000.0)
        self.assertEqual(resultado["custo_mensal_rs"], esperado_custo_mensal)
        self.assertEqual(resultado["custo_anual_rs"], esperado_custo_anual)
        self.assertEqual(resultado["emissao_anual_kg_co2"], esperado_emissao)

    def test_calcular_alternativa_eficiencia_completa(self):
        """Valida a Alternativa 1 (Eficiência com troca de lâmpadas e geladeira)."""
        resultado = calcular_alternativa_eficiencia(
            self.consumo_padrao,
            self.tarifa_padrao,
            trocar_geladeira=True,
            trocar_iluminacao=True
        )

        # Custo esperado: 120 (LEDs) + 2400 (Geladeira A+++) = 2520.00
        custo_esperado = (
            EQUIPAMENTOS_REF["iluminacao_led"]["custo_aparelho"] +
            EQUIPAMENTOS_REF["geladeira_inverter_a"]["custo_aparelho"]
        )
        self.assertEqual(resultado["investimento_inicial_rs"], custo_esperado)

        # Deve haver economia positiva
        self.assertGreater(resultado["economia_mensal_kwh"], 0.0)
        self.assertGreater(resultado["economia_mensal_rs"], 0.0)
        self.assertGreater(resultado["economia_anual_rs"], 0.0)

        # Payback deve ser positivo e razoável (< 5 anos)
        self.assertGreater(resultado["payback_estimado_anos"], 0.0)
        self.assertLess(resultado["payback_estimado_anos"], 5.0)

        # Emissões evitadas devem ser calculadas
        self.assertGreater(resultado["emissao_evitada_anual_kg_co2"], 0.0)

    def test_calcular_alternativa_eficiencia_parcial(self):
        """Valida cálculo de eficiência trocando apenas lâmpadas LED."""
        resultado = calcular_alternativa_eficiencia(
            self.consumo_padrao,
            self.tarifa_padrao,
            trocar_geladeira=False,
            trocar_iluminacao=True
        )

        custo_apenas_led = EQUIPAMENTOS_REF["iluminacao_led"]["custo_aparelho"]
        self.assertEqual(resultado["investimento_inicial_rs"], custo_apenas_led)
        # Payback do LED costuma ser ultrarrápido (< 0.5 anos)
        self.assertLess(resultado["payback_estimado_anos"], 1.0)

    def test_calcular_alternativa_solar_fotovoltaica(self):
        """Valida a Alternativa 2 (Dimensionamento solar fotovoltaico On-Grid)."""
        resultado = calcular_alternativa_solar_fotovoltaica(self.consumo_padrao, self.tarifa_padrao)

        # Para 250 kWh, esperamos 4 painéis de 550W (2.2 kWp)
        self.assertEqual(resultado["quantidade_paineis_550w"], 4)
        self.assertEqual(resultado["potencia_instalada_kwp"], 2.2)
        self.assertEqual(resultado["area_estimada_m2"], 10.4)

        # Investimento: 2.2 kWp * 3800 = R$ 8.360,00
        self.assertEqual(resultado["investimento_inicial_rs"], 8360.0)

        # Geração estimada e economia
        self.assertGreater(resultado["geracao_mensal_estimada_kwh"], 200.0)
        self.assertGreater(resultado["economia_mensal_rs"], 150.0)
        self.assertGreater(resultado["economia_anual_rs"], 1800.0)

        # Payback solar deve estar entre 3 e 6 anos
        self.assertGreaterEqual(resultado["payback_estimado_anos"], 3.0)
        self.assertLessEqual(resultado["payback_estimado_anos"], 6.0)

        # Emissões evitadas
        self.assertGreater(resultado["emissao_evitada_anual_kg_co2"], 200.0)

    def test_comparar_todas_alternativas(self):
        """Valida a estrutura completa da API de comparação e a síntese híbrida."""
        resultado = comparar_todas_alternativas(self.consumo_padrao, self.tarifa_padrao)

        self.assertIn("cenario_atual", resultado)
        self.assertIn("alternativa_1_eficiencia", resultado)
        self.assertIn("alternativa_2_solar_renovavel", resultado)
        self.assertIn("sintese_hibrida", resultado)
        self.assertIn("referencias", resultado)

        # Valida que as referências obrigatórias estão presentes
        refs_texto = " ".join(resultado["referencias"])
        self.assertIn("ANEEL", refs_texto)
        self.assertIn("INPE", refs_texto)
        self.assertIn("MCTI", refs_texto)
        self.assertIn("PROCEL", refs_texto)
        self.assertIn("14.300", refs_texto)

        # Valida síntese híbrida
        hibrido = resultado["sintese_hibrida"]
        inv_combinado_esperado = (
            resultado["alternativa_1_eficiencia"]["investimento_inicial_rs"] +
            resultado["alternativa_2_solar_renovavel"]["investimento_inicial_rs"]
        )
        self.assertEqual(hibrido["investimento_total_rs"], round(inv_combinado_esperado, 2))
        self.assertGreater(hibrido["payback_medio_anos"], 0.0)

    def test_consumo_limite_baixo(self):
        """Valida que o sistema não falha com consumos baixos de entrada."""
        resultado = comparar_todas_alternativas(50.0, 0.85)
        self.assertGreater(resultado["cenario_atual"]["custo_mensal_rs"], 0.0)
        self.assertGreaterEqual(resultado["alternativa_2_solar_renovavel"]["quantidade_paineis_550w"], 1)


if __name__ == "__main__":
    unittest.main()
