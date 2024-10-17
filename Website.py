import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image


st.set_page_config(page_title="Airo Auto", page_icon=":tada:", layout="wide")
st.markdown('<h1 style="font-size: 50px;">Airo Auto</h1>', unsafe_allow_html=True)

#  Lottie animations
def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_coding = load_lottieurl(
    "https://lottie.host/19a10b2d-6de7-4a05-9c7a-bfe7ccfbad3e/v3V4DjqTTE.json"
)
st_lottie(lottie_coding, height=300, key="cargif")


st.markdown(
    "<h1 style='text-align: center; color: white;'>Comparison of Automobile Aerodynamics</h1>",
    unsafe_allow_html=True,
)

# Loading CSV
csv_file_path = 'table_data.csv'  
csv_data = pd.read_csv(csv_file_path)

# Display selected car data
def display_data(data, make, model, year, column):
    records = data[(data['Make'] == make) & 
                   (data['Model'] == model) & 
                   (data['Year'] == year)]
    column.write(records)


def get_cda_value(data, make, model, year):
    record = data[(data['Make'] == make) & 
                  (data['Model'] == model) & 
                  (data['Year'] == year)]
    return float(record['CdA'].values[0]) if not record.empty else None

# Function to draw aerodynamics diagram
def draw_aero_diagram(cda_value, column):
    fig, ax = plt.subplots()
    ax.axis([0, 20, 0, 20])
    plt.axis('off')

    # Car body
    ax.add_patch(Rectangle((7.5, 5), width=5, height=10, color="Green"))

    # Aerodynamics visualization
    if cda_value:
        ax.add_patch(Rectangle((8.75, 10 + cda_value * 0.1), width=2.5, height=4, color="Yellow"))
        ax.add_patch(Rectangle((9, 12.5 + cda_value * 0.14), width=2, height=1, color="Red"))

    # Wheels
    for x, y in [(6.5, 12.5), (6.5, 5.5), (12.5, 5.5), (12.5, 12.5)]:
        ax.add_patch(Rectangle((x, y), width=1, height=2, color="Black"))

    # Save and display diagram
    plt.savefig('aero_diagram.png')
    column.image(Image.open('aero_diagram.png'))

# Create two columns for vehicle comparisons
col1, col2 = st.columns(2)

# Vehicle 1 selection and visualization
with col1:
    st.subheader("Vehicle 1:")
    make1 = st.selectbox('Select a Make:', csv_data['Make'].unique(), key='make1')
    model1 = st.selectbox('Select a Model:', csv_data[csv_data['Make'] == make1]['Model'].unique(), key='model1')
    year1 = st.selectbox('Select a Year:', csv_data[(csv_data['Make'] == make1) & (csv_data['Model'] == model1)]['Year'].unique(), key='year1')

    if st.button('Show Data 1', key='show_data1'):
        display_data(csv_data, make1, model1, year1, col1)

    cda_value1 = get_cda_value(csv_data, make1, model1, year1)
    draw_aero_diagram(cda_value1, col1)

# Vehicle 2 selection and visualization
with col2:
    st.subheader("Vehicle 2:")
    make2 = st.selectbox('Select a Make:', csv_data['Make'].unique(), key='make2')
    model2 = st.selectbox('Select a Model:', csv_data[csv_data['Make'] == make2]['Model'].unique(), key='model2')
    year2 = st.selectbox('Select a Year:', csv_data[(csv_data['Make'] == make2) & (csv_data['Model'] == model2)]['Year'].unique(), key='year2')

    if st.button('Show Data 2', key='show_data2'):
        display_data(csv_data, make2, model2, year2, col2)

    cda_value2 = get_cda_value(csv_data, make2, model2, year2)
    draw_aero_diagram(cda_value2, col2)
