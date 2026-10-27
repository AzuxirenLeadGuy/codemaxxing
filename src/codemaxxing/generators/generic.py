"""Generic chaotic Python generator.

Synthesizes absurd procedural patterns including 20-level nested if-else statements,
recursive wrapper call chains, enormous enum definitions, and simulated unit test suites.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class GenericGenerator(SlopGenerator):
    """Generic Python code generator demonstrating anti-patterns and code bloat.

    Produces synthetic python source code filled with deeply nested conditional branches,
    convoluted wrapper layers, hundred-member enums, and trivial unit tests.
    """

    name = "generic"
    language = "generic"
    extension = ".py"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a generic synthetic Python file (.py).

        Selects among slop archetypes ('nested_if', 'wrapper_hell', 'massive_enum',
        'fake_tests', or a combination of all) to construct an output file.

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized generic Python code.
        """
        buf = StringIO()

        # pick which type of slop to generate
        slop_type = random.choice(["nested_if", "wrapper_hell", "massive_enum", "fake_tests", "mixed"])
        cname = naming.class_name(sanity)

        if slop_type == "nested_if":
            self._nested_if_else(buf, sanity, cname)
        elif slop_type == "wrapper_hell":
            self._wrapper_hell(buf, sanity, cname)
        elif slop_type == "massive_enum":
            self._massive_enum(buf, sanity, cname)
        elif slop_type == "fake_tests":
            self._fake_tests(buf, sanity, cname)
        else:
            self._nested_if_else(buf, sanity, cname)
            self._wrapper_hell(buf, sanity, cname)
            self._massive_enum(buf, sanity, cname)
            self._fake_tests(buf, sanity, cname)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"generic/{cname.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _nested_if_else(self, buf: StringIO, sanity: float, cname: str):
        """Emit a function with 10 to 20 levels of nested if-else statements.

        Args:
            buf: String buffer receiving generated Python code.
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            cname: Base class/component name used for naming context.
        """
        buf.write(f"# {comments.comment(sanity)}\n\n\n")
        func_name = naming.method_name(sanity)
        buf.write(f"def {func_name}({naming.var_name(sanity)}, {naming.var_name(sanity)}, {naming.var_name(sanity)}):\n")
        buf.write(f'    """{comments.docstring(sanity, func_name)}"""\n')

        depth = random.randint(10, 20)
        for d in range(depth):
            indent = "    " * (d + 1)
            var = naming.var_name(sanity)
            condition = random.choice([
                f"{var} is not None",
                f"isinstance({var}, object)",
                f"len(str({var})) > 0",
                f"{var} != {var}",
                f"True",
                f"not False",
                f"bool({var}) or not bool({var})",
                f"hash({var}) == hash({var})",
                f"type({var}) == type({var})",
            ])
            buf.write(f"{indent}if {condition}:  # {comments.comment(sanity)}\n")
            buf.write(f"{indent}    {naming.var_name(sanity)} = None\n")

        # unwind with else clauses
        for d in range(depth, 0, -1):
            indent = "    " * d
            buf.write(f"{indent}else:\n")
            buf.write(f"{indent}    pass  # {comments.comment(sanity)}\n")

        buf.write(f"    return None\n\n\n")

    def _wrapper_hell(self, buf: StringIO, sanity: float, cname: str):
        """Emit a series of chained wrapper functions delegating through multiple layers.

        Args:
            buf: String buffer receiving generated Python code.
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            cname: Base class/component name used for naming context.
        """
        buf.write(f"# {comments.comment(sanity)}\n\n")
        base_name = naming.method_name(sanity)
        layers = ["", "Internal", "InternalImpl", "InternalImplV2",
                   "InternalImplV2Final", "InternalImplV2FinalFinal",
                   "InternalImplV2FinalFinalForReal", "InternalImplV2FinalFinalForRealThisTime"]
        num_layers = random.randint(4, len(layers))

        for i in range(num_layers):
            suffix = layers[i]
            next_suffix = layers[i + 1] if i + 1 < num_layers else None
            fname = f"{base_name}{suffix}"
            params = ", ".join(naming.var_name(sanity) for _ in range(random.randint(1, 4)))

            buf.write(f"def {fname}({params}):\n")
            buf.write(f'    """{comments.docstring(sanity, fname)}"""\n')
            buf.write(f"    # {comments.comment(sanity)}\n")
            for _ in range(random.randint(1, 3)):
                buf.write(f"    {naming.var_name(sanity)} = None\n")

            if next_suffix is not None:
                next_name = f"{base_name}{next_suffix}"
                buf.write(f"    return {next_name}({params})\n\n\n")
            else:
                buf.write(f"    return None  # {comments.comment(sanity)}\n\n\n")

    def _massive_enum(self, buf: StringIO, sanity: float, cname: str):
        """Emit a massive Python Enum definition with 50 to 100 auto() values.

        Args:
            buf: String buffer receiving generated Python code.
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            cname: Base class/component name used to name the enum.
        """
        buf.write(f"# {comments.comment(sanity)}\n")
        buf.write(f"from enum import Enum, auto\n\n\n")
        enum_name = cname + "Type"
        buf.write(f"class {enum_name}(Enum):\n")
        buf.write(f'    """{comments.docstring(sanity, enum_name)}"""\n\n')

        num_values = random.randint(50, 100)
        used_names = set()
        for i in range(num_values):
            if sanity > 0.5:
                parts = [random.choice(naming.CORPORATE_PREFIXES).upper(),
                         random.choice(naming.CORPORATE_NOUNS).upper()]
                val_name = "_".join(parts) + f"_{i}"
            else:
                val_name = random.choice(naming.CHAOS_WORDS).upper() + f"_{i}"
            if val_name in used_names:
                val_name += f"_EXTRA_{i}"
            used_names.add(val_name)
            buf.write(f"    {val_name} = auto()  # {comments.comment(sanity)}\n")
        buf.write("\n\n")

    def _fake_tests(self, buf: StringIO, sanity: float, cname: str):
        """Emit a synthetic unittest TestCase containing 10 to 30 trivial assertions.

        Args:
            buf: String buffer receiving generated Python code.
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            cname: Base class/component name under test.
        """
        buf.write(f"# {comments.comment(sanity)}\n")
        buf.write(f"import unittest\n\n\n")

        test_class = f"Test{cname}"
        buf.write(f"class {test_class}(unittest.TestCase):\n")
        buf.write(f'    """{comments.docstring(sanity, test_class)}"""\n\n')

        num_tests = random.randint(10, 30)
        for i in range(num_tests):
            test_name = naming.method_name(sanity)
            buf.write(f"    def test_{test_name}_{i}(self):\n")
            buf.write(f"        # {comments.comment(sanity)}\n")

            num_asserts = random.randint(1, 5)
            for _ in range(num_asserts):
                assertion = random.choice([
                    "self.assertTrue(True)",
                    "self.assertFalse(False)",
                    "self.assertEqual(1, 1)",
                    "self.assertIsNone(None)",
                    "self.assertIsNotNone(object())",
                    "self.assertIn(1, [1, 2, 3])",
                    "self.assertEqual('a', 'a')",
                    "self.assertGreater(2, 1)",
                    "self.assertLess(1, 2)",
                    f"self.assertTrue(True)  # {comments.comment(sanity)}",
                ])
                buf.write(f"        {assertion}\n")
            buf.write("\n")

        buf.write(f"\nif __name__ == '__main__':\n")
        buf.write(f"    unittest.main()\n\n")
