import argparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def create_content_filter(scripts, threshold=0.04):
    """content filter for questions."""
    combined_text = " ".join(scripts)
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=1.0
    )
    texts_to_fit = scripts + [combined_text]
    vectorizer.fit(texts_to_fit)
    
    def filter_func(question):
        try:
            question = question.strip().lower()
            if not question:
                return False
            question_tfidf = vectorizer.transform([question])
            texts_tfidf = vectorizer.transform(texts_to_fit)
            max_sim = np.max(cosine_similarity(question_tfidf, texts_tfidf).flatten())
            return max_sim > threshold
        except Exception:
            return True
    
    return filter_func

def setup_qa_chain(scripts, api_key):
    """setup QA chain."""
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vector_store = FAISS.from_texts(scripts, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = OpenAI(api_key=api_key)
    
    prompt = ChatPromptTemplate.from_template("""
You are an expert lecturer. Below is some context from the lecture:
{context}

Now, answer the following question:
Question: {question}

If the question requires further explanation beyond what is in the provided lecture notes,
feel free to include additional relevant details from your expertise. However, if the
question is completely off-topic, reply with: 'I can only answer questions related to
the lecture content.'

Answer:""")
    
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def main():
    parser = argparse.ArgumentParser(description="Chat with your lecture content")
    parser.add_argument("scripts_dir", help="Directory containing script files")
    parser.add_argument("api_key", help="OpenAI API key")
    args = parser.parse_args()

    # Load scripts
    scripts = []
    import os
    for file in sorted(os.listdir(args.scripts_dir)):
        if file.endswith("_script.txt"):
            with open(os.path.join(args.scripts_dir, file)) as f:
                scripts.append(f.read())

    # Setup QA
    content_filter = create_content_filter(scripts)
    qa_chain = setup_qa_chain(scripts, args.api_key)

    print("Chat system ready! Type 'quit' to exit.")
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() == 'quit':
            break
            
        if not content_filter(question):
            print("I can only answer questions related to the lecture content.")
            continue
            
        try:
            answer = qa_chain.invoke(question)
            print("\nAnswer:", answer)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()