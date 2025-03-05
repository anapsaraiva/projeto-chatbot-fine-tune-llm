from pydriller import Repository

def process_repository(repo_url, max_commits=100):
    repo_data = []
    
    for i, commit in enumerate(Repository(repo_url).traverse_commits()):
        if i >= max_commits:
            break 

        repo_data.append({
            "hash": commit.hash,
            "author": commit.author.name,
            "date": str(commit.author_date),
            "message": commit.msg,
            "modified_files": [file.filename for file in commit.modified_files]
        })
    
    return repo_data

