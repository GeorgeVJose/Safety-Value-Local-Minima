import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.signal import find_peaks


@st.cache_data
def read_data(input_file):
    df = pd.read_csv(input_file)
    return df


@st.cache_data
def process_data(df, safety_thresh):
    df = df[df['ACT'] < safety_thresh]
    peaks, _ = find_peaks(df['ACT']*-1)
    df_peaks = df.iloc[peaks]
    return df_peaks


st.set_page_config(page_title='Safety Analysis',
                   layout='wide', initial_sidebar_state='auto')

uploaded_file = st.sidebar.file_uploader('Upload CSV File', type=['csv'])
st.sidebar.title('Parameters')
st.sidebar.write('---')
saftey_thresh = st.sidebar.slider('Safety Value Threshold', 0, 15, 2, 1)

st.title('Safety Analysis')
st.write('---')

if uploaded_file is not None:
    df = read_data(uploaded_file)
    vehicle_id = st.selectbox(
        "Select vehicle ID", df['VehicleID'].unique())
    st.header(vehicle_id)

    df_vehicle = df[df['VehicleID'] == vehicle_id]
    df_vehicle = df_vehicle[df_vehicle['ACT'] < saftey_thresh]

    df_peaks = process_data(df, saftey_thresh)

    df_peaks_vehicle = df_peaks[df_peaks['VehicleID'] == vehicle_id]

    fig = px.line(df_vehicle, x='Time', y='ACT', title='Time v/s ACT')
    fig.add_scatter(
        x=df_peaks_vehicle['Time'],
        y=df_peaks_vehicle['ACT'],
        mode='markers',
        name='Minima Point',
        marker_color='red',
        marker_size=10
    )

    fig.update_xaxes(mirror=True, showline=True, linecolor='black')
    fig.update_yaxes(mirror=True, showline=True, linecolor='black')

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write(df_peaks_vehicle)

    st.header('Final Minima Data')
    st.write(df_peaks)
    st.download_button(
        'Download Minima Data',
        df_peaks.to_csv(index=False).encode('utf-8'),
        file_name='minima_data.csv',
        mime='text/csv'
    )
