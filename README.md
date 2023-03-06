# Quarto Help Bot

This repo is an implementation of a locally hosted chatbot specifically focused on question answering over the [Quarto documentation](https://quarto.org).
Built with [LangChain](https://github.com/hwchase17/langchain/) and [FastAPI](https://fastapi.tiangolo.com/).

The app leverages LangChain's streaming support and async API to update the page in real time for multiple users.

## ✅ Running locally
1. Install dependencies: `pip install -r requirements.txt`
1. Run the app: `make start`
1. In [templates/index.html](./templates/index.html), change the line of code `var endpoint = "wss://quarto-bot.onrender.com/chat";` to `var endpoint = "ws://localhost:9000/chat` (this is super hacky will fix this later).
1. Open [localhost:9000](http://localhost:9000) in your browser.

## 🚀 Important Links

Deployed version: [https://quarto-bot.onrender.com/](https://quarto-bot.onrender.com/)

I am using [render](https://render.com/) to deploy the site.  The [render.yaml](./render.yaml) facilitates this deployment.


## 📚 Technical description

There are two components: ingestion and question-answering.

Ingestion has the following steps:

1. Pull search.json from the rendered site
2. Load the search.json into a vector database (see `startup_event` in `main.py`).
3. Split documents with LangChain's [TextSplitter](https://langchain.readthedocs.io/en/latest/modules/utils/combine_docs_examples/textsplitter.html)
4. Create a vectorstore of embeddings, using LangChain's [vectorstore wrapper](https://langchain.readthedocs.io/en/latest/modules/utils/combine_docs_examples/vectorstores.html) (with OpenAI's embeddings and FAISS vectorstore).

Question-Answering has the following steps, all handled by [ChatVectorDBChain](https://langchain.readthedocs.io/en/latest/modules/chains/combine_docs_examples/chat_vector_db.html):

1. Given the chat history and new user input, determine what a standalone question would be (using GPT-3).
2. Given that standalone question, look up relevant documents from the vectorstore.
3. Pass the standalone question and relevant documents to GPT-3 to generate a final answer.
