# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# if __name__ == "__main__":
#     uvicorn.run(
#         "api.main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )

# from cryptography.fernet import Fernet


# # Generate a fresh key
# key = Fernet.generate_key()
# print(key.decode())