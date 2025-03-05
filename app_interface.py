import streamlit as st
import requests

st.set_page_config(page_title="Consulta de Repositórios GitHub", page_icon="🔎️")

st.title("🔎️ Consulta de Repositórios GitHub")

repo_url = st.text_input("Insira a URL do repositório do GitHub:", placeholder="Ex: https://github.com/pallets/flask")

if st.button("Processar Repositório"):
    if repo_url:
        try:
            # Chamar o endpoint /process_repo da API FastAPI
            response = requests.post(
                "http://localhost:8000/process_repo",
                json={"repo_url": repo_url}
            )
            if response.status_code == 200:
                st.success("Repositório processado com sucesso!")
            else:
                st.error(f"Erro ao processar repositório: {response.json().get('detail', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {str(e)}")
    else:
        st.warning("Por favor, insira uma URL válida.")

question = st.text_input("Faça uma pergunta sobre o repositório:", placeholder="Ex: O que é Flask?")

if st.button("Enviar Pergunta"):
    if repo_url and question:
        try:
            # Chamar o endpoint /ask da API FastAPI
            response = requests.post(
                "http://localhost:8000/ask",
                json={"repo_url": repo_url, "question": question}
            )
            if response.status_code == 200:
                st.success("Resposta gerada com sucesso!")
                st.write("**Resposta:**")
                st.write(response.json().get("response", "Nenhuma resposta encontrada."))
            else:
                st.error(f"Erro ao gerar resposta: {response.json().get('detail', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {str(e)}")
    else:
        st.warning("Por favor, insira uma URL e uma pergunta válidas.")
