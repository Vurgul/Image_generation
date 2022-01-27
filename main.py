from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR)

app = FastAPI(title='ImageGenerationAPI')


def main():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == '__main__':
    main()
