import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time

EXAMPLE_DESC = """
Ticket de estacionamiento BAZ mes de octubre.
"""

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.html()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

def stream_data():
    for word in EXAMPLE_DESC.split(" "):
        yield word + " "
        time.sleep(0.2)

def change_page():
    get_started = st.button("¡Comencemos!")
    if get_started:
        switch_page("datos")


st.title("""How to page""")
st.markdown(''' 
            1. Introduce tus datos y los de tu compra, estos deben incluir el monto y una pequeña descripción. Ejemplo:''')

container = st.container(border=True)
container.write(EXAMPLE_DESC)
st.markdown(''' 
            2. Adjunta una foto de tu comprobante, tu factura o ambos.''')
st.markdown(""" * Recuerda que si proporcionas una factura el reembolso será más rápido y podrá incluirse en tu próxima quincena.*""")
st.markdown(""" Si necesitas incluir más compras selecciona el botón de más. """)
st.markdown(''' 
            3. Tu compra será revisada y podrá ser aceptada o rechazada. Mantente atento para recibir una 
            notificación que te informe la fecha y el formato en el que se realizará el reembolso. Si tu compra
            fue rechazada, te invitamos a introducir los datos nuevamente.''')

change_page()




