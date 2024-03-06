import os
from dotenv import load_dotenv
import pandas as pd
from backtesting import Backtest
from strategy import PriceActionStrategy
from openai_integration import query_openai_assistant

load_dotenv()  # Load environment variables from .env file

def validate_assistant_output(output):
    return output and isinstance(output, dict)

def optimize_strategy(data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key, xml_file_path):
    current_params = {'bb_window': 20, 'bb_std_num': 2}
    best_sharpe = float('-inf')
    iteration = 0
    max_iterations = 100

    while best_sharpe < 5 and iteration < max_iterations:
        dynamic_prompt = parse_xml(xml_file_path) + " Current parameters: " + str(current_params)
        strategy_params = query_openai_assistant(strategy_agent_id, dynamic_prompt, openai_api_key)
        if validate_assistant_output(strategy_params):
            current_params.update(strategy_params)

        bt = Backtest(data, PriceActionStrategy, cash=10000, commission=.002, **current_params)
        stats = bt.run()

        if stats['Sharpe Ratio'] > best_sharpe:
            best_sharpe = stats['Sharpe Ratio']

        iteration += 1

    return current_params, best_sharpe

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

    xml_file_path = 'config/cr-agent-xml-assistant-v0.2.xml'
    data_selector_id, strategy_agent_id, backtest_agent_id, analysis_agent_id = "id0", "id1", "id2", "id3"
    
    selected_data = query_openai_assistant(data_selector_id, "Select market data based on trends", openai_api_key, xml_file_path)
    data = pd.read_csv(f'data/{selected_data}.csv', index_col='Date', parse_dates=True)
    optimized_params, best_sharpe = optimize_strategy(data, strategy_agent_id, backtest_agent_id, analysis_agent_id, openai_api_key, xml_file_path)
    
    print(f"Optimized Parameters: {optimized_params}")
    print(f"Best Sharpe Ratio Achieved: {best_sharpe}")

if __name__ == "__main__":
    main()
