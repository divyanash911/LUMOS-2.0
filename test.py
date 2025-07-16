from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import json
import uvicorn
import re

app = FastAPI()

class UserRequest(BaseModel):
    user_prompt: str
    
@app.post("/generate_tool")
async def generate_tool(request: UserRequest):
    OPENAI_API_KEY = ""
    prompt =f'''
    You are a tool generator for Agentic systems and are asked to generate a tool for the user strictly in the given example format. Wrap the tool name in double quotes and provide the description, input, and output in the specified format. Provide it in a json parsable format. The keys of the parameter object depend on the type of Tool.
    Example Tool:
        {{
            "name": "Code Analyzer",
            "description": "Extracts information from source code",
            "type": "Information",
            "subtype": "Parser",
            "parameters":{{
                "language": "Python",
                "code":"(Source code to be analyzed)",
                "output_format": "json"
            }}
        }}
    
    User: {request.user_prompt}
    '''
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        message = response.choices[0].message.content.strip()
        print("Generated Tool:", message)
        message = re.sub(r"^```json\n|```$", "", message.strip())
        return {"tool": json.loads(message)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/generate_agent")
async def generate_agent(request: UserRequest):
    OPENAI_API_KEY = ""
    prompt =f'''
    You are a an agent generator and are asked to generate an agent for the user strictly in the given example format. The description should be detailed and must list down an exhaustive list of capabilities. Wrap the Agent name in double quotes and provide the description, capabilities and suggested tools in the specified format. Provide it in a json parsable format. The suggested tools depend on the task of the agent.  
    Example Agent:
        {{
            "name": "Documentation Writer",
            "description": "Creates initial documentation drafts for Software Engineering format and follows proper formatting along with content generation. It also has text summarization capabilities.",
            "type": "AI",
            "subtype": "LLM",
            "capabilities": [
                "contentGeneration", 
                "textSummarization", 
                "formatting"
            ],
            "memory": {{
                "type": "Vector",
                "capacity": "1GB",
                "persistence": true,
                "storage": "Database"
            }},
            suggested_tools: {{
                "GrammarChecker": "Checks for grammatical correctness, sentence structure, and clarity in the documentation.",
                "PlagiarismDetector": "Ensures the generated documentation is original and not copied from external sources.",
                "MarkdownFormatter": "Formats the documentation into proper Markdown syntax, useful for README files and wikis.",
                "PDFExporter": "Exports finalized documentation to PDF format for easy sharing and publishing.",
                "TextSummarizer": "Summarizes long paragraphs or documents into concise descriptions or TL;DR sections.",
            }}
        }},
    
    User: {request.user_prompt}
    '''
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        message = response.choices[0].message.content.strip()
        print("Generated Agent:", message)
        message = re.sub(r"^```json\n|```$", "", message.strip())
        return {"agent": json.loads(message)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("description:app", host="127.0.0.1", port=8000, reload=True)