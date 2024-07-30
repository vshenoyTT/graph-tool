import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Streamlit application to analyze Tenstorrent performance sheets
st.title('Tenstorrent Performance Graphs')
st.markdown("Create graphs")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# File uploader for excel or csv
uploaded_file = st.file_uploader("Upload an excel or csv performance sheet", type=["xlsx", "csv"])

if uploaded_file is not None:
    name = uploaded_file.name
    if ".xlsx" in name:
        df = pd.read_excel(uploaded_file)
    elif ".csv" in name:
        df = pd.read_csv(uploaded_file)

    # Calculate adjusted utilization for all on-device operations
    df['Adjusted Utilization'] = ((df['PM IDEAL [ns]'] / df['DEVICE KERNEL DURATION [ns]']) * (108 / df['CORE COUNT']) * 100)
    df['Adjusted Utilization'] = df['Adjusted Utilization'].replace([np.inf, -np.inf], np.nan).fillna(0)
    df['Adjusted Utilization'] = df['Adjusted Utilization'].astype(float)

    # Adding a global call count to represent operation number
    df['Operation Number'] = df.index + 1

    # Plotting the graphs
    # First graph: Bar chart of core count + Line graph of utilization
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.bar(df['Operation Number'], df['CORE COUNT'], color='b', alpha=0.6, label='Core Count')
    ax2.plot(df['Operation Number'], df['Adjusted Utilization'], color='r', label='Utilization')
    ax1.set_xlabel('Operation Number')
    ax1.set_ylabel('Core Count')
    ax2.set_ylabel('Utilization (%)')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    st.pyplot(fig1)
    '''
    # Second graph: Bar chart of device kernel duration + Line graph of utilization
    fig2, ax3 = plt.subplots()
    ax4 = ax3.twinx()
    ax3.bar(df['Operation Number'], df['DEVICE KERNEL DURATION [ns]'], color='g', alpha=0.6, label='Device Kernel Duration')
    ax4.plot(df['Operation Number'], df['Adjusted Utilization'], color='r', label='Utilization')
    ax3.set_xlabel('Operation Number')
    ax3.set_ylabel('Device Kernel Duration (ns)')
    ax4.set_ylabel('Utilization (%)')
    ax3.legend(loc='upper left')
    ax4.legend(loc='upper right')
    st.pyplot(fig2)

    # Third graph: Scatter plot of device duration vs. utilization
    fig3, ax5 = plt.subplots()
    ax5.scatter(df['DEVICE KERNEL DURATION [ns]'], df['Adjusted Utilization'], color='purple')
    ax5.set_xlabel('Device Kernel Duration (ns)')
    ax5.set_ylabel('Utilization (%)')
    st.pyplot(fig3)
    '''