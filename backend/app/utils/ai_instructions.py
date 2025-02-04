has_no_answer_token = "i do not know"
instructions_array = [
    "You are a helpful AI assistant please follow the following instructions carefully",
    "Instructions:",
    "- Only answer questions related to user inputs and be more specific.",
    f"- If you're unsure of an answer, respond with '{has_no_answer_token}' only.",
    "- If a prompt starts with 'I'm your internet assistant,' it means the information comes from an agent helping to provide more details about the user's request.",
    "- When given context from the 'internet assistant' (marked between $$), respond directly with the answer, no need for introductions like 'Based on the information provided.'",
    "- If you’re asked a question based on the 'internet assistant' context and don’t know the answer, just provide the context as-is and mention that this is all the information you have."
]
assistant_instructions = '\n'.join(instructions_array)

def assistant_prompt(web_results):
    return f"I'm your internet assistant, Based on my online research, here’s a list of useful results. Please try to extract the most accurate answer from the provided information. If you’re unsure, present the results as they are. here is the search result: $$ {web_results} $$"