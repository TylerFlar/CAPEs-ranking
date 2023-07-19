# Better CAPEs

![Banner](https://raw.githubusercontent.com/TylerFlar/CAPEs-ranking/main/banner.png)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TylerFlar/CAPEs-ranking/blob/main/Better_CAPEs.ipynb)

This project aims to provide a better tool to anaylize the Course and Professor Evaluations (CAPEs) data from the University of California, San Diego. This repository contains CSV files of CAPEs data and Python scripts for data cleaning, processing, and visualization.

## Getting Started

The visualization is carried out in a Jupyter notebook and requires Python along with several data processing and visualization libraries. Here are the requirements:

* Python 3.7.+
* Jupyter Notebook
* Pandas
* Numpy
* ipyaggrid
* ipywidgets

## Run the Visualizer on Google Colab

If you don't want to set up a local environment, you can run the notebok directly on Google Colab. Click the badge at the top of this README to open the notebook in Colab.

Please note that Google Colab enviroments are ephemeral and you will lose all your changes once the session ends.

## Run the Visualizer Locally

This is untested, but you should be able to run the notebook locally by installing the required libraries. I recommend using a virtual environment to avoid conflicts with your system Python installation.

## Data and Data Augmentation

The analysis is based on the CAPEs data from the University of California, San Diego. The data includes information like course name, instructor, term, enrollments, evaluations made, average grades expected and received, study hours per week, and recommendations for the course and instructor.

In order to make the data more user friendly, if two or more rows share the same course name and instructor, the rows are combined into one row. The enrollments and evaluations made are summed. The average grades expected, received, recommandations, and study hours per week are averaged. The term is set to the most recent term the instructor taught.

## Contributing

If you have any suggestions or ideas, feel free to open an issue or submit a pull request.
