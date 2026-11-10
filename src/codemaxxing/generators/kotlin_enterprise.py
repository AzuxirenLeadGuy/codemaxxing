"""Kotlin enterprise code generator.

Synthesizes rich Kotlin source files across multiple distinct archetypes:
Coroutines and asynchronous Flow pipelines, sealed class DSL builders with receivers,
Spring Boot transactional services with extension functions, and inline reified value classes.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class KotlinEnterpriseGenerator(SlopGenerator):
    """Enterprise Kotlin code generator.

    Emits idiomatic Kotlin code spanning Flow coroutines, sealed DSL builders,
    Spring services with delegated properties, and reified inline classes.
    """

    name = "kotlin_enterprise"
    language = "kotlin"
    extension = ".kt"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Kotlin source file (.kt).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Kotlin source code.
        """
        buf = StringIO()
        package_name = naming.java_package(sanity).replace("-", "_")
        class_name = naming.class_name(sanity)

        buf.write(f"package {package_name}\n\n")
        buf.write("import java.time.Instant\nimport java.util.UUID\nimport java.util.concurrent.ConcurrentHashMap\n\n")

        archetype = random.choice([
            "coroutines_flow",
            "sealed_dsl_builder",
            "spring_service_ext",
            "inline_reified_class",
        ])

        if archetype == "coroutines_flow":
            self._generate_coroutines_flow(buf, sanity, class_name)
        elif archetype == "sealed_dsl_builder":
            self._generate_sealed_dsl(buf, sanity, class_name)
        elif archetype == "spring_service_ext":
            self._generate_spring_ext(buf, sanity, class_name)
        else:
            self._generate_inline_reified(buf, sanity, class_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"kotlin/{class_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_coroutines_flow(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit coroutines and Flow stream pipelines."""
        buf.write(f"class {class_name}FlowEngine {{\n")
        buf.write("    private val cache = ConcurrentHashMap<String, String>()\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    suspend fun {mname}(input: String): Result<String> {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        val sanitized = input.trim()\n")
        buf.write('        cache[UUID.randomUUID().toString()] = sanitized\n')
        buf.write("        return Result.success(sanitized.uppercase())\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_sealed_dsl(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit sealed interface hierarchy with exhaustive when expression."""
        buf.write(f"sealed interface {class_name}State {{\n")
        buf.write("    data object Idle : " + class_name + "State\n")
        buf.write("    data class Running(val progress: Int) : " + class_name + "State\n")
        buf.write("    data class Terminated(val reason: String) : " + class_name + "State\n")
        buf.write("}\n\n")

        buf.write(f"class {class_name}Machine {{\n")
        buf.write(f"    fun evaluate(state: {class_name}State): String = when (state) {{\n")
        buf.write(f"        is {class_name}State.Idle -> \"STANDBY\"\n")
        buf.write(f"        is {class_name}State.Running -> \"PROGRESS: ${{state.progress}}%\"\n")
        buf.write(f"        is {class_name}State.Terminated -> \"HALTED: ${{state.reason}}\"\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_spring_ext(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit extension functions and delegated properties."""
        buf.write(f"class {class_name}Service {{\n")
        buf.write("    val instanceId: String by lazy { UUID.randomUUID().toString() }\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    fun {mname}(tokens: List<String>): List<String> {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return tokens.filter { it.isNotBlank() }.map { \"${it}_$instanceId\" }\n")
        buf.write("    }\n")
        buf.write("}\n\n")

        buf.write(f"fun <T> List<T>.synergize(): List<T> = this.shuffled()\n")

    def _generate_inline_reified(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit inline value class and reified helper."""
        buf.write(f"@JvmInline\nvalue class {class_name}Token(val raw: String) {{\n")
        buf.write("    init {\n")
        buf.write('        require(raw.isNotEmpty()) { "Token cannot be empty" }\n')
        buf.write("    }\n")
        buf.write("}\n")
