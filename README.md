# Plant-Sensor-Pipeline
A group project to develop a pipeline for botanical data.

## Installation
`bash setup.sh` - This command creates and activates a virtual environment in the current directory and install required libraries from requirements.txt

### Virtual Environment (Optional)

Navigate to the working directory:

```
cd <working directory>
```

- To create a virtual environment:

```
python3 -m venv venv
```

- Activate virtual environment:

```
source ./venv/bin/activate
```

### Install Required Libraries

Install requirements from .txt file:

```
pip install -r requirements.txt
```

## Environment
Add a `.env` file with the following variables
```
API_PATH = https://data-eng-plants-api.herokuapp.com
DB_USER = XXX
DB_PASSWORD = XXX
DB_HOST = XXX
DB_PORT = XXX
DB_NAME = XXX
```

## Pipeline
Run the full pipeline using: `python3 pipeline.py`