from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import os
import time
import json

load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize LLM and parser
llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=2000)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create prompt template (same as your main.py)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
             You are a comprehensive research assistant that generates detailed, well-structured research summaries.
            
            IMPORTANT INSTRUCTIONS:
            1. Create a COMPREHENSIVE summary with multiple sections and subsections
            2. Use clear headings with numbers (1., 2., etc.) and subheadings with letters or bullets
            3. Include detailed explanations, not just brief overviews
            4. Each main section should have 3-5 detailed points
            5. The summary should be AT LEAST 300-500 words
            6. Format with proper structure: Main points → Sub-points → Details
            7. Include specific examples, steps, or strategies where relevant
            
            CRITICAL FORMATTING RULES:
            - DO NOT use ## for headers (just use plain text with numbers)
            - DO NOT use ** for bold text (just use plain text)
            - DO NOT use any Markdown symbols (no **, __, ##, ###, etc.)
            - Use only plain text with proper indentation and line breaks
            
            Example structure (plain text only):
            
            1. Section Title
               - Detailed point with explanation
               - Another detailed point
               
            2. Another Section
               A. Subsection
                  - Comprehensive explanation
                  - Specific examples or steps
               B. Another Subsection
                  - More details
            
            TOOL USAGE:
            - Use Wikipedia for foundational knowledge
            - Use search for current information when available
            - If search fails, rely on your training knowledge to provide comprehensive answers
            - DO NOT use the save_text_to_file tool during research
            
            Even if tools return limited results, you should still provide a comprehensive,
            detailed answer based on your training knowledge about the topic.
            
            Remember: NO MARKDOWN FORMATTING. Use only plain text with numbers, letters, and dashes.
            
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Initialize tools and agent (same as your main.py)
tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Health check endpoint - GET /api/health
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "FusionAI API is running"}), 200

# Research endpoint - POST /api/research with {"query": "topic"}
@app.route('/api/research', methods=['POST'])
def research():
    """Main research endpoint - optimized LangChain implementation"""
    try:
        # Get and validate query
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
        
        query = data['query'].strip()
        
        if len(query) < 3:
            return jsonify({"error": "Query too short"}), 400
        
        print(f"\n{'='*60}")
        print(f"🔍 Research Request: {query}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Execute agent with timeout
        try:
            response = agent_executor.invoke(
                {"query": query, "chat_history": []},
                config={"max_execution_time": 30}
            )
        except Exception as agent_error:
            print(f"⚠️  Agent execution error: {agent_error}")
            return jsonify({
                "topic": query.title(),
                "summary": f"Research completed with limited information: {str(agent_error)}",
                "sources": ["Research attempted"],
                "tools_used": ["error"]
            }), 200
        
        # Extract output
        output = response.get('output', '')
        
        # Clean output - handle different response formats
        if isinstance(output, list):
            # If it's a list, get the first item
            output = output[0] if output else ''
            
        # If output is a dict with 'text' field (LangChain structure)
        if isinstance(output, dict):
            output = output.get('text', str(output))

        # Convert to string
        output = str(output).strip()

        # Remove markdown code blocks
        output = output.replace('```json', '').replace('```', '').strip()
        
        # Remove any leading/trailing newlines and whitespace
        output = output.strip('\n').strip()
        
        print(f"\n📊 Output length: {len(output)} chars")
        print(f"📄 Preview: {output[:200]}...")
        
        # Parse response with improved error handling
        try:
            structured_response = parser.parse(output)
            print(f"✅ Successfully parsed response")
        except Exception as parse_error:
            print(f"⚠️  Initial parsing failed: {parse_error}")
            
            # Try to extract JSON manually
            try:
                # Find JSON in output
                start_idx = output.find('{')
                end_idx = output.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = output[start_idx:end_idx]
                    print(f"📄 Extracted JSON: {json_str[:200]}...")
                    data = json.loads(json_str)
                    structured_response = ResearchResponse(**data)
                    print(f"✅ Successfully parsed extracted JSON")
                else:
                    raise ValueError("No JSON found in output")
            except Exception as extraction_error:
                print(f"⚠️  JSON extraction also failed: {extraction_error}")
                # Last resort fallback
                return jsonify({
                    "topic": query.title(),
                    "summary": output if len(output) < 5000 else output[:5000] + "...",
                    "sources": ["Research completed"],
                    "tools_used": ["langchain", "claude-ai"]
                }), 200
        
        # Convert to dictionary
        result = {
            "topic": structured_response.topic,
            "summary": structured_response.summary,
            "sources": structured_response.sources,
            "tools_used": structured_response.tools_used
        }
        
        elapsed = time.time() - start_time
        print(f"\n✅ Research completed in {elapsed:.2f} seconds")
        print(f"{'='*60}\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    # Get port from environment variable, default to 5000
    port = int(os.getenv('PORT', 5000))
    # Print startup messages
    print(f"\n🚀 Server starting on http://localhost:{port}")
    print(f"📍 Test health check: http://localhost:{port}/api/health\n")
    # Start Flask server (host, port, debug mode)    
    app.run(host='0.0.0.0', port=port, debug=True)