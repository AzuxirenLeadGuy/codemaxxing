"""Generic chaotic Python generator.

Synthesizes absurd procedural anti-patterns, deeply nested control flows,
mock bytecode virtual machines, chaotic multi-table recursive SQL generators,
dependency injection graph mazes, and simulated deep neural tensor graphs.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class GenericGenerator(SlopGenerator):
    """Generic Python code generator demonstrating anti-patterns and extreme code bloat.

    Produces synthetic python source code filled with deeply nested conditional branches,
    wrapper layers, mock virtual machines, enterprise SQL builders, and neural graph pipelines.
    """

    name = "generic"
    language = "generic"
    extension = ".py"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a generic synthetic Python file (.py).

        Selects among slop archetypes ('nested_if', 'wrapper_hell', 'massive_enum',
        'fake_tests', 'bytecode_vm', 'sql_builder', 'di_graph', 'neural_pipeline', or 'mixed')
        to construct an output file.

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized generic Python code.
        """
        buf = StringIO()
        cname = naming.class_name(sanity)

        slop_types = [
            "nested_if",
            "wrapper_hell",
            "massive_enum",
            "fake_tests",
            "bytecode_vm",
            "sql_builder",
            "di_graph",
            "neural_pipeline",
            "mixed",
        ]
        chosen = random.choice(slop_types)

        if chosen == "nested_if":
            self._nested_if_else(buf, sanity, cname)
        elif chosen == "wrapper_hell":
            self._wrapper_hell(buf, sanity, cname)
        elif chosen == "massive_enum":
            self._massive_enum(buf, sanity, cname)
        elif chosen == "fake_tests":
            self._fake_tests(buf, sanity, cname)
        elif chosen == "bytecode_vm":
            self._bytecode_vm(buf, sanity, cname)
        elif chosen == "sql_builder":
            self._sql_builder(buf, sanity, cname)
        elif chosen == "di_graph":
            self._di_graph(buf, sanity, cname)
        elif chosen == "neural_pipeline":
            self._neural_pipeline(buf, sanity, cname)
        else:
            # Mixed archetype
            self._nested_if_else(buf, sanity, cname)
            self._bytecode_vm(buf, sanity, cname)
            self._fake_tests(buf, sanity, cname)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"generic/{cname.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _nested_if_else(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit a function with 10 to 25 levels of nested if-else statements."""
        buf.write(f"# {comments.comment(sanity)}\n\n\n")
        func_name = naming.method_name(sanity)
        buf.write(f"def {func_name}({naming.var_name(sanity)}, {naming.var_name(sanity)}, {naming.var_name(sanity)}):\n")
        buf.write(f'    """{comments.docstring(sanity, func_name)}"""\n')

        depth = random.randint(10, 25)
        for d in range(depth):
            indent = "    " * (d + 1)
            var = naming.var_name(sanity)
            condition = random.choice([
                f"{var} is not None",
                f"isinstance({var}, object)",
                f"len(str({var})) > 0",
                f"hash({var}) == hash({var})",
                f"type({var}) is type({var})",
                f"callable(getattr({var}, '__str__', None))",
                f"id({var}) > 0",
                f"any([True, bool({var})])",
                f"all([True, not False])",
                f"len(repr({var})) >= 0",
                f"getattr({var}, '__class__', None) is not None",
                f"hex(id({var})).startswith('0x')",
            ])
            buf.write(f"{indent}if {condition}:  # {comments.comment(sanity)}\n")
            buf.write(f"{indent}    {naming.var_name(sanity)} = None\n")

        for d in range(depth, 0, -1):
            indent = "    " * d
            buf.write(f"{indent}else:\n")
            buf.write(f"{indent}    pass  # {comments.comment(sanity)}\n")

        buf.write("    return None\n\n\n")

    def _wrapper_hell(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit deeply layered wrapper delegations."""
        buf.write(f"# {comments.comment(sanity)}\n\n")
        base_name = naming.method_name(sanity)
        layers = [
            "", "Internal", "Proxy", "Adapter", "Bridge", "Facade",
            "Interceptor", "Wrapper", "Fallback", "FinalV2", "TerminalBuild",
        ]
        num_layers = random.randint(5, len(layers))

        for i in range(num_layers):
            suffix = layers[i]
            next_suffix = layers[i + 1] if i + 1 < num_layers else None
            fname = f"{base_name}_{suffix}" if suffix else base_name
            params = ", ".join(naming.var_name(sanity) for _ in range(random.randint(1, 3)))

            buf.write(f"def {fname}({params}):\n")
            buf.write(f'    """{comments.docstring(sanity, fname)}"""\n')
            if next_suffix is not None:
                next_name = f"{base_name}_{next_suffix}"
                buf.write(f"    return {next_name}({params})\n\n\n")
            else:
                buf.write(f"    return None  # {comments.comment(sanity)}\n\n\n")

    def _massive_enum(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit a massive Python Enum definition with 50+ members."""
        buf.write("from enum import Enum, auto\n\n\n")
        enum_name = cname + "Type"
        buf.write(f"class {enum_name}(Enum):\n")
        buf.write(f'    """{comments.docstring(sanity, enum_name)}"""\n\n')

        num_values = random.randint(40, 70)
        for i in range(num_values):
            val_name = f"MEMBER_{i}_{naming.var_name(sanity).upper()}"
            buf.write(f"    {val_name} = auto()  # {comments.comment(sanity)}\n")
        buf.write("\n\n")

    def _fake_tests(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit synthetic unittest TestCase with mock assertions."""
        buf.write("import unittest\n\n\n")
        test_class = f"Test{cname}"
        buf.write(f"class {test_class}(unittest.TestCase):\n")
        buf.write(f'    """{comments.docstring(sanity, test_class)}"""\n\n')

        num_tests = random.randint(8, 16)
        for i in range(num_tests):
            test_name = naming.method_name(sanity)
            buf.write(f"    def test_{test_name}_{i}(self):\n")
            buf.write(f"        # {comments.comment(sanity)}\n")
            buf.write("        self.assertTrue(True)\n")
            buf.write("        self.assertEqual(1, 1)\n\n")

    def _bytecode_vm(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit a mock stack-based bytecode virtual machine interpreter."""
        buf.write(f"# --- Bytecode VM Interpreter: {cname} ---\n\n")
        vm_name = f"{cname}VM"
        buf.write(f"class {vm_name}:\n")
        buf.write("    OP_PUSH = 0x01\n    OP_POP = 0x02\n    OP_ADD = 0x03\n    OP_HALT = 0xFF\n\n")
        buf.write("    def __init__(self) -> None:\n")
        buf.write("        self.stack: list[int] = []\n")
        buf.write("        self.registers: dict[str, int] = {'r0': 0, 'r1': 0}\n")
        buf.write("        self.pc: int = 0\n\n")
        buf.write("    def execute(self, bytecode: list[int]) -> int:\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write("        while self.pc < len(bytecode):\n")
        buf.write("            op = bytecode[self.pc]\n")
        buf.write("            self.pc += 1\n")
        buf.write("            if op == self.OP_PUSH:\n")
        buf.write("                val = bytecode[self.pc]\n")
        buf.write("                self.pc += 1\n")
        buf.write("                self.stack.append(val)\n")
        buf.write("            elif op == self.OP_ADD:\n")
        buf.write("                b = self.stack.pop() if self.stack else 0\n")
        buf.write("                a = self.stack.pop() if self.stack else 0\n")
        buf.write("                self.stack.append(a + b)\n")
        buf.write("            elif op == self.OP_HALT:\n")
        buf.write("                break\n")
        buf.write("        return self.stack[-1] if self.stack else 0\n\n\n")

    def _sql_builder(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit an enterprise recursive CTE query builder with multi-table joins."""
        buf.write(f"# --- Enterprise SQL Builder: {cname} ---\n\n")
        buf.write(f"def build_{cname.lower()}_query() -> str:\n")
        buf.write(f'    """{comments.docstring(sanity, "query_builder")}"""\n')
        buf.write("    query = (\n")
        buf.write('        "WITH RECURSIVE hierarchy_tree AS (\\n"\n')
        buf.write('        "    SELECT id, parent_id, 1 as depth FROM enterprise_nodes WHERE parent_id IS NULL\\n"\n')
        buf.write('        "    UNION ALL\\n"\n')
        buf.write('        "    SELECT c.id, c.parent_id, h.depth + 1 FROM enterprise_nodes c JOIN hierarchy_tree h ON c.parent_id = h.id\\n"\n')
        buf.write('        ")\\n"\n')
        buf.write('        "SELECT t.id, t.depth, d.data_payload, SUM(m.metric_value) OVER (PARTITION BY t.parent_id) as window_sum\\n"\n')
        buf.write('        "FROM hierarchy_tree t\\n"\n')
        buf.write('        "LEFT JOIN telemetry_data d ON t.id = d.node_id\\n"\n')
        buf.write('        "LEFT JOIN metrics_ledger m ON t.id = m.account_id\\n"\n')
        buf.write('        "WHERE t.depth < 10 AND d.status = \'ACTIVE\'\\n"\n')
        buf.write('        "ORDER BY window_sum DESC LIMIT 500;"\n')
        buf.write("    )\n")
        buf.write("    return query\n\n\n")

    def _di_graph(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit a dependency injection service locator container."""
        buf.write(f"# --- Dependency Injection Graph: {cname} ---\n\n")
        buf.write(f"class {cname}Container:\n")
        buf.write("    def __init__(self) -> None:\n")
        buf.write("        self._singletons: dict[str, object] = {}\n\n")
        buf.write("    def register(self, key: str, instance: object) -> None:\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write("        self._singletons[key] = instance\n\n")
        buf.write("    def resolve(self, key: str) -> object:\n")
        buf.write("        if key not in self._singletons:\n")
        buf.write("            raise KeyError(f'Unbound dependency: {key}')\n")
        buf.write("        return self._singletons[key]\n\n\n")

    def _neural_pipeline(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Emit deep neural network tensor forward/backward pass simulation."""
        buf.write(f"# --- Neural Tensor Graph: {cname} ---\n\n")
        buf.write(f"class {cname}AttentionLayer:\n")
        buf.write("    def __init__(self, hidden_dim: int = 256, heads: int = 8) -> None:\n")
        buf.write("        self.hidden_dim = hidden_dim\n")
        buf.write("        self.heads = heads\n")
        buf.write("        self.head_dim = hidden_dim // heads\n\n")
        buf.write("    def forward(self, x: list[list[float]]) -> list[list[float]]:\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write("        # Simulated scaled dot-product attention\n")
        buf.write("        return [[val * 0.5 for val in row] for row in x]\n")
