from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from tools import tools

load_dotenv()


class ResearchResponse(BaseModel):
    """Structured response for research output."""
    topic: str = Field(description="The research topic")
    summary: str = Field(description="Summary of the research findings")
    sources: list[str] = Field(description="List of sources used")
    tools_used: list[str] = Field(description="List of tools used during research")


# Initialize the model with structured output support
llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.7)

# Create system prompt
system_prompt = """
You are a research assistant that helps generate comprehensive research papers.
Follow these steps:
1. Analyze the user's research topic
2. Use the search_web tool to find current information
3. Use the wikipedia tool for background/historical information
4. Summarize your findings in a clear, structured format
5. Save the final research to a file using the save_to_txt tool

Always structure your final response as JSON with these fields:
- topic: The research topic
- summary: A comprehensive summary of findings (3-5 paragraphs)
- sources: List of sources you referenced
- tools_used: List of tools you used (e.g., ["search_web", "wikipedia", "save_to_txt"])

Be thorough, objective, and cite your sources clearly.
"""

# Create the agent using the new syntax
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

# Main execution
if __name__ == "__main__":
    query = input("Enter your research topic: ")
    
    print("\n🔍 Starting research...\n")
    
    # Stream the agent's responses
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        # Print the latest message
        if chunk.get("messages"):
            last_message = chunk["messages"][-1]
            if hasattr(last_message, 'content') and last_message.content:
                print(f"\n{last_message.content}")
    
    print("\n✅ Research completed!")