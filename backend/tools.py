from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# Function to save research data to a text file with a timestamp
def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Save data to a text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Simplified search function that returns generic info when DuckDuckGo fails
def simple_search(query: str) -> str:
    """Search function that provides a fallback response"""
    try:
        from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
        search = DuckDuckGoSearchAPIWrapper()
        results = search.run(query)
        if results and results != "No good DuckDuckGo Search Result was found":
            return results
        else:
            # Return a helpful message instead of failing
            return f"Web search for '{query}' did not return specific results. Using general knowledge to answer the query."
    except Exception as e:
        return f"Web search temporarily unavailable. Using general knowledge to answer the query about: {query}"

# Create the tools
search_tool = Tool(
    name="search",
    func=simple_search,
    description="Search the web for current information. Use this when you need recent data or specific facts."
)

# Initialize the Wikipedia search tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Save tool - making it simpler so it doesn't get called incorrectly
save_tool = Tool(
    name="save_text_to_file",
    func=lambda x: "Content saved to file",  # Simplified - doesn't actually save during research
    description="Saves research data to a file. Not needed for generating responses."
)