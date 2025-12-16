import streamlit as st

from repo_ingestion.clone_repo import clone_repository
from repo_ingestion.read_files import read_source_files
from repo_ingestion.parse_ast import parse_python_code
from repo_ingestion.embeddings import CodeEmbeddingStore
from repo_ingestion.llm import ask_llm
from repo_ingestion.issues import fetch_issues
from repo_ingestion.issue_analyzer import estimate_difficulty, extract_skills

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(
    page_title="GenAI OSS Onboarding Assistant",
    layout="wide"
)

st.title("🧠 GenAI-Powered Open Source Onboarding Assistant")

# -------------------------
# Repository Input
# -------------------------
repo_url = st.text_input("Enter GitHub Repository URL")

# -------------------------
# Analyze Repository
# -------------------------
if repo_url:
    with st.spinner("Analyzing repository..."):
        repo_path = clone_repository(repo_url)
        code_files = read_source_files(repo_path)

        store = CodeEmbeddingStore()
        texts, meta = [], []

        # Limit files for speed (important for demo)
        for path, content in code_files[:15]:
            chunks = parse_python_code(path, content)
            for chunk in chunks:
                if chunk.get("code"):
                    texts.append(chunk["code"])
                    meta.append({
                        "file": path,
                        "type": chunk["type"],
                        "name": chunk["name"],
                        "code": chunk["code"]
                    })

        store.add_embeddings(texts, meta)

    st.success("Repository analyzed successfully!")

    # ======================================================
    # 🔍 QUESTION ANSWERING (FIXED & STABLE)
    # ======================================================
    st.subheader("🔍 Ask about the codebase")

    question = st.text_input("Your question")
    ask_btn = st.button("Ask AI")

    if ask_btn and question:
        with st.spinner("Thinking..."):
            retrieved = store.search(question, top_k=3)


            context = "\n\n".join(
    f"{r['type']} {r['name']}:\n{r['code'][:1200]}"
    for r in retrieved
            )

            prompt = f"""
You are an open-source mentor.
Answer ONLY using the code below.

QUESTION:
{question}

CODE:
{context}
"""

            answer = ask_llm(prompt)

        st.markdown("### 🧠 AI Explanation")
        st.write(answer)

    # ======================================================
    # 📌 CONTRIBUTOR INTELLIGENCE
    # ======================================================
    st.subheader("📌 Suggested Issues for New Contributors")

    owner = repo_url.split("/")[-2]
    repo = repo_url.split("/")[-1]

    issues = fetch_issues(owner, repo, max_issues=5)

    if not issues:
        st.info("No open issues found.")
    else:
        for issue in issues:
            issue_text = issue["title"] + "\n" + (issue["body"] or "")
            related = store.search_with_scores(issue_text, top_k=3)

            difficulty = estimate_difficulty(issue, related)
            skills = extract_skills(related)

            with st.expander(f"Issue #{issue['number']} — {issue['title']}"):
                st.write(f"**Difficulty:** {difficulty}")
                st.write(f"**Skills Needed:** {', '.join(skills)}")
                st.write("**Relevant Files:**")
                for r in related:
                    st.write(f"- {r['meta']['file']}")
