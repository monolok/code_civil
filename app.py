import streamlit as st
from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import requests

# Load the .env file
load_dotenv()

# Use the environment variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
bearer = os.getenv('Bearer')
pc = Pinecone(api_key=pinecone_api_key)
# Connect to the Pinecone vector database
index = pc.Index("civil")
embeddings = HuggingFaceEmbeddings()
# Mistral Instruct
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": bearer}

def query_def(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# Streamlit app
def main():
    st.title("Code Civil Mariage & Divorce")

    # User input
    query = st.text_input("Enter your query", value="Est-ce que je peux me marier si je suis mineur ?")

    # Run the query
    if st.button("Run Query"):
        query_embedding = embeddings.embed_documents([query])[0]
        query_results = index.query(
            vector=query_embedding,
            top_k=2,
            include_values=True,
            include_metadata=True
        )
        for result in query_results['matches']:
             context = result['metadata']['text']
        output = query_def({
             "inputs": f"<s>[INST]Que pouvez-vous répondre à propos de {query} avec le texte suivant: {context}[/INST]"
        })
        # Display the results
        st.subheader("Results:")
        st.write(output)

# Run the Streamlit app
if __name__ == "__main__":
    main()