"""Enterprise Java code generator.

Synthesizes rich, unpredictable enterprise Java classes spanning multiple architectural archetypes:
Spring Boot transactional services, fluent builder records, reactive event mediators,
and legacy reflection-heavy enterprise beans with deep Stream API pipelines and switch expressions.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class EnterpriseJavaGenerator(SlopGenerator):
    """Enterprise Java class generator.

    Emits Java source code adhering to heavy enterprise conventions across diverse
    architectural archetypes: Spring services, builder records, reactive mediators,
    and reflective legacy beans.
    """

    name = "enterprise_java"
    language = "java"
    extension = ".java"

    JAVA_TYPES = [
        "String", "int", "long", "boolean", "double", "float", "short", "Object",
        "List<String>", "List<Object>", "Map<String, Object>", "Map<String, String>",
        "Optional<String>", "Optional<Object>", "CompletableFuture<Void>", "CompletableFuture<String>",
        "UUID", "Instant", "Duration", "AtomicInteger", "AtomicLong", "AtomicBoolean",
        "ConcurrentMap<String, Object>", "Set<String>", "Supplier<String>",
        "Function<Object, Object>", "ByteBuffer", "BigDecimal", "BigInteger",
    ]

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Java source file (.java).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Java source code.
        """
        buf = StringIO()
        cname = naming.class_name(sanity)
        pkg = naming.java_package(sanity)

        # Select one of 4 distinct architectural archetypes
        archetype = random.choice(["spring_service", "builder_record", "reactive_mediator", "legacy_chaos_bean"])

        buf.write(f"package {pkg};\n\n")
        self._write_imports(buf, sanity, archetype)
        self._write_header_doc(buf, sanity, cname)

        if archetype == "spring_service":
            self._generate_spring_service(buf, sanity, cname, file_index)
        elif archetype == "builder_record":
            self._generate_builder_record(buf, sanity, cname, file_index)
        elif archetype == "reactive_mediator":
            self._generate_reactive_mediator(buf, sanity, cname, file_index)
        else:
            self._generate_legacy_chaos_bean(buf, sanity, cname, file_index)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"java/{cname}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _write_imports(self, buf: StringIO, sanity: float, archetype: str) -> None:
        """Emit imports tailored to the selected Java archetype."""
        imports = [
            "java.io.Serializable",
            "java.time.Instant",
            "java.time.Duration",
            "java.util.UUID",
            "java.util.List",
            "java.util.ArrayList",
            "java.util.Map",
            "java.util.HashMap",
            "java.util.Set",
            "java.util.HashSet",
            "java.util.Optional",
            "java.util.Objects",
            "java.util.Collections",
            "java.util.concurrent.CompletableFuture",
            "java.util.concurrent.ConcurrentHashMap",
            "java.util.concurrent.atomic.AtomicBoolean",
            "java.util.concurrent.atomic.AtomicInteger",
            "java.util.concurrent.atomic.AtomicLong",
            "java.util.stream.Collectors",
            "java.util.stream.Stream",
            "java.util.function.Function",
            "java.util.function.Predicate",
            "java.util.function.Supplier",
        ]

        if archetype == "spring_service":
            imports.extend([
                "org.springframework.stereotype.Service",
                "org.springframework.transaction.annotation.Transactional",
                "org.springframework.beans.factory.annotation.Autowired",
                "org.springframework.cache.annotation.Cacheable",
                "org.springframework.retry.annotation.Retryable",
                "org.slf4j.Logger",
                "org.slf4j.LoggerFactory",
            ])
        elif archetype == "reactive_mediator":
            imports.extend([
                "java.util.concurrent.locks.ReentrantReadWriteLock",
                "java.util.concurrent.CopyOnWriteArrayList",
                "java.util.concurrent.TimeUnit",
                "org.slf4j.Logger",
                "org.slf4j.LoggerFactory",
            ])
        elif archetype == "legacy_chaos_bean":
            imports.extend([
                "java.lang.reflect.Method",
                "java.lang.reflect.Field",
                "java.lang.reflect.InvocationTargetException",
                "java.security.PrivilegedAction",
                "java.util.concurrent.Callable",
            ])

        # Randomize sample and inject random enterprise packages
        sampled = random.sample(imports, random.randint(min(8, len(imports)), len(imports)))
        for imp in sorted(sampled):
            buf.write(f"import {imp};\n")

        extra_imports = random.randint(3, 8)
        for _ in range(extra_imports):
            buf.write(f"import {naming.java_package(sanity)}.{naming.class_name(sanity)};\n")
        buf.write("\n")

    def _write_header_doc(self, buf: StringIO, sanity: float, cname: str) -> None:
        """Write JavaDoc header documentation."""
        buf.write("/**\n")
        buf.write(f" * {comments.docstring(sanity, cname)}\n")
        author_corp = [
            "Enterprise Code Generator", "Architecture Team", "Senior Staff Engineer",
            "Principal Solutions Architect", "Chief Enterprise Evangelist", "Global Infrastructure Committee",
        ]
        author_chaos = [
            "a mass of vibes", "the mass void", "nobody", "the 3am caffeine demon",
            "an unpaid intern", "hyperintelligent racoon", "chatgpt hallucination",
        ]
        buf.write(f" * @author {naming._blend(author_corp, author_chaos, sanity)}\n")
        buf.write(" * @since 1.0.0\n")
        buf.write(" * @deprecated Since before it was written\n")
        buf.write(" */\n")

    def _generate_spring_service(self, buf: StringIO, sanity: float, cname: str, file_index: int) -> None:
        """Emit a Spring Boot transactional service with annotations and streams."""
        buf.write("@Service\n")
        buf.write(f'@Transactional(rollbackFor = Exception.class)\n')
        buf.write(f"public class {cname} implements Serializable {{\n\n")
        buf.write(f'    private static final Logger log = LoggerFactory.getLogger({cname}.class);\n')
        buf.write(f"    private static final long serialVersionUID = {random.randint(1000000, 9999999)}L;\n\n")

        # Injected dependencies
        deps = [f"I{naming.class_name(sanity)}Service" for _ in range(random.randint(2, 4))]
        for dep in deps:
            dep_var = dep[1].lower() + dep[2:]
            buf.write(f"    private final {dep} {dep_var};\n")
        buf.write("    private final AtomicLong transactionCounter = new AtomicLong(0L);\n\n")

        # Constructor injection
        buf.write("    @Autowired\n")
        buf.write(f"    public {cname}(")
        buf.write(", ".join(f"{dep} {dep[1].lower() + dep[2:]}" for dep in deps))
        buf.write(") {\n")
        for dep in deps:
            var = dep[1].lower() + dep[2:]
            buf.write(f"        this.{var} = Objects.requireNonNull({var}, \"{dep} must not be null\");\n")
        buf.write("    }\n\n")

        # Business methods with Stream API, CompletableFutures, and error handling
        num_methods = random.randint(4, 7)
        used_m = set()
        for idx in range(num_methods):
            mname = naming.method_name(sanity)
            if mname in used_m:
                mname = f"{mname}_{idx}"
            used_m.add(mname)
            ret_type = random.choice(["List<String>", "CompletableFuture<Map<String, Object>>", "Optional<String>", "boolean", "int"])
            param_var = naming.var_name(sanity)

            buf.write(f"    /**\n     * {comments.comment(sanity)}\n     */\n")
            if random.random() < 0.5:
                buf.write("    @Cacheable(value = \"enterprise_cache\", key = \"#root.methodName\")\n")
            if random.random() < 0.4:
                buf.write("    @Retryable(maxAttempts = 3)\n")
            buf.write(f"    public {ret_type} {mname}(String {param_var}) {{\n")
            buf.write(f'        log.debug("Invoking {mname} with traceId: {{}}", UUID.randomUUID());\n')
            buf.write(f"        long currentTx = transactionCounter.incrementAndGet();\n")
            buf.write(f"        // {comments.comment(sanity)}\n")

            # Method logic
            if ret_type == "List<String>":
                buf.write(f"        return Stream.of({param_var}, \"{comments.comment(sanity)}\", UUID.randomUUID().toString())\n")
                buf.write(f"            .filter(Objects::nonNull)\n")
                buf.write(f"            .map(item -> item.toUpperCase() + \"_TX_\" + currentTx)\n")
                buf.write(f"            .collect(Collectors.toList());\n")
            elif ret_type == "CompletableFuture<Map<String, Object>>":
                buf.write("        return CompletableFuture.supplyAsync(() -> {\n")
                buf.write("            Map<String, Object> payload = new HashMap<>();\n")
                buf.write('            payload.put("status", "ACTIVE");\n')
                buf.write('            payload.put("timestamp", Instant.now().toString());\n')
                buf.write(f'            payload.put("correlationId", {param_var});\n')
                buf.write("            return Collections.unmodifiableMap(payload);\n")
                buf.write("        }).exceptionally(ex -> {\n")
                buf.write(f'            log.error("Compensating transaction fallback on {mname}", ex);\n')
                buf.write("            return Collections.emptyMap();\n")
                buf.write("        });\n")
            elif ret_type == "Optional<String>":
                buf.write(f"        if ({param_var} == null || {param_var}.isBlank()) {{\n")
                buf.write(f"            return Optional.empty();\n")
                buf.write(f"        }}\n")
                buf.write(f"        return Optional.of({param_var}.trim());\n")
            elif ret_type == "boolean":
                buf.write(f"        try {{\n")
                buf.write(f"            return {param_var} != null && !{param_var}.isEmpty();\n")
                buf.write(f"        }} catch (Exception ex) {{\n")
                buf.write(f'            log.warn("Non-fatal verification fault in {mname}: {{}}", ex.getMessage());\n')
                buf.write(f"            return false;\n")
                buf.write(f"        }}\n")
            else:
                buf.write(f"        return (int) (currentTx % 1000);\n")
            buf.write("    }\n\n")

        # Custom Enterprise Exception class
        buf.write(f"    public static class {cname}ExecutionException extends RuntimeException {{\n")
        buf.write(f"        public {cname}ExecutionException(String message, Throwable cause) {{\n")
        buf.write(f"            super(message, cause);\n")
        buf.write(f"        }}\n")
        buf.write(f"    }}\n")
        buf.write("}\n")

    def _generate_builder_record(self, buf: StringIO, sanity: float, cname: str, file_index: int) -> None:
        """Emit modern Java records and a generic class with static nested Builder."""
        record_name = cname + "Record"
        builder_name = cname + "Builder"

        # Record declaration
        buf.write(f"/** {comments.comment(sanity)} */\n")
        buf.write(f"public record {record_name}(\n")
        record_fields = [
            ("UUID", "id"),
            ("String", "name"),
            ("Instant", "createdAt"),
            ("boolean", "enabled"),
            ("Map<String, String>", "attributes"),
        ]
        for idx, (ftype, fname) in enumerate(record_fields):
            comma = "," if idx < len(record_fields) - 1 else ""
            buf.write(f"    {ftype} {fname}{comma}\n")
        buf.write(") implements Serializable {\n")
        buf.write(f"    public {record_name} {{\n")
        buf.write(f"        Objects.requireNonNull(id, \"Record ID must not be null\");\n")
        buf.write(f"        Objects.requireNonNull(name, \"Name must not be null\");\n")
        buf.write(f"    }}\n")
        buf.write("}\n\n")

        # Main class with Builder
        buf.write(f"public class {cname} {{\n\n")
        num_fields = random.randint(4, 8)
        fields = []
        for _ in range(num_fields):
            ft = random.choice(self.JAVA_TYPES)
            fn = naming.var_name(sanity)
            fields.append((ft, fn))
            buf.write(f"    private final {ft} {fn};\n")
        buf.write(f"    private final {record_name} metadataRecord;\n\n")

        # Private constructor
        buf.write(f"    private {cname}({builder_name} builder) {{\n")
        for ft, fn in fields:
            buf.write(f"        this.{fn} = builder.{fn};\n")
        buf.write(f"        this.metadataRecord = builder.metadataRecord;\n")
        buf.write("    }\n\n")

        # Getters
        for ft, fn in fields:
            cap = fn[0].upper() + fn[1:] if fn else "X"
            buf.write(f"    public {ft} get{cap}() {{\n")
            buf.write(f"        return this.{fn};\n")
            buf.write("    }}\n\n")

        # Static builder factory
        buf.write(f"    public static {builder_name} builder() {{\n")
        buf.write(f"        return new {builder_name}();\n")
        buf.write("    }}\n\n")

        # Static Builder class
        buf.write(f"    public static final class {builder_name} {{\n")
        for ft, fn in fields:
            buf.write(f"        private {ft} {fn};\n")
        buf.write(f"        private {record_name} metadataRecord;\n\n")

        for ft, fn in fields:
            buf.write(f"        public {builder_name} with{fn[0].upper() + fn[1:]}({ft} {fn}) {{\n")
            buf.write(f"            this.{fn} = {fn};\n")
            buf.write(f"            return this;\n")
            buf.write("        }}\n\n")

        buf.write(f"        public {builder_name} withMetadataRecord({record_name} record) {{\n")
        buf.write(f"            this.metadataRecord = record;\n")
        buf.write(f"            return this;\n")
        buf.write("        }}\n\n")

        buf.write(f"        public {cname} build() {{\n")
        buf.write(f"            // {comments.comment(sanity)}\n")
        buf.write(f"            return new {cname}(this);\n")
        buf.write("        }}\n")
        buf.write("    }}\n")
        buf.write("}\n")

    def _generate_reactive_mediator(self, buf: StringIO, sanity: float, cname: str, file_index: int) -> None:
        """Emit a reactive concurrent event mediator with locks and switch expressions."""
        enum_name = cname + "State"
        buf.write(f"public class {cname} {{\n\n")
        buf.write(f"    public enum {enum_name} {{\n")
        states = ["INITIALIZING", "DISPATCHING", "SUSPENDED", "QUARANTINED", "DRAINING", "TERMINATED"]
        for s in states:
            buf.write(f"        {s},\n")
        buf.write("    }\n\n")

        buf.write("    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();\n")
        buf.write("    private final ConcurrentHashMap<String, Object> registry = new ConcurrentHashMap<>();\n")
        buf.write(f"    private volatile {enum_name} currentState = {enum_name}.INITIALIZING;\n\n")

        # Dispatch method with modern switch expressions
        mname = naming.method_name(sanity)
        buf.write(f"    public String {mname}(String eventKey, Object eventPayload) {{\n")
        buf.write("        rwLock.writeLock().lock();\n")
        buf.write("        try {\n")
        buf.write(f"            // {comments.comment(sanity)}\n")
        buf.write("            registry.put(eventKey, eventPayload);\n")
        buf.write("            currentState = switch (currentState) {\n")
        buf.write(f"                case INITIALIZING -> {enum_name}.DISPATCHING;\n")
        buf.write(f"                case DISPATCHING -> eventKey.length() > 10 ? {enum_name}.DRAINING : {enum_name}.DISPATCHING;\n")
        buf.write(f"                case DRAINING -> {enum_name}.QUARANTINED;\n")
        buf.write(f"                default -> {enum_name}.SUSPENDED;\n")
        buf.write("            };\n")
        buf.write("            return \"DISPATCHED_\" + currentState.name() + \"_\" + eventKey;\n")
        buf.write("        } finally {\n")
        buf.write("            rwLock.writeLock().unlock();\n")
        buf.write("        }\n")
        buf.write("    }\n\n")

        # Read method
        buf.write("    public Optional<Object> querySnapshot(String key) {\n")
        buf.write("        rwLock.readLock().lock();\n")
        buf.write("        try {\n")
        buf.write("            return Optional.ofNullable(registry.get(key));\n")
        buf.write("        } finally {\n")
        buf.write("            rwLock.readLock().unlock();\n")
        buf.write("        }\n")
        buf.write("    }\n\n")

        # Telemetry method
        buf.write("    public Map<String, Object> exportMetrics() {\n")
        buf.write("        return Map.of(\n")
        buf.write("            \"state\", currentState.name(),\n")
        buf.write("            \"size\", registry.size(),\n")
        buf.write("            \"timestamp\", Instant.now().toEpochMilli()\n")
        buf.write("        );\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_legacy_chaos_bean(self, buf: StringIO, sanity: float, cname: str, file_index: int) -> None:
        """Emit a legacy enterprise monstrosity with reflection and anonymous inner classes."""
        buf.write(f"public class {cname} implements Serializable {{\n\n")
        buf.write(f"    private static final long serialVersionUID = {random.randint(1000000, 9999999)}L;\n")
        buf.write("    private final Map<String, Object> shadowMemory = new HashMap<>();\n\n")

        num_methods = random.randint(4, 7)
        used_m = set()
        for idx in range(num_methods):
            mname = naming.method_name(sanity)
            if mname in used_m:
                mname = f"{mname}_{idx}"
            used_m.add(mname)
            buf.write(f"    @SuppressWarnings(\"unchecked\")\n")
            buf.write(f"    public <T> T {mname}(Class<T> expectedType, Object... args) {{\n")
            buf.write(f"        // {comments.comment(sanity)}\n")
            buf.write(f"        try {{\n")
            buf.write(f"            Method[] declaredMethods = this.getClass().getDeclaredMethods();\n")
            buf.write(f"            for (Method m : declaredMethods) {{\n")
            buf.write(f"                if (m.getName().equals(\"{mname}\") && m.getParameterCount() == 2) {{\n")
            buf.write(f"                    shadowMemory.put(\"{mname}_invoked\", true);\n")
            buf.write(f"                }}\n")
            buf.write(f"            }}\n")
            buf.write(f"            if (args != null && args.length > 0 && expectedType.isInstance(args[0])) {{\n")
            buf.write(f"                return (T) args[0];\n")
            buf.write(f"            }}\n")
            buf.write(f"            return expectedType.getDeclaredConstructor().newInstance();\n")
            buf.write(f"        }} catch (Exception ex) {{\n")
            buf.write(f"            throw new IllegalStateException(\"Reflection invocation failure in {mname}\", ex);\n")
            buf.write(f"        }}\n")
            buf.write("    }\n\n")

        # Anonymous inner class worker
        buf.write("    public void executePrivilegedTask() {\n")
        buf.write("        Callable<Void> task = new Callable<Void>() {\n")
        buf.write("            @Override\n")
        buf.write("            public Void call() throws Exception {\n")
        buf.write(f"                // {comments.comment(sanity)}\n")
        buf.write("                shadowMemory.clear();\n")
        buf.write("                return null;\n")
        buf.write("            }\n")
        buf.write("        };\n")
        buf.write("        try {\n")
        buf.write("            task.call();\n")
        buf.write("        } catch (Exception ignored) {\n")
        buf.write(f"            // {comments.comment(sanity)}\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n")
