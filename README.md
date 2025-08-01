
-----

# 🤖 Support Ticket Agent using RAG and LangGraph

[](https://www.python.org/)
[](https://langchain-ai.github.io/langgraph/)
[](https://opensource.org/licenses/MIT)
[](https://ollama.com/)

This project implements an intelligent **AI-powered Support Ticket Agent** leveraging **LangGraph** for robust workflow orchestration and **Retrieval-Augmented Generation (RAG)** for contextual responses. A key feature is its **autonomous self-correction loop**, ensuring high-quality outputs before customer delivery.

The agent aims to streamline customer support by resolving routine inquiries independently and gracefully escalating complex cases with comprehensive context for human intervention. This application is specifically designed to work seamlessly with **LangGraph Server** and **LangGraph Studio**, a visual debugging IDE.

-----

## ✨ Key Features

  * **Intelligent Ticket Classification:** Automatically categorizes inquiries (e.g., `billing`, `technical`).
  * **Contextual RAG:** Fetches and synthesizes information from `data/mock_docs.json` for accurate, grounded responses.
  * **Dynamic Response Drafting:** Generates tailored, empathetic support responses.
  * **Autonomous Self-Correction Loop:** Agent reviews its own drafts, provides feedback, and iteratively refines responses until quality standards are met.
  * **Graceful Escalation:** For unresolved issues, logs all details to `escalations.csv` for smooth human handover.
  * **Modular Design:** Clear separation of concerns for easy understanding, maintenance, and expansion.
  * **LangGraph Studio Integration:** Easily visualize, debug, and iterate on the agent's workflow.
  * **LangSmith Tracing Support:** Integrate with LangSmith for in-depth tracing and performance analysis.


## ASCII


```

\+---------------+
|    START      |
\+-------+-------+
|
v
\+-------+-------+     User Input (Subject, Description)
|  INPUT Node   |
\+-------+-------+
|
v
\+-------+-------+     Classify ticket (e.g., billing, technical)
| CLASSIFY Node |
\+-------+-------+
|
v
\+-------+-------+     Retrieve context from knowledge base (RAG)
| RETRIEVE Node |
\+-------+-------+
|
v
\+-------+-------+     Draft response using LLM & context
|  DRAFT Node   | \<----------------+
\+-------+-------+                  |
|                          |
v                          |
\+-------+-------+     Review drafted response
|  REVIEW Node  |
\+-------+-------+
|
| Conditional Routing (route\_review function)
|
\+-------+-------+--------------------------+
|       |                                  |
v       v                                  v
\+-------+-------+  (IF APPROVED)    +-------+-------+ (IF REJECTED & Attempts \< 2)
|      END      |                   |  RETRY Node   |
\+---------------+                   +-------+-------+
|
| (Prep for next draft)
|
\+-------------------------\>
^
|
| (IF REJECTED & Attempts \>= 2)
|
\+-------+-------+
| ESCALATE Node |
\+-------+-------+
|
v
\+---------------+
|      END      |
\+---------------+

```


-----

## LangGraph Studio Workflow

<img width="307" height="263" alt="image" src="https://github.com/user-attachments/assets/c00ccc45-d0aa-49c0-a836-1f1fdd825d7d" />


**Simplified Flow:**

1.  **Input:** User provides `subject` and `description`.
2.  **Classify:** Determines ticket category.
3.  **Retrieve:** Fetches relevant knowledge base articles from `data/mock_docs.json`.
4.  **Draft:** Generates a response.
5.  **Review:** Checks draft quality.
      * **Approved?** ✅ Done.
      * **Rejected?** ❌
          * **Retries left?** Get feedback, try `Draft` again.
          * **No retries?** `Escalate` to human.

-----

## ⚙️ Architectural Decisions

The agent's robust architecture is meticulously designed using **LangGraph's `StateGraph`**, embodying a modular and highly extensible approach.

1.  **LangGraph Orchestration (`src/main.py`):** The `create_support_agent()` function in `src/main.py` centrally defines and compiles the entire LangGraph workflow. This provides a clear, visualizable, and debuggable blueprint for the agent's behavior, handling complex, multi-step AI workflows with loops and conditional transitions.
2.  **Atomic & Single-Responsibility Nodes (`src/nodes/*.py`):** Each distinct operation (e.g., `classify`, `retrieve`, `draft`, `review`, `escalate`) is a separate function in its own file. This promotes extreme modularity, reusability, and simplifies testing and maintenance.
3.  **Centralized `AgentState` (`src/state.py`):** A `TypedDict` defines the shared memory (`AgentState`) passed between all nodes. This ensures strong type-hinting, code clarity, and consistent context tracking throughout the entire process.
4.  **Robust Retrieval-Augmented Generation (RAG):** Leverages `src/simple_rag.py` to ground LLM responses in factual, domain-specific information loaded from `data/mock_docs.json`, preventing hallucinations and increasing accuracy.
5.  **Intelligent Self-Correction Loop:** The `review` node provides actionable feedback to the `draft` node, enabling the LLM to iteratively refine its output. This significantly boosts response quality and reliability by mimicking human quality assurance.
6.  **Graceful & Accountable Escalation (`src/nodes/escalate.py`):** Provides a secure fallback for unresolved issues. Details are logged to `escalations.csv` for a smooth and informed human handover.

-----

## 🚀 Getting Started

### Prerequisites

  * **Python 3.9+**
  * **Ollama:** An open-source framework for running LLMs locally.
      * Download and install [Ollama](https://ollama.com/download) for your OS.
      * Start the Ollama application/service.
      * Pull the `mistral` model:
        ```bash
        ollama run mistral
        ```
      * **Crucial:** Ensure Ollama service is actively running before proceeding.

### Installation

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/Dev-Shiw7/Junior-AI-ZikraInfoTech.git
    cd Junior-AI-ZikraInfoTech
    ```
2.  **Create & Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```
3.  **Install Core Dependencies (including LangGraph CLI for server):**
    ```bash
    pip install -r requirements.txt
    pip install "langgraph-cli[inmem]"
    ```

### `requirements.txt` Content:

```
langchain==0.2.5
langchain-core==0.2.9
langgraph==0.0.51
langchain-community==0.2.5
ollama==0.1.8
pydantic==2.7.4
pandas==2.2.2
sentence-transformers==2.7.0
scikit-learn==1.5.0
```

### Knowledge Base Setup

The RAG system loads data from `data/mock_docs.json`. This file contains a JSON object where keys are categories and values are lists of documents. Ensure this file is correctly populated with your support knowledge.

**Example `data/mock_docs.json` content:**

```json
{
  "billing": [
    "For billing disputes, please contact billing@example.com or call 1-800-555-BILL. Provide your account number and transaction details. Refunds are processed in 5-7 business days."
  ],
  "technical": [
    "For login issues, try resetting your password. Ensure your browser is updated, clear cache/cookies."
  ]
}
```

### Environment Variables (Optional but Recommended)

If your application needs to use secrets (e.g., API keys for other services), create a `.env` file in the root of your project:

```bash
cp .env.example .env
```

Then, edit the `.env` file with your specific environment variables. For example, for LangSmith tracing:

```ini
# .env
LANGSMITH_API_KEY=lsv2...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=support-ticket-agent
```

-----

## ▶️ How to Run the Agent

### 1\. Command Line Interface (CLI)

1.  **Ensure Ollama is Running** with the `mistral` model.
2.  **Activate Virtual Environment**.
3.  **Execute:**
    ```bash
    python src/main.py
    ```
4.  Follow prompts for ticket `Subject` and `Description`. Type `exit` to quit.

### 2\. With LangGraph Studio (for Visualization & Debugging)

LangGraph Studio provides an interactive visualization and debugging environment for your agent.

1.  **Ensure you have activated your virtual environment** and installed `langgraph-cli`.
2.  **Start the LangGraph Server:**
    ```bash
    langgraph dev --host 0.0.0.0 --port 8123 src.main:support_agent
    ```
      * This command tells `langgraph dev` to load the compiled `support_agent` graph from `src/main.py` and serve it.
3.  **Access the Studio:** Open your web browser and navigate to `http://localhost:8123`.
4.  **Interact:** You can now input your `AgentState` (in JSON format) and visualize the agent's execution path step-by-step, inspecting the state changes at each node. This is invaluable for understanding and debugging complex flows.
      * **Development Tip:** While iterating, you can edit past states and rerun your app from previous points to debug specific nodes. Local code changes will be automatically applied via hot reload. For follow-up requests on the same "thread," continue from the current state. To start an entirely new interaction, clear the history using the `+` button in the top right of the Studio.

-----

## 🧪 Testing & Demonstrations

Use these scenarios to observe the agent's capabilities in the CLI (or LangGraph Studio):

### 1\. Happy Path: Successful Autonomous Resolution ✅

  * **Scenario:** A straightforward inquiry that the agent can fully resolve using its knowledge base and generate an approved, high-quality response.
  * **Input Example:**
      * **Subject:** `Question about my bill`
      * **Description:** `I have an unrecognized charge of $85. Account CUST456. How can I dispute it?`
  * **Expected Outcome:** Agent processes, reviews, `APPROVES` the draft, and displays the final response.

### 2\. Self-Correction Loop: Iterative Improvement 🔄

  * **Scenario:** An inquiry that might initially lead to a less-than-perfect draft, requiring the agent to refine its response based on internal feedback.
  * **Input Example:**
      * **Subject:** `Persistent login issue`
      * **Description:** `I can't log into my account since the OS update. Username: user.test. The page just hangs.`
  * **Expected Outcome:** Initial `Draft` is `REJECTED` with `reviewer_feedback`. Agent then `retries`, incorporating feedback, and an improved subsequent `Draft` is `APPROVED`.

### 3\. Escalation Path: Beyond Agent's Capabilities 🚨

  * **Scenario:** Complex or out-of-scope inquiry, leading to human handover.
  * **Input Example:**
      * **Subject:** `Critical bug in custom reporting module`
      * **Description:** `My custom report generation crashes the app on 'export to PDF' (error 0x80070005). New feature, critical. macOS Sonoma, Chrome.`
  * **Expected Outcome:** Agent attempts multiple `Draft` and `Review` cycles, all `REJECTED`. After max retries, `🚨 Ticket has been logged for human escalation.` appears. Verify new entry in `escalations.csv`.

-----

## 📂 Project Structure

```
Junior-AI-ZikraInfoTech/
├── .gitignore                   # Standard Git ignore file
├── README.md                    # This documentation file
├── demo_video.mp4               # Your project demonstration video (or link)
├── requirements.txt             # Python dependencies
├── escalations.csv              # Log file for escalated tickets (created on first escalation)
├── LICENSE                      # Project license file (e.g., MIT License)
├── .env.example                 # Example environment variable file
├── .env                         # Your local environment variables (gitignore'd)
├── data/                        # Directory for RAG data
│   └── mock_docs.json           # JSON knowledge base for RAG
└── src/                         # Source code directory
    ├── main.py                  # CLI entry point AND LangGraph workflow definition
    ├── state.py                 # AgentState TypedDict (shared memory)
    ├── llm.py                   # Ollama LLM client configuration
    ├── simple_rag.py            # RAG system logic (loads from data/mock_docs.json)
    └── nodes/                   # Individual workflow nodes
        ├── __init__.py          # Makes 'nodes' a Python package
        ├── classify.py          # Classifies the support ticket
        ├── draft.py             # Drafts response
        ├── escalate.py          # Handles escalation
        ├── input_node.py        # Processes initial input
        ├── review.py            # Reviews draft quality
        ├── retry.py             # Prepares for draft retry
        └── retrieve.py          # Retrieves RAG context
```

-----

## 📈 Future Enhancements

  * **Advanced RAG:** Integrate vector databases and embedding models for semantic search.
  * **Real-time User Feedback:** Allow direct user input to refine agent behavior.
  * **Ticketing System Integration:** Connect to platforms like Zendesk or ServiceNow.
  * **Multi-Agent Collaboration:** Extend the graph for specialized sub-agents.
  * **Human-in-the-Loop:** Design clear hand-off points for human intervention or oversight.
  * **Configurable Parameters:** Utilize LangGraph's `Configuration` class more extensively to expose dynamic LLM models, prompts, or tool choices directly from LangGraph Studio.

-----

## NOTE: The commented code in files like review.py and retrieve.py is to generate context from Ollama Mistral. I tried experimenting the significance and relativity. If someone wants to see its working, they can comment out the current code and used the currently commented code. 

## 🤝 Contributing

Contributions are welcome\! Feel free to open issues or submit pull requests.

-----

## 📄 License

This project is open-source and distributed under the **MIT License**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

-----

## 📧 Contact & Acknowledgments

Developed by Shiwani Thourani for Junior AI Assessment Role, at Z360.

Special thanks to the LangChain and LangGraph communities for their powerful tools.

-----
