"""PHP enterprise code generator.

Synthesizes rich PHP 8+ source files across multiple distinct archetypes:
PHP 8.2+ backed enums with match expressions and readonly classes,
Symfony-style attribute event dispatchers, Laravel collection pipelines,
and magic method Fiber coroutines.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class PhpEnterpriseGenerator(SlopGenerator):
    """Enterprise PHP code generator.

    Emits PHP 8+ class files adhering to modern PSR architecture spanning
    backed enums, match expressions, attribute dispatchers, and fibers.
    """

    name = "php_enterprise"
    language = "php"
    extension = ".php"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic PHP source file (.php).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized PHP source code.
        """
        buf = StringIO()
        namespace_name = "Codemaxxing\\" + naming.class_name(sanity)
        class_name = naming.class_name(sanity)

        buf.write("<?php\n\ndeclare(strict_types=1);\n\n")
        buf.write(f"namespace {namespace_name};\n\n")
        buf.write("use DateTimeImmutable;\nuse RuntimeException;\n\n")

        archetype = random.choice([
            "php8_match_enum",
            "symfony_event_attr",
            "laravel_collection",
            "chaos_magic_fiber",
        ])

        if archetype == "php8_match_enum":
            self._generate_match_enum(buf, sanity, class_name)
        elif archetype == "symfony_event_attr":
            self._generate_symfony_attr(buf, sanity, class_name)
        elif archetype == "laravel_collection":
            self._generate_collection_pipeline(buf, sanity, class_name)
        else:
            self._generate_magic_fiber(buf, sanity, class_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"php/{class_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_match_enum(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit PHP 8.2+ backed enum with match expression and readonly class."""
        enum_name = f"{class_name}Status"
        buf.write(f"enum {enum_name}: string {{\n")
        buf.write("    case PENDING = 'pending';\n")
        buf.write("    case RUNNING = 'running';\n")
        buf.write("    case COMPLETED = 'completed';\n\n")
        buf.write("    public function isTerminal(): bool {\n")
        buf.write("        return match($this) {\n")
        buf.write("            self::COMPLETED => true,\n")
        buf.write("            default => false,\n")
        buf.write("        };\n")
        buf.write("    }\n")
        buf.write("}\n\n")

        buf.write(f"final readonly class {class_name}Payload {{\n")
        buf.write("    public function __construct(\n")
        buf.write("        public string $id,\n")
        buf.write(f"        public {enum_name} $status = {enum_name}::PENDING,\n")
        buf.write("        public DateTimeImmutable $createdAt = new DateTimeImmutable(),\n")
        buf.write("    ) {}\n")
        buf.write("}\n")

    def _generate_symfony_attr(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Symfony-style attribute-decorated event subscriber."""
        buf.write("#[\\Attribute]\nclass AsEventListener { public function __construct(public string $event) {} }\n\n")

        buf.write(f"final class {class_name}Listener {{\n")
        mname = naming.method_name(sanity)
        buf.write(f"    #[AsEventListener(event: '{mname}.dispatched')]\n")
        buf.write(f"    public function onDispatch(object $event): void {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_collection_pipeline(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Laravel collection-like pipeline transformations."""
        buf.write(f"final class {class_name}Pipeline {{\n")
        mname = naming.method_name(sanity)
        buf.write(f"    public function {mname}(array $items): array {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return array_values(array_filter(\n")
        buf.write("            array_map(fn($x) => strtoupper((string)$x), $items),\n")
        buf.write("            fn($x) => strlen($x) > 0\n")
        buf.write("        ));\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_magic_fiber(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Fiber coroutines with dynamic magic method dispatch."""
        buf.write("use Fiber;\n\n")
        buf.write(f"final class {class_name}FiberEngine {{\n")
        buf.write("    public function runAsync(callable $task): mixed {\n")
        buf.write("        $fiber = new Fiber($task);\n")
        buf.write("        return $fiber->start();\n")
        buf.write("    }\n")
        buf.write("}\n")
