# Medical Conversational AI

This is a friendly RAG-based conversational AI that helps answer questions related to outlooks and researches regarding medical diseases. 

<p align="center">
  <img src="assets/med_conv_ai_image.jpg" width="300">
</p>

This project was implemented as part of 
[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) -
a free course about LLMs and RAG.

## Project Description

This application is a RAG-based conversational AI designed to simplify access to reliable, research-driven information about medical diseases.

It addresses the challenge of navigating overwhelming, complex medical data by providing clear, concise answers related to disease prognosis and research, all based on verified sources.

Its user-friendly, conversational interface helps patients, healthcare professionals, and researchers quickly find relevant medical insights.

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

## Running the application


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

### Run

Since `docker-compose` is used, you just have to run to start the *postgres*, *grafana* and *app* containers:

```bash
docker-compose up
```

### Time configuration

Make sure the time is correct.

You can change the timezone by replacing `TZ` in `.env`.
