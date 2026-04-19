# Biblioteca de Estratégias de Trading

Este documento contém 100 estratégias de trading organizadas para consulta de agentes. Cada estratégia apresenta um nome curto e uma descrição prática para orientar decisões de trade.

## Uso
- Os agentes podem ler este documento para priorizar regras de entrada, saída e gerenciamento de risco.
- Estratégias são apresentadas em formato simples para facilitar a extração automática.
- Cada estratégia foca em análise técnica, momentum, reversão, gerenciamento de risco ou sinal combinado.

## Estratégias

1. **RSI sobrevendido + reversão**: Compra quando RSI < 30 e preço começa a subir acima de suporte.
2. **RSI sobrecomprado + pullback**: Venda/short quando RSI > 70 após candle de rejeição.
3. **Cruzar Médias Móveis (MA): Golden Cross**: Compra quando MA curta cruza MA longa para cima.
4. **Cruzar Médias Móveis: Death Cross**: Venda quando MA curta cruza MA longa para baixo.
5. **Suporte e resistência**: Compra próxima a suporte e vende próxima a resistência.
6. **Breakout de canal**: Compra no rompimento acima da zona de congestionamento com volume alto.
7. **Breakdown de canal**: Venda no rompimento abaixo da zona de congestionamento.
8. **Bollinger Bands squeeze**: Entrada após compressão das bandas e expansão do preço.
9. **Bollinger Bands reversão**: Reversão de preço ao tocar a banda superior ou inferior.
10. **MACD crossover**: Compra quando linha MACD cruza acima da sinal.
11. **MACD divergência**: Compra/venda quando preço e MACD divergem.
12. **ADX tendência forte**: Operar na direção da tendência quando ADX > 25.
13. **ADX tendência fraca**: Evitar trades ou buscar range quando ADX < 20.
14. **Momentum de volume**: Compra em rompimento acompanhado de aumento de volume.
15. **Volume divergente**: Sinal de fraqueza quando preço sobe e volume diminui.
16. **Estocástico sobrevendido**: Compra quando estocástico cruza abaixo de 20 e vira para cima.
17. **Estocástico sobrecomprado**: Venda quando estocástico cruza acima de 80 e vira para baixo.
18. **Candle engolfo bullish**: Entrada de compra após padrão de candle engolfo de alta.
19. **Candle engolfo bearish**: Entrada de venda após padrão de candle engolfo de baixa.
20. **Martelo e martelo invertido**: Reversão de alta em fundo após martelo de alta.
21. **Estrela cadente**: Reversão de baixa após estrela cadente em topo.
22. **Fibonacci retração**: Compra em retração de 38-61,8% dentro de tendência de alta.
23. **Fibonacci extensão**: Definir alvo em 127,2% ou 161,8% após rompimento.
24. **Pivôs diários**: Operar posições próximas ao pivot point com S1/R1.
25. **Canal de regressão linear**: Compra no limite inferior em tendência de alta.
26. **Price action inside bar**: Rompimento de candle interno com gestão de risco clara.
27. **Price action pin bar**: Reversão após candle pin bar em suporte/resistência.
28. **Volume Profile high node**: Evitar trades na área de valor alto, buscar rompimento.
29. **Volume Profile low node**: Entrada em baixa liquidez com expectativa de reversão.
30. **Sentimento de mercado**: Ajuste de trades quando notícias programadas influenciam o par.
31. **Pullback à média móvel**: Compra no preço recuando para a EMA em tendência de alta.
32. **Retest de rompimento**: Entrada após primeiro retorno ao nível rompido.
33. **Trade de gap**: Fechar gaps no início de sessão com suporte/resistência.
34. **Trade de notícia**: Operar com menos alavancagem perto de eventos macro.
35. **Multi-timeframe confirmação**: Confirmação de tendência em timeframe maior antes de abrir trade.
36. **Hedge parcial**: Abrir posição contrária menor para reduzir risco em momentos voláteis.
37. **Scalping range**: Múltiplos trades curtos dentro de faixa bem definida.
38. **Swing trade em canal**: Compra na base do canal e venda no topo.
39. **Trend following com EMA 21/55**: Compra se preço acima de EMA21 e EMA55 ascendente.
40. **Trend following com EMA 8/21**: Uso em timeframes curtos para entradas rápidas.
41. **Padrão de triângulo**: Compra no rompimento de triângulo ascendente.
42. **Padrão de bandeira**: Compra após rompimento de bandeira em tendência de alta.
43. **Padrão de flâmula**: Compra no rompimento após período de consolidação.
44. **Padrão cabeça e ombros invertido**: Compra após quebra da linha de pescoço.
45. **Padrão cabeça e ombros**: Venda após quebra da linha de pescoço de topo.
46. **Trade com paridade correlacionada**: Ajustar exposição quando dois pares correlacionados divergem.
47. **Trade de volatilidade baixa**: Evitar trades ou usar estratégias de breakout mais conservadoras.
48. **Trade de volatilidade alta**: Reduzir tamanho e ampliar stops.
49. **Segue a tendência com Supertrend**: Compra quando Supertrend vira para alta.
50. **Venda com Supertrend**: Venda quando Supertrend indica baixa.
51. **Cluster de candles de indecisão**: Evitar posição até confirmação de rompimento.
52. **Volume on Balance (OBV)**: Confirmação de tendência pela linha OBV.
53. **On Balance Volume divergência**: Sinal de reversão se OBV diverge do preço.
54. **Commodity Channel Index (CCI)**: Compra quando CCI < -100 e vira para cima.
55. **CCI sobrecompra**: Venda quando CCI > 100 e desce.
56. **Linha de tendência dinâmica**: Ajustar stop trailing conforme linha de tendência valida.
57. **Keltner Channel breakout**: Compra no rompimento superior do canal.
58. **Keltner Channel fade**: Venda ao tocar faixa externa em tendência lateral.
59. **Ichimoku baselines**: Compra quando preço acima de nuvem e conversão cruza acima de base.
60. **Ichimoku sell setup**: Venda se preço abaixo da nuvem e sem suporte de Kijun.
61. **Padrão de reversão de três corvos**: Venda em topo após três candles de baixa.
62. **Padrão de trinca de brancos**: Compra após três candles de alta consecutiva.
63. **Trade com SAR parabólico**: Uso de SAR como stop móvel em tendências claras.
64. **Trade de média arqueada**: Uso de arco de 20/50 EMAs para entradas em tendência.
65. **Trade de confluência**: Combinar suporte/resistência, RSI e volume antes de entrar.
66. **Estratégia de telhado e chão**: Venda em topo históricos, compra em fundo histórico.
67. **Estratégia de reversão de 50%**: Busca recuo de 50% de movimento recente.
68. **Estratégia de escala de posição**: Entrar em partes conforme o preço confirma a tendência.
69. **Trade de breakout falso**: Venda quando rompimento falha e preço volta ao range.
70. **Transferência de risco parcial**: Ajustar posição usando ordem limite para saída parcial.
71. **Estratégia de tapering**: Diminuir exposição progressivamente com ganho.
72. **Estratégia de capitalização**: Aumentar posição apenas após confirmação de lucro consistente.
73. **Estratégia de tendência com MACD e RSI**: Compra com MACD em alta e RSI ainda abaixo de 70.
74. **Estratégia de convergência média móvel**: Compra se EMA longa e curta estão alinhadas e separadas.
75. **Estratégia de reversão ao VWAP**: Compra quando o preço recua ao VWAP em sessão de alta.
76. **Estratégia de rompimento diário**: Compra se preço romper máximo diário com volume acima da média.
77. **Estratégia de rompimento semanal**: Uso em timeframe maior para entradas mais robustas.
78. **Estratégia de faixa com RSI**: Compra em zonas de suporte se RSI estiver abaixo de 40.
79. **Estratégia de tendência com canal de Donchian**: Compra no rompimento superior de canal de 20 períodos.
80. **Estratégia de reversão com Bandas de Donchian**: Venda no rompimento inferior após topo ou fundo.
81. **Estratégia de Fibonacci cluster**: Usa múltiplos níveis de Fibonacci e pivôs para entrada.
82. **Estratégia de múltiplos indicadores**: Entrada apenas se 3 indicadores concordarem.
83. **Estratégia de hedge inverso**: Abre posição contrária menor após grande oscilação para equilibrar risco.
84. **Estratégia de stop mental**: Usa níveis fixos em vez de stops de mercado em day trade.
85. **Estratégia de posição única**: Focar em um único trade de alta convicção por vez.
86. **Estratégia de gestão de perdas**: Stop apertado e busca lucro de pelo menos 1,5x risco.
87. **Estratégia de relação risco/retorno**: Apenas trades com RR mínimo 1:2.
88. **Estratégia de correlação cruzada**: Ajusta exposição quando USD contra EUR e USD contra JPY divergem.
89. **Estratégia de volatilidade implícita**: Evita entradas antes de grandes releases de volatilidade.
90. **Estratégia de momentum diário**: Compra se fechamento diário está acima de abertura e volume crescente.
91. **Estratégia de retorno médio**: Reversão em preços muito afastados da média de 20 dias.
92. **Estratégia de risco reduzido**: Negocia apenas 5% do capital em períodos de incerteza.
93. **Estratégia de alavancagem controlada**: Ajusta tamanho pelo drawdown histórico do agente.
94. **Estratégia de treino com dados passados**: Prioriza sinais que geraram lucros em backtests.
95. **Estratégia de sinal de consenso**: Usa maioria de sinais em múltiplos ativos correlacionados.
96. **Estratégia de reentrada em tendência**: Reabre posição após reversão breve, se o sinal original permanece válido.
97. **Estratégia de trailing stop adaptativo**: Move stop conforme ATR e volatilidade.
98. **Estratégia de fechamento parcial**: Fecha metade da posição quando atinge o primeiro alvo.
99. **Estratégia de capitalização de lucros**: Move stop para breakeven após metade do alvo alcançado.
100. **Estratégia de revisão contínua**: Avalia e registra trades vencedores para ajustar regras de entrada e sair.

## Observações
- Esta biblioteca deve ser utilizada como referência e não como recomendação automática irrestrita.
- Os agentes podem combinar regras de várias estratégias para formar um conjunto de critérios de entrada e saída.
- O sucesso melhora quando as regras são adaptadas ao ativo e ao timeframe.
