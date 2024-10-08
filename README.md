# Medical Conversational AI

This is a friendly RAG-based conversational AI that helps answer questions related to outlooks and researches regarding medical diseases. 

<p align="center">
  <img src="assets/med_conv_ai_image.jpg" width="300">
</p>

This project was implemented as part of 
[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) -
a free course about LLMs and RAG.

To help evaluate the project, an internal project evaluation is available [here](assets/internal_project_evaluation.md).

## Project Description

This application is a RAG-based conversational AI designed to simplify access to reliable, research-driven information about medical diseases.

It addresses the challenge of navigating overwhelming, complex medical data by providing clear, concise answers related to disease prognosis and research, all based on verified sources.

Its conversational interface helps patients, healthcare professionals, and researchers quickly find relevant medical insights.


<p align="center">
  <img src="assets/cli_image.jpg">
</p>

## Dataset

The dataset used in this project contains outlooks and research on various medical diseases.

It is a 210-row subset from the [Comprehensive Medical Q&A (Kaggle) Dataset](https://www.kaggle.com/datasets/thedevastator/comprehensive-medical-q-a-dataset), where the questions are only categorized as either "outlook" or "research", with the ratio of these categories preserved from the original dataset.

This data provides reliable, research-driven information on medical diseases for the application's users.

You can find the original data in [`data/kaggle_data.csv`](data/kaggle_data.csv), the curated data in [`data/qa_data.csv`](data/qa_data.csv), and the notebook detailing the transformations between these files in [`notebooks/from_kaggle_to_qa_data.ipynb`](notebooks/from_kaggle_to_qa_data.ipynb).

## Technologies

- Python 3.12
- Docker and Docker Compose for containerization
- [Minsearch](https://github.com/alexeygrigorev/minsearch) for full-text search
- OpenAI as an LLM
- Flask as the API interface (see [Background](#background) for more information on Flask)
- Grafana for monitoring and PostgreSQL as the backend for it

**Note**: All developments were done using GitHub Codespaces.

## Preparation

In order to use your own Open AI key:

1. Install `direnv`. On Linux you need to run the following commands: 
    - `sudo apt-get update`
	- `sudo apt-get install direnv`
	- `direnv hook bash >> ~/.bashrc`
2. Copy `.envrc_template` into `.envrc` and insert your key there.
3. For OpenAI, it's recommended to create a new project and use a separate key.
4. Run `direnv allow` to load the key into your environment.

For dependency management, pipenv was used, so you need to install it:

```bash
pip install pipenv
```

Once installed, you can install the app dependencies:

```bash
pipenv install --dev
```

## Reproducibility


### Database configuration

Before the application starts for the first time, the database
needs to be initialized.

First, run `postgres`:

```bash
docker-compose up postgres
```

Then run the [`db_prep.py`](fitness_assistant/db_prep.py) script:

```bash
pipenv shell

cd fitness_assistant

export POSTGRES_HOST=localhost
python db_prep.py
```

To check the content of the database, use `pgcli` (already
installed with pipenv):

```bash
pipenv run pgcli -h localhost -U your_username -d course_assistant -W
```

You can view the schema using the `\d` command:

```sql
\d conversations;
```

And select from this table:

```sql
select * from conversations;
```

### Run containers

Since `docker-compose` is used, you just have to run to start the *postgres*, *grafana* and *app* containers:

```bash
docker-compose up
```

### Restart containers

To restart containers, run the following commands:

```bash
docker-compose down
```

```bash
docker-compose up --build
```

### Time configuration

Make sure the time is correct. The current timezone (my own) is Europe/Lisbon.

You can change the timezone by replacing `TZ` in `.env`.

## How to use the application

After the application is running, the built interactive CLI application using
[questionary](https://questionary.readthedocs.io/en/stable/) can be started by running the following commmands:

```bash
pipenv run python cli.py
```

You can also make it randomly select a question from
[our ground truth dataset](data/ground-truth-retrieval-gpt-4-mini.csv):

```bash
pipenv run python cli.py --random
```

## Code

The code for the application is in the [`med-conv-ai`](med-conv-ai) folder:

- [`app.py`](med-conv-ai/app.py) - the Flask API, the main entrypoint to the application
- [`rag.py`](med-conv-ai/rag.py) - the main RAG logic for building the retrieving the data and building the prompt
- [`data_ingestion.py`](med-conv-ai/ingest.py) - loading the data into the knowledge base
- [`minsearch.py`](med-conv-ai/minsearch.py) - an in-memory search engine
- [`db.py`](fitness_assistant/db.py) - the logic for logging the requests and responses to postgres
- [`db_prep.py`](med-conv-ai/db_prep.py) - the script for initializing the database

We also [`cli.py`](cli.py) - interactive CLI for the application - in the project root directory.

### Interface

Flask was used to serve the application as an API.

Refer to the ["Using the Application" section](#using-the-application)
for examples on how to interact with the application.

### Ingestion

The ingestion script is in [`data_ingestion.py`](med-conv-ai/ingest.py).

Since an in-memory database, `minsearch` was used, as our
knowledge base, the ingestion script is run at the startup
of the application.

It's executed inside [`rag.py`](med-conv-ai/rag.py).

## Experiments

For experiments, we use Jupyter notebooks.
They are in the [`notebooks`](notebooks/) folder.

To start Jupyter, run:

```bash
cd notebooks
pipenv run jupyter notebook
```

Apart from the notebook detailing the transformations between the source files in [`notebooks/from_kaggle_to_qa_data.ipynb`], there are the following notebooks:
- [`evaluation-data-generation.ipynb`](notebooks/evaluation-data-generation.ipynb): Generating the ground truth dataset for retrieval evaluation.
- [`testing-rag.ipynb`](notebooks/testing-rag.ipynb): The RAG flow and the evaluation of the system.


### Retrieval evaluation

The basic approach - using `minsearch` without any boosting - gave the following metrics:

- Hit rate: 95.9%
- MRR: 85.6%

There was only performed one approach regarding the retrieval evaluation. 


### RAG flow evaluation

We used the LLM-as-a-Judge metric to evaluate the quality
of our RAG flow.

Using `gpt-4o-mini`, two prompts were tested in a sample with 200 records. They differed only on the first lines.

The first prompt started with the phrases "You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question." and obtained the following results:

- 182 (91%) `RELEVANT`
- 16 (8%) `PARTLY_RELEVANT`
- 2 (1%) `NON_RELEVANT`

The second prompt started with the phrases "Imagine you are a seasoned quality assurance specialist for an advanced question-answering system. 
Your expertise lies in assessing the precision and relevance of AI-generated responses. 
Today, your mission is to scrutinize the correlation between a given question and its corresponding AI-generated answer."

- 191 (95.5%) `RELEVANT`
- 8 (4.0%) `PARTLY_RELEVANT`
- 1 (0.05%) `NON_RELEVANT`

The second prompt obtained the best result, thus it was the chosen one.

## Monitoring

We use Grafana for monitoring the application. 

It's accessible at [localhost:3000](http://localhost:3000):

- Login: "admin"
- Password: "admin2"

### Dashboards

<p align="center">
  <img src="assets/grafana_dashboard_image.jpg">
</p>

The monitoring dashboard contains several panels:

1. **Last 5 Conversations (Table):** Displays a table showing the five most recent conversations, including details such as the question, answer, relevance, and timestamp. This panel helps monitor recent interactions with users.
2. **+1/-1 (Pie Chart):** A pie chart that visualizes the feedback from users, showing the count of positive (thumbs up) and negative (thumbs down) feedback received. This panel helps track user satisfaction.
3. **Relevancy Distribution (Gauge):** A gauge chart representing the relevance of the responses provided during conversations. The chart categorizes relevance and indicates thresholds using different colors to highlight varying levels of response quality.
4. **OpenAI Cost (Time Series):** A time series line chart depicting the cost associated with OpenAI usage over time. This panel helps monitor and analyze the expenditure linked to the AI model's usage.
5. **Tokens Usage (Time Series):** Another time series chart that tracks the number of tokens used in conversations over time. This helps to understand the usage patterns and the volume of data processed.

- [`dashboard.json`](grafana/dashboard.json) - the actual exported grafana dashboard.


## Background

Some background on some tech not used in the
course and links for further reading.

### Flask

Flask was used for creating the API interface for our application.
It's a web application framework for Python: we can easily
create an endpoint for asking questions and use web clients
(like `curl` or `requests`) for communicating with it.

In this case, questions were sent to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).


## Acknowledgements 

Thank you [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) from DataTalks.Club for the amazing content, courses and slack community.

## Next steps

Next possible steps are mentioned in [`assets/next_steps.md`](assets/next_steps.md)