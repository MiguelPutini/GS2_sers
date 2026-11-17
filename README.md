# Citizen Assist AI - EcoCitizen
## Soluções em Energias Renováveis e Sustentáveis
**Global Solution - Ciência da Computação (Turmas 1CC) - FIAP**

---

### Integrantes do Grupo
* **Miguel Putini** - RM: 571624
* **Alexandre Rizzi** - RM: 569621
* **Lucas Klein de Veiga** - RM: 570029

**Repositório GitHub:** `https://github.com/MiguelPutini/GS2_sers.git`  
**Link do Vídeo no YouTube (Não Listado):** `https://youtu.be/SEU_VIDEO_AQUI`

---

## 1. Descrição do Público-Alvo e do Problema Abordado

### 1.1 Público-Alvo
Cidadãos e famílias residentes em áreas urbanas e periféricas, com padrão de consumo residencial médio (entre 180 e 350 kWh/mês), vulneráveis aos reajustes constantes da tarifa de eletricidade e acionamento de bandeiras tarifárias (amarela/vermelha).

### 1.2 O Problema
Grande parte das famílias sofre com o peso da conta de luz no orçamento doméstico devido a:
1. **Desperdício e equipamentos ineficientes:** Uso de refrigeradores com mais de 10 anos de uso, lâmpadas incandescentes/fluorescentes e banhos prolongados com chuveiros elétricos de alta potência (5500W).
2. **Falta de clareza e desinformação:** O cidadão comum não sabe se a energia solar fotovoltaica "vale a pena" para o seu caso, desconhece o tempo de retorno financeiro (*payback*) e não tem acesso a orientações técnicas mastigadas e confiáveis.

---

## 2. A Solução: EcoCitizen (Citizen Assist AI)
O **EcoCitizen** é o módulo de energia e sustentabilidade integrado ao assistente digital **Citizen Assist AI**. A aplicação conta com:
- **Motor de Cálculo Energético Determinístico:** Realiza os dimensionamentos e cálculos exatos sem alucinações matemáticas.
- **Comparativo Técnico de Alternativas:** Compara lado a lado o cenário atual contra **Eficiência Energética** e **Microgeração Solar Fotovoltaica (Fonte Renovável)**.
- **Assistente Interativo:** Responde às dúvidas do cidadão em linguagem acessível, apresentando dados de custos, viabilidade, economia, redução de emissões e limitações reais.

---

## 3. Dados Utilizados, Origem e Premissas dos Cálculos

| Variável / Parâmetro | Valor Utilizado | Unidade | Origem / Premissa |
| :--- | :--- | :--- | :--- |
| **Tarifa de Eletricidade Residencial** | R$ 0,85 | R$ / kWh | Média homologada ANEEL / Enel SP com tributos (ICMS/PIS/COFINS) |
| **Irradiação Solar Média Diária (H)** | 4,50 | kWh/m².dia | Atlas Brasileiro de Energia Solar (INPE / CRESESB) para região Sudeste |
| **Fator de Performance do Sistema (PR)**| 75% (0,75) | Adimensional | Perdas por temperatura, cabeamento, sujidade e inversor (ABSOLAR) |
| **Fator de Emissão de CO₂ do SIN** | 0,085 | kg CO₂ / kWh | Ministério da Ciência, Tecnologia e Inovação (MCTI) / EPE |
| **Custo de Instalação Solar Residencial** | R$ 3.800,00 | R$ / kWp | Estudo de Mercado Greener / ABSOLAR 2024 para sistemas até 3 kWp |
| **Geladeira Antiga vs Nova Procel A+++** | 65 kWh vs 26 kWh | kWh / mês | Tabela de Eficiência Energética PROCEL / INMETRO |
| **Iluminação Mista vs 100% LED** | 72 kWh vs 10,8 kWh | kWh / mês | Comparação de 8 pontos de luz (60W incand./fluoresc. vs 9W LED) |

---

## 4. Comparação entre Alternativas Técnicas

Considerando um consumo residencial de **250 kWh/mês** (Custo atual: **R$ 212,50/mês** ou **R$ 2.550,00/ano**):

| Métrica Analisada | Cenário 1: Eficiência Energética (Procel A+++ & LED) | Cenário 2: Fonte Renovável (Solar Fotovoltaico On-Grid) |
| :--- | :--- | :--- |
| **Tecnologia Aplicada** | Lâmpadas LED (8 un.) + Geladeira Inverter A+++ | 4 Módulos Fotovoltaicos 550W (2,2 kWp) + Inversor |
| **Investimento Inicial (Capex)** | **R$ 2.520,00** (R$ 120 lâmpadas + R$ 2.400 geladeira) | **R$ 8.360,00** (Kit completo instalado com homologação) |
| **Economia Mensal Gerada** | **~100,2 kWh / R$ 85,17 por mês** | **~222,8 kWh / R$ 189,34 por mês** |
| **Economia Anual Projetada** | **R$ 1.022,04 / ano** | **R$ 2.272,05 / ano** |
| **Tempo de Retorno (Payback)** | **~2,5 anos** | **~3,7 anos** |
| **Impacto Ambiental (CO₂ evitado)**| **102,2 kg CO₂ / ano** | **227,2 kg CO₂ / ano** |
| **Viabilidade Técnica** | **Alta**: não requer obras, telhado ou homologação | **Alta para donos de telhado**; moradores de apto dependem de assinatura |
| **Vida Útil da Solução** | ~10 a 12 anos | > 25 anos (garantia linear dos módulos solares) |

