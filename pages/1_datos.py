import streamlit as st
from pymongo import MongoClient

def update_sections(pill_value):
    if pill_value == 1 and st.session_state.num_sections < 4:
        st.session_state.num_sections += 1
    elif pill_value == 0 and st.session_state.num_sections > 0:
        st.session_state.num_sections -= 1
    
    # Force clear the pill selection after use
    st.session_state.pill_key = None
    st.rerun()

# MongoDB connection details
#MONGO_URI = "mongodb://localhost:27017"
# "mongodb:// mongodb:27017" is used for networks
MONGO_URI = "mongodb://mongodb:27017/"
DB_NAME = "mydatabase"  
COLLECTION_NAME = "mycollection"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


st.title("Solicitud de reembolso")

# Datos personales
st.header("1. Introduce tus datos")
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Nombre", "")

with col2:
    last_name = st.text_input("Primer apellido", "")

# Datos de la compra
st.header("2. Introduce los datos de tu compra")
monto_cero = st.number_input(label='Monto',step=1.,format="%.2f")
descripcion_cero = st.text_area("Descripción", height = 136)

col3, col4 = st.columns(2)

with col3:
    if st.button("Comprobante"):
        uploaded_files_comp = st.file_uploader('Carga tu comprobante', accept_multiple_files=True)

with col4:
    if st.button("Factura"):
        uploaded_files_fac = st.file_uploader('Carga tu factura', accept_multiple_files=True)

# Inluir más de un ticket
st.header('Incluye más compras')

if 'num_sections' not in st.session_state:
    st.session_state.num_sections = 0  # Start with zero sections


# Track the pill selection in session state
if 'pill_selection' not in st.session_state:
    st.session_state.pill_selection = None

# Define the pill options
option_map = {
    0: "\-",
    1: "\+",
}

# Create the pill component
pill_selection = st.pills(
    'Máximo 4 compras más', 
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
    key="section_pills"
)

# Process the pill selection
if pill_selection is not None and pill_selection != st.session_state.pill_selection:
    st.session_state.pill_selection = pill_selection
    update_sections(pill_selection)

# Display the input fields for each section
monto = []
descripcion = {}
for i in range(st.session_state.num_sections):
    st.subheader(f"Compra {i+1}")
    monto.append(st.number_input(label=f'Monto {i+1}', step=1., format="%.2f", key=f'monto_{i}'))
    descripcion[i] = st.text_area(f"Descripción {i+1}", height=136, key=f'descripcion_{i}')

    col5, col6 = st.columns(2)
    with col5:
        if st.button(f"Comprobante {i+1}"):
            uploaded_files_comp = st.file_uploader('Carga tu comprobante', accept_multiple_files=True,  key=f'comprobante_uploader_{i}')

    with col6:
        if st.button(f"Factura {i+1}"):
            uploaded_files_comp = st.file_uploader('Carga tu factura', accept_multiple_files=True, key=f'factura_uploader_{i}')


finalizar = st.button("Finalizar")
if finalizar and st.session_state.num_sections == 0:
        if name and last_name and monto_cero and descripcion_cero:
            data = {
                "name": name, 
                "last name": last_name,
                "monto": monto_cero,
                "descripcion": descripcion_cero
                    }
            collection.insert_one(data)
            st.success('Data inserted successfully!')
            st.success(data)
        else: 
            st.error("Please be sure to enter information in all the necessary fields")
elif finalizar and st.session_state.num_sections > 0:
    if name and last_name and monto_cero and descripcion_cero:
        data = {
            "name": name, 
            "last name": last_name,
            "monto": monto_cero,
            "descripcion": descripcion_cero,
        }
        
        # Add all additional sections to the data dictionary
        for i in range(st.session_state.num_sections):
            data[f"monto_{i+1}"] = monto[i]
            data[f"descripcion_{i+1}"] = descripcion[i]
            
        collection.insert_one(data)
        st.success('Data inserted successfully!')
    else: 
        st.error("Please be sure to enter information in all the necessary fields")