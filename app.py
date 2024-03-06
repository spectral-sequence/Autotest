import streamlit as st
from your_strategy_module import MyStrategy  # Import your strategy
from backtesting import Backtest

st.title('Strategy Optimization and Visualization')

# Load your historical data
historical_data = load_historical_data()

bt = Backtest(historical_data, MyStrategy)
result = bt.run()

# Display the plot
st.pyplot(result.plot())

# Display textual results
st.subheader('Backtesting Metrics')
for key, value in result._trade_data.items():
    st.text(f"{key}: {value}")

if st.button('Optimize Strategy'):
    # Define your parameter grid
    params = {'param1': range(1, 20), 'param2': range(10, 100)}
    opt_results = bt.optimize(**params)
    st.write(opt_results._trade_data)  # Adjust as per the actual results structure