### Síntese e Recomendação Estratégica:
A recomendação técnica do **Citizen Assist AI** é a **Estratégia Combinada**: primeiro adotar medidas de eficiência energética de baixo custo (troca de lâmpadas e racionalização de uso), reduzindo a demanda da residência. Em seguida, ao dimensionar o sistema solar fotovoltaico, o cidadão precisará de um sistema menor e mais barato, maximizando a taxa de retorno do seu capital.

---

## 5. Referências e Limitações das Estimativas

### Condições e Limitações Declaradas ao Cidadão:
1. **Não garantia de valores exatos:** A geração solar real sofre flutuações sazonais (menor no inverno, maior no verão) e perdas por sombreamento predial ou arbóreo.
2. **Custo de Disponibilidade e Fio B:** Sistemas On-Grid continuam sujeitos à taxa mínima de disponibilidade da rede da distribuidora e às regras graduais da Lei Federal nº 14.300/2022 (Marco Legal da Microgeração).
3. **Comportamento Humano:** A eficiência energética dos aparelhos depende da manutenção das borrachas de vedação, frequência de abertura de portas e hábitos diários de uso.

### Referências Bibliográficas e Normativas:
- **ANEEL:** Cadernos Temáticos de Regulação e Tarifas Homologadas das Distribuidoras (Resolução Normativa nº 1.000/2021).
- **INPE / CRESESB:** Atlas Brasileiro de Energia Solar, 2ª Edição (Laboratório de Modelagem e Estudos de Recursos Renováveis de Energia).
- **MCTI / EPE:** Fatores de Emissão de Dióxido de Carbono do Sistema Interligado Nacional (SIN) para inventários corporativos e residenciais.
- **PROCEL / Eletrobras:** Tabelas de Consumo e Eficiência Energética de Eletrodomésticos Nacionais.
- **BRASIL:** Lei nº 14.300, de 6 de janeiro de 2022 (Marco Legal da Microgeração e Minigeração Distribuída).

---

## 6. Registro dos Testes com Usuários e Ajustes Realizados

Para cumprir a exigência do edital quanto à usabilidade e utilidade da solução, o assistente foi submetido a testes práticos com 3 perfis de usuários:

| Teste # | Perfil do Usuário | Situação Testada | Comentários Recebidos | Ajuste Realizado no Assistente |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Morador de casa própria, 52 anos | Perguntou se valia a pena colocar painel solar e quanto custava. | "Achei os cálculos bons, mas não sabia o que significava kWp e achei o termo muito técnico." | O assistente foi atualizado para traduzir kWp em **número de placas solares** (ex: 4 painéis de 550W) e área de telhado em metros quadrados ($m^2$). |
| **02** | Moradora de apartamento alugado, 28 anos | Queria economizar na conta de luz, mas não tem telhado para placas solares. | "Gostei da simulação, mas moro de aluguel e não posso furar telhado. O que eu faço?" | Incluímos a recomendação de **Energia Solar por Assinatura (consórcio/fazendas solares)** e o foco imediato em Eficiência Energética (lâmpadas e hábitos). |
| **03** | Estudante universitário, 21 anos | Testou orientações sobre chuveiro elétrico e substituição de lâmpadas. | "Ficou muito claro o impacto de reduzir 5 minutos no banho na conta de luz final." | Adicionamos os botões de atalho (*quick pills*) na interface para acesso imediato a perguntas sobre chuveiro e comparação direta. |

---

## 7. Instruções para Executar e Testar a Solução

A solução foi desenvolvida utilizando a biblioteca padrão do Python (sem dependência obrigatória de pacotes pesados externos), garantindo portabilidade e execução imediata em qualquer ambiente.

### Pré-requisitos
- Python 3.8 ou superior instalado.

### Passo a Passo de Execução:
1. Abra o terminal na pasta do projeto:
   ```bash
   cd gs2_sers
   ```
2. (Opcional) Instalar ou verificar dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Executar os testes unitários automatizados:
   ```bash
   python test_simulador.py
   ```
4. Iniciar o servidor da aplicação:
   ```bash
   python app.py
   ```
5. Abra o seu navegador e acesse:
   ```text
   http://localhost:8000
   ```
6. Teste as funcionalidades:
   - Altere os valores de consumo (kWh) e tarifa para ver a atualização em tempo real dos cálculos (Cenário Base, Eficiência, Solar e Estratégia Híbrida).
   - Utilize o chat interativo do **EcoCitizen** clicando nos atalhos ou digitando dúvidas sobre economia de energia, aluguel/apartamento, eletrodomésticos e fontes renováveis.

