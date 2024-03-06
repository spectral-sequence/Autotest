import streamlit as st
from openai_integration import query_openai_assistant  # Ensure this module is set up to interact with OpenAI API

# Function to interact with an assistant to load historical data
def load_historical_data(assistant_id, openai_api_key):
    try:
        historical_data = query_openai_assistant(assistant_id, "load historical data", openai_api_key)
        
        if historical_data is None or not historical_data:
            st.error("No historical data received. Please check the assistant or the query.")
            return None
        return historical_data
    except Exception as e:
        st.error(f"An error occurred while loading historical data: {e}")
        return None

# Function to interact with an assistant to generate strategies
def generate_strategy(assistant_id, openai_api_key):
    try:
        strategy = query_openai_assistant(assistant_id, "generate strategy", openai_api_key)
        
        if not strategy:
            st.error("Failed to generate a strategy. Please try again.")
            return None
        return strategy
    except Exception as e:
        st.error(f"An error occurred while generating the strategy: {e}")
        return None

# Function to interact with an assistant for backtesting and return results
def backtest_strategy(assistant_id, strategy, openai_api_key):
    try:
        results = query_openai_assistant(assistant_id, f"backtest {strategy}", openai_api_key)
        
        if results is None or 'error' in results:
            st.error("Error during backtesting. Please review the strategy and try again.")
            return None
        return results
    except Exception as e:
        st.error(f"An error occurred during backtesting: {e}")
        return None

# Assuming you have setup to securely fetch your OpenAI API Key
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title('Autotest Strategy Analysis')

# Load and display historical data
historical_data = load_historical_data('assistant_id_for_data', openai_api_key)
if historical_data:
    st.write("Historical Data:")
    st.dataframe(historical_data)

# Generate and display strategy
strategy = generate_strategy('assistant_id_for_strategy', openai_api_key)
if strategy:
    st.write("Generated Strategy:")
    st.text(strategy)

# Backtest and display results
backtest_results = backtest_strategy('assistant_id_for_backtesting', strategy, openai_api_key)
if backtest_results:
    st.write("Backtesting Results:")
    st.text(backtest_results['text'])  # Assuming the result is a dictionary with text and possibly other data
    # Consider adding a condition to check if 'plot' is in the results for displaying a plot, if applicable
