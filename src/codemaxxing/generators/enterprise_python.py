"""Enterprise Python code generator.

Synthesizes diverse enterprise Python modules across multiple distinct architectural archetypes:
async FastAPI-style microservices, descriptor-driven metaprogramming engines,
Python 3.10+ structural pattern matching pipelines, and low-level introspection machines.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class EnterprisePythonGenerator(SlopGenerator):
    """Enterprise Python code generator.

    Emits Python source modules featuring extensive structural ceremony across
    four varied archetypes: async microservices, descriptor metaclasses,
    dataclass pattern matchers, and reflective introspection engines.
    """

    name = "enterprise_python"
    language = "python"
    extension = ".py"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic enterprise Python source file (.py).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Python source code.
        """
        buf = StringIO()
        cname = naming.class_name(sanity)
        module_name = cname.lower()

        buf.write(f'"""\n{comments.docstring(sanity, cname)}\n\n')
        buf.write(f"Module: {module_name}\n")
        buf.write(f'"""\n\n')

        archetype = random.choice([
            "async_fastapi_engine",
            "metaclass_descriptor_magic",
            "pattern_matching_dataclass",
            "scientific_introspection_chaos",
        ])

        if archetype == "async_fastapi_engine":
            self._generate_async_engine(buf, sanity, cname)
        elif archetype == "metaclass_descriptor_magic":
            self._generate_metaclass_engine(buf, sanity, cname)
        elif archetype == "pattern_matching_dataclass":
            self._generate_pattern_matching(buf, sanity, cname)
        else:
            self._generate_introspection_chaos(buf, sanity, cname)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"python/{module_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_async_engine(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit an async microservice engine with asyncio queues and typed models."""
        buf.write("from __future__ import annotations\n\n")
        buf.write("import asyncio\nimport logging\nimport uuid\nfrom typing import Any, AsyncIterator, Optional\n")
        buf.write("from dataclasses import dataclass, field\n\n")
        buf.write("logger = logging.getLogger(__name__)\n\n\n")

        # Pydantic-like dataclass
        payload_name = f"{cname}Payload"
        buf.write(f"@dataclass(slots=True)\nclass {payload_name}:\n")
        buf.write(f'    """{comments.docstring(sanity, payload_name)}"""\n')
        buf.write(f"    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))\n")
        buf.write(f"    payload: dict[str, Any] = field(default_factory=dict)\n")
        buf.write(f"    is_active: bool = True\n")
        buf.write(f"    retry_budget: int = 3\n\n\n")

        # Async engine class
        buf.write(f"class {cname}:\n")
        buf.write(f'    """{comments.docstring(sanity, cname)}"""\n\n')
        buf.write(f"    def __init__(self, concurrency_limit: int = 16) -> None:\n")
        buf.write(f"        self._queue: asyncio.Queue[{payload_name}] = asyncio.Queue(maxsize=1024)\n")
        buf.write(f"        self._semaphore = asyncio.Semaphore(concurrency_limit)\n")
        buf.write(f"        self._running = False\n")
        buf.write(f"        self._metrics: dict[str, int] = {{'processed': 0, 'errors': 0}}\n\n")

        # Async context manager
        buf.write(f"    async def __aenter__(self) -> {cname}:\n")
        buf.write(f"        self._running = True\n")
        buf.write(f"        logger.info('Started async engine: {cname}')\n")
        buf.write(f"        return self\n\n")
        buf.write(f"    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:\n")
        buf.write(f"        self._running = False\n")
        buf.write(f"        await self.drain()\n\n")

        # Async methods
        for _ in range(random.randint(3, 5)):
            mname = naming.method_name(sanity)
            var_arg = naming.var_name(sanity)
            buf.write(f"    async def {mname}(self, {var_arg}: {payload_name}) -> Optional[dict[str, Any]]:\n")
            buf.write(f'        """{comments.comment(sanity)}"""\n')
            buf.write(f"        async with self._semaphore:\n")
            buf.write(f"            if not self._running:\n")
            buf.write(f"                raise RuntimeError('{cname} engine is stopped')\n")
            buf.write(f"            # {comments.comment(sanity)}\n")
            buf.write(f"            await self._queue.put({var_arg})\n")
            buf.write(f"            self._metrics['processed'] += 1\n")
            buf.write(f"            return {{'status': 'ACK', 'id': {var_arg}.correlation_id}}\n\n")

        # Async generator
        buf.write(f"    async def stream_events(self) -> AsyncIterator[{payload_name}]:\n")
        buf.write(f"        while self._running or not self._queue.empty():\n")
        buf.write(f"            try:\n")
        buf.write(f"                event = await asyncio.wait_for(self._queue.get(), timeout=0.1)\n")
        buf.write(f"                yield event\n")
        buf.write(f"                self._queue.task_done()\n")
        buf.write(f"            except asyncio.TimeoutError:\n")
        buf.write(f"                continue\n\n")

        buf.write(f"    async def drain(self) -> None:\n")
        buf.write(f"        await self._queue.join()\n")
        buf.write(f"        logger.info(f'Drained {cname} successfully')\n")

    def _generate_metaclass_engine(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit advanced metaprogramming with custom descriptors and __init_subclass__."""
        buf.write("from typing import Any, Callable, TypeVar, Generic\n")
        buf.write("import functools\n\n")

        descriptor_name = f"{cname}Descriptor"
        buf.write(f"class {descriptor_name}:\n")
        buf.write(f'    """{comments.docstring(sanity, descriptor_name)}"""\n\n')
        buf.write(f"    def __set_name__(self, owner: type, name: str) -> None:\n")
        buf.write(f"        self.private_name = f'_{{name}}'\n\n")
        buf.write(f"    def __get__(self, instance: Any, owner: type) -> Any:\n")
        buf.write(f"        if instance is None:\n")
        buf.write(f"            return self\n")
        buf.write(f"        return getattr(instance, self.private_name, None)\n\n")
        buf.write(f"    def __set__(self, instance: Any, value: Any) -> None:\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write(f"        setattr(instance, self.private_name, value)\n\n\n")

        meta_name = f"{cname}Meta"
        buf.write(f"class {meta_name}(type):\n")
        buf.write(f"    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type:\n")
        buf.write(f"        attrs['_registry'] = {{k: v for k, v in attrs.items() if not k.startswith('_')}}\n")
        buf.write(f"        return super().__new__(mcs, name, bases, attrs)\n\n\n")

        buf.write(f"class {cname}(metaclass={meta_name}):\n")
        buf.write(f'    """{comments.docstring(sanity, cname)}"""\n\n')
        for _ in range(random.randint(3, 6)):
            field_name = naming.var_name(sanity)
            buf.write(f"    {field_name} = {descriptor_name}()\n")
        buf.write("\n")

        buf.write(f"    def __init_subclass__(cls, **kwargs: Any) -> None:\n")
        buf.write(f"        super().__init_subclass__(**kwargs)\n")
        buf.write(f"        cls._is_subclassed = True\n\n")

        for _ in range(random.randint(3, 5)):
            mname = naming.method_name(sanity)
            buf.write(f"    def {mname}(self, *args: Any, **kwargs: Any) -> dict[str, Any]:\n")
            buf.write(f'        # {comments.comment(sanity)}\n')
            buf.write(f"        return {{'method': '{mname}', 'args_count': len(args), 'kwargs': list(kwargs.keys())}}\n\n")

    def _generate_pattern_matching(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit Python 3.10+ match/case structural pattern matching with dataclasses."""
        buf.write("from dataclasses import dataclass\n")
        buf.write("from typing import Union\n\n")

        state_a = f"{cname}InitialState"
        state_b = f"{cname}ProcessingState"
        state_c = f"{cname}CompletedState"

        buf.write(f"@dataclass(frozen=True)\nclass {state_a}:\n    token: str\n\n")
        buf.write(f"@dataclass(frozen=True)\nclass {state_b}:\n    token: str\n    depth: int\n\n")
        buf.write(f"@dataclass(frozen=True)\nclass {state_c}:\n    token: str\n    result_code: int\n\n")

        buf.write(f"StateUnion = Union[{state_a}, {state_b}, {state_c}]\n\n\n")

        buf.write(f"class {cname}:\n")
        buf.write(f'    """{comments.docstring(sanity, cname)}"""\n\n')

        mname = naming.method_name(sanity)
        buf.write(f"    def {mname}(self, state: StateUnion) -> StateUnion:\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write(f"        match state:\n")
        buf.write(f"            case {state_a}(token=t):\n")
        buf.write(f"                return {state_b}(token=t, depth=1)\n")
        buf.write(f"            case {state_b}(token=t, depth=d) if d < 5:\n")
        buf.write(f"                return {state_b}(token=t, depth=d + 1)\n")
        buf.write(f"            case {state_b}(token=t, depth=_):\n")
        buf.write(f"                return {state_c}(token=t, result_code=200)\n")
        buf.write(f"            case {state_c}(token=_, result_code=_):\n")
        buf.write(f"                return state\n")
        buf.write(f"            case _:\n")
        buf.write(f"                raise ValueError(f'Unknown state: {{state}}')\n\n")

        for _ in range(random.randint(2, 4)):
            sub_m = naming.method_name(sanity)
            buf.write(f"    def {sub_m}(self, raw_input: str) -> StateUnion:\n")
            buf.write(f"        # {comments.comment(sanity)}\n")
            buf.write(f"        initial = {state_a}(token=raw_input)\n")
            buf.write(f"        return self.{mname}(initial)\n\n")

    def _generate_introspection_chaos(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit low-level introspection and memoized recursive functions."""
        buf.write("import sys\nimport functools\nfrom typing import Any\n\n")

        func_name = naming.method_name(sanity)
        buf.write(f"@functools.lru_cache(maxsize=1024)\n")
        buf.write(f"def {func_name}(depth: int) -> int:\n")
        buf.write(f'    """{comments.docstring(sanity, func_name)}"""\n')
        buf.write(f"    if depth <= 1:\n")
        buf.write(f"        return 1\n")
        buf.write(f"    # {comments.comment(sanity)}\n")
        buf.write(f"    frame = sys._getframe()\n")
        buf.write(f"    _ = frame.f_code.co_name\n")
        buf.write(f"    return ({func_name}(depth - 1) + depth) % 65536\n\n\n")

        buf.write(f"class {cname}:\n")
        buf.write(f'    """{comments.docstring(sanity, cname)}"""\n\n')
        buf.write(f"    def __init__(self) -> None:\n")
        buf.write(f"        self._shadow = bytearray(b'{comments.comment(sanity)[:32]}')\n")
        buf.write(f"        self._history = [x ** 2 for x in range(16) if x % 2 == 0]\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    def {mname}(self, seed: int) -> dict[str, Any]:\n")
        buf.write(f"        calc = {func_name}(seed % 32)\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write(f"        return {{\n")
        buf.write(f"            'result': calc,\n")
        buf.write(f"            'shadow_len': len(self._shadow),\n")
        buf.write(f"            'history': self._history,\n")
        buf.write(f"        }}\n")
