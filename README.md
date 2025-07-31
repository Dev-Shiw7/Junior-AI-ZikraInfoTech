🤖 Support Ticket Agent using RAG and LangGraph
This project implements an intelligent AI-powered Support Ticket Agent leveraging LangGraph for robust workflow orchestration and Retrieval-Augmented Generation (RAG) for contextual responses. A key feature is its autonomous self-correction loop, ensuring high-quality outputs before customer delivery.

The agent aims to streamline customer support by resolving routine inquiries independently and gracefully escalating complex cases with comprehensive context for human intervention. This application is specifically designed to work seamlessly with LangGraph Server and LangGraph Studio, a visual debugging IDE.

✨ Key Features
Intelligent Ticket Classification: Automatically categorizes inquiries (e.g., billing, technical).

Contextual RAG: Fetches and synthesizes information from data/mock_docs.json for accurate, grounded responses.

Dynamic Response Drafting: Generates tailored, empathetic support responses.

Autonomous Self-Correction Loop: Agent reviews its own drafts, provides feedback, and iteratively refines responses until quality standards are met.

Graceful Escalation: For unresolved issues, logs all details to escalations.csv for smooth human handover.

Modular Design: Clear separation of concerns for easy understanding, maintenance, and expansion.

LangGraph Studio Integration: Easily visualize, debug, and iterate on the agent's workflow.

LangSmith Tracing Support: Integrate with LangSmith for in-depth tracing and performance analysis.

💡 How It Works (Workflow Overview)
The agent operates as a state machine orchestrated by LangGraph, enabling complex decision-making and iterative loops.

Code snippet

graph TD
    A[Start] --> B(Receive Input);
    B --> C{Classify Ticket};
    C --> D[Retrieve Context (RAG)];
    D --> E(Draft Response);
    E --> F{Review Draft Quality};
    F -- Approved --> G[End Workflow (Success)];
    F -- Rejected (Attempts < 2) --> H(Provide Feedback);
    H --> E;
    F -- Rejected (Attempts >= 2) --> I[Log Escalation to CSV];
    I --> G;

    style A fill:#DDF,stroke:#333,stroke-width:2px;
    style G fill:#DDF,stroke:#333,stroke-width:2px;
    style B fill:#FFF,stroke:#333,stroke-width:1px;
    style C fill:#FFF,stroke:#333,stroke-width:1px;
    style D fill:#FFF,stroke:#333,stroke-width:1px;
    style E fill:#FFF,stroke:#333,stroke-width:1px;
    style F fill:#FFF,stroke:#333,stroke-width:1px;
    style H fill:#FFF,stroke:#333,stroke-width:1px;
    style I fill:#FFF,stroke:#333,stroke-width:1px;
Simplified Flow:

Input: User provides subject and description.

Classify: Determines ticket category.

Retrieve: Fetches relevant knowledge base articles from data/mock_docs.json.

Draft: Generates a response.

Review: Checks draft quality.

Approved? ✅ Done.

Rejected? ❌

Retries left? Get feedback, try Draft again.

No retries? Escalate to human.

⚙️ Architectural Decisions
The agent's robust architecture is meticulously designed using LangGraph's StateGraph, embodying a modular and highly extensible approach.

LangGraph Orchestration (src/main.py): The create_support_agent() function in src/main.py centrally defines and compiles the entire LangGraph workflow. This provides a clear, visualizable, and debuggable blueprint for the agent's behavior, handling complex, multi-step AI workflows with loops and conditional transitions.

