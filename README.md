# Maklai Assignment by Zharikova Natalia
## Installation
1.	Clone the repository to your local machine
2.	Go to the cloned repository directory
3.	Install necessary requirements with the command
```
pip install -r requirements.txt
```
## Running the server
1.	Start the server with command
```
uvicorn main:app
```
2.	Open the browser at http://localhost:8000/paraphrase?tree=<tree:str>&limit=<limit:int>
## Endpoints
The API has one endpoint:

-path: /paraphrase
  -HTTP method: GET
  -query parameters:
      tree: str (required) – syntax tree
      limit: int (optional, default: 20) –limit of pharaphrase trees to display


