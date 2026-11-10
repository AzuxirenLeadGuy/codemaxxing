"""Lua chaos code generator.

Synthesizes rich Lua scripts across multiple distinct archetypes:
Coroutine event loop schedulers, advanced metamethod OOP with prototype inheritance,
functional pipelines with protected pcall wrappers, and lexical upvalue environments.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class LuaChaosGenerator(SlopGenerator):
    """Lua language code generator.

    Emits dynamic Lua scripts utilizing coroutines, metamethods, functional
    iterators, and lexical environment manipulation.
    """

    name = "lua_chaos"
    language = "lua"
    extension = ".lua"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Lua source file (.lua).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Lua source code.
        """
        buf = StringIO()
        module_name = naming.class_name(sanity)
        table_name = naming.class_name(sanity)

        buf.write(f"-- {comments.comment(sanity)}\n")

        archetype = random.choice([
            "coroutine_scheduler",
            "advanced_metamethods",
            "functional_pipeline",
            "chaos_upvalues",
        ])

        if archetype == "coroutine_scheduler":
            self._generate_coroutine_scheduler(buf, sanity, table_name)
        elif archetype == "advanced_metamethods":
            self._generate_metamethods(buf, sanity, table_name)
        elif archetype == "functional_pipeline":
            self._generate_functional(buf, sanity, table_name)
        else:
            self._generate_upvalues(buf, sanity, table_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"lua/{module_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_coroutine_scheduler(self, buf: StringIO, sanity: float, table_name: str) -> None:
        """Emit coroutine-based task scheduler."""
        buf.write(f"local {table_name}Scheduler = {{ tasks = {{}} }}\n\n")
        buf.write(f"function {table_name}Scheduler.spawn(fn)\n")
        buf.write("    local co = coroutine.create(fn)\n")
        buf.write(f"    table.insert({table_name}Scheduler.tasks, co)\n")
        buf.write("    return co\n")
        buf.write("end\n\n")

        buf.write(f"function {table_name}Scheduler.step()\n")
        buf.write(f"    -- {comments.comment(sanity)}\n")
        buf.write(f"    for i, co in ipairs({table_name}Scheduler.tasks) do\n")
        buf.write("        if coroutine.status(co) ~= 'dead' then\n")
        buf.write("            local ok, err = coroutine.resume(co)\n")
        buf.write("            if not ok then error(err) end\n")
        buf.write("        end\n")
        buf.write("    end\n")
        buf.write("end\n\n")
        buf.write(f"return {table_name}Scheduler\n")

    def _generate_metamethods(self, buf: StringIO, sanity: float, table_name: str) -> None:
        """Emit OOP metatable with __add, __tostring, and __call."""
        buf.write(f"local {table_name} = {{}}\n")
        buf.write(f"{table_name}.__index = {table_name}\n\n")

        buf.write(f"function {table_name}.new(val)\n")
        buf.write(f"    return setmetatable({{ value = val or 0 }}, {table_name})\n")
        buf.write("end\n\n")

        buf.write(f"function {table_name}:__tostring()\n")
        buf.write(f"    return string.format('[Enterprise:%s value=%s]', '{table_name}', tostring(self.value))\n")
        buf.write("end\n\n")

        buf.write(f"function {table_name}:__add(other)\n")
        buf.write(f"    -- {comments.comment(sanity)}\n")
        buf.write(f"    local v2 = type(other) == 'table' and other.value or other\n")
        buf.write(f"    return {table_name}.new(self.value + v2)\n")
        buf.write("end\n\n")
        buf.write(f"return {table_name}\n")

    def _generate_functional(self, buf: StringIO, sanity: float, table_name: str) -> None:
        """Emit functional pipeline iterators with pcall."""
        buf.write(f"local {table_name}Pipe = {{}}\n\n")
        buf.write(f"function {table_name}Pipe.map(tbl, fn)\n")
        buf.write("    local res = {}\n")
        buf.write("    for k, v in pairs(tbl) do\n")
        buf.write("        local ok, out = pcall(fn, v, k)\n")
        buf.write("        if ok then table.insert(res, out) end\n")
        buf.write("    end\n")
        buf.write("    return res\n")
        buf.write("end\n\n")
        buf.write(f"return {table_name}Pipe\n")

    def _generate_upvalues(self, buf: StringIO, sanity: float, table_name: str) -> None:
        """Emit closure generator capturing lexical upvalues."""
        buf.write(f"local function create_{table_name.lower()}()\n")
        buf.write("    local counter = 0\n")
        buf.write(f"    -- {comments.comment(sanity)}\n")
        buf.write("    return function(delta)\n")
        buf.write("        counter = counter + (delta or 1)\n")
        buf.write("        return counter\n")
        buf.write("    end\n")
        buf.write("end\n\n")
        buf.write(f"return {{ create = create_{table_name.lower()} }}\n")
