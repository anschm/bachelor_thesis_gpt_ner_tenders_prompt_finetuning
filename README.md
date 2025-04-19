# Bachelor Thesis - Increase GPT performance for named entity recognition in public tenders through targeted customisation and fine-tuning of prompts

# Abstract

Public tenders are an essential instrument for ensuring transparency, fairness, and
competition in public procurement. Due to the heterogeneity and complexity of on-
line procurement platforms, manual extraction of relevant entities such as contract-
ing authorities or deadlines can be challenging. To automate this process, Named
Entity Recognition (NER) from the field of Natural Language Processing (NLP) can
be utilized. Fine-tuning large language models (LLMs) like Bidirectional Encoder
Representations from Transformers (BERT) is resource-intensive, especially given
the relatively small dataset in public tenders. Recent research indicates that high
model performance can be achieved through targeted prompt design for pure de-
coder models like Generative Pre-trained Transformers (GPT), without the need
for costly fine-tuning. This study explores strategies for optimizing prompts for
Named Entity Recognition in public tenders using GPT. Theoretical foundations
on language models, prompt engineering, and in-context learning (ICL) are pre-
sented, alongside cross-domain applications of NER. Various prompt designs are
tested in an experimental setup, evaluating their efficiency. The results provide in-
sights into how GPT, through targeted prompt adjustments, can enable efficient and
cost-effective extraction of relevant entities in public tenders.

# Role of the repository

This repository contains the source code, tender test data und the result of the experiment
of the bachelor thesis.

# About the experiment

The experiment was conducted using the OpenAI API and the model 'gpt-4o-mini'.

The experiment was designed to test the performance of different prompt design and strategies (One-Shot/Zero-Shot) for Named Entity Recognition (NER) in public tenders.

The results of the experiment are stored in the 'results' directory.

The test data used in the experiment is stored in the 'tender-test-data' directory. The test data directory
contains a set of public tenders that were used to evaluate the performance of the different prompt design and strategies. The sub directory
'tender-websites' contains the raw data of the public tenders that were used in the experiment. The sub directory 'tender-websites-labelled'
contains the labelled data of the public tenders that were used in the experiment. The labelled data was used to evaluate the performance of the different prompt design and
strategies. The tender-test-data.xlsx file contains the metadata of the public tenders that were used in the experiment as a control file. The metadata includes the title, date,
and URL of the
public tenders. The example tender used for Zero-Shot is stored in the sub directory 'tender-examples'.

# Getting Started

1) Clone this repository to your local machine:

```bash
git clone https://github.com/anschm/bachelor_thesis_gpt_ner_tenders_prompt_finetuning.git
```

2) Setup a local python virtual environment based on the python version:

* 3.12.x

3) Install the required python packages:

```bash
pip install -r requirements.txt
```

4) Open the the '.env' file localed at the root and set the following environment variables:

* OPENAI_ROLE: The role of the OpenAI API key. This is usually set to "user".
* OPENAI_API_KEY: Your OpenAI API key. You can get it from the OpenAI website.
* OPENAI_MODEL: The OpenAI model you want to use. The experiment in this bachelor thesis was done with the model 'gpt-4o-mini'.
* RESULTS_DIR: The directory where the results of the experiment will be saved. This should be a path to a directory on your local machine.
* TEST_DATA_DIR: The directory where the test data is stored. This should be a path to a directory on your local machine.

# Run the experiment

The experiment can be run by executing the following command in the root directory of the repository:

```bash
python main.py <options>
```

The following options are available:

* --prompt-strategy: The prompt strategy to use. This can be either 'ZERO_SHOT' or 'ONE_SHOT'. Is required. No default.
* --index: The index of the tender from the test data to use. Is optional. No default.