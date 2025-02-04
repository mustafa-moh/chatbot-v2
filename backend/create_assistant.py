from openai import AzureOpenAI
from openai import OpenAI
from config import Config

# client = AzureOpenAI(
#     api_key=Config.AZURE_OPENAI_API_KEY,
#     api_version="2024-07-01-preview",
#     azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
# )

client = OpenAI(api_key=Config.OPENAI_API_KEY)

assistant = client.beta.assistants.create(
    name="Chatbot Assistant",
    instructions=(
        "You are a helpful assistant that answers user questions accurately and concisely. "
        "If you don’t know the answer or if the information might be outdated, use the 'search_internet' function "
        "to retrieve real-time data. The 'search_internet' function accepts a 'query' parameter. "
        "When using this function, try to generate a clear and concise search query based on the user's prompt "
        "for better search results. If the user's prompt is already suitable as a query, pass it as it is. "
        "After retrieving search results, summarize them clearly, focusing on the most relevant information. "
        "Avoid guessing answers. If the search results are unclear, inform the user politely. "
        "Avoid appending any dates to the 'query' parameter by your self. "
    ),
    model="gpt-4o",
    tools=[{
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Search for real-time information over the internet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query based on the user's question, for example 'latest AI regulations'"
                    }
                },
                "required": ["query"]
            }
        }
    }]
)

print(assistant.model_dump_json(indent=2))
