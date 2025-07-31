# 🛍️ PriceHunt

A **Model Context Protocol (MCP)** implementation that finds the lowest-priced products with good ratings (4+ stars) across major Pakistani e-commerce platforms including Daraz, Telemart, and iShopping.


## MCP

**Model Context Protocol (MCP)** is a standardized protocol that enables AI applications to securely connect to external data sources and tools. It acts as a bridge between AI models (like Gemini) and various services, databases, APIs, and applications.

### MCP Architecture Components:
- **MCP Servers** - Provide specific tools, resources, or data to clients
- **MCP Clients** - AI applications that want to access external resources  
- **Transport Layer** - Communication mechanism between clients and servers

## 🎯 Project Overview

This project demonstrates MCP implementation by creating:
1. **MCP Server**: Provides three tools for scraping Pakistani e-commerce sites
2. **MCP Client**: Uses LangChain + Google Gemini to orchestrate tool calls
3. **Streamlit Frontend**: User-friendly web interface for product searches

**Note**: In this project both server and client run on the same host for learning purposes.

## ✨ Features

- 🔍 **Multi-Platform Search**: Scrapes Daraz, Telemart, and iShopping simultaneously
- ⭐ **Quality Filtering**: Prioritizes products with 4+ star ratings
- 💰 **Price Search**: Finds the lowest-priced genuine products
- 🤖 **AI-Powered**: Uses Google Gemini for intelligent product matching
- 💬 **Chat Interface**: Conversational UI with memory
- 🚀 **Async Processing**: Non-blocking operations for better performance


<img width="1366" height="671" alt="PriceHunt" src="https://github.com/user-attachments/assets/19b36d89-77cc-4295-b9aa-44d51d098e0c" />



## 🏛️ MCP Architecture

### This Project's MCP Implementation:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   MCP Client    │    │   MCP Server    │
│   Frontend      │◄──►│  (LangChain +   │◄──►│   (FastMCP)     │
│   (app.py)      │    │   Gemini)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   E-commerce    │
                                               │   Websites      │
                                               │ • Daraz.pk      │
                                               │ • Telemart.pk   │
                                               │ • iShopping.pk  │
                                               └─────────────────┘
```


### MCP Tools Defined:
1. **`get_daraz_products(query)`** - Scrapes Daraz with 4+ rating filter
2. **`get_telemart_products(query)`** - Scrapes Telemart search results  
3. **`get_ishopping_products(query)`** - Scrapes iShopping catalog


## 📁 Project Structure

```
PriceHunt-MCP/
├── project/             # Client-side code
│   └── app.py              # Streamlit web interface
|   └── mcp_client.py          # MCP Client with LangChain integration
|   └── mcp_server.py          # MCP Server with 3 e-commerce tools
├── python-version         # Python version specification
├── pyproject.toml         # Python project configuration
├── README.md             # This file
└── uv.lock               # UV dependency lock file
```



## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/FassihShah/PriceHunt-MCP.git
cd PriceHunt-MCP
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies
Since we're using `uv`, install dependencies with:
```bash
# If using uv (recommended)
uv install

# Or using pip with requirements.txt
pip install -r requirements.txt
```

**If you don't have `uv` installed:**
```bash
# Install uv first
pip install uv
# Then install dependencies
uv install
```


### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```


## 🖥️ Using with Claude Desktop

This MCP server can also be integrated directly with **Claude Desktop** application, allowing to use the e-commerce tools directly in your conversations with Claude!

### Setup for Claude Desktop:

**1. Install Claude Desktop:**
- Download from [Claude Desktop](https://claude.ai/download)
- Make sure you have the latest version

**2. Configure Claude Desktop:**
Open the Claude Desktop configuration file:


**Windows:**
```bash
code %APPDATA%\Claude\claude_desktop_config.json
```

**3. Add Your MCP Server:**
Create or update the `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "ecommerce-scraper": {
      "command": "python",
      "args": ["/path/to/your/project/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

Once configured, you can directly ask Claude things like:
- "Find me the cheapest Ronin Earbuds"

Claude will automatically use these MCP tools to scrape the websites and provide results!


## 🎮 Usage

### Method 1: Claude Desktop Integration
After setting up Claude Desktop configuration (see section above)

### Method 2: Streamlit Web Interface
```bash
streamlit run app.py
```

### Method 3: MCP Inspector (Development & Testing)
Use the official MCP Inspector to test and debug your server:

```bash
uv run mcp dev mcp_server.py
```

This will:
- **Launch a web interface**
- **Test all your tools** interactively
- **View tool schemas** and parameters


## 📚 Learning Outcomes

This project demonstrates:
- **MCP Protocol**: Understanding of server/client architecture
- **AI Integration**: LangChain + LLM tool orchestration
- **Async Programming**: Non-blocking operations
