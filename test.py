"""
this is the file containig Tools & Dependency Injection Example usign pydantic 
"""

import asyncio
from pydantic_ai import Agent, RunContext 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from dataclasses import dataclass
from user_detaisl import get_user_name, get_user_region
import os
load_dotenv()

@dataclass
class SupportDependancies:
    user_id: str
    summarization_length: str

class SupportResult(BaseModel):
    respond_to_user: str = Field(description="llm's respond to user")
    summarization_length: str = Field(description="what type of summarizatoin user has applied")
    summarizatio: str = Field(description="summzarization of given prompt")
    native_translation: str = Field(description="Translatoin of the given user input into the native langauge")


support_agent = Agent( "google-gla:gemini-1.5-flash",
    result_type=SupportResult, 
    # result_retries=3,
    deps_type=SupportDependancies,
    system_prompt=(
        "you are a summarizer and you have to summarise the proivded thing into the given length"
        "also findout the native language of the user based on his native city or native country"
        "and translate the whole summarised content into user's native language"
    )
)

@support_agent.tool
async def get_users_name(cnx: RunContext[SupportDependancies]):
    user_name = await get_user_name(cnx.deps.user_id) 
    return user_name    
    # return f"user name is :{user_name}"


@support_agent.system_prompt
async def get_users_region(cnx: RunContext[SupportDependancies]):

    return f"Users' native region is : {await get_user_region(cnx.deps.user_id)}"


async def main():

    dep = SupportDependancies(user_id="12345",summarization_length="long")
    response = await support_agent.run("here is a paregraph : 'Before diving into the technical details, I want to summarize the key approach: We'll create a WhatsApp bot using Python that leverages AI to respond to your friend Diya in your style based on your previous conversations. This system will require conversation data collection, AI model training, WhatsApp integration, and deployment'", deps=dep)
    # response = await support_agent.run("what is name of user? ", deps=dep)
    print(response.data)


if __name__ == "__main__": 
    asyncio.run(main()) 