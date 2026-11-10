"""C synthetic code generator.

Synthesizes rich C source files across multiple distinct archetypes:
C-style object-oriented vtables with reference counting, bump memory arenas with ring buffers,
X-Macro preprocessor metaprogramming, and embedded driver hardware abstractions.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class CSlopGenerator(SlopGenerator):
    """Synthetic C language code generator.

    Emits procedural C source code spanning object vtables, memory arenas,
    preprocessor macro gymnastics, and hardware driver simulations.
    """

    name = "c_slop"
    language = "c"
    extension = ".c"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic C source file (.c).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized C source code.
        """
        buf = StringIO()
        struct_name = naming.class_name(sanity)

        buf.write(f"/* {comments.docstring(sanity, struct_name)} */\n")
        buf.write("#include <stdio.h>\n")
        buf.write("#include <stdlib.h>\n")
        buf.write("#include <string.h>\n")
        buf.write("#include <stdbool.h>\n")
        buf.write("#include <stdint.h>\n\n")

        archetype = random.choice([
            "vtable_oop_engine",
            "arena_ring_buffer",
            "macro_x_madness",
            "embedded_driver_mock",
        ])

        if archetype == "vtable_oop_engine":
            self._generate_vtable_engine(buf, sanity, struct_name, file_index)
        elif archetype == "arena_ring_buffer":
            self._generate_arena_buffer(buf, sanity, struct_name, file_index)
        elif archetype == "macro_x_madness":
            self._generate_x_macro_engine(buf, sanity, struct_name, file_index)
        else:
            self._generate_driver_mock(buf, sanity, struct_name, file_index)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"c/{struct_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_vtable_engine(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit C-style OOP with function pointer vtable and reference counting."""
        buf.write(f"typedef struct {struct_name} {struct_name};\n\n")
        buf.write(f"typedef struct {struct_name}VTable {{\n")
        buf.write("    int (*initialize)(struct " + struct_name + " *self);\n")
        buf.write("    int (*execute)(struct " + struct_name + " *self, const char *payload);\n")
        buf.write("    void (*destroy)(struct " + struct_name + " *self);\n")
        buf.write(f"}} {struct_name}VTable;\n\n")

        buf.write(f"struct {struct_name} {{\n")
        buf.write(f"    const {struct_name}VTable *vptr;\n")
        buf.write("    int32_t ref_count;\n")
        buf.write("    uint32_t state_flags;\n")
        buf.write("    char telemetry_tag[64];\n")
        buf.write("};\n\n")

        # Method implementations
        buf.write(f"static int {struct_name.lower()}_init({struct_name} *self) {{\n")
        buf.write("    if (!self) return -1;\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    self->state_flags = 0x01;\n")
        buf.write("    return 0;\n")
        buf.write("}\n\n")

        buf.write(f"static int {struct_name.lower()}_exec({struct_name} *self, const char *payload) {{\n")
        buf.write("    int rc = 0;\n")
        buf.write("    if (!self || !payload) return -1;\n")
        buf.write("    self->ref_count++;\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    if (strlen(payload) == 0) {\n")
        buf.write("        rc = -2;\n")
        buf.write("        goto cleanup;\n")
        buf.write("    }\n")
        buf.write("    self->state_flags |= 0x02;\n")
        buf.write("cleanup:\n")
        buf.write("    return rc;\n")
        buf.write("}\n\n")

        buf.write(f"static void {struct_name.lower()}_free({struct_name} *self) {{\n")
        buf.write("    if (self) free(self);\n")
        buf.write("}\n\n")

        buf.write(f"static const {struct_name}VTable g_{struct_name}VTable = {{\n")
        buf.write(f"    .initialize = {struct_name.lower()}_init,\n")
        buf.write(f"    .execute = {struct_name.lower()}_exec,\n")
        buf.write(f"    .destroy = {struct_name.lower()}_free,\n")
        buf.write("};\n\n")

        buf.write(f"{struct_name} *create_{struct_name.lower()}(void) {{\n")
        buf.write(f"    {struct_name} *obj = ({struct_name} *)calloc(1, sizeof({struct_name}));\n")
        buf.write("    if (!obj) return NULL;\n")
        buf.write(f"    obj->vptr = &g_{struct_name}VTable;\n")
        buf.write("    obj->ref_count = 1;\n")
        buf.write("    return obj;\n")
        buf.write("}\n")

    def _generate_arena_buffer(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit memory arena allocator with circular ring buffer."""
        buf.write(f"typedef struct {struct_name}Arena {{\n")
        buf.write("    uint8_t *buffer;\n")
        buf.write("    size_t capacity;\n")
        buf.write("    size_t offset;\n")
        buf.write(f"}} {struct_name}Arena;\n\n")

        buf.write(f"static void *arena_alloc({struct_name}Arena *arena, size_t size) {{\n")
        buf.write("    // Align to 8 bytes\n")
        buf.write("    size_t aligned = (size + 7) & ~7;\n")
        buf.write("    if (arena->offset + aligned > arena->capacity) {\n")
        buf.write("        return NULL; // Out of memory in arena\n")
        buf.write("    }\n")
        buf.write("    void *ptr = &arena->buffer[arena->offset];\n")
        buf.write("    arena->offset += aligned;\n")
        buf.write("    return ptr;\n")
        buf.write("}\n\n")

        buf.write(f"static void arena_reset({struct_name}Arena *arena) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    arena->offset = 0;\n")
        buf.write("}\n")

    def _generate_x_macro_engine(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit preprocessor X-Macros defining enums and string lookup tables."""
        buf.write("#define ENTERPRISE_METRICS(X) \\\n")
        buf.write('    X(PENDING, "pending_state") \\\n')
        buf.write('    X(RUNNING, "running_state") \\\n')
        buf.write('    X(COMPLETED, "completed_state") \\\n')
        buf.write('    X(RETRYING, "retrying_state") \\\n')
        buf.write('    X(FAILED, "failed_state")\n\n')

        buf.write("typedef enum {\n")
        buf.write("#define AS_ENUM(name, str) METRIC_##name,\n")
        buf.write("    ENTERPRISE_METRICS(AS_ENUM)\n")
        buf.write("#undef AS_ENUM\n")
        buf.write("} EnterpriseMetricEnum;\n\n")

        buf.write("static const char *get_metric_name(EnterpriseMetricEnum metric) {\n")
        buf.write("    switch (metric) {\n")
        buf.write('#define AS_CASE(name, str) case METRIC_##name: return str;\n')
        buf.write("        ENTERPRISE_METRICS(AS_CASE)\n")
        buf.write("#undef AS_CASE\n")
        buf.write('        default: return "UNKNOWN";\n')
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_driver_mock(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit embedded hardware register driver abstraction."""
        buf.write(f"typedef struct volatile {struct_name}Registers {{\n")
        buf.write("    uint32_t CTRL_STATUS;\n")
        buf.write("    uint32_t DATA_IN;\n")
        buf.write("    uint32_t DATA_OUT;\n")
        buf.write("    uint32_t IRQ_MASK;\n")
        buf.write(f"}} {struct_name}Registers;\n\n")

        buf.write(f"static uint32_t calculate_crc32(const uint8_t *data, size_t length) {{\n")
        buf.write("    uint32_t crc = 0xFFFFFFFF;\n")
        buf.write("    for (size_t i = 0; i < length; i++) {\n")
        buf.write("        crc ^= data[i];\n")
        buf.write("        for (int j = 0; j < 8; j++) {\n")
        buf.write("            crc = (crc >> 1) ^ ((crc & 1) ? 0xEDB88320 : 0);\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("    return ~crc;\n")
        buf.write("}\n")
