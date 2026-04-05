# Auto PPT Agent using MCP

## Overview

This project implements an Auto PPT Agent that automatically generates PowerPoint presentations from a user prompt.
The agent uses an LLM for planning and multiple MCP servers for execution.

## Features

* Accepts full presentation requirement from user
* Generates structured slide outline
* Creates slide bullet content
* Applies selectable presentation themes
* Saves planning outputs
* Generates downloadable PPT file
* Uses multiple MCP servers

## Architecture

User Input → LLM Planning → Filesystem MCP → PPT MCP → Generated Presentation

## MCP Servers Used

1. PPT MCP Server – creates slides and saves presentation
2. Filesystem MCP Server – stores outline and slide content

## Technologies Used

* Python
* Streamlit
* FastMCP
* Hugging Face LLM
* python-pptx

## How to Run

1. Install dependencies

```
pip install -r requirements.txt
```

2. Start PPT MCP server

```
fastmcp run mcp_servers/ppt_server.py:mcp --transport http --port 8000
```

3. Start filesystem MCP server

```
fastmcp run mcp_servers/filesystem_server.py:mcp --transport http --port 8002
```

4. Run Streamlit app

```
streamlit run app.py
```

## Example Prompt

Create a 6-slide presentation on machine learning for college students. Include supervised learning, unsupervised learning, real-world applications, advantages, and challenges. Use simple language.

## Output

* Generated PowerPoint presentation
* outline.json
* slide_content.json

##🎥 Demo Video:
https://drive.google.com/file/d/1SmevNjyNCbyqdaWVM6SGVRHKO1IWrUMU/view?usp=sharing
