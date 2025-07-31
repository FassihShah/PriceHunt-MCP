import asyncio
import streamlit as st
from mcp_client import MCPClient  

if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = MCPClient()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="E-Commerce AI Assistant", layout="centered")

st.title("🛍️ E-Commerce Price Finder (Pakistan)")
query = st.text_input("Ask me to find a product:", placeholder="e.g., iPhone 13, earbuds, smart watch...")

search_button = st.button("Search")


async def handle_query():
    client = st.session_state.mcp_client

    if not client.session:
        await client.connect_to_server("mcp_server.py") 

    await client.run_chat(query)
    st.session_state.chat_history = client.memory


if search_button and query.strip():
    with st.spinner("🔍 Searching Daraz, Telemart, and others.."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(handle_query())
        loop.close()



if st.session_state.chat_history:
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        if msg.type == "human":
            st.markdown(f"👤 **You:** {msg.content}")
        elif msg.type == "ai":
            st.markdown(f"🤖 **Gemini:** {msg.content}")
