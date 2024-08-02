# Query tool AI 

[Neurobagel](https://www.neurobagel.org/) is a federated data ecosystem that allows researchers and other data users to find and consume research data that has to remain at their original institute for data governance reasons. 

Currently, the researcher or the data user has to answer a number of queries to get the desired results and it often requires iteration. 

The aim of query-tol-ai would be to make this search process more user-friendly by adding an LLM style chatbot interface. This is to be done by utilizing large language models that will be able to interpret the user prompts and initiate the API calls accurately giving the user the desired results.

## Local installation
- Clone the repository:
  ```
  git clone https://github.com/neurobagel/query-tool-ai.git
  cd query-tool-ai
  ```
- Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
- Install the required packages and pull the Ollama model:
   ```
   pip install -r requirements.txt
   ollama pull mistral
   ```
- Run the python script:
  ```
  python3 app/api/url_generator.py
  ```
- You should see the following prompt:
  ```
  Enter user query (or 'exit' to quit): 
  ```
  Enter your query to get the desired API URL.

## Dockerized version
- First, [install Docker](https://docs.docker.com/get-docker/).

- After cloning the current repository, build the Docker image locally:
  ```
  docker build -t query-tool-ai .
  ```
- Run the container from the built image:
  ```
  docker run -d \
  -v ollama:/root/.ollama \
  -v /home/user/data:/app/output/ \
  --name query-tool-ai-container query-tool-ai
  ```
- Execute the python script:
  ```
  docker exec -it query-tool-ai-container python3 /app/api/url_generator.py
  ```
- You should see the following prompt:
  ```
  Enter user query (or 'exit' to quit): 
  ```
  Enter your query to get the desired API URL.


