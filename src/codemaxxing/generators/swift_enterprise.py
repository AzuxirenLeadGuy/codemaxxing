"""Swift enterprise code generator.

Synthesizes rich Swift source files across multiple distinct archetypes:
Swift modern concurrency with actors and async/await TaskGroups, Combine reactive publisher pipelines,
Observable SwiftUI state architectures, and protocol composition with custom operators.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class SwiftEnterpriseGenerator(SlopGenerator):
    """Protocol-oriented Swift code generator.

    Emits idiomatic Swift source code spanning modern actors, Combine pipelines,
    Observable SwiftUI architectures, and generic protocols.
    """

    name = "swift_enterprise"
    language = "swift"
    extension = ".swift"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Swift source file (.swift).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Swift source code.
        """
        buf = StringIO()
        class_name = naming.class_name(sanity)

        buf.write("import Foundation\nimport Combine\n\n")
        buf.write(f"/// {comments.docstring(sanity, class_name)}\n")

        archetype = random.choice([
            "actor_async_concurrency",
            "combine_reactive",
            "observable_state",
            "protocol_operators",
        ])

        if archetype == "actor_async_concurrency":
            self._generate_actor(buf, sanity, class_name)
        elif archetype == "combine_reactive":
            self._generate_combine(buf, sanity, class_name)
        elif archetype == "observable_state":
            self._generate_observable(buf, sanity, class_name)
        else:
            self._generate_protocol_operators(buf, sanity, class_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"swift/{class_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_actor(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Swift actor with async/await and TaskGroup."""
        buf.write(f"public actor {class_name}Coordinator {{\n")
        buf.write("    private var processedEvents: Int = 0\n")
        buf.write("    private var registry: [String: Date] = [:]\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    public func {mname}(tokens: [String]) async -> [String] {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return await withTaskGroup(of: String.self) { group in\n")
        buf.write("            for token in tokens {\n")
        buf.write("                group.addTask {\n")
        buf.write("                    return token.uppercased()\n")
        buf.write("                }\n")
        buf.write("            }\n")
        buf.write("            var results: [String] = []\n")
        buf.write("            for await res in group {\n")
        buf.write("                results.append(res)\n")
        buf.write("            }\n")
        buf.write("            self.processedEvents += results.count\n")
        buf.write("            return results\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_combine(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit Combine reactive publishers and cancellable sinks."""
        buf.write(f"public final class {class_name}Pipeline {{\n")
        buf.write("    private let subject = PassthroughSubject<String, Never>()\n")
        buf.write("    private var cancellables = Set<AnyCancellable>()\n\n")
        buf.write("    public init() {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        subject\n")
        buf.write("            .filter { !$0.isEmpty }\n")
        buf.write("            .sink { _ in }\n")
        buf.write("            .store(in: &cancellables)\n")
        buf.write("    }\n\n")
        buf.write("    public func emit(_ event: String) {\n")
        buf.write("        subject.send(event)\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_observable(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit ObservableObject state viewmodel."""
        buf.write(f"public final class {class_name}ViewModel: ObservableObject {{\n")
        buf.write("    @Published public var isLoading: Bool = false\n")
        buf.write("    @Published public var telemetryData: [String] = []\n\n")
        mname = naming.method_name(sanity)
        buf.write(f"    public func {mname}() {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        isLoading = true\n")
        buf.write("        telemetryData.append(UUID().uuidString)\n")
        buf.write("        isLoading = false\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_protocol_operators(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit generic protocols with custom operators."""
        buf.write(f"public protocol {class_name}Contract {{\n")
        buf.write("    associatedtype Payload: Codable\n")
        buf.write("    func validate(_ input: Payload) -> Bool\n")
        buf.write("}\n")
