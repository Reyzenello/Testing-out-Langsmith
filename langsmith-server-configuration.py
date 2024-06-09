from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Node(BaseModel):
    prompt: str
    responses: Dict[str, str]

graph = {}

@app.post("/add_node/")
def add_node(node_id: str, node: Node):
    graph[node_id] = node
    return {"message": "Node added successfully"}

@app.get("/get_node/{node_id}")
def get_node(node_id: str):
    node = graph.get(node_id, None)
    if node:
        return node
    else:
        return {"error": "Node not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
