"""Go synthetic code generator.

Synthesizes diverse Go source files across multiple distinct archetypes:
gRPC streaming microservice handlers, concurrent worker pools with atomic CAS operations,
generic Go 1.18+ thread-safe caches, and unsafe low-level memory manipulation stubs.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class GoSlopGenerator(SlopGenerator):
    """Go slop code generator.

    Emits idiomatic Go source files spanning gRPC streaming servers, worker pools,
    generic caches, and low-level unsafe routines.
    """

    name = "go_slop"
    language = "go"
    extension = ".go"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Go source file (.go).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Go source code.
        """
        buf = StringIO()
        pkg = naming.go_package(sanity)
        struct_name = naming.class_name(sanity)

        buf.write(f"package {pkg}\n\n")

        archetype = random.choice([
            "grpc_streaming_service",
            "concurrent_worker_pool",
            "generic_cache",
            "unsafe_low_level",
        ])

        if archetype == "grpc_streaming_service":
            self._generate_grpc_service(buf, sanity, struct_name)
        elif archetype == "concurrent_worker_pool":
            self._generate_worker_pool(buf, sanity, struct_name)
        elif archetype == "generic_cache":
            self._generate_generic_cache(buf, sanity, struct_name)
        else:
            self._generate_unsafe_routine(buf, sanity, struct_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"go/{struct_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_grpc_service(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit gRPC streaming server with context, metadata, and sync.Pool."""
        buf.write("import (\n")
        buf.write('\t"bytes"\n')
        buf.write('\t"context"\n')
        buf.write('\t"errors"\n')
        buf.write('\t"fmt"\n')
        buf.write('\t"io"\n')
        buf.write('\t"sync"\n')
        buf.write('\t"time"\n')
        buf.write(")\n\n")

        buf.write(f"// {comments.comment(sanity)}\n")
        buf.write(f"type {struct_name}Server struct {{\n")
        buf.write("\tmu sync.RWMutex\n")
        buf.write("\tbufferPool sync.Pool\n")
        buf.write("\tisHealthy  bool\n")
        buf.write("}\n\n")

        # Constructor
        buf.write(f"func New{struct_name}Server() *{struct_name}Server {{\n")
        buf.write(f"\treturn &{struct_name}Server{{\n")
        buf.write("\t\tisHealthy: true,\n")
        buf.write("\t\tbufferPool: sync.Pool{\n")
        buf.write("\t\t\tNew: func() any { return new(bytes.Buffer) },\n")
        buf.write("\t\t},\n")
        buf.write("\t}\n")
        buf.write("}\n\n")

        mname = naming.method_name(sanity)
        mname = mname[0].upper() + mname[1:]
        buf.write(f"func (s *{struct_name}Server) {mname}(ctx context.Context, inStream <-chan []byte) (<-chan []byte, error) {{\n")
        buf.write("\ts.mu.RLock()\n")
        buf.write("\tdefer s.mu.RUnlock()\n\n")
        buf.write("\tif !s.isHealthy {\n")
        buf.write('\t\treturn nil, errors.New("server is not accepting connections")\n')
        buf.write("\t}\n\n")
        buf.write("\toutStream := make(chan []byte, 32)\n")
        buf.write("\tgo func() {\n")
        buf.write("\t\tdefer close(outStream)\n")
        buf.write("\t\tfor {\n")
        buf.write("\t\t\tselect {\n")
        buf.write("\t\t\tcase <-ctx.Done():\n")
        buf.write("\t\t\t\treturn\n")
        buf.write("\t\t\tcase payload, ok := <-inStream:\n")
        buf.write("\t\t\t\tif !ok {\n")
        buf.write("\t\t\t\t\treturn\n")
        buf.write("\t\t\t\t}\n")
        buf.write("\t\t\t\tbuf := s.bufferPool.Get().(*bytes.Buffer)\n")
        buf.write("\t\t\t\tbuf.Reset()\n")
        buf.write(f"\t\t\t\tbuf.WriteString(\"ACK: \")\n")
        buf.write("\t\t\t\tbuf.Write(payload)\n")
        buf.write("\t\t\t\toutStream <- append([]byte(nil), buf.Bytes()...)\n")
        buf.write("\t\t\t\ts.bufferPool.Put(buf)\n")
        buf.write("\t\t\t}\n")
        buf.write("\t\t}\n")
        buf.write("\t}()\n\n")
        buf.write("\treturn outStream, nil\n")
        buf.write("}\n")

    def _generate_worker_pool(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit concurrent worker pool with atomic CAS operations and channels."""
        buf.write("import (\n")
        buf.write('\t"context"\n')
        buf.write('\t"sync"\n')
        buf.write('\t"sync/atomic"\n')
        buf.write('\t"time"\n')
        buf.write(")\n\n")

        job_name = f"{struct_name}Job"
        buf.write(f"type {job_name} struct {{\n")
        buf.write("\tID        int64\n")
        buf.write("\tPayload   any\n")
        buf.write("\tCreatedAt time.Time\n")
        buf.write("}\n\n")

        buf.write(f"type {struct_name}Pool struct {{\n")
        buf.write(f"\tjobs      chan {job_name}\n")
        buf.write("\tworkers   int\n")
        buf.write("\tprocessed atomic.Int64\n")
        buf.write("\twg        sync.WaitGroup\n")
        buf.write("}\n\n")

        buf.write(f"func New{struct_name}Pool(workers int, queueSize int) *{struct_name}Pool {{\n")
        buf.write(f"\treturn &{struct_name}Pool{{\n")
        buf.write(f"\t\tjobs:    make(chan {job_name}, queueSize),\n")
        buf.write("\t\tworkers: workers,\n")
        buf.write("\t}\n")
        buf.write("}\n\n")

        buf.write(f"func (p *{struct_name}Pool) Start(ctx context.Context) {{\n")
        buf.write("\tfor i := 0; i < p.workers; i++ {\n")
        buf.write("\t\tp.wg.Add(1)\n")
        buf.write("\t\tgo func(workerID int) {\n")
        buf.write("\t\t\tdefer p.wg.Done()\n")
        buf.write("\t\t\tfor {\n")
        buf.write("\t\t\t\tselect {\n")
        buf.write("\t\t\t\tcase <-ctx.Done():\n")
        buf.write("\t\t\t\t\treturn\n")
        buf.write("\t\t\t\tcase job, ok := <-p.jobs:\n")
        buf.write("\t\t\t\t\tif !ok {\n")
        buf.write("\t\t\t\t\t\treturn\n")
        buf.write("\t\t\t\t\t}\n")
        buf.write("\t\t\t\t\tp.processed.Add(1)\n")
        buf.write(f"\t\t\t\t\t_ = job // {comments.comment(sanity)}\n")
        buf.write("\t\t\t\t}\n")
        buf.write("\t\t\t}\n")
        buf.write("\t\t}(i)\n")
        buf.write("\t}\n")
        buf.write("}\n")

    def _generate_generic_cache(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit Go 1.18+ generic thread-safe cache."""
        buf.write("import (\n")
        buf.write('\t"sync"\n')
        buf.write('\t"time"\n')
        buf.write(")\n\n")

        buf.write(f"type {struct_name}Cache[K comparable, V any] struct {{\n")
        buf.write("\tmu      sync.RWMutex\n")
        buf.write("\tentries map[K]V\n")
        buf.write("\texpiries map[K]time.Time\n")
        buf.write("}\n\n")

        buf.write(f"func New{struct_name}Cache[K comparable, V any]() *{struct_name}Cache[K, V] {{\n")
        buf.write(f"\treturn &{struct_name}Cache[K, V]{{\n")
        buf.write("\t\tentries:  make(map[K]V),\n")
        buf.write("\t\texpiries: make(map[K]time.Time),\n")
        buf.write("\t}\n")
        buf.write("}\n\n")

        buf.write(f"func (c *{struct_name}Cache[K, V]) Set(key K, val V, ttl time.Duration) {{\n")
        buf.write("\tc.mu.Lock()\n")
        buf.write("\tdefer c.mu.Unlock()\n")
        buf.write("\tc.entries[key] = val\n")
        buf.write("\tc.expiries[key] = time.Now().Add(ttl)\n")
        buf.write("}\n\n")

        buf.write(f"func (c *{struct_name}Cache[K, V]) Get(key K) (V, bool) {{\n")
        buf.write("\tc.mu.RLock()\n")
        buf.write("\tdefer c.mu.RUnlock()\n")
        buf.write("\tval, ok := c.entries[key]\n")
        buf.write("\tif !ok || time.Now().After(c.expiries[key]) {{\n")
        buf.write("\t\tvar zero V\n")
        buf.write("\t\treturn zero, false\n")
        buf.write("\t}\n")
        buf.write("\treturn val, true\n")
        buf.write("}\n")

    def _generate_unsafe_routine(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit low-level unsafe pointer conversions with panic recovery."""
        buf.write("import (\n")
        buf.write('\t"fmt"\n')
        buf.write('\t"unsafe"\n')
        buf.write(")\n\n")

        buf.write(f"// FastString converts a byte slice to string with zero heap allocations.\n")
        buf.write(f"func FastString_{struct_name}(b []byte) (s string) {{\n")
        buf.write("\tdefer func() {\n")
        buf.write("\t\tif r := recover(); r != nil {\n")
        buf.write(f"\t\t\t// {comments.comment(sanity)}\n")
        buf.write("\t\t\ts = string(b)\n")
        buf.write("\t\t}\n")
        buf.write("\t}()\n")
        buf.write("\tif len(b) == 0 {\n")
        buf.write('\t\treturn ""\n')
        buf.write("\t}\n")
        buf.write("\treturn *(*string)(unsafe.Pointer(&b))\n")
        buf.write("}\n")
