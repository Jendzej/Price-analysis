from typing import Union

import uvicorn
from fastapi import FastAPI

from app.main import find_data

app = FastAPI()


@app.get('/')
async def get_item(q: Union[str, None] = 'iphone 14 pro max'):
    return find_data(q)


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
