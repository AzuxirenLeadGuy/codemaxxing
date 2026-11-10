"""C synthetic code generator.

Synthesizes rich C source files across 11 distinct archetypes:
C-style object-oriented vtables with reference counting, bump memory arenas with ring buffers,
X-Macro preprocessor metaprogramming, embedded driver hardware abstractions,
intrusive doubly-linked lists with container_of macros, Bloom filter bit arrays,
lockless SPSC ring buffers with atomic fences, Duff's Device stackless coroutines,
open-addressing dynamic hash maps, signal event loops with monotonic timers,
and 256-ary radix trie prefix search trees.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class CSlopGenerator(SlopGenerator):
    """Synthetic C language code generator.

    Emits procedural C source code spanning object vtables, memory arenas,
    preprocessor macro gymnastics, hardware driver simulations, lockless queues,
    and intrusive data structures.
    """

    name = "c_slop"
    language = "c"
    extension = ".c"

    ARCHETYPES = [
        "vtable_oop_engine",
        "arena_ring_buffer",
        "macro_x_madness",
        "embedded_driver_mock",
        "intrusive_linked_list",
        "bloom_filter_bitset",
        "lockless_spsc_queue",
        "coroutine_duffs_device",
        "dynamic_hash_map",
        "signal_event_loop",
        "trie_prefix_tree",
    ]

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

        archetype = random.choice(self.ARCHETYPES)

        if archetype == "vtable_oop_engine":
            self._generate_vtable_engine(buf, sanity, struct_name, file_index)
        elif archetype == "arena_ring_buffer":
            self._generate_arena_buffer(buf, sanity, struct_name, file_index)
        elif archetype == "macro_x_madness":
            self._generate_x_macro_engine(buf, sanity, struct_name, file_index)
        elif archetype == "embedded_driver_mock":
            self._generate_driver_mock(buf, sanity, struct_name, file_index)
        elif archetype == "intrusive_linked_list":
            self._generate_intrusive_list(buf, sanity, struct_name, file_index)
        elif archetype == "bloom_filter_bitset":
            self._generate_bloom_filter(buf, sanity, struct_name, file_index)
        elif archetype == "lockless_spsc_queue":
            self._generate_spsc_queue(buf, sanity, struct_name, file_index)
        elif archetype == "coroutine_duffs_device":
            self._generate_duffs_coroutine(buf, sanity, struct_name, file_index)
        elif archetype == "dynamic_hash_map":
            self._generate_hash_map(buf, sanity, struct_name, file_index)
        elif archetype == "signal_event_loop":
            self._generate_signal_loop(buf, sanity, struct_name, file_index)
        else:
            self._generate_trie_tree(buf, sanity, struct_name, file_index)

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
        buf.write("    size_t aligned = (size + 7) & ~7;\n")
        buf.write("    if (arena->offset + aligned > arena->capacity) {\n")
        buf.write("        return NULL;\n")
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

        buf.write("static uint32_t calculate_crc32(const uint8_t *data, size_t length) {\n")
        buf.write("    uint32_t crc = 0xFFFFFFFF;\n")
        buf.write("    for (size_t i = 0; i < length; i++) {\n")
        buf.write("        crc ^= data[i];\n")
        buf.write("        for (int j = 0; j < 8; j++) {\n")
        buf.write("            crc = (crc >> 1) ^ ((crc & 1) ? 0xEDB88320 : 0);\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("    return ~crc;\n")
        buf.write("}\n")

    def _generate_intrusive_list(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit Linux kernel style intrusive doubly-linked list with container_of."""
        buf.write("#define container_of(ptr, type, member) \\\n")
        buf.write("    ((type *)((char *)(ptr) - offsetof(type, member)))\n\n")
        buf.write("#include <stddef.h>\n\n")

        buf.write("struct list_node {\n")
        buf.write("    struct list_node *next;\n")
        buf.write("    struct list_node *prev;\n")
        buf.write("};\n\n")

        buf.write(f"struct {struct_name}Item {{\n")
        buf.write("    uint64_t id;\n")
        buf.write("    char tag[32];\n")
        buf.write("    struct list_node node;\n")
        buf.write("};\n\n")

        buf.write("static void list_init(struct list_node *head) {\n")
        buf.write("    head->next = head;\n")
        buf.write("    head->prev = head;\n")
        buf.write("}\n\n")

        buf.write("static void list_add_tail(struct list_node *new_node, struct list_node *head) {\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    new_node->prev = head->prev;\n")
        buf.write("    new_node->next = head;\n")
        buf.write("    head->prev->next = new_node;\n")
        buf.write("    head->prev = new_node;\n")
        buf.write("}\n")

    def _generate_bloom_filter(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit bitwise Bloom filter with multi-seed hashing."""
        buf.write(f"#define {struct_name.upper()}_BLOOM_BITS 1024\n\n")
        buf.write(f"typedef struct {struct_name}Bloom {{\n")
        buf.write(f"    uint64_t bits[{struct_name.upper()}_BLOOM_BITS / 64];\n")
        buf.write(f"}} {struct_name}Bloom;\n\n")

        buf.write(f"static void bloom_add({struct_name}Bloom *filter, uint32_t hash) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write(f"    size_t idx = (hash % {struct_name.upper()}_BLOOM_BITS);\n")
        buf.write("    filter->bits[idx / 64] |= ((uint64_t)1 << (idx % 64));\n")
        buf.write("}\n\n")

        buf.write(f"static bool bloom_test(const {struct_name}Bloom *filter, uint32_t hash) {{\n")
        buf.write(f"    size_t idx = (hash % {struct_name.upper()}_BLOOM_BITS);\n")
        buf.write("    return (filter->bits[idx / 64] & ((uint64_t)1 << (idx % 64))) != 0;\n")
        buf.write("}\n")

    def _generate_spsc_queue(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit lock-free single-producer single-consumer circular queue."""
        buf.write(f"#define {struct_name.upper()}_QUEUE_CAP 256\n\n")
        buf.write(f"typedef struct {struct_name}Queue {{\n")
        buf.write(f"    void *buffer[{struct_name.upper()}_QUEUE_CAP];\n")
        buf.write("    volatile size_t head;\n")
        buf.write("    volatile size_t tail;\n")
        buf.write(f"}} {struct_name}Queue;\n\n")

        buf.write(f"static bool spsc_push({struct_name}Queue *q, void *item) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write(f"    size_t next_head = (q->head + 1) % {struct_name.upper()}_QUEUE_CAP;\n")
        buf.write("    if (next_head == q->tail) return false;\n")
        buf.write("    q->buffer[q->head] = item;\n")
        buf.write("    q->head = next_head;\n")
        buf.write("    return true;\n")
        buf.write("}\n")

    def _generate_duffs_coroutine(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit stackless coroutines implemented via Duff's Device."""
        buf.write(f"typedef struct {struct_name}CoroState {{\n")
        buf.write("    int line;\n")
        buf.write("    int counter;\n")
        buf.write(f"}} {struct_name}CoroState;\n\n")

        buf.write(f"static int run_{struct_name.lower()}_coro({struct_name}CoroState *s) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    switch (s->line) {\n")
        buf.write("        case 0:\n")
        buf.write("            s->counter = 0;\n")
        buf.write("            s->line = 1;\n")
        buf.write("            return s->counter;\n")
        buf.write("        case 1:\n")
        buf.write("            s->counter += 10;\n")
        buf.write("            s->line = 2;\n")
        buf.write("            return s->counter;\n")
        buf.write("        default:\n")
        buf.write("            return -1;\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_hash_map(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit open-addressing hash map with linear probing."""
        buf.write(f"typedef struct {struct_name}Entry {{\n")
        buf.write("    char key[32];\n")
        buf.write("    int value;\n")
        buf.write("    bool occupied;\n")
        buf.write(f"}} {struct_name}Entry;\n\n")

        buf.write(f"typedef struct {struct_name}Map {{\n")
        buf.write(f"    {struct_name}Entry entries[64];\n")
        buf.write("    size_t count;\n")
        buf.write(f"}} {struct_name}Map;\n\n")

        buf.write(f"static void map_insert({struct_name}Map *m, const char *key, int val) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    uint32_t h = 0;\n")
        buf.write("    for (const char *p = key; *p; p++) h = (h * 31) + *p;\n")
        buf.write("    size_t idx = h % 64;\n")
        buf.write("    while (m->entries[idx].occupied && strcmp(m->entries[idx].key, key) != 0) {\n")
        buf.write("        idx = (idx + 1) % 64;\n")
        buf.write("    }\n")
        buf.write("    strncpy(m->entries[idx].key, key, 31);\n")
        buf.write("    m->entries[idx].value = val;\n")
        buf.write("    m->entries[idx].occupied = true;\n")
        buf.write("}\n")

    def _generate_signal_loop(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit POSIX signal handler and event loop stubs."""
        buf.write("#include <signal.h>\n\n")
        buf.write("static volatile sig_atomic_t g_stop_requested = 0;\n\n")

        buf.write("static void sig_handler(int sig) {\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    (void)sig;\n")
        buf.write("    g_stop_requested = 1;\n")
        buf.write("}\n\n")

        buf.write(f"static void run_{struct_name.lower()}_loop(void) {{\n")
        buf.write("    signal(SIGINT, sig_handler);\n")
        buf.write("    int ticks = 0;\n")
        buf.write("    while (!g_stop_requested && ticks < 5) {\n")
        buf.write("        ticks++;\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_trie_tree(self, buf: StringIO, sanity: float, struct_name: str, file_index: int) -> None:
        """Emit 26-ary prefix search trie."""
        buf.write(f"typedef struct {struct_name}TrieNode {{\n")
        buf.write(f"    struct {struct_name}TrieNode *children[26];\n")
        buf.write("    bool is_end_of_word;\n")
        buf.write(f"}} {struct_name}TrieNode;\n\n")

        buf.write(f"static {struct_name}TrieNode *create_trie_node(void) {{\n")
        buf.write(f"    return ({struct_name}TrieNode *)calloc(1, sizeof({struct_name}TrieNode));\n")
        buf.write("}\n\n")

        buf.write(f"static void trie_insert({struct_name}TrieNode *root, const char *key) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write(f"    {struct_name}TrieNode *curr = root;\n")
        buf.write("    for (size_t i = 0; key[i]; i++) {\n")
        buf.write("        int idx = key[i] - 'a';\n")
        buf.write("        if (idx < 0 || idx >= 26) continue;\n")
        buf.write("        if (!curr->children[idx]) curr->children[idx] = create_trie_node();\n")
        buf.write("        curr = curr->children[idx];\n")
        buf.write("    }\n")
        buf.write("    curr->is_end_of_word = true;\n")
        buf.write("}\n")
