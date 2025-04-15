import asyncio
from typing import Optional, List

from crewai import Agent


class AgentFlow:
    def __init__(self, agent: Agent, flow_chain_id: str, output_event: asyncio.Event):
        self.agent = agent
        self.flow_chain_id = flow_chain_id
        self.output_event = output_event
        self.output_data = None
        self.flow_tasks: Optional[List[asyncio.Task]] = None
