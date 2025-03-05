import requests
import json
import time

# Lista de repositórios para coletar dados
repos = [
    ("torvalds", "linux"),        
    ("microsoft", "vscode"),      
    ("pallets", "flask"),         
    ("facebook", "react"),        
    ("scikit-learn", "scikit-learn"),  
    ("django", "django"),         
    ("apple", "swift"),           
    ("golang", "go")            
]

dataset = []

# Coletar commits
def coletar_commits(owner, repo, max_commits=50):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()
        for commit in commits[:max_commits]: 
            if "commit" in commit and "message" in commit["commit"]:
                message = commit["commit"]["message"].strip()
                author = commit["commit"]["author"]["name"]
                date = commit["commit"]["author"]["date"]

                dataset.append({
                    "question": "O que esse commit faz?",
                    "context": f"Repositório: {repo}\nMensagem do commit: {message}",
                    "answer": f"Esse commit implementa a seguinte mudança: {message}"
                })
                dataset.append({
                    "question": "Quem é o autor deste commit?",
                    "context": f"Repositório: {repo}\nMensagem do commit: {message}",
                    "answer": f"O autor deste commit é: {author}"
                })
                dataset.append({
                    "question": "Quando este commit foi feito?",
                    "context": f"Repositório: {repo}\nMensagem do commit: {message}",
                    "answer": f"Este commit foi feito em: {date}"
                })
                dataset.append({
                    "question": "Qual é o repositório deste commit?",
                    "context": f"Repositório: {repo}\nMensagem do commit: {message}",
                    "answer": f"Este commit pertence ao repositório: {repo}"
                })
    else:
        print(f"❌ Erro ao acessar commits do repositório {repo}: {response.status_code}")

# Coletar issues
def coletar_issues(owner, repo, max_issues=50):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url)

    if response.status_code == 200:
        issues = response.json()
        for issue in issues[:max_issues]:  
            title = issue.get("title", "Sem título")
            body = issue.get("body", "Sem descrição detalhada.")
            author = issue["user"]["login"]
            created_at = issue["created_at"]

            dataset.append({
                "question": "Qual é o problema descrito nesta issue?",
                "context": f"Repositório: {repo}\nTítulo: {title}\nDescrição: {body}",
                "answer": f"A issue reporta o seguinte problema no repositório: {body}"
            })
            dataset.append({
                "question": "Quem criou esta issue?",
                "context": f"Repositório: {repo}\nTítulo: {title}\nDescrição: {body}",
                "answer": f"A issue foi criada por: {author}"
            })
            dataset.append({
                "question": "Quando esta issue foi criada?",
                "context": f"Repositório: {repo}\nTítulo: {title}\nDescrição: {body}",
                "answer": f"A issue foi criada em: {created_at}"
            })
            dataset.append({
                "question": "Qual é o título desta issue?",
                "context": f"Repositório: {repo}\nTítulo: {title}\nDescrição: {body}",
                "answer": f"O título desta issue é: {title}"
            })
    else:
        print(f"❌ Erro ao acessar issues do repositório {repo}: {response.status_code}")

# Coletar README
def coletar_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url)

    if response.status_code == 200:
        readme_data = response.json()
        readme_text = requests.get(readme_data["download_url"]).text[:500]  

        dataset.append({
            "question": "Qual é o propósito deste repositório?",
            "context": f"Repositório: {repo}\nREADME:\n{readme_text}",
            "answer": f"O propósito deste repositório é: {readme_text[:200]}..."
        })
        dataset.append({
            "question": "O que este repositório contém?",
            "context": f"Repositório: {repo}\nREADME:\n{readme_text}",
            "answer": f"Este repositório contém: {readme_text[:200]}..."
        })
        dataset.append({
            "question": "Quem mantém este repositório?",
            "context": f"Repositório: {repo}\nREADME:\n{readme_text}",
            "answer": f"Este repositório é mantido por: {owner}"
        })
        dataset.append({
            "question": "Qual é a linguagem principal deste repositório?",
            "context": f"Repositório: {repo}\nREADME:\n{readme_text}",
            "answer": f"A linguagem principal deste repositório é: {repo.split('-')[-1]}"
        })
    else:
        print(f"❌ Erro ao acessar README do repositório {repo}: {response.status_code}")

for owner, repo in repos:
    print(f"📥 Coletando dados do repositório: {repo}...")
    
    coletar_commits(owner, repo)
    coletar_issues(owner, repo)
    coletar_readme(owner, repo)
    
    time.sleep(1)  # Evitar rate limits da API do GitHub

with open("dataset.jsonl", "w", encoding="utf-8") as file:
    for entry in dataset:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"✅ Dataset gerado com sucesso! Total de entradas: {len(dataset)}")
