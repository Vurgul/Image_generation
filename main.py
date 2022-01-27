from fastapi import FastAPI
import uvicorn

app = FastAPI()


def main():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == '__main__':
    main()
