import os
import uvicorn
from fastapi import FastAPI


import routes
from config import get_settings
settings = get_settings()
app = FastAPI()


app.include_router(routes.router)


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 9000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
