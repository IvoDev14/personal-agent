# Personal Mini Agent 🤖

This project is a personal playground for learning about AI agents. It is designed to experiment with building a custom agent using **Google's Gemma** model and the **GenAI SDK**.

## 🌟 Highlights

* **Learning Focus**: Built specifically for understanding agentic flows and LLM interactions.
* **Model Power**: Utilizes `gemma-3-27b-it` for intelligent responses.
* **Simple Implementation**: A straightforward testing ground for GenAI capabilities.

## ✨ Features

* **ReAct Architecture**: Implements a generic Reasoning + Acting loop.
* **Tool Usage**: Supports dynamic function calling with arguments, including system command execution (with user approval).
* **Extensible**: Easily add new tools via the `tools` registry.

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
    pip install -r requirements.txt
    ```

3. **Environment Setup**:
    Create a `.env` file in the root directory and add your API Key:

    ```bash
    GEMINI_API_KEY=your_api_key_here
    # OR
    GOOGLE_API_KEY=your_api_key_here
    ```

    You can use `GOOGLE_API_KEY` to access other models like Gemma.

## 🚀 Usage

Run the interactive agent mode to start a conversation:

```bash
python main.py
```

The agent will start an interactive loop where you can enter your queries and receive responses. Type `exit` to quit.

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'config'"

* Make sure you run the script from the **root directory** using `python main.py`. Do not run files inside `core/` directly.

### "Warning: GEMINI_API_KEY not found"

* Ensure you have created the `.env` file in the root directory.
* Ensure it contains `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## 🛠️ Tech Stack

* **Language**: Python
* **Model**: Gemma 3 (27B IT)
* **SDK**: Google GenAI
