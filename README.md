# Query tool AI 

[Neurobagel](https://www.neurobagel.org/) is a federated data ecosystem that allows researchers and other data users to find and consume research data that has to remain at their original institute for data governance reasons. 

Currently, the researcher or the data user has to answer a number of queries to get the desired results and it often requires iteration. 

The aim of query-tool-ai would be to make this search process more user-friendly by adding an LLM style chatbot interface. This is to be done by utilizing large language models that will be able to interpret the user prompts and initiate the API calls accurately giving the user the desired results.

## Local installation - 
  ### Clone the repository :
  ```bash
  git clone https://github.com/neurobagel/query-tool-ai.git
  cd query-tool-ai
  ```
  
  After cloning the repository, you can choose to either use the Dockerized version or run the application locally using Python but before proceeding with either you need to set the environment variables.

  ### Set the environment variables - 
   | Environment Variable   | Type    | Required                                 | Default Value if Not Set | Example                                                   |
   | ---------------------- | ------- | ---------------------------------------- | ------------------------ | --------------------------------------------------------- |
   | `NB_API_QUERY_URL`                 | string  | Yes                                       | `None`                | `https://api.neurobagel.org/query/?`                                               |
   | `HOST`                 | string  | No                                       | `0.0.0.0`                | `127.0.0.1`                                               |
   | `PORT`                 | integer | No                                       | `8000`                   | `8080`                                                    |
   

  ### Option 1 : Docker :
  - #### First, [install Docker](https://docs.docker.com/get-docker/).
  - #### Build the image using the Dockerfile
    After cloning the current repository, build the Docker image locally:
    ```bash
    docker build -t neurobagel-query-tool-ai .
    ```
  - #### Run the container from the built image:
    Start the container from the built image. Ensure you map the necessary volumes and set the container name.
    ```bash
    docker run -d \
    -p 8000:8000 \
    -v ollama:/root/.ollama \
    -v /home/user/data:/app/output/ \
    --name query-tool-ai-container neurobagel-query-tool-ai
    ```

    Then you can access the query tool ai at http://localhost:8000

    **Note:** the query tool ai is listening on port 8000 inside the docker container, replace port 8000 by the port you would like to expose to the host. For example if you'd like to run the tool on port 8080 of your machine you can run the following command:
    ```bash
    docker run -d \
    -p 8080:8000 \
    -v ollama:/root/.ollama \
    -v /home/user/data:/app/output/ \
    --name query-tool-ai-container neurobagel-query-tool-ai
    ```


  - #### Verify Host and Port
    To ensure the server is running on localhost, you can check the logs or try accessing the server in your browser or with `curl`(assuming the the query tool ai is listening on port 8000):
    ```bash
    curl -X GET "http://localhost:8000/"
    ```
    You should see the response:
    ```json
    {"message": "Welcome to the Neurobagel Query Tool AI API"}
    ``` 

### Option 2 : Python
- #### Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
- #### Install the required packages and pull the Ollama model:
   ```bash
   pip install -r requirements.txt
   ollama pull mistral
   ```

- #### Run the FastAPI Server:
  ```bash
  python3 -m app.main
  ```
  This command starts the FastAPI server on `http://localhost:8000`. (assuming PORT=8000)

- #### Verify Host and Port
  To ensure the server is running on localhost, you can check the logs or try accessing the server in your browser or with `curl`:
  ```bash
  curl -X GET "http://localhost:8000/" 
  ```
  You should see the response:
  ```json
  {"message": "Welcome to the Neurobagel Query Tool AI API"}
  ```
 
## Interacting with the Query Tool AI 
After the local installation is complete, you can ask your query in the following 2 ways.

### API Interaction - 
  You can interact with the FastAPI application by sending a POST request to the generate_url endpoint. Here’s how you can do it using curl (assuming the the query tool ai is listening on port 8000):
  ```bash
  curl -X POST "http://localhost:8000/generate_url/" -H "Content-Type: application/json" -d '{"query": "your query here"}'
  ```
  Replace "your query here" with the actual query you want to test.

### Python Script Interaction (Optional) -
  - If you have completed the local installation using **`docker`**, write the following command in the terminal.
    ```bash
    docker exec -it query-tool-ai-container python3 -m app.api.url_generator
    ```

  - If you have completed the local installation using **`python`**, write the following command in the terminal.
    ```bash
    python3 -m app.api.url_generator
    ```

  You should see the following prompt - 

  ```bash
  Enter user query (or 'exit' to quit): 
  ```

  Enter your query to get the desired API URL.


## Testing

Neurobagel API utilizes [Pytest](https://docs.pytest.org/en/7.2.x/) framework for testing.

To run the tests first make sure you're in repository's main directory.

You can then run the tests by executing the following command in your terminal:

```bash
pytest tests
```

### License

Neurobagel API is released under the terms of the [MIT License](LICENSE)







