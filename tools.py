from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime


@tool
def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """Saves structured research data to a text file.
    
    Args:
        data: The research data to save
        filename: The name of the file to save to (default: research_output.txt)
    
    Returns:
        A confirmation message with the filename
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"


@tool
def search_web(query: str) -> str:
    """Search the web for information using DuckDuckGo.
    
    Args:
        query: The search query
        
    Returns:
        Search results as a string
    """
    search = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper())
    return search.run(query)


# Wikipedia tool setup
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Export all tools as a list for easy import
tools = [save_to_txt, search_web, wiki_tool]