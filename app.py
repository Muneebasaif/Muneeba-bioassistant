import streamlit as st
import google.generativeai as genai

# 1. AI Assistant ka Core Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Interface Layout
st.set_page_config(page_title="Muneeba BioAssistant", page_icon="🧬", layout="wide")
st.title("🧬 Muneeba BioAssistant")
st.subheader("Your Specialized Generative AI for Bioinformatics")
st.write("Ask me anything about Gene Analysis, CRISPR, Docking, or Mutation Predictions.")

# 3. System Instructions (AI ko Bioinformatician banana)
SYSTEM_PROMPT = """
You are 'Muneeba BioAssistant', a highly specialized expert AI in Bioinformatics, Computational Biology, and Genomics.
Your job is ONLY to solve bioinformatics problems, explain biological pathways, assist with tools like PyRx, Geneious, and Benchling, and interpret sequence data.

CRITICAL RULE: If the user asks general questions (e.g., world history, jokes, weather, general programming not related to biology, or casual chat), politely refuse by saying:
'I am Muneeba BioAssistant, specialized strictly in Bioinformatics. Please ask me a computational biology or gene-related question!'
Always be precise, academic, and highly helpful.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask a bioinformatics problem..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-pro')
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_query}"
            response = model.generate_content(full_prompt)
            output_text = response.text
            st.markdown(output_text)
        except Exception as e:
            output_text = f"🧬 **Muneeba BioAssistant** ready hai! Isay fully live karne ke liye code mein Gemini API Key daalni hogi. Aapka sawal tha: '{user_query}'"
            st.markdown(output_text)
            
    st.session_state.messages.append({"role": "assistant", "content": output_text})
