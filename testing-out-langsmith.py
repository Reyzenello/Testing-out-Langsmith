import requests
from langchain_openai import OpenAI

# Configuration for OpenAI GPT
openai_config = {
    "api_key": "your_openai_key",
    "model_name": "text-davinci-003"
}

# Initialize the OpenAI language model
llm = OpenAI(api_key=openai_config["api_key"], model_name=openai_config["model_name"])

class LangGraph:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_node(self, node_id, prompt, responses):
        data = {"prompt": prompt, "responses": responses}
        response = requests.post(f"{self.base_url}/add_node/?node_id={node_id}", json=data)
        return response.json()

    def get_node(self, node_id):
        response = requests.get(f"{self.base_url}/get_node/{node_id}")
        return response.json()

# Initialize LangGraph
lang_graph = LangGraph("http://localhost:8000")

# Define a simple prompt and response graph
prompts_responses = {
    "start": {
        "prompt": "Hi, how can I assist you today?",
        "responses": {
            "I need help with my account": "Sure, what exactly do you need help with regarding your account?",
            "Tell me a joke": "Why don't scientists trust atoms? Because they make up everything!"
        }
    },
    "account_help": {
        "prompt": "Sure, what exactly do you need help with regarding your account?",
        "responses": {
            "I forgot my password": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
            "How do I update my profile?": "You can update your profile by going to the account settings page."
        }
    }
}

# Add nodes to LangGraph
for node, content in prompts_responses.items():
    lang_graph.add_node(node, content["prompt"], content["responses"])

# Define a function to simulate a conversation
def simulate_conversation(lang_graph, llm, user_inputs):
    current_node = "start"
    for user_input in user_inputs:
        node = lang_graph.get_node(current_node)
        if node and "prompt" in node and "responses" in node:
            print(f"Agent: {node['prompt']}")
            print(f"User: {user_input}")
            response_key = next((key for key in node["responses"].keys() if key.lower() in user_input.lower()), None)
            if response_key:
                response = node["responses"][response_key]
                print(f"Agent: {response}")
                current_node = response_key
            else:
                print("Agent: I'm sorry, I didn't understand that.")
        else:
            print("Agent: I'm not sure how to help with that.")
            break

# Simulate a conversation
user_inputs = [
    "Hi",
    "I need help with my account",
    "I forgot my password"
]

simulate_conversation(lang_graph, llm, user_inputs)
