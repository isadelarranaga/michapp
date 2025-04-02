import streamlit as st
from pymongo import MongoClient
import sys
import os

MONGO_URI = "mongodb://mongodb:27017"
DB_NAME = "mydatabase"  
COLLECTION_NAME = "mycollection"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    st.title("Ver Datos de Reembolsos")

    #dos opciones: ver o filtrar los datos
    view_option = st.selectbox("Mostrar datos", ["Todos los registros", "Filtrar por nombre"])

    if view_option == "Todos los registros":
        documents = list(collection.find())

        if documents:
            for doc in documents:
                with st.container():
                    st.write(f"**Nombre:** {doc.get('name', 'N/A')}")
                    st.write(f"**Apellido** {doc.get('last name', 'N/A')}")
                    st.write(f"**Monto:** ${doc.get('monto', 'N/A')}")
                    st.write(f"**Descripción:** {doc.get('descripcion', 'N/A')}")
                    st.write(f"**Comprobante:** {doc.get('urlcomp', 'N/A')}")
                    st.write(f"**Factura:** {doc.get('urlfact', 'N/A')}")
                    
                    for i in range(1, 5):  
                        monto_key = f'monto_{i}'
                        desc_key = f'descripcion_{i}'
                        
                        if doc.get(monto_key, 'N/A') != 'N/A' and doc.get(desc_key, 'N/A') != 'N/A':
                            st.write(f"**Monto {i}:** ${doc.get(monto_key)}")
                            st.write(f"**Descripción {i}:** {doc.get(desc_key)}")
                
                st.divider()
        else:
            st.write("No hay registros almacenados.")

    else:
        search_name = st.text_input("Ingresa el nombre a buscar")

        if search_name:
            filtered_docs = list(collection.find({"name": search_name}))
            
            if filtered_docs:
                for doc in filtered_docs:
                    with st.container():
                        st.write(f"**Nombre:** {doc.get('name', 'N/A')} {doc.get('last_name', '')}")
                        st.write(f"**Monto:** ${doc.get('monto', 'N/A')}")
                        st.write(f"**Descripción:** {doc.get('descripcion', 'N/A')}")
                        st.write(f"**Comprobante:** {doc.get('url', 'N/A')}")
                    
                    for i in range(1, 5): 
                        monto_key = f'monto_{i}'
                        desc_key = f'descripcion_{i}'
                        
                        if doc.get(monto_key, 'N/A') != 'N/A' and doc.get(desc_key, 'N/A') != 'N/A':
                            st.write(f"**Monto {i}:** ${doc.get(monto_key)}")
                            st.write(f"**Descripción {i}:** {doc.get(desc_key)}")
                
                st.divider()
            else:
                st.write(f"No se encontraron registros para el nombre: {search_name}")

except Exception as e:
    st.error(f"An error occurred: {e}")
    import traceback
    st.error(traceback.format_exc())