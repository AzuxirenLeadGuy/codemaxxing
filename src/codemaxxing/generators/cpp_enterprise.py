"""C++ enterprise code generator.

Synthesizes rich C++ source files spanning modern C++20 concepts and fold expressions,
RAII smart pointer pipelines, Curiously Recurring Template Patterns (CRTP),
and compile-time template metaprogramming recursion.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class CppEnterpriseGenerator(SlopGenerator):
    """Modern C++ enterprise pattern code generator.

    Emits object-oriented and template-metaprogramming C++ with concepts,
    std::variant visitors, RAII synchronization guards, and CRTP factories.
    """

    name = "cpp_enterprise"
    language = "cpp"
    extension = ".cpp"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic C++ source file (.cpp).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized C++ source code.
        """
        buf = StringIO()
        namespace_name = naming.class_name(sanity)
        class_name = naming.class_name(sanity)

        buf.write(f"// {comments.docstring(sanity, class_name)}\n")
        buf.write("#include <iostream>\n#include <memory>\n#include <string>\n#include <vector>\n")
        buf.write("#include <variant>\n#include <optional>\n#include <mutex>\n#include <type_traits>\n\n")

        buf.write(f"namespace {namespace_name} {{\n\n")

        archetype = random.choice([
            "modern_cpp20_concepts",
            "raii_smart_pipeline",
            "crtp_factory",
            "chaos_template_meta",
        ])

        if archetype == "modern_cpp20_concepts":
            self._generate_cpp20_concepts(buf, sanity, class_name)
        elif archetype == "raii_smart_pipeline":
            self._generate_raii_pipeline(buf, sanity, class_name)
        elif archetype == "crtp_factory":
            self._generate_crtp_factory(buf, sanity, class_name)
        else:
            self._generate_template_meta(buf, sanity, class_name)

        buf.write(f"\n}} // namespace {namespace_name}\n")

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"cpp/{class_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_cpp20_concepts(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit C++20 concepts, std::variant visitors, and fold expressions."""
        buf.write("template<typename T>\n")
        buf.write("concept EnterpriseValidatable = requires(T a) {\n")
        buf.write("    { a.validate() } -> std::same_as<bool>;\n")
        buf.write("};\n\n")

        buf.write(f"class {class_name} {{\n")
        buf.write("public:\n")
        buf.write("    using StateVariant = std::variant<int, std::string, double>;\n\n")
        buf.write(f"    {class_name}() = default;\n\n")

        # Fold expression method
        buf.write("    template<typename... Args>\n")
        buf.write("    auto foldSum(Args... args) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return (... + args);\n")
        buf.write("    }\n\n")

        # Variant visitor
        mname = naming.method_name(sanity)
        buf.write(f"    std::string {mname}(const StateVariant& state) {{\n")
        buf.write("        return std::visit([](const auto& val) -> std::string {\n")
        buf.write("            using T = std::decay_t<decltype(val)>;\n")
        buf.write("            if constexpr (std::is_same_v<T, std::string>) return val;\n")
        buf.write("            else return std::to_string(val);\n")
        buf.write("        }, state);\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_raii_pipeline(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit RAII lock guard and smart pointer lifecycle manager."""
        buf.write(f"class {class_name} {{\n")
        buf.write("private:\n")
        buf.write("    mutable std::mutex mutex_;\n")
        buf.write("    std::vector<std::shared_ptr<std::string>> pool_;\n\n")
        buf.write("public:\n")
        buf.write(f"    {class_name}() = default;\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    void {mname}(std::string item) {{\n")
        buf.write("        std::lock_guard<std::mutex> lock(mutex_);\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        pool_.push_back(std::make_shared<std::string>(std::move(item)));\n")
        buf.write("    }\n\n")

        buf.write("    size_t size() const noexcept {\n")
        buf.write("        std::lock_guard<std::mutex> lock(mutex_);\n")
        buf.write("        return pool_.size();\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_crtp_factory(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Curiously Recurring Template Pattern (CRTP)."""
        buf.write("template<typename Derived>\n")
        buf.write("class CRTPBase {\n")
        buf.write("public:\n")
        buf.write("    void process() {\n")
        buf.write("        static_cast<Derived*>(this)->onProcess();\n")
        buf.write("    }\n")
        buf.write("};\n\n")

        buf.write(f"class {class_name} : public CRTPBase<{class_name}> {{\n")
        buf.write("public:\n")
        buf.write("    void onProcess() {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_template_meta(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit compile-time template metaprogramming recursion."""
        buf.write("template<size_t N>\n")
        buf.write("struct Factorial {\n")
        buf.write("    static constexpr size_t value = N * Factorial<N - 1>::value;\n")
        buf.write("};\n\n")
        buf.write("template<>\n")
        buf.write("struct Factorial<0> {\n")
        buf.write("    static constexpr size_t value = 1;\n")
        buf.write("};\n\n")

        buf.write(f"struct {class_name}Meta {{\n")
        buf.write("    static constexpr size_t depth = Factorial<5>::value;\n")
        buf.write("};\n")