Atomic & Single-Responsibility Nodes (src/nodes/*.py): Each distinct operation (e.g., classify, retrieve, draft, review, escalate) is a separate function in its own file. This promotes extreme modularity, reusability, and simplifies testing and maintenance.

Centralized AgentState (src/state.py): A TypedDict defines the shared memory (AgentState) passed between all nodes. This ensures strong type-hinting, code clarity, and consistent context tracking throughout the entire process.

Robust Retrieval-Augmented Generation (RAG): Leverages src/simple_rag.py to ground LLM responses in factual, domain-specific information loaded from data/mock_docs.json, preventing hallucinations and increasing accuracy.

Intelligent Self-Correction Loop: The review node provides actionable feedback to the draft node, enabling the LLM to iteratively refine its output. This significantly boosts response quality and reliability by mimicking human quality assurance.

Graceful & Accountable Escalation (src/nodes/escalate.py): Provides a secure fallback for unresolved issues. Details are logged to escalations.csv for a smooth and informed human handover.

🚀 Getting Started
Prerequisites
Python 3.9+

Ollama: An open-source framework for running LLMs locally.

Download and install Ollama for your OS.

Start the Ollama application/service.

Pull the mistral model:

Bash

ollama run mistral
Crucial: Ensure Ollama service is actively running before proceeding.

Installation
Clone Repository:

Bash

git clone https://github.com/Dev-Shiw7/Junior-AI-ZikraInfoTech.git
cd Junior-AI-ZikraInfoTech
Create & Activate Virtual Environment:

Bash

python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
Install Core Dependencies (including LangGraph CLI for server):

Bash

pip install -r requirements.txt
pip install "langgraph-cli[inmem]"
requirements.txt Content:
langchain==0.2.5
langchain-core==0.2.9
langgraph==0.0.51
langchain-community==0.2.5
ollama==0.1.8
pydantic==2.7.4
pandas==2.2.2
sentence-transformers==2.7.0
scikit-learn==1.5.0
Knowledge Base Setup
The RAG system loads data from data/mock_docs.json. This file contains a JSON object where keys are categories and values are lists of documents. Ensure this file is correctly populated with your support knowledge.

Example data/mock_docs.json content:

JSON

{
  "billing": [
    "For billing disputes, please contact billing@example.com or call 1-800-555-BILL. Provide your account number and transaction details. Refunds are processed in 5-7 business days."
  ],
  "technical": [
    "For login issues, try resetting your password. Ensure your browser is updated, clear cache/cookies."
  ]
}
Environment Variables (Optional but Recommended)
If your application needs to use secrets (e.g., API keys for other services), create a .env file in the root of your project:

Bash

cp .env.example .env
Then, edit the .env file with your specific environment variables. For example, for LangSmith tracing:

Ini, TOML

# .env
LANGSMITH_API_KEY=lsv2...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=support-ticket-agent
▶️ How to Run the Agent
1. Command Line Interface (CLI)
Ensure Ollama is Running with the mistral model.

Activate Virtual Environment.

Execute:

Bash

python src/main.py
Follow prompts for ticket Subject and Description. Type exit to quit.

2. With LangGraph Studio (for Visualization & Debugging)
LangGraph Studio provides an interactive visualization and debugging environment for your agent.

Ensure you have activated your virtual environment and installed langgraph-cli.

Start the LangGraph Server:

Bash

langgraph dev --host 0.0.0.0 --port 8123 src.main:support_agent
This command tells langgraph dev to load the compiled support_agent graph from src/main.py and serve it.

Access the Studio: Open your web browser and navigate to http://localhost:8123.

Interact: You can now input your AgentState (in JSON format) and visualize the agent's execution path step-by-step, inspecting the state changes at each node. This is invaluable for understanding and debugging complex flows.

Development Tip: While iterating, you can edit past states and rerun your app from previous points to debug specific nodes. Local code changes will be automatically applied via hot reload. For follow-up requests on the same "thread," continue from the current state. To start an entirely new interaction, clear the history using the + button in the top right of the Studio.

🧪 Testing & Demonstrations
Use these scenarios to observe the agent's capabilities in the CLI (or LangGraph Studio):

1. Happy Path: Successful Autonomous Resolution ✅
Scenario: A straightforward inquiry that the agent can fully resolve using its knowledge base and generate an approved, high-quality response.

Input Example:

Subject: Question about my bill

Description: I have an unrecognized charge of $85. Account CUST456. How can I dispute it?

Expected Outcome: Agent processes, reviews, APPROVES the draft, and displays the final response.

2. Self-Correction Loop: Iterative Improvement 🔄
Scenario: An inquiry that might initially lead to a less-than-perfect draft, requiring the agent to refine its response based on internal feedback.

Input Example:

Subject: Persistent login issue

Description: I can't log into my account since the OS update. Username: user.test. The page just hangs.

Expected Outcome: Initial Draft is REJECTED with reviewer_feedback. Agent then retries, incorporating feedback, and an improved subsequent Draft is APPROVED.

3. Escalation Path: Beyond Agent's Capabilities 🚨
Scenario: Complex or out-of-scope inquiry, leading to human handover.

Input Example:

Subject: Critical bug in custom reporting module

Description: My custom report generation crashes the app on 'export to PDF' (error 0x80070005). New feature, critical. macOS Sonoma, Chrome.

Expected Outcome: Agent attempts multiple Draft and Review cycles, all REJECTED. After max retries, 🚨 Ticket has been logged for human escalation. appears. Verify new entry in escalations.csv.

📂 Project Structure
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
📈 Future Enhancements
Advanced RAG: Integrate vector databases and embedding models for semantic search.

Real-time User Feedback: Allow direct user input to refine agent behavior.

Ticketing System Integration: Connect to platforms like Zendesk or ServiceNow.

Multi-Agent Collaboration: Extend the graph for specialized sub-agents.

Human-in-the-Loop: Design clear hand-off points for human intervention or oversight.

Configurable Parameters: Utilize LangGraph's Configuration class more extensively to expose dynamic LLM models, prompts, or tool choices directly from LangGraph Studio.

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

📄 License
This project is open-source and distributed under the MIT License. See the LICENSE file for more details.

📧 Contact & Acknowledgments
Developed by [Your Name/Team Name].

Special thanks to the LangChain and LangGraph communities for their powerful tools.

Generate code to prototype this with Canvas# New LangGraph Project

[![CI](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml)

This template demonstrates a simple application implemented using [LangGraph](https://github.com/langchain-ai/langgraph), designed for showing how to get started with [LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/#langgraph-server) and using [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/), a visual debugging IDE.

<div align="center">
  <img src="./static/studio_ui.png" alt="Graph view in LangGraph studio UI" width="75%" />
</div>

The core logic defined in `src/agent/graph.py`, showcases an single-step application that responds with a fixed string and the configuration provided.

You can extend this graph to orchestrate more complex agentic workflows that can be visualized and debugged in LangGraph Studio.

## Getting Started

<!--
Setup instruction auto-generated by `langgraph template lock`. DO NOT EDIT MANUALLY.
-->

<!--
End setup instructions
-->

1. Install dependencies, along with the [LangGraph CLI](https://langchain-ai.github.io/langgraph/concepts/langgraph_cli/), which will be used to run the server.

```bash
cd path/to/your/app
pip install -e . "langgraph-cli[inmem]"
```

2. (Optional) Customize the code and project as needed. Create a `.env` file if you need to use secrets.

```bash
cp .env.example .env
```

If you want to enable LangSmith tracing, add your LangSmith API key to the `.env` file.

```text
# .env
LANGSMITH_API_KEY=lsv2...
```

3. Start the LangGraph Server.

```shell
langgraph dev
```

For more information on getting started with LangGraph Server, [see here](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/).

## How to customize

1. **Define configurable parameters**: Modify the `Configuration` class in the `graph.py` file to expose the arguments you want to configure. For example, in a chatbot application you may want to define a dynamic system prompt or LLM to use. For more information on configurations in LangGraph, [see here](https://langchain-ai.github.io/langgraph/concepts/low_level/?h=configuration#configuration).

2. **Extend the graph**: The core logic of the application is defined in [graph.py](./src/agent/graph.py). You can modify this file to add new nodes, edges, or change the flow of information.

## Development

While iterating on your graph in LangGraph Studio, you can edit past state and rerun your app from previous states to debug specific nodes. Local changes will be automatically applied via hot reload.

Follow-up requests extend the same thread. You can create an entirely new thread, clearing previous history, using the `+` button in the top right.

For more advanced features and examples, refer to the [LangGraph documentation](https://langchain-ai.github.io/langgraph/). These resources can help you adapt this template for your specific use case and build more sophisticated conversational agents.

LangGraph Studio also integrates with [LangSmith](https://smith.langchain.com/) for more in-depth tracing and collaboration with teammates, allowing you to analyze and optimize your chatbot's performance.

<!--
Configuration auto-generated by `langgraph template lock`. DO NOT EDIT MANUALLY.
{
  "config_schemas": {
    "agent": {
      "type": "object",
      "properties": {}
    }
  }
}
-->
