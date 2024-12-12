from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
import time
import my_routes
import auth_routes
import users_routes
from my_db import get_db
from models import Contact
import redis.asyncio as redis
from config import settings
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix='/api')
app.include_router(my_routes.router, prefix='/api')
app.include_router(users_routes.router, prefix='/api')


@app.get('/')
def index():
    """
    The read_root function is a simple function that returns a dictionary with the key &quot;message&quot; and value &quot;REST APP v-0.0&quot;.
    This function is used to test if the REST API server is running.

    :return: A dictionary with a single key/value pair    
    """
    return {'message': 'Welcome to Web Assistant'}


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as databases or caches.

    :return: A future object, which is a special type of object that represents the result of an asynchronous operation
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks the health of the database.
    It does this by making a request to the database and checking if it returns any results.
    If there are no results, then we know something is wrong with our connection to the database.

    :param db: The database session.
    :type db: Session
    :return: A dictionary with a message key    
    """
    try:
        # Make request
        result = db.execute(select(Contact)).all()

        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Error connecting to the database")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called &quot;My-Process-Time&quot;
    that contains the time it took for this function to run. This is useful for debugging purposes.

    :param request: Access the request object.
    :type request: Request
    :param call_next: Call the next middleware in the chain.    
    :return: The response object.    
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response
