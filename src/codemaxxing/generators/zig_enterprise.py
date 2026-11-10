"""Zig enterprise code generator.

Synthesizes rich Zig source files across multiple distinct archetypes:
Comptime generic reflection engines, tagged union state machines with error sets,
SIMD vector buffers with atomic operations, and C-ABI interop pointer arithmetic.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class ZigEnterpriseGenerator(SlopGenerator):
    """Enterprise Zig code generator.

    Emits manual memory management Zig source code spanning comptime generics,
    tagged unions, SIMD vectors, and pointer math.
    """

    name = "zig_enterprise"
    language = "zig"
    extension = ".zig"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Zig source file (.zig).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Zig source code.
        """
        buf = StringIO()
        struct_name = naming.class_name(sanity)

        buf.write(f"// {comments.docstring(sanity, struct_name)}\n")
        buf.write("const std = @import(\"std\");\n\n")

        archetype = random.choice([
            "comptime_generic",
            "tagged_union_errors",
            "simd_buffer",
            "pointer_interop",
        ])

        if archetype == "comptime_generic":
            self._generate_comptime_generic(buf, sanity, struct_name)
        elif archetype == "tagged_union_errors":
            self._generate_tagged_union(buf, sanity, struct_name)
        elif archetype == "simd_buffer":
            self._generate_simd_buffer(buf, sanity, struct_name)
        else:
            self._generate_pointer_interop(buf, sanity, struct_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"zig/{struct_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_comptime_generic(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit comptime generic factory and type inspection."""
        buf.write(f"pub fn {struct_name}Engine(comptime T: type) type {{\n")
        buf.write("    return struct {\n")
        buf.write("        allocator: std.mem.Allocator,\n")
        buf.write("        items: std.ArrayList(T),\n\n")
        buf.write("        const Self = @This();\n\n")
        buf.write("        pub fn init(allocator: std.mem.Allocator) Self {\n")
        buf.write("            return .{\n")
        buf.write("                .allocator = allocator,\n")
        buf.write("                .items = std.ArrayList(T).init(allocator),\n")
        buf.write("            };\n")
        buf.write("        }\n\n")
        buf.write("        pub fn deinit(self: *Self) void {\n")
        buf.write("            self.items.deinit();\n")
        buf.write("        }\n\n")
        mname = naming.method_name(sanity)
        buf.write(f"        pub fn {mname}(self: *Self, item: T) !void {{\n")
        buf.write(f"            // {comments.comment(sanity)}\n")
        buf.write("            try self.items.append(item);\n")
        buf.write("        }\n")
        buf.write("    };\n")
        buf.write("}\n")

    def _generate_tagged_union(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit tagged union and custom error set."""
        buf.write("pub const EnterpriseError = error{\n")
        buf.write("    BufferUnderflow,\n    ValidationFault,\n    Timeout,\n")
        buf.write("};\n\n")

        buf.write(f"pub const {struct_name}Event = union(enum) {{\n")
        buf.write("    Text: []const u8,\n")
        buf.write("    Number: i64,\n")
        buf.write("    Abort: void,\n")
        buf.write("};\n")

    def _generate_simd_buffer(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit SIMD vector operations."""
        buf.write(f"pub const {struct_name}SIMD = struct {{\n")
        buf.write("    pub fn sumVectors(a: @Vector(4, f32), b: @Vector(4, f32)) @Vector(4, f32) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return a + b;\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_pointer_interop(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit raw pointer math and memory slice copies."""
        buf.write(f"pub fn copyBytes_{struct_name.lower()}(dest: []u8, src: []const u8) usize {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    const len = @min(dest.len, src.len);\n")
        buf.write("    @memcpy(dest[0..len], src[0..len]);\n")
        buf.write("    return len;\n")
        buf.write("}\n")
