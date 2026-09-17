# Copyright (c) Microsoft. All rights reserved.

import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    model_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL_NAME")
    if not model_name:
        raise RuntimeError(
            "Model deployment name is not configured. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME or FOUNDRY_MODEL_NAME."
        )

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model_name,
        credential=DefaultAzureCredential(),
    )

    instructions = (
        "Você é o WashingtonProNet AI Agent, um assistente inteligente, ágil e prestativo "
        "hospedado no Microsoft Azure AI Foundry.\n"
        "Diretrizes principais:\n"
        "- Responda prioritariamente em português do Brasil de forma clara, educada e estruturada com Markdown.\n"
        "- Atue como especialista em desenvolvimento de software, automações, Python, PowerShell, Cloud (Azure & GCP) e DevOps.\n"
        "- Seja direto e prático, fornecendo explicações pontuais e exemplos de código sempre que relevante."
    )

    agent = Agent(
        client=client,
        instructions=instructions,
        # History will be managed by the hosting infrastructure, thus there
        # is no need to store history by the service. Learn more at:
        # https://developers.openai.com/api/reference/resources/responses/methods/create
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
