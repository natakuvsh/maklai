from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from utils import paraphrase_tree


app = FastAPI()


@app.get("/paraphrase")
def paraphrase(tree: str, limit: int = None):

    if not tree:
        raise HTTPException(status_code=400, detail="No tree provided")

    paraphrases = paraphrase_tree(tree, limit)

    if not paraphrases:
        raise HTTPException(status_code=404, detail="No paraphrases found")

    json_compatible_item_data = jsonable_encoder(paraphrases)

    return JSONResponse(content=json_compatible_item_data)
