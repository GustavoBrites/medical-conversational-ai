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

It is a 210-row sample from the [Comprehensive Medical Q&A (Kaggle) Dataset](https://www.kaggle.com/datasets/thedevastator/comprehensive-medical-q-a-dataset), where the questions are only categorized as either "outlook" or "research", with the ratio of these categories preserved from the original dataset.

This data provides reliable, research-driven information on medical diseases for the application's users.

You can find the original data in [`data/kaggle_data.csv`](data/kaggle_data.csv), the curated data in [`data/qa_data.csv`](data/qa_data.csv), and the notebook detailing the transformations between these files in [`notebooks/from_kaggle_to_qa_data.ipynb`](notebooks/from_kaggle_to_qa_data.ipynb).

