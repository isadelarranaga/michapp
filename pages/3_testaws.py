import streamlit as st
from st_files_connection import FilesConnection
import time
import boto3
import tempfile

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

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
#conn = st.connection('s3', type=FilesConnection)
#df = conn.read("s3://test-test-test-test-dd/myfileisa.csv", input_format="csv", ttl=600)

# Print results.
#for row in df.itertuples():
 #   st.write(f"{row.Owner} has a :{row.Pet}:")

   

c1, c2 = st.columns(2)
c1.subheader("Upload image")
uploaded_image = c1.file_uploader("Select an image", type = (["jpg", "jpeg", "png"]))

#upload_button = st.button('Upload image')
        
if uploaded_image is not None:

    st.write(uploaded_image.name)
    
    if uploaded_image.type not in ["image/jpeg", "image/jpg", "image/png"]:
        c1.error('Only images are supported. Please upload a different file')
    else:
        c1.success(uploaded_image.name + ' Selected')
        bytes_data = uploaded_image.getvalue()
        if c1.button('Upload image'):
            with st.spinner('Uploading...'):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_image.getvalue())
                    temp_file_path = temp_file.name

                path_s3 = f'images-michapp'
                uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{uploaded_image.name}')
                st.success(f'test-test-test-test-dd/{path_s3}/{uploaded_image.name}')

c2.subheader("Upload image")
uploaded_image = c1.file_uploader("Select an image", key='up_image',  type = (["jpg", "jpeg", "png"]))

#upload_button = st.button('Upload image')
        
if uploaded_image is not None:

    st.write(uploaded_image.name)
    
    if uploaded_image.type not in ["image/jpeg", "image/jpg", "image/png"]:
        c1.error('Only images are supported. Please upload a different file')
    else:
        c1.success(uploaded_image.name + ' Selected')
        bytes_data = uploaded_image.getvalue()
        if c1.button('Upload image'):
            with st.spinner('Uploading...'):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_image.getvalue())
                    temp_file_path = temp_file.name

                path_s3 = f'images-michapp'
                uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{uploaded_image.name}')
                st.success(f'test-test-test-test-dd/{path_s3}/{uploaded_image.name}')

c2.subheader("Factura")
c2.uploaded_comprobante = c1.file_uploader("Select an image as a factura", key="up_factura", type = (["jpg", "jpeg", "png"]))
        
if c2.uploaded_comprobante is not None:

    st.write(c2.uploaded_comprobante.name)
    
    if c2.uploaded_comprobante.type not in ["image/jpeg", "image/jpg", "image/png"]:
        c2.error('Only images are supported. Please upload a different file')
    else:
        c2.success(c2.uploaded_comprobante.name + ' Selected')
        bytes_data = c2.uploaded_comprobante.getvalue()
        if c2.button('Upload image'):
            with st.spinner('Uploading...'):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(c2.uploaded_comprobante.getvalue())
                    temp_file_path = temp_file.name

                path_s3 = f'images-michapp'
                uploadImageToS3(temp_file_path,'test-test-test-test-dd', f'{path_s3}/{c1.uploaded_comprobante.name}')
                st.success(f'test-test-test-test-dd/{path_s3}/{c2.uploaded_comprobante.name}')
                s3_url2 = f'test-test-test-test-dd/{path_s3}/{c2.uploaded_comprobante.name}'