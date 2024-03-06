import os
from dotenv import load_dotenv
import pandas as pd
from backtesting import Backtest
from strategy import MyStrategy  # Assume this is your custom strategy class
from openai_integration import query_openai_assistant, parse_strategy_params

load_dotenv()  # Load environment variables from .env file

def get_assistant_responses(assistant_id, prompt, api_key, xml_config):
    response = query_openai_assistant(assistant_id, prompt, api_key, xml_config)
    if not response:
        raise ValueError(f"No valid response received from assistant {assistant_id}")
    return response

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

    xml_file_path = 'config/cr-agent-xml-assistant-v0.2.xml'
    
    # Initialize IDs for different assistants
    data_selector_id, strategy_agent_id, backtest_agent_id, analysis_agent_id = "id-data", "id-strategy", "id-backtest", "id-analysis"
    
    # Data Selection Assistant
    data_prompt = "Provide the file name of the most suitable market data for today's trading strategy."
    selected_file = get_assistant_responses(data_selector_id, data_prompt, openai_api_key, xml_file_path)
    data = pd.read_csv(f'data/{selected_file}.csv', index_col='Date', parse_dates=True)

    # Strategy Formulation Assistant
    strategy_prompt = "Suggest optimal parameters for the trading strategy considering the current market data."
    strategy_parameters_json = get_assistant_responses(strategy_agent_id, strategy_prompt, openai_api_key, xml_file_path)
    strategy_params = parse_strategy_params(strategy_parameters_json)  # Converts JSON response to Python dict

    # Backtesting with suggested parameters
    bt = Backtest(data, MyStrategy, cash=10_000, commission=.002, **strategy_params)
    stats = bt.run()

    # Backtest Analysis Assistant
    backtest_results_prompt = "Analyze the following backtest statistics and provide insights or improvements."
    backtest_insights = get_assistant_responses(backtest_agent_id, backtest_results_prompt, openai_api_key, xml_file_path)

    print(f"Backtest Insights: {backtest_insights}")

    # Overall Strategy Analysis Assistant
    overall_analysis_prompt = "Evaluate the trading strategy performance and suggest future actions or optimizations."
    strategy_overview = get_assistant_responses(analysis_agent_id, overall_analysis_prompt, openai_api_key, xml_file_path)

    print(f"Strategy Overview: {strategy_overview}")

if __name__ == "__main__":
    main()
