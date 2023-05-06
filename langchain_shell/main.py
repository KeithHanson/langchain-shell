import typer
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import load_tools, get_all_tool_names
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)

def main(list_agents: bool = False, agent: str = "LLMSingleActionAgent", verbose: bool = False, list_tools: bool = False):
    """Langchain: A tool for automating language tasks"""
    if list_agents:
        known_agents()
        return

    if list_tools:
        known_tools()
        return

    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm, verbose=verbose)
    
    first_line = "Talk to the AI!\n"
    while(True):
        human_input = typer.prompt(first_line, prompt_suffix="<human>:")
        first_line = ""
        print(conversation.predict(input=human_input))

    raise NotImplementedError

def known_agents():
    for agent in AgentType:
        print(f"{agent.name} - {agent.value}")

def known_tools():
    for tool in get_all_tool_names():
        print(f"{tool}")


def __main__():
    typer.run(main)

if __name__ == "__main__":
    typer.run(main)
