"""C# enterprise code generator.

Synthesizes rich C# enterprise source files across multiple distinct archetypes:
MediatR CQRS pipelines with behavior middlewares, async Channels with LINQ switch expressions,
high-performance Span/Memory ref structs, and Entity Framework repository patterns.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class CSharpEnterpriseGenerator(SlopGenerator):
    """Enterprise C# code generator.

    Emits idiomatic .NET architecture patterns spanning CQRS mediator pipelines,
    async Channels, high-performance ref structs, and EF Core repositories.
    """

    name = "csharp_enterprise"
    language = "csharp"
    extension = ".cs"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic C# source file (.cs).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized C# source code.
        """
        buf = StringIO()
        namespace_name = naming.class_name(sanity)
        class_name = naming.class_name(sanity)

        buf.write("using System;\nusing System.Collections.Generic;\nusing System.Threading;\n")
        buf.write("using System.Threading.Tasks;\nusing System.Threading.Channels;\n\n")

        buf.write(f"namespace Codemaxxing.{namespace_name};\n\n")

        archetype = random.choice([
            "cqrs_mediatr_pipeline",
            "async_channel_linq",
            "high_perf_span",
            "efcore_repository",
        ])

        if archetype == "cqrs_mediatr_pipeline":
            self._generate_cqrs_mediatr(buf, sanity, class_name)
        elif archetype == "async_channel_linq":
            self._generate_async_channel(buf, sanity, class_name)
        elif archetype == "high_perf_span":
            self._generate_high_perf(buf, sanity, class_name)
        else:
            self._generate_efcore_repo(buf, sanity, class_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"csharp/{class_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_cqrs_mediatr(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit CQRS MediatR request, handler, and pipeline behavior."""
        req_name = f"{class_name}Command"
        resp_name = f"{class_name}Result"

        buf.write(f"public sealed record {req_name}(Guid CorrelationId, string Payload);\n")
        buf.write(f"public sealed record {resp_name}(bool Success, DateTime Timestamp);\n\n")

        buf.write(f"public interface IHandler<in TReq, TResp> {{\n")
        buf.write("    Task<TResp> HandleAsync(TReq request, CancellationToken ct);\n")
        buf.write("}\n\n")

        buf.write(f"public sealed class {class_name}Handler : IHandler<{req_name}, {resp_name}> {{\n")
        buf.write(f"    public async Task<{resp_name}> HandleAsync({req_name} request, CancellationToken ct) {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        await Task.Yield();\n")
        buf.write("        ct.ThrowIfCancellationRequested();\n")
        buf.write(f"        return new {resp_name}(true, DateTime.UtcNow);\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_async_channel(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit async bounded channel with pattern matching switch expressions."""
        buf.write(f"public sealed class {class_name}Channel {{\n")
        buf.write("    private readonly Channel<string> _channel;\n\n")
        buf.write(f"    public {class_name}Channel(int capacity = 100) {{\n")
        buf.write("        _channel = Channel.CreateBounded<string>(new BoundedChannelOptions(capacity) {\n")
        buf.write("            FullMode = BoundedChannelFullMode.Wait\n")
        buf.write("        });\n")
        buf.write("    }\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    public async Task<string> {mname}(string input, CancellationToken ct) {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        await _channel.Writer.WriteAsync(input, ct);\n")
        buf.write("        var status = input.Length switch {\n")
        buf.write('            0 => "EMPTY",\n')
        buf.write('            > 50 => "OVERFLOW",\n')
        buf.write('            _ => "OPTIMAL"\n')
        buf.write("        };\n")
        buf.write("        return status;\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_high_perf(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit high-performance ref struct with Span<byte>."""
        buf.write(f"public readonly ref struct {class_name}Buffer {{\n")
        buf.write("    private readonly ReadOnlySpan<byte> _span;\n\n")
        buf.write(f"    public {class_name}Buffer(ReadOnlySpan<byte> span) {{\n")
        buf.write("        _span = span;\n")
        buf.write("    }\n\n")

        buf.write("    public int Length => _span.Length;\n\n")
        buf.write("    public bool TryFindDelimiter(byte delimiter, out int index) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        index = _span.IndexOf(delimiter);\n")
        buf.write("        return index >= 0;\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_efcore_repo(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit mock Entity Framework Core repository."""
        buf.write(f"public interface I{class_name}Repository<T> where T : class {{\n")
        buf.write("    Task<T?> GetByIdAsync(Guid id, CancellationToken ct);\n")
        buf.write("    Task AddAsync(T entity, CancellationToken ct);\n")
        buf.write("}\n\n")

        buf.write(f"public sealed class {class_name}Repository<T> : I{class_name}Repository<T> where T : class {{\n")
        buf.write("    private readonly List<T> _entities = new();\n\n")
        buf.write("    public Task<T?> GetByIdAsync(Guid id, CancellationToken ct) =>\n")
        buf.write("        Task.FromResult(_entities.Count > 0 ? _entities[0] : null);\n\n")
        buf.write("    public Task AddAsync(T entity, CancellationToken ct) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        _entities.Add(entity);\n")
        buf.write("        return Task.CompletedTask;\n")
        buf.write("    }\n")
        buf.write("}\n")
