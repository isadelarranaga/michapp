import streamlit as st
from pymongo import MongoClient
import boto3
import tempfile
#from st_files_connection import FilesConnection

def update_sections(pill_value):
    if pill_value == 1 and st.session_state.num_sections < 4:
        st.session_state.num_sections += 1
    elif pill_value == 0 and st.session_state.num_sections > 0:
        st.session_state.num_sections -= 1
    
    # Force clear the pill selection after use
    st.session_state.pill_key = None
    st.rerun()

def uploadImageToS3(file, bucket, s3_file):
    aws_creds = st.secrets["aws_credentials"]
    s3 = boto3.client(service_name="s3", 
                      region_name=aws_creds['AWS_DEFAULT_REGION'],
                      aws_access_key_id=aws_creds['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=aws_creds['AWS_SECRET_ACCESS_KEY'])
    
    try:
        s3.upload_file(file, bucket, s3_file)
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        st.error('File not found.')
        return False  
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        return False

# MongoDB connection details
# MONGO_URI = "mongodb://localhost:27017"
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

c1, c2 = st.columns(2)

with c1:
    c1.subheader("Comprobante")
    c1.uploaded_comprobante = c1.file_uploader("Select an image as a comprobante", key="up_comprobante", type = (["jpg", "jpeg", "png"]))

            
    if c1.uploaded_comprobante is not None:

        st.write(c1.uploaded_comprobante.name)
        
        if c1.uploaded_comprobante.type not in ["image/jpeg", "image/jpg", "image/png"]:
            c1.error('Only images are supported. Please upload a different file')
        else:
            c1.success(c1.uploaded_comprobante.name + ' Selected')
            bytes_data = c1.uploaded_comprobante.getvalue()
                

with c2:
    c2.subheader("Factura")
    c2.uploaded_factura = c2.file_uploader("Select an image as a factura", key="up_factura", type = (["jpg", "jpeg", "png"]))

            
    if c2.uploaded_factura is not None:

        st.write(c2.uploaded_comprobante.name)
        
        if c2.uploaded_comprobante.type not in ["image/jpeg", "image/jpg", "image/png"]:
            c2.error('Only images are supported. Please upload a different file')
        else:
            c2.success(c2.uploaded_comprobante.name + ' Selected')
            bytes_data = c2.uploaded_comprobante.getvalue()
            # if c2.button('Upload image'):
            #     with st.spinner('Uploading...'):
            #         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            #             temp_file.write(c2.uploaded_comprobante.getvalue())
            #             temp_file_path = temp_file.name

            #         path_s3 = f'images-michapp'
            #         uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_comprobante.name}')
            #         st.success(f'test-test-test-test-dd/{path_s3}/{c2.uploaded_comprobante.name}')
            #         s3_url2 = f'test-test-test-test-dd/{path_s3}/{c2.uploaded_comprobante.name}'
                

# Inluir más de un ticket 
st.header('Incluye más compras')

# Empezar con cero secciones
if 'num_sections' not in st.session_state:
    st.session_state.num_sections = 0  


if 'pill_selection' not in st.session_state:
    st.session_state.pill_selection = None

# Options for pill section
option_map = {
    0: "\-",
    1: "\+",
}

pill_selection = st.pills(
    'Máximo 4 compras más', 
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
    key="section_pills"
)

# Process the pill selection
if pill_selection != st.session_state.pill_selection:
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
if finalizar:
    if not (name and last_name and monto_cero and descripcion_cero):
        st.error("Please be sure to enter information in all the necessary fields")
    else:
        if c1.uploaded_comprobante is not None and c2.uploaded_factura is not None:
            with st.spinner('Uploading comprobante to s3...'):
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(c1.uploaded_comprobante.getvalue())
                            temp_file_path = temp_file.name

                        path_s3 = f'images-michapp'
                        uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_comprobante.name}')
                        st.success(f'test-test-test-test-dd/{path_s3}/{c1.uploaded_comprobante.name}')
                        s3_url = f'test-test-test-test-dd/{path_s3}/{c1.uploaded_comprobante.name}'
            with st.spinner('Uploading...'):
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(c2.uploaded_factura.getvalue())
                        temp_file_path = temp_file.name

                    path_s3 = f'images-michapp'
                    uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_factura.name}')
                    st.success(f'test-test-test-test-dd/{path_s3}/{c2.uploaded_factura.name}')
                    s3_url2 = f'test-test-test-test-dd/{path_s3}/{c2.uploaded_factura.name}'
            
            data = {
            "name": name,
            "last name": last_name,
            "monto": monto_cero,
            "descripcion": descripcion_cero,
            "urlcomp": s3_url,
            "urlfact": s3_url2
            }
            all_fields_filled = True 
        elif c1.uploaded_comprobante is not None and c2.uploaded_factura is None:
            with st.spinner('Uploading comprobante to s3...'):
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(c1.uploaded_comprobante.getvalue())
                            temp_file_path = temp_file.name

                        path_s3 = f'images-michapp'
                        uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_comprobante.name}')
                        st.success(f'test-test-test-test-dd/{path_s3}/{c1.uploaded_comprobante.name}')
                        s3_url = f'test-test-test-test-dd/{path_s3}/{c1.uploaded_comprobante.name}'
            
            data = {
            "name": name,
            "last name": last_name,
            "monto": monto_cero,
            "descripcion": descripcion_cero,
            "urlcomp": s3_url
            }

            all_fields_filled = True

        elif c2.uploaded_factura is not None and c1.uploaded_comprobante is None:
            with st.spinner('Uploading...'):
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(c2.uploaded_factura.getvalue())
                        temp_file_path = temp_file.name

                    path_s3 = f'images-michapp'
                    uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_factura.name}')
                    st.success(f'test-test-test-test-dd/{path_s3}/{c2.uploaded_factura.name}')
                    s3_url2 = f'test-test-test-test-dd/{path_s3}/{c2.uploaded_factura.name}'

            data = {
            "name": name,
            "last name": last_name,
            "monto": monto_cero,
            "descripcion": descripcion_cero,
            "urlfact": s3_url2
            }
            all_fields_filled = True
        else:
            st.error('Please select at least one image as factura or comprobante')


        if st.session_state.num_sections > 0:
            for i in range(st.session_state.num_sections):
                if monto[i] and descripcion[i]: 
                    data[f"monto_{i+1}"] = monto[i]
                    data[f"descripcion_{i+1}"] = descripcion[i]
                    
                else:
                    st.error(f"Please fill out both 'Monto' and 'Descripcion' for section {i+1}")
                    all_fields_filled = False  

        if all_fields_filled:
            collection.insert_one(data)
            st.success('Data inserted successfully!')