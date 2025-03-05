Este projeto é um sistema de perguntas e respostas sobre repositórios GitHub. Foi realizado um fine-tuning adaptativo para que a LLM passe a interpretar e responder questões relacionadas a commits, código-fonte, documentação e outros aspectos dos repositórios. Ele permite que os usuários consultem informações sobre commits, issues e READMEs de repositórios públicos do GitHub. O sistema usa um modelo de linguagem fine-tunado para gerar respostas precisas com base nos dados recuperados.
Isso envolve a criação de um dataset especializado, desenvolvendo um conjunto de dados com exemplos de perguntas e respostas extraídas de repositórios de software.

## Instalações necessárias:
pip install transformers datasets chromadb sentence-transformers pydriller fastapi uvicorn streamlit requests

## Iniciar a API:
uvicorn app:app --reload

## Iniciar a Interface Streamlit:
streamlit run app_interface.py
