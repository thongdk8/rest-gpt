### OpenAI API chat wrapper implemented with fastapi
This is a simple Rest API wrapper for chat API of OpenAPI GPT models.
The Rest API is implemented using `fastapi`

## Setup
```bash
pip install -r requirements.txt
```

## Run

You need the OpenAI API key to run the app. This API key is set via enviroment variable `OPENAI_API_KEY`. Then you can start API server with `uvicorn`

```
export OPENAI_API_KEY=<your OpenAI API key>
uvicorn main:app
```

Once the API server is running, you can access the Swagger UI by accesss `http://localhost:8000/docs`, Redocs also be integrated at `http://localhost:8000/redoc`

## Enpoints

- `/chat` Using to post the chat request, sample request as below:

```
{
  "messages": [
    {
      "name": "user_01",
      "role": "user",
      "content": "Hello world"
    }
  ],
  "stream": true,
  "model": "gpt-4-0125-preview"
}
```

If `stream` is set to `true` the response will be a stream with SSE (Server-Sent Events), you can retrieve the full response message by reading the stream events

If `stream` is set to `false` the full reponse message will be returned
