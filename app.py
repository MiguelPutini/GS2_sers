"""
Servidor e Assistente Citizen Assist AI - EcoCitizen
Combina motor determinístico de cálculos energéticos com interface web e chat interativo.
Utiliza apenas a biblioteca padrão do Python (http.server e json) para execução imediata em qualquer máquina.
"""

import http.server
import socketserver
import json
import urllib.parse
from simulador_energia import (
    comparar_todas_alternativas,
    calcular_cenario_base,
    calcular_alternativa_eficiencia,
    calcular_alternativa_solar_fotovoltaica,
    TARIFA_PADRAO_KWH
)

PORT = 8000

# Base de Conhecimento e Respostas do Assistente Citizen Assist AI
PROMPT_SISTEMA_REGRAS = """
Você é o EcoCitizen AI, o módulo de energia e sustentabilidade do Citizen Assist AI.
Suas respostas devem ser sempre:
1. Baseadas em dados técnicos e cálculos verificáveis (kWh, R$, kg CO2).
2. Claras e acessíveis para cidadãos comuns e famílias.
3. Transparentes sobre condições e limitações (não garantir economias mágicas).
4. Indicando as fontes oficiais (ANEEL, INPE, PROCEL, MCTI).
"""

HTML_INTERFACE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Citizen Assist AI - Módulo EcoCitizen (Energias Renováveis)</title>
  <style>
    :root {
      --primary: #059669;
      --primary-dark: #047857;
      --accent: #2563eb;
      --bg: #f8fafc;
      --surface: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --border: #e2e8f0;
      --solar: #d97706;
      --efficiency: #0284c7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { background: var(--bg); color: var(--text); line-height: 1.5; padding: 20px; }
    .container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    @media (max-width: 900px) { .container { grid-template-columns: 1fr; } }
    
    header { grid-column: 1 / -1; background: linear-gradient(135deg, #065f46, #047857); color: white; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    header h1 { font-size: 1.8rem; margin-bottom: 6px; }
    header p { opacity: 0.9; font-size: 0.95rem; }
    .badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-top: 8px; }

    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .card h2 { font-size: 1.25rem; margin-bottom: 16px; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    
    .input-group { margin-bottom: 14px; }
    label { display: block; font-size: 0.85rem; font-weight: 600; color: #475569; margin-bottom: 4px; }
    input, select { width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 0.95rem; }
    input:focus, select:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15); }
    button.btn-primary { width: 100%; background: var(--primary); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
    button.btn-primary:hover { background: var(--primary-dark); }

    .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 16px; }
    .metric-box { background: #f1f5f9; padding: 12px; border-radius: 8px; text-align: center; }
    .metric-box.highlight { background: #ecfdf5; border: 1px solid #a7f3d0; }
    .metric-val { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
    .metric-lbl { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }

    .comparative-card { border-left: 4px solid var(--border); margin-top: 14px; padding: 12px; background: #fafafa; border-radius: 0 8px 8px 0; }
    .comparative-card.solar { border-left-color: var(--solar); }
    .comparative-card.efficiency { border-left-color: var(--efficiency); }
    .comparative-card.hybrid { border-left-color: var(--primary); background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid var(--primary); }
    .comparative-card h3 { font-size: 0.95rem; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
    .comparative-card p { font-size: 0.85rem; color: #334155; margin-bottom: 4px; }

    /* Chat Section */
    .chat-box { display: flex; flex-direction: column; height: 640px; }
    .chat-history { flex: 1; overflow-y: auto; padding: 12px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 12px; display: flex; flex-direction: column; gap: 10px; }
    .chat-msg { max-width: 88%; padding: 10px 14px; border-radius: 12px; font-size: 0.88rem; line-height: 1.45; }
    .chat-msg.user { align-self: flex-end; background: var(--primary); color: white; border-bottom-right-radius: 2px; }
    .chat-msg.assistant { align-self: flex-start; background: white; border: 1px solid var(--border); color: #1e293b; border-bottom-left-radius: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
    .chat-quick-actions { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; }
    .quick-pill { background: #e2e8f0; border: none; padding: 6px 12px; border-radius: 999px; font-size: 0.75rem; cursor: pointer; white-space: nowrap; color: #334155; }
    .quick-pill:hover { background: #cbd5e1; }
    .chat-input-bar { display: flex; gap: 8px; }
    .chat-input-bar input { flex: 1; }
    .chat-input-bar button { padding: 10px 18px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }

    .limitation-alert { background: #fffbeb; border: 1px solid #fde68a; color: #92400e; padding: 10px 14px; border-radius: 8px; font-size: 0.8rem; margin-top: 14px; }
  </style>
</head>
<body>

<header>
  <h1>Citizen Assist AI &bull; EcoCitizen</h1>
  <p>Assistente Digital para Cidadãos em Eficiência Energética e Microgeração Renovável</p>
  <span class="badge">Global Solution &bull; Soluções em Energias Renováveis e Sustentáveis</span>
</header>

<main class="container" style="margin-top: 20px;">
  <!-- Coluna 1: Simulador Técnico de Consumo & Alternativas -->
  <section class="card">
    <h2>Simulador Energético do Cidadão</h2>
    <p style="font-size:0.85rem; color:var(--muted); margin-bottom:14px;">
      Insira os dados do imóvel para gerar o estudo comparativo técnico exigido pelo desafio.
    </p>

    <div class="input-group">
      <label for="consumo">Consumo Mensal de Eletricidade (kWh/mês)</label>
      <input type="number" id="consumo" value="250" min="30" max="2000" step="10">
      <small style="color:var(--muted); font-size:0.75rem;">Média residencial urbana típica: 180 a 300 kWh/mês</small>
    </div>

    <div class="input-group">
      <label for="tarifa">Tarifa com Impostos (R$/kWh)</label>
      <input type="number" id="tarifa" value="0.85" min="0.4" max="2.0" step="0.05">
      <small style="color:var(--muted); font-size:0.75rem;">Referência ANEEL/Distribuidora local (padrão R$ 0,85)</small>
    </div>

    <button class="btn-primary" onclick="executarSimulacao()">Calcular Comparativo de Alternativas</button>

    <div class="metrics-grid" id="metricsCenario">
      <div class="metric-box">
        <div class="metric-val" id="custoMensalAtual">R$ 212,50</div>
        <div class="metric-lbl">Gasto Mensal Atual</div>
      </div>
      <div class="metric-box">
        <div class="metric-val" id="emissaoAtual">255 kg</div>
        <div class="metric-lbl">Emissão CO₂ / ano</div>
      </div>
    </div>

    <div class="comparative-card efficiency" id="cardEficiencia">
      <h3><span>Alternativa 1: Eficiência Energética</span> <span id="paybackEficiencia" style="color:var(--efficiency);">Payback ~2.5 anos</span></h3>
      <p id="descEficiencia">Troca por LED e refrigerador Selo Procel A+++.</p>
      <p><strong>Investimento Estimado:</strong> <span id="invEficiencia">R$ 2.520,00</span></p>
      <p><strong>Economia Projetada:</strong> <span id="econEficiencia">R$ 85,17/mês (~100 kWh/mês)</span></p>
      <p><strong>Impacto:</strong> <span id="co2Eficiencia">102 kg CO₂ evitados/ano</span></p>
    </div>

    <div class="comparative-card solar" id="cardSolar">
      <h3><span>Alternativa 2: Fonte Renovável (Solar On-Grid)</span> <span id="paybackSolar" style="color:var(--solar);">Payback ~3.7 anos</span></h3>
      <p id="descSolar">4 painéis solares 550W (~2,2 kWp) instalados no telhado.</p>
      <p><strong>Investimento Estimado:</strong> <span id="invSolar">R$ 8.360,00</span></p>
      <p><strong>Economia Projetada:</strong> <span id="econSolar">R$ 189,34/mês (~222 kWh/mês)</span></p>
      <p><strong>Impacto:</strong> <span id="co2Solar">227 kg CO₂ evitados/ano</span></p>
    </div>

    <div class="comparative-card hybrid" id="cardHibrido">
      <h3><span>💡 Recomendação Estratégica Híbrida</span> <span id="paybackHibrido" style="color:var(--primary-dark);">Payback Médio ~3.4 anos</span></h3>
      <p id="descHibrido">Passo 1: Enxugar desperdício com Eficiência -> Passo 2: Dimensionar Solar menor sob medida.</p>
      <p><strong>Investimento Combinado:</strong> <span id="invHibrido">R$ 10.880,00</span></p>
      <p><strong>Economia Anual Projetada:</strong> <span id="econHibrido">R$ 3.294,09 / ano</span></p>
      <p><strong>Vantagem Estratégica:</strong> <span style="color:#047857; font-weight:600;">Máxima taxa de retorno de capital e menor necessidade de telhado.</span></p>
    </div>

    <div class="limitation-alert">
      <strong>Condições & Limitações:</strong> Estimativas baseadas em 4,5 kWh/m².dia de insolação (Atlas Solar INPE) e tarifa média ANEEL. Resultados reais dependem de sombreamento, orientação do telhado e tarifas em bandeiras vermelhas.
    </div>
  </section>

  <!-- Coluna 2: Assistente Digital Citizen Assist AI -->
  <section class="card chat-box">
    <h2>Assistente Digital EcoCitizen</h2>
    <div class="chat-history" id="chatHistory">
      <div class="chat-msg assistant">
        Olá! Sou o assistente de sustentabilidade do <strong>Citizen Assist AI</strong>. Posso te orientar sobre economia na conta de luz, dimensionamento de energia solar fotovoltaica, moradores de aluguel e combate ao desperdício doméstico. O que você gostaria de analisar hoje?
      </div>
    </div>

    <div class="chat-quick-actions">
      <button class="quick-pill" onclick="enviarMensagemRapida('Como diminuir o gasto do chuveiro elétrico?')">Chuveiro Elétrico</button>
      <button class="quick-pill" onclick="enviarMensagemRapida('Vale a pena colocar energia solar na minha casa?')">Energia Solar Vale a Pena?</button>
      <button class="quick-pill" onclick="enviarMensagemRapida('O que compensa mais: trocar eletrodomésticos ou colocar painel solar?')">Eficiência vs. Solar</button>
      <button class="quick-pill" onclick="enviarMensagemRapida('Moro de aluguel ou apartamento, como posso economizar com energia?')">Aluguel / Apartamento</button>
      <button class="quick-pill" onclick="enviarMensagemRapida('Vale a pena trocar a geladeira antiga e lâmpadas?')">Geladeira e LEDs</button>
      <button class="quick-pill" onclick="enviarMensagemRapida('Quais as limitações e referências dos cálculos?')">Fontes e Limitações</button>
    </div>

    <div class="chat-input-bar">
      <input type="text" id="chatInput" placeholder="Faça uma pergunta sobre energia e economia..." onkeypress="if(event.key==='Enter') enviarMensagem()">
      <button onclick="enviarMensagem()">Enviar</button>
    </div>
  </section>
</main>

<script>
let dadosUltimaSimulacao = null;

async function executarSimulacao() {
  const consumo = parseFloat(document.getElementById('consumo').value) || 250;
  const tarifa = parseFloat(document.getElementById('tarifa').value) || 0.85;

  try {
    const resp = await fetch(`/api/simular?consumo=${consumo}&tarifa=${tarifa}`);
    const data = await resp.json();
    dadosUltimaSimulacao = data;

    document.getElementById('custoMensalAtual').innerText = `R$ ${data.cenario_atual.custo_mensal_rs.toFixed(2)}`;
    document.getElementById('emissaoAtual').innerText = `${data.cenario_atual.emissao_anual_kg_co2.toFixed(0)} kg`;

    // Eficiência
    document.getElementById('paybackEficiencia').innerText = `Payback ~${data.alternativa_1_eficiencia.payback_estimado_anos} anos`;
    document.getElementById('invEficiencia').innerText = `R$ ${data.alternativa_1_eficiencia.investimento_inicial_rs.toFixed(2)}`;
    document.getElementById('econEficiencia').innerText = `R$ ${data.alternativa_1_eficiencia.economia_mensal_rs.toFixed(2)}/mês (${data.alternativa_1_eficiencia.economia_mensal_kwh} kWh)`;
    document.getElementById('co2Eficiencia').innerText = `${data.alternativa_1_eficiencia.emissao_evitada_anual_kg_co2.toFixed(1)} kg CO₂ evitados/ano`;

    // Solar
    document.getElementById('paybackSolar').innerText = `Payback ~${data.alternativa_2_solar_renovavel.payback_estimado_anos} anos`;
    document.getElementById('descSolar').innerText = `${data.alternativa_2_solar_renovavel.quantidade_paineis_550w} painéis solares 550W (${data.alternativa_2_solar_renovavel.potencia_instalada_kwp} kWp, ~${data.alternativa_2_solar_renovavel.area_estimada_m2} m²).`;
    document.getElementById('invSolar').innerText = `R$ ${data.alternativa_2_solar_renovavel.investimento_inicial_rs.toFixed(2)}`;
    document.getElementById('econSolar').innerText = `R$ ${data.alternativa_2_solar_renovavel.economia_mensal_rs.toFixed(2)}/mês (${data.alternativa_2_solar_renovavel.geracao_mensal_estimada_kwh} kWh)`;
    document.getElementById('co2Solar').innerText = `${data.alternativa_2_solar_renovavel.emissao_evitada_anual_kg_co2.toFixed(1)} kg CO₂ evitados/ano`;

    // Híbrido
    if (data.sintese_hibrida) {
      document.getElementById('paybackHibrido').innerText = `Payback Médio ~${data.sintese_hibrida.payback_medio_anos} anos`;
      document.getElementById('invHibrido').innerText = `R$ ${data.sintese_hibrida.investimento_total_rs.toFixed(2)}`;
      document.getElementById('econHibrido').innerText = `R$ ${data.sintese_hibrida.economia_anual_total_rs.toFixed(2)} / ano`;
    }
  } catch (err) {
    console.error("Erro ao simular:", err);
  }
}

async function enviarMensagem() {
  const input = document.getElementById('chatInput');
  const texto = input.value.trim();
  if (!texto) return;

  const history = document.getElementById('chatHistory');
  history.innerHTML += `<div class="chat-msg user">${texto}</div>`;
  input.value = '';
  history.scrollTop = history.scrollHeight;

  const consumo = parseFloat(document.getElementById('consumo').value) || 250;
  const tarifa = parseFloat(document.getElementById('tarifa').value) || 0.85;

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensagem: texto, consumo, tarifa })
    });
    const data = await resp.json();

    history.innerHTML += `<div class="chat-msg assistant">${data.resposta}</div>`;
    history.scrollTop = history.scrollHeight;
  } catch (err) {
    history.innerHTML += `<div class="chat-msg assistant">Erro ao processar mensagem. Verifique a conexão com o servidor.</div>`;
    history.scrollTop = history.scrollHeight;
  }
}

function enviarMensagemRapida(txt) {
  document.getElementById('chatInput').value = txt;
  enviarMensagem();
}

window.onload = executarSimulacao;
</script>
</body>
</html>
"""

def responder_chat_ia(mensagem: str, consumo: float, tarifa: float) -> str:
    """Motor de resposta inteligente e fundamentado do assistente EcoCitizen."""
    simulacao = comparar_todas_alternativas(consumo, tarifa)
    msg_lower = mensagem.lower()

    if "chuveiro" in msg_lower or "banho" in msg_lower:
        return (
            "🚿 <strong>Análise do Chuveiro Elétrico:</strong><br>"
            "O chuveiro elétrico comum consome cerca de 5.500W. Se uma família tomar 4 banhos de 10 min por dia (40 min totais), "
            f"o consumo é de aproximadamente <strong>110 kWh/mês</strong>, o que custa <strong>R$ {110 * tarifa:.2f}/mês</strong>.<br>"
            "<strong>Dicas práticas de economia:</strong><br>"
            "• Reduzir 5 minutos de banho por pessoa economiza ~55 kWh/mês (economia de ~R$ 46,00/mês).<br>"
            "• Usar a chave na posição 'Verão' reduz a potência em cerca de 30% a 40% nos dias mais quentes.<br>"
            "<em>Fonte: Programa Procel / Eletrobras.</em>"
        )

    elif "solar" in msg_lower and ("vale" in msg_lower or "compensa" in msg_lower or "colocar" in msg_lower or "placa" in msg_lower or "painel" in msg_lower):
        solar = simulacao["alternativa_2_solar_renovavel"]
        return (
            f"☀️ <strong>Viabilidade de Energia Solar para {consumo:.0f} kWh/mês:</strong><br>"
            f"• <strong>Sistema recomendado:</strong> {solar['quantidade_paineis_550w']} placas de 550W ({solar['potencia_instalada_kwp']} kWp), ocupando ~{solar['area_estimada_m2']} m² de telhado.<br>"
            f"• <strong>Investimento estimado:</strong> ~R$ {solar['investimento_inicial_rs']:.2f}.<br>"
            f"• <strong>Economia na conta:</strong> até <strong>R$ {solar['economia_mensal_rs']:.2f}/mês</strong>.<br>"
            f"• <strong>Retorno do investimento (Payback):</strong> em cerca de <strong>{solar['payback_estimado_anos']} anos</strong> (com vida útil dos módulos superior a 25 anos).<br>"
            "⚠️ <strong>Condições importantes:</strong> É necessário ter telhado próprio sem sombras. Caso more de aluguel ou prédio, a opção recomendada é energia solar por assinatura (consórcio)."
        )

    elif "aluguel" in msg_lower or "apartamento" in msg_lower or "sem telhado" in msg_lower or "inquilino" in msg_lower or "predio" in msg_lower or "prédio" in msg_lower:
        return (
            "🏢 <strong>Mora de Aluguel ou em Apartamento? Saiba como economizar:</strong><br>"
            "Se você não tem telhado próprio ou não pode fazer obras, existem duas soluções imediatas:<br>"
            "1️⃣ <strong>Energia Solar por Assinatura (Fazendas Solares):</strong> Regulamentada pela Lei 14.300/2022, "
            "você se associa a um consórcio ou fazenda solar remota e recebe créditos de energia limpa na sua conta atual, "
            "com desconto direto de <strong>10% a 15% todo mês</strong> sem gastar 1 real de obra.<br>"
            "2️⃣ <strong>Eficiência Portátil:</strong> Troque lâmpadas por LED e opte por refrigerador Procel A+++. "
            "Ao mudar de imóvel, você leva todos os seus equipamentos eficientes com você!"
        )

    elif "geladeira" in msg_lower or "refrigerador" in msg_lower:
        return (
            "🧊 <strong>Impacto da Troca de Geladeira:</strong><br>"
            "• Uma geladeira antiga (>10 anos) consome cerca de <strong>65 kWh/mês</strong> (R$ 55,25/mês).<br>"
            "• Um modelo moderno Inverter Selo Procel A+++ consome apenas <strong>26 kWh/mês</strong> (R$ 22,10/mês).<br>"
            f"• <strong>Economia direta:</strong> 39 kWh/mês (~R$ {39 * tarifa:.2f}/mês ou quase R$ 400,00/ano).<br>"
            "O investimento de ~R$ 2.400,00 se paga pelo próprio consumo reduzido e ainda valoriza a cozinha com menos ruído e mais durabilidade."
        )

    elif "lampada" in msg_lower or "lâmpada" in msg_lower or "led" in msg_lower or "iluminac" in msg_lower or "iluminaç" in msg_lower:
        return (
            "💡 <strong>Substituição por Lâmpadas LED:</strong><br>"
            "• 8 lâmpadas incandescentes ou fluorescentes comuns (60W cada) consomem cerca de 72 kWh/mês.<br>"
            "• Substituindo por 8 lâmpadas LED de 9W (mesmo fluxo luminoso), o consumo cai para apenas 10,8 kWh/mês.<br>"
            f"• <strong>Economia:</strong> mais de 61 kWh/mês (economia de ~R$ {61.2 * tarifa:.2f}/mês).<br>"
            "• <strong>Payback relâmpago:</strong> O investimento de ~R$ 120,00 se paga em apenas <strong>2 a 3 meses</strong>!"
        )

    elif "trocar" in msg_lower or "compensa mais" in msg_lower or "efici" in msg_lower or "versus" in msg_lower or "vs" in msg_lower:
        efic = simulacao["alternativa_1_eficiencia"]
        solar = simulacao["alternativa_2_solar_renovavel"]
        return (
            "⚖️ <strong>Comparativo Técnico: Eficiência vs. Energia Solar:</strong><br>"
            f"1️⃣ <strong>Eficiência Energética (Procel A+++ / LEDs):</strong><br>"
            f"Investimento menor (R$ {efic['investimento_inicial_rs']:.2f}), economia de R$ {efic['economia_mensal_rs']:.2f}/mês e payback rápido de <strong>{efic['payback_estimado_anos']} anos</strong>.<br><br>"
            f"2️⃣ <strong>Energia Solar Fotovoltaica:</strong><br>"
            f"Investimento maior (R$ {solar['investimento_inicial_rs']:.2f}), mas gera uma economia alta (R$ {solar['economia_mensal_rs']:.2f}/mês) com payback de <strong>{solar['payback_estimado_anos']} anos</strong>.<br><br>"
            "💡 <strong>Recomendação do EcoCitizen:</strong> Faça primeiro a eficiência energética para enxugar o desperdício; assim, quando for dimensionar a energia solar, precisará de menos placas e gastará muito menos!"
        )

    elif "hibrid" in msg_lower or "combinad" in msg_lower or "passo a passo" in msg_lower or "estrateg" in msg_lower:
        hib = simulacao["sintese_hibrida"]
        return (
            "🎯 <strong>Estratégia Combinada Híbrida (Recomendação Oficial):</strong><br>"
            f"• <strong>{hib['estrategia_recomendada']}</strong><br>"
            f"• <strong>Investimento total combinado:</strong> R$ {hib['investimento_total_rs']:.2f}<br>"
            f"• <strong>Economia anual conjunta:</strong> R$ {hib['economia_anual_total_rs']:.2f}/ano<br>"
            f"• <strong>Payback médio ponderado:</strong> ~{hib['payback_medio_anos']} anos.<br>"
            "Essa estratégia reduz o risco financeiro e maximiza a autossuficiência da sua casa."
        )

    elif "ar condicionado" in msg_lower or "ar-condicionado" in msg_lower or "climatiz" in msg_lower:
        return (
            "❄️ <strong>Dicas para Ar-Condicionado:</strong><br>"
            "• Prefira sempre tecnologia <strong>Inverter com Selo Procel A</strong> (economiza até 40% em relação ao convencional).<br>"
            "• Mantenha a temperatura regulada em <strong>23°C ou 24°C</strong> (cada grau a menos aumenta o consumo em até 8%).<br>"
            "• Limpe os filtros a cada 15 dias: a poeira acumulada força o compressor a trabalhar mais."
        )

    elif "bandeira" in msg_lower or "vermelha" in msg_lower or "amarela" in msg_lower:
        return (
            "🚩 <strong>Impacto das Bandeiras Tarifárias:</strong><br>"
            "Quando as chuvas diminuem, a ANEEL aciona termoelétricas fósseis caras e poluentes, aplicando bandeiras Amarela e Vermelha (acrescentando até R$ 7,87 a cada 100 kWh).<br>"
            "Adotando eficiência energética e microgeração solar, sua residência fica muito menos vulnerável a esses aumentos repentinos na conta!"
        )

    elif "co2" in msg_lower or "carbono" in msg_lower or "emiss" in msg_lower or "ambiente" in msg_lower or "sustentav" in msg_lower:
        solar = simulacao["alternativa_2_solar_renovavel"]
        efic = simulacao["alternativa_1_eficiencia"]
        return (
            "🌱 <strong>Impacto Ambiental e Emissões de CO₂:</strong><br>"
            "No Brasil, o Sistema Interligado Nacional (SIN) tem fator médio de <strong>0,085 kg de CO₂ por kWh</strong> gerado.<br>"
            f"• Com Eficiência Energética, sua casa evita <strong>{efic['emissao_evitada_anual_kg_co2']:.1f} kg CO₂/ano</strong>.<br>"
            f"• Com Energia Solar, sua casa evita <strong>{solar['emissao_evitada_anual_kg_co2']:.1f} kg CO₂/ano</strong> (equivalente ao plantio de cerca de 10 a 15 árvores a cada ciclo).<br>"
            "<em>Fonte: Ministério da Ciência, Tecnologia e Inovação (MCTI).</em>"
        )

    elif "fonte" in msg_lower or "limita" in msg_lower or "refer" in msg_lower:
        return (
            "📚 <strong>Referências e Limitações dos Modelos:</strong><br>"
            "• <strong>Fontes oficiais utilizadas:</strong> Atlas Solar Brasileiro (INPE/CRESESB), Tarifas Homologadas da ANEEL, Fatores de Emissão de Carbono do MCTI e Selo Procel (Eletrobras).<br>"
            "• <strong>Limitações das estimativas:</strong> As economias não são garantidas de forma absoluta. Variam de acordo com irradiação solar sazonal, variações de tarifa (bandeiras amarela/vermelha), "
            "e cobrança da taxa mínima de disponibilidade da rede elétrica (Lei 14.300/2022)."
        )

    else:
        # Resposta orientadora padrão contextualizada com os dados do consumo
        base = simulacao["cenario_atual"]
        efic = simulacao["alternativa_1_eficiencia"]
        solar = simulacao["alternativa_2_solar_renovavel"]
        return (
            f"Para o seu consumo de <strong>{consumo:.0f} kWh/mês</strong> (custo atual de ~R$ {base['custo_mensal_rs']:.2f}/mês):<br>"
            f"• <strong>Com Eficiência (LEDs + Inverter):</strong> você economiza cerca de <strong>R$ {efic['economia_mensal_rs']:.2f}/mês</strong> com payback em {efic['payback_estimado_anos']} anos.<br>"
            f"• <strong>Com Solar Renovável:</strong> você economiza cerca de <strong>R$ {solar['economia_mensal_rs']:.2f}/mês</strong> e evita {solar['emissao_evitada_anual_kg_co2']:.1f} kg de CO₂ por ano.<br>"
            "Você gostaria de saber detalhes sobre: chuveiro elétrico, energia solar, geladeira/LEDs, morador de aluguel ou limitações técnicas?"
        )


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        if url_parsed.path == "/" or url_parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode("utf-8"))
        elif url_parsed.path == "/api/simular":
            qs = urllib.parse.parse_qs(url_parsed.query)
            try:
                consumo = float(qs.get("consumo", [250])[0])
            except (ValueError, TypeError, IndexError):
                consumo = 250.0
            try:
                tarifa = float(qs.get("tarifa", [TARIFA_PADRAO_KWH])[0])
            except (ValueError, TypeError, IndexError):
                tarifa = TARIFA_PADRAO_KWH

            resultado = comparar_todas_alternativas(consumo, tarifa)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                data = {}

            mensagem = data.get("mensagem", "")
            try:
                consumo = float(data.get("consumo", 250))
            except (ValueError, TypeError):
                consumo = 250.0
            try:
                tarifa = float(data.get("tarifa", TARIFA_PADRAO_KWH))
            except (ValueError, TypeError):
                tarifa = TARIFA_PADRAO_KWH

            resposta = responder_chat_ia(mensagem, consumo, tarifa)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"resposta": resposta}, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"Citizen Assist AI (EcoCitizen) rodando com sucesso em http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    start_server()
