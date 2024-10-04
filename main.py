from fastapi import FastAPI


app = FastAPI()


@app.get('/check')
async def main():
    return 'Hello. check done'
