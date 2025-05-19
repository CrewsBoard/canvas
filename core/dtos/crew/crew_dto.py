from crewai import Process

from core.dtos.base.base_dto import BaseDto


class CrewDto(BaseDto):
    name: str
    process: Process = Process.sequential
    verbose: bool = False
