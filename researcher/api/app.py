from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from researcher.agent.researcher import Researcher
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/research")
async def research(query: Query):
    try:
        researcher = Researcher()
        result = await researcher.research(query.question)

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
