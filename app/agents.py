from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import GOOGLE_API_KEY
from app.tools import get_project_structure, read_project_files

# Use Gemini 1.5 Pro or Flash depending on your token limits
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI Technical Writer. Your task is to generate a professional, comprehensive README.md file for a codebase.
    
    CRITICAL REQUIREMENTS:
    1. Write a Project Title and clear Description.
    2. Provide an 'Architecture / Project Structure' section explaining the key files.
    3. Provide an 'Installation & Setup' guide.
    4. Provide 'Usage Instructions'.
    5. EDGE CASE HANDLING: If code appears incomplete or stubbed out, acknowledge it gracefully in a 'Future Work' section rather than hallucinating functionality.
    
    Output ONLY valid Markdown."""),
    ("human", """Here is the Project Directory Structure:
    {structure}
    
    Here are the contents of the files:
    {contents}""")
])

chain = prompt_template | llm

def run_readme_agent(folder_path: str) -> str:
    """Executes the tools to gather context, then calls the LLM."""
    print(f"Scanning directory: {folder_path}...")
    
    # Execute our defined LangChain tools
    structure = get_project_structure.invoke({"folder_path": folder_path})
    contents = read_project_files.invoke({"folder_path": folder_path})
    
    print("Generating README via Gemini...")
    response = chain.invoke({
        "structure": structure,
        "contents": contents
    })
    
    return response.content