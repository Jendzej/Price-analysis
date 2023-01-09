from typing import Union

import uvicorn
from fastapi import FastAPI

from app.analyze import analyze
from app.main import find_data

app = FastAPI()


@app.get('/')
async def get_item(q: Union[str, None] = 'iphone 14 pro max'):
    data = find_data(q)
    return {
        'data': data,
        'analysis': analyze(data)
    }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
