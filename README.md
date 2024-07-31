## Getting started

- clone the repo

  ```
  git clone https://github.com/neurobagel/query-tool-ai.git
  ```
- create virtual environment
   
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

- complete installations and pull the required ollama model
 
   ```
   pip install -r requirements.txt
   ollama pull mistral
   ```

- run python file
  ```
  python3 -m app.core_api.url_generator
  ```


