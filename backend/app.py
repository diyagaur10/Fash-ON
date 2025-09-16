# FastAPI server
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Fashion Search API'}
