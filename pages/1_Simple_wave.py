import streamlit as st
import time
import numpy as np
import plotly.graph_objs as go


st.set_page_config(page_title="Plotting interference", page_icon="⚡️")

st.markdown("# Simple Interference between carrier frequencies")
st.sidebar.header("Visualise frequencies")
st.write(
    """Channel 1 + Channel 2"""
)
s_to_p = st.number_input("Seconds", value=1)

freq1 = st.number_input("Channel 1 frequency", value=2000)
freq2 = st.number_input("Channel 2 frequency", value=2010)

x = np.arange(0, s_to_p, 1/10000)

y1 = np.sin(2 * np.pi * freq1 * x)
y2 = np.sin(2 * np.pi * freq2 * x)

i = y1 + y2

trace1 = go.Scatter(
    x=x,
    y=i,
    mode='lines',
)

trace_data = [trace1]
fig = go.Figure(data=trace_data)
fig.update_xaxes(rangeslider_visible=True)

st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")