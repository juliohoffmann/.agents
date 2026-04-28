from src.agents.trading_agent import TradingAgent
from src.agents.super_agent import SuperAgent
from src.data.data_fetcher import DataFetcher
from src.core.indicators import add_indicators
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger("VerdentSimulator")

class VerdentSimulator:
    def __init__(self, include_super_agent=True):
        self.fetcher = DataFetcher()
        self.agents  = [
            TradingAgent(i, Config.INITIAL_BALANCE)
            for i in range(Config.NUM_AGENTS)
        ]
        if include_super_agent and Config.ENABLE_SUPER_AGENT:
            self.agents.append(SuperAgent(Config.INITIAL_BALANCE))

    def run(self):
        logger.info("Buscando dados de mercado...")
        df = self.fetcher.fetch(limit=Config.NUM_TRADES)
        df = add_indicators(df)
        logger.info(f"{len(df)} candles carregados. Iniciando simulação...")

        for _, row in df.iterrows():
            price = row["close"]
            for agent in self.agents:
                action = agent.decide(row)
                agent.execute(action, price)

        results = [a.summary() for a in self.agents]
        self._print_results(results)
        return results

    def _print_results(self, results):
        print("\n" + "="*60)
        print("RESULTADO DA SIMULAÇÃO")
        print("="*60)
        for r in sorted(results, key=lambda x: x["total_profit"], reverse=True):
            tag = "[SUPER]" if r["agent_id"] == 999 else f"[Agente {r['agent_id']}]"
            print(
                f"{tag} | Lucro: {r['total_profit']:+.2f} USDT "
                f"| Win Rate: {r['win_rate']:.1%} "
                f"| Trades: {r['total_trades']}"
            )
        print("="*60)