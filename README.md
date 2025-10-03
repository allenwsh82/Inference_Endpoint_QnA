# Creating an AI Question and Answer Endpoint with fastAPI


![fastAPI_Image](https://github.com/user-attachments/assets/e74947d4-ae5d-458f-b9cd-6f2e59f1977e)


Fast API is a high-performance, open-source Python web framework used to develop web APIs with the hint types of Python 3.6 or higher. It enables data types to be validated even within JSON requests. It is based on standards such as JSON Schema, OAuth 2.0 and OpenAPI.

<br/>

![fastAPI](https://github.com/user-attachments/assets/10955176-73ee-49b7-8668-97ec5312923b)

<br/>

This version shows the full flow:
- 🧑‍💻 Client sends an HTTP request (GET, POST, etc.)
- ⚡ FastAPI App receives and routes the request
- 🧠 Pydantic Models validate and parse data
- 🖥️ Server hosts the FastAPI application
- 🗄️ Database stores and retrieves persistent data
- 🔁 Response is returned to the client in JSON forma


To try our the demo script, please follow the steps:

1) Clone this repo:
```
git clone https://github.com/allenwsh82/Inference_Endpoint_QnA.git
```

2) Create a virtual environment for this project:
```
python -m venv endpoint_env
```

3) Make sure you enable the virtual environment for this project:
```
source endpoint_env/bin/activate
```

4) Install dependencies:
```
pip install -r requirements.txt
```

5) Run the script:
```
./start_server_sealion_7b.sh
```
6) There are two ways run test the 'text-generation' workload :
<br/>

   a) By Endppint_Sealion_7B_Inference.ipynb

   ![Inference_1](https://github.com/user-attachments/assets/dc89041d-6915-457e-815f-0b50094259a4)

<br/>

   b) By inference_endpoint_sealion.py
  
   ![Inference_2](https://github.com/user-attachments/assets/e7a1f8e5-8534-49d8-b17b-4e44d8404d96)
