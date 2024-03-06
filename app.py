import streamlit as st
from your_module import generate_strategies, run_backtest, optimize_strategy

st.title('Autotest Strategy Dashboard')

if st.button('Generate Strategies'):
    strategies = generate_strategies()
    st.write(strategies)

if st.button('Run Backtest'):
    backtest_results = run_backtest(strategies)
    st.dataframe(backtest_results)

if st.button('Optimize Strategies'):
    optimized_strategies = optimize_strategy(backtest_results)
    st.write(optimized_strategies)

# Add more interactive widgets as needed to display data or control the processes
