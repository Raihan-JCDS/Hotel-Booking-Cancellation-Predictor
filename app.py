import streamlit as st
import pandas as pd
from joblib import load

# Load data
cleaned_df = pd.read_csv('cleaned_data.csv', dtype={'country': str, 'market_segment': str, 'deposit_type': str, 'customer_type': str, 'reserved_room_type': str})

# Set page title and favicon
st.set_page_config(page_title="Hotel Booking Cancellation Predictor", page_icon=":hotel:")

# Main title and description
st.title('Hotel Booking Cancellation Predictor')
st.markdown("Welcome to the Hotel Booking Cancellation Predictor app! Use the sidebar to input customer's features and get predictions.")

# Sidebar for user input
st.sidebar.header("Please input customer's features")

def user_input_feature():
    # Dropdown menus for categorical input fields
    country = st.sidebar.selectbox('Country of Origin', cleaned_df['country'].unique())
    market_segment = st.sidebar.selectbox('Market Segment', cleaned_df['market_segment'].unique())
    deposit_type = st.sidebar.selectbox('Deposit Type', cleaned_df['deposit_type'].unique())
    customer_type = st.sidebar.selectbox('Customer Type', cleaned_df['customer_type'].unique())
    reserved_room_type = st.sidebar.selectbox('Reserved Room Type', cleaned_df['reserved_room_type'].unique())

    # Number inputs
    previous_cancellations = st.sidebar.number_input('Previous Cancellations', min_value=0)
    booking_changes = st.sidebar.number_input('Booking Changes', min_value=0)
    days_in_waiting_list = st.sidebar.number_input('Days in Waiting List', min_value=0)
    required_car_parking_spaces = st.sidebar.number_input('Required Car Parking Spaces', min_value=0)
    total_of_special_requests = st.sidebar.number_input('Total Special Requests', min_value=0)

    # Create dataframe
    df = pd.DataFrame({
        'country': [country],
        'market_segment': [market_segment],
        'deposit_type': [deposit_type],
        'customer_type': [customer_type],
        'reserved_room_type': [reserved_room_type],
        'previous_cancellations': [previous_cancellations],
        'booking_changes': [booking_changes],
        'days_in_waiting_list': [days_in_waiting_list],
        'required_car_parking_spaces': [required_car_parking_spaces],
        'total_of_special_requests': [total_of_special_requests]
    })

    return df

# Get user input
df_customer = user_input_feature()
df_customer.index = ['value']

# Load model
model_loaded = load('model.joblib')

# Make prediction
kelas = model_loaded.predict(df_customer)

# Show prediction
st.write("## Prediction")
if kelas == 1:
    st.success('Class 1: This customer will **CANCEL**')
else:
    st.success('Class 0: This customer will **NOT CANCEL**')

# Display customer features
st.write("## Customer Features")
st.table(df_customer.transpose())
