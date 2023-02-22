import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.signal import find_peaks


@st.cache_data
def read_data(input_file):
    df = pd.read_csv(input_file)
    return df

st.set_page_config(page_title='Safety Analysis',layout='wide', initial_sidebar_state='auto')

excel_file = st.sidebar.file_uploader('Upload Excel File', type=['csv'])
st.sidebar.title('Parameters')
st.sidebar.write('---')
saftey_thresh = st.sidebar.slider('Safety Value Threshold', 0, 15, 2, 1)

st.title('Safety Analysis')
st.write('---')

if excel_file is not None:
    df = read_data(input_file=excel_file)

    vehicle_id = st.sidebar.selectbox("Select vehicle ID", df['VehicleID'].unique())
    df = df[df['VehicleID'] == vehicle_id]

    df = df[df['ACT'] < saftey_thresh]

    # for id_name, df_group in df.groupby('VehicleID'):
    st.subheader(vehicle_id)
    peaks, _ = find_peaks(df['ACT']*-1)

    peak_x = df['Time'].iloc[peaks]
    peak_y = df['ACT'].iloc[peaks]

    fig = px.line(df, x='Time', y='ACT', title='Time v/s ACT')
    fig.add_scatter(x=peak_x, y=peak_y, mode='markers', name='Minima Point', marker_color='red', marker_size=10)

    fig.update_xaxes(mirror=True, showline=True, linecolor='black')
    fig.update_yaxes(mirror=True, showline=True, linecolor='black')

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write(df.iloc[peaks])
        

    # for sheetname, df in data.items():
    #     # st.write('---')
    #     st.subheader(sheetname)
    #     df = df[df['Safety'] < saftey_thresh]

    #     peaks, _ = find_peaks(df['Safety']*-1)
        
    #     # Draw plot Time v/s Safety
    #     peak_x = df['Time'].iloc[peaks]
    #     peak_y = df['Safety'].iloc[peaks]
    #     fig = px.line(df, x='Time', y='Safety', title='Time v/s Safety')
    #     fig.add_scatter(x=peak_x, y=peak_y, mode='markers', name='Minima Point', marker_color='red', marker_size=10)
    #     # fig.update_layout(showlegend=False)
    #     fig.update_xaxes(mirror=True, showline=True, linecolor='black')
    #     fig.update_yaxes(mirror=True, showline=True, linecolor='black')

    #     col1, col2 = st.columns([3, 1])
    #     with col1:
    #         st.plotly_chart(fig, use_container_width=True)
    #     with col2:
    #             st.table({'Safety': peak_y.values, 'Time': peak_x.values})
