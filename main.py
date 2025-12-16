from repo_ingestion.clone_repo import clone_repository
from repo_ingestion.read_files import read_source_files
from repo_ingestion.parse_ast import parse_python_code
from repo_ingestion.embeddings import CodeEmbeddingStore
from repo_ingestion.llm import ask_llm

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")

    repo_path = clone_repository(repo_url)
    code_files = read_source_files(repo_path)

    store = CodeEmbeddingStore()

    texts = []
    meta = []

    for path, content in code_files[:10]:
        chunks = parse_python_code(path, content)
        for chunk in chunks:
            if chunk["code"]:
                texts.append(chunk["code"])
                meta.append({
                    "file": path,
                    "type": chunk["type"],
                    "name": chunk["name"],
                    "code": chunk["code"]
                })

    store.add_embeddings(texts, meta)

    question = input("\nAsk a question about the codebase: ")

    retrieved = store.search(question)

    context = "\n\n".join(
        f"{r['type']} {r['name']}:\n{r['code']}" for r in retrieved
    )

    prompt = f"""
You are an experienced open-source mentor.
Answer the question ONLY using the code context below.
If unsure, say you don't know.

QUESTION:
{question}

CODE CONTEXT:
{context}

Explain clearly for a beginner contributor.
"""

    answer = ask_llm(prompt)

    print("\n🧠 AI Explanation:\n")
    print(answer)


from repo_ingestion.issues import fetch_issues
from repo_ingestion.issue_analyzer import estimate_difficulty, extract_skills

print("\n📌 Contributor Suggestions:\n")

owner = repo_url.split("/")[-2]
repo = repo_url.split("/")[-1]

issues = fetch_issues(owner, repo, max_issues=5)

for issue in issues:
    issue_text = issue["title"] + "\n" + issue["body"]
    related = store.search_with_scores(issue_text, top_k=3)

    difficulty = estimate_difficulty(issue, related)
    skills = extract_skills(related)

    print(f"Issue #{issue['number']}: {issue['title']}")
    print(f"  Difficulty: {difficulty}")
    print(f"  Skills: {', '.join(skills)}")
    print("  Related files:")
    for r in related:
        print(f"    - {r['meta']['file']}")
    print()

