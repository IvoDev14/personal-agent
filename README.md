# Personal Mini Agent 🤖

This project is a personal playground for learning about AI agents. It is designed to experiment with building a custom agent using **Google's Gemma** model and the **GenAI SDK**.

## 🌟 Highlights

* **Learning Focus**: Built specifically for understanding agentic flows and LLM interactions.
* **Model Power**: Utilizes `gemma-3-27b-it` for intelligent responses.
* **Simple Implementation**: A straightforward testing ground for GenAI capabilities.

## ℹ️ Overview

The goal of this project is to explore the capabilities of building AI agents from scratch. It connects to Google's GenAI API to leverage the Gemma family of open models. As a learning resource, it will evolve from simple "Hello World" prompts to more complex agentic behaviors.

## ⬇️ Installation

To run this project, you need Python installed and the Google GenAI SDK.

1. **Clone the repository** (if valid):

    ```bash
    git clone <repository-url>
    cd personal-mini-agent
    ```

2. **Install Dependencies**:

    ```bash
    pip install google-genai
    ```

3. **Environment Setup**:
    Ensure you have your API Key ready.
    *Note: The current code has a hardcoded key for testing, but it is recommended to use environment variables for security.*

## 🚀 Usage

Run the interactive agent mode to start a conversation:

```bash
python AIagent/main.py
```

The agent will start an interactive loop where you can enter your queries and receive responses. Type `exit` to quit.

## 🛠️ Tech Stack

* **Language**: Python
* **Model**: Gemma 3 (27B IT)
* **SDK**: Google GenAI
