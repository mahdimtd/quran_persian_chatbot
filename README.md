# Quran_Persian_QA 📖🧠
## Answering questions about the Quran based on RAG system 
Nowadays, many users utilize language models to save time and quickly access answers to their questions. Language models typically provide the best and shortest possible answer to the user's question. However, in some cases—especially when users' questions are about a specific topic or when the answer can be subjective—language models often cannot provide an accurate response. Furthermore, if they do not know the answer to a question at all, they may generate an incorrect response, believing it to be correct.It is in such cases that building chatbots which answer questions based on specific data can be effective.
In this project, language models have been used to answer questions about the Quran based on authoritative Shia Quranic interpretation books. 

# The steps of the work are as follows:
1-Extraction of data from the two books: **Majma' al-Bayan** and **Majma' al-Burhan**.

2-Using **LlamaIndex** to create an index from the extracted data.

3-Using the **sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2** model to convert the data into vector space.

4-Using a language model to answer the user's question **only based on the available data**.


---

## How to Run the Project

# 1. Install Requirements

Make sure you have **Python 3.8** or newer installed. Then, install the required packages.


# 2. Extract Data

Download the `data.rar` file from the repository and extract it in the main project directory so that the `data/` folder is available.

# 3. Build the Index

To prepare the required information retrieval index, run the `preparing_index.ipynb` Jupyter notebook. This will process the data and create necessary index files.


# 4. Using the QA System

In the web interface, you can ask questions in Persian. The system, using a Retrieval-Augmented Generation (RAG) architecture and large language models, will generate answers with relevant Quranic verses.

---


