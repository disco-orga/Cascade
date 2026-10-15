from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from component import Component

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable
from backends.backend import Backend

@dataclass
class Step:
    pass

class Executable(ABC):
    def process(self, backend):
        pass

@dataclass
class Workflow(Executable):
    steps: list[Step]

    def process(self, backend):
        for step in self.steps:
            step.process(backend)
            
@dataclass
class Deploy(Step):
    comp: Component
    node: str

    def process(self, backend):
        backend.deploy(self.comp, self.node)
        

@dataclass
class Do(Step):
    action: Callable[[Backend], None]

    def process(self, backend):
        self.action(backend)

@dataclass
class ParallelGroup(Executable):
    workflows: list[Workflow]
    max_concurrency: int

    def process(self, backend):
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def exec_one_workflow(workflow):
            workflow.process(backend)

        max_concurrency = len(self.workflows) if self.max_concurrency <= 0 else self.max_concurrency
        
        with ThreadPoolExecutor() as ex:
            futures = []
            i = 0
            while len(futures) < max_concurrency and i < len(self.workflows):
                futures.append(ex.submit(exec_one_workflow, self.workflows[i]))
                i += 1

            while i < len(self.workflows):
                done_future = next(as_completed(futures))
                futures.remove(done_future)
                futures.append(ex.submit(exec_one_workflow, self.workflows[i]))
                i += 1

            for future in futures:
                future.result()
            

@dataclass
class WaitFor(Step):
    port: int
    host: str
    timeout: float

    def process(self, backend):
        backend.wait_for(self.host, self.port, self.timeout)
