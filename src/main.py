import os
from dotenv import load_dotenv
import pandas as pd
from backtesting import Backtest
from strategy import PriceActionStrategy
from openai_integration import query_openai_assistant

load_dotenv()  # Load environment variables from .env file

def optimize_strategy(data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key):
    current_params = {'bb_window': 20, 'bb_std_num': 2}
    best_sharpe = float('-inf')
    iteration = 0
    max_iterations = 100

    while best_sharpe < 5 and iteration < max_iterations:
        strategy_params = query_openai_assistant(strategy_agent_id, current_params, openai_api_key)
        current_params.update(strategy_params)  # Assuming the assistant returns a dict

        bt = Backtest(data, PriceActionStrategy, cash=10000, commission=.002, **current_params)
        stats = bt.run()

        backtest_metrics = query_openai_assistant(backtest_agent_id, stats, openai_api_key)
        analysis_feedback = query_openai_assistant(analysis_agent_id, backtest_metrics, openai_api_key)

        # Logic to interpret analysis feedback and adjust current_params as needed

        sharpe_ratio = stats['Sharpe Ratio']
        if sharpe_ratio > best_sharpe:
            best_sharpe = sharpe_ratio

        iteration += 1

    return current_params, best_sharpe

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

    data = pd.read_csv('historical_data.csv', index_col='Date', parse_dates=True)
    strategy_agent_id, backtest_agent_id, analysis_agent_id = "id1", "id2", "id3"
    optimized_params, best_sharpe = optimize_strategy(
        data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key)

    print(f"Optimized Parameters: {optimized_params}")
    print(f"Best Sharpe Ratio Achieved: {best_sharpe}")

if __name__ == "__main__":
    main()
