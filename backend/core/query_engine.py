def generate_answer(query, docs, llm):
    context = "\n".join([d["text"] for d in docs])
    prompt = f"Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    return llm.generate(prompt, context)