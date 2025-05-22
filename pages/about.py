import streamlit as st



st.title(" About UoW Assistant")  #st.title the layout function
col1, col2 = st.columns([2, 1])  # two columns with width ratio 2:1 are created for visual purposes

with col2:
    st.image("https://i.ibb.co/rGjx140y/UoW-Logo.jpg", caption="Muhammad Yasir", use_container_width=True)


with col1:
    st.markdown(
    """
    # The Web App is developed by Muhammad Yasir

    ### The UoW Assistant is your chatbot for University of Westminster.
    It is designed to help students navigate university life with ease. 
    From academic guidance to campus resources, the assistant is here to answer your questions and provide the support you need. 
    Whether you're a new student exploring campus or a returning student seeking career advice, UoW Assistant is your go-to digital companion for instant, reliable assistance.
    """)

st.write("\n")
st.write(
    """
    The chat bot would provide Information that a university student wished they knew when they first arrived at your university.


    The starting days of university life can be a challenging experience for many new students. This is a period of life marked by many challenges including emotional, social and academic challenges. Studies have revealed that new students face challenges such as difficulty making social adjustments as well as reluctance in seeking help. Current university support is known to be strained at the start of the term which results in delayed responses to new student which can be a cause of worry.
    
    
    The aim of this project is to address these challenges by developing a chatbot using IBM’s watsonx Assistant which is powered by AI. The chatbot will be accessible via QR codes placed across the campuses at the University of Westminster. This is achieved by integrating the app into a web application that is responsive. The primary goal of the chatbot is to provide instant and reliable information to new students which can also help reducing strain on university’s support services.

    """
)
