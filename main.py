from fastapi import FastAPI, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
from rag import process_document, retrieve_context
from agent import run_agent
from memory import save_context, get_history
from langchain.llms import GoogleGenerativeAI

app = FastAPI()

llm = GoogleGenerativeAI(model="gemini-pro")

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    try:
        process_document(content, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Document processed"}


def generate_stream(session_id: str, query: str):
    context = retrieve_context(query)
    history = get_history(session_id)

    if context:
        prompt = f"""
You are an expert assistant.

Chat History:
{history}

Context:
{context}

Using only the context above, answer the question. If the answer is not contained in the provided context, respond with exactly NOT_FOUND.

Question: {query}
"""
        response = llm.invoke(prompt)

        if "NOT_FOUND" in response.upper():
            response = run_agent(query)
    else:
        response = run_agent(query)

    save_context(session_id, query, response)

    for token in response.split():
        yield token + " "


@app.get("/chat")
def chat(query: str = Query(...), session_id: str = Query("default")):
    return StreamingResponse(generate_stream(session_id, query), media_type="text/plain")