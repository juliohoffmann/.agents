# Verdent Trading Agent Simulator

Projeto de simulação de agentes de trading em pares de moedas com aprendizado a partir de trades vencedores.

## Arquivos
- `verdent.py`: implementa `TradingAgent`, `AgentManager` e `VerdentSimulator`
- `requirements.txt`: dependências do Python
- `verdent_logs.txt`: arquivo de logs gerado durante a simulação

## Instalação
```bash
pip install -r requirements.txt
```

> Se quiser usar o `TA-Lib` nativo, instale-o separadamente via conda ou wheel, mas este projeto usa a biblioteca `ta` para indicadores técnicos.

## Execução do simulador standalone
```bash
python verdent.py
```

## Execução do aplicativo frontend/backend
```bash
python app.py
```

Abra o navegador em `http://127.0.0.1:8000`.

## Configuração com .env
- Copie ou edite o arquivo `.env` em `c:\Users\julio\.agents\.env`
- Preencha `BINANCE_API_KEY` e `BINANCE_API_SECRET`
- Ajuste `USE_BINANCE=true` para usar dados reais
- Opcionalmente altere `BINANCE_SYMBOL`, `BINANCE_INTERVAL`, `NUM_AGENTS` e `NUM_TRADES`
- Opcional: defina `BINANCE_API_BASE` para usar um endpoint diferente da API Binance Spot padrão

Use símbolos no formato Binance, por exemplo `EURUSDT`, `BTCUSDT` ou `ETHUSDT`.

Para conectar sua conta Binance:
- habilite dados da Binance no app
- informe sua `API Key` e `API Secret`
- clique em "Testar Binance" para validar a conexão
- o app retornará saldos reais e uma estimativa total em USDT

Para o modo real futuro:
- marque "Habilitar modo real (futuro)"
- atualmente os agentes ainda executam simulação com dados reais ou simulados
- no futuro, esse modo poderá ser usado para enviar ordens reais à sua conta Binance

Super Agente:
- marque "Incluir Super Agente" para que um agente evolua sua estratégia a partir dos acertos
- ele ajusta parâmetros com base em trades vencedores e tenta criar uma nova estratégia mais precisa

O frontend permite configurar a Binance API, salvar sua configuração localmente, testar a conexão e ver o desempenho dos agentes. Os logs aparecem em `verdent_logs.txt`.
