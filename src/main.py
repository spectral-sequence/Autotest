import os
from dotenv import load_dotenv
import pandas as pd
from backtesting import Backtest
from strategy import PriceActionStrategy
from openai_integration import query_openai_assistant

load_dotenv()  # Load environment variables from .env file

def select_market_data(data_selector_id, openai_api_key):
    recommendation_prompt = "Recommend which market data file to use based on current market trends."
    recommended_data = query_openai_assistant(data_selector_id, recommendation_prompt, openai_api_key)
    if recommended_data and isinstance(recommended_data, str):
        return recommended_data.strip()
    else:
        raise ValueError("Invalid data recommendation received.")

def validate_assistant_output(output):
    if not output or not isinstance(output, dict):
        return False
    return True

def optimize_strategy(data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key):
    current_params = {'bb_window': 20, 'bb_std_num': 2}
    best_sharpe = float('-inf')
    iteration = 0
    max_iterations = 100

    while best_sharpe < 5 and iteration < max_iterations:
        strategy_params = query_openai_assistant(strategy_agent_id, current_params, openai_api_key)
        if validate_assistant_output(strategy_params):
            current_params.update(strategy_params)

        bt = Backtest(data, PriceActionStrategy, cash=10000, commission=.002, **current_params)
        stats = bt.run()

        backtest_metrics = query_openai_assistant(backtest_agent_id, stats, openai_api_key)
        analysis_feedback = query_openai_assistant(analysis_agent_id, backtest_metrics, openai_api_key)

        sharpe_ratio = stats['Sharpe Ratio']
        if sharpe_ratio > best_sharpe:
            best_sharpe = sharpe_ratio

        iteration += 1

    return current_params, best_sharpe

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

    data_selector_id, strategy_agent_id, backtest_agent_id, analysis_agent_id = "id0", "id1", "id2", "id3"
    selected_data = select_market_data(data_selector_id, openai_api_key)
    data = pd.read_csv(f'data/{selected_data}.csv', index_col='Date', parse_dates=True)

    optimized_params, best_sharpe = optimize_strategy(data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key)
    
    print(f"Optimized Parameters: {optimized_params}")
    print(f"Best Sharpe Ratio Achieved: {best_sharpe}")

if __name__ == "__main__":
    main()
