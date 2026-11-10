"""C++ enterprise code generator.

Synthesizes rich C++ source files across 11 distinct archetypes:
modern C++20 concepts and fold expressions, RAII smart pointer pipelines,
Curiously Recurring Template Patterns (CRTP), compile-time template metaprogramming,
C++20 stackless coroutines, multi-threaded packaged task worker pools,
lockless tagged atomic stacks, std::variant state machines with visitors,
PMR polymorphic memory resource allocators, expression template linear algebra,
and strongly typed signal/slot observer event dispatchers.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class CppEnterpriseGenerator(SlopGenerator):
    """Modern C++ enterprise pattern code generator.

    Emits object-oriented and template-metaprogramming C++ across eleven varied
    archetypes for deep architectural diversity and realistic sophistication.
    """

    name = "cpp_enterprise"
    language = "cpp"
    extension = ".cpp"

    ARCHETYPES = [
        "modern_cpp20_concepts",
        "raii_smart_pipeline",
        "crtp_factory",
        "chaos_template_meta",
        "cpp20_coroutines",
        "thread_pool_future",
        "lockfree_tagged_stack",
        "state_machine_variant",
        "custom_allocator_pmr",
        "expression_templates",
        "observer_signals_slots",
    ]

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

        archetype = random.choice(self.ARCHETYPES)

        if archetype == "modern_cpp20_concepts":
            self._generate_cpp20_concepts(buf, sanity, class_name)
        elif archetype == "raii_smart_pipeline":
            self._generate_raii_pipeline(buf, sanity, class_name)
        elif archetype == "crtp_factory":
            self._generate_crtp_factory(buf, sanity, class_name)
        elif archetype == "chaos_template_meta":
            self._generate_template_meta(buf, sanity, class_name)
        elif archetype == "cpp20_coroutines":
            self._generate_coroutines(buf, sanity, class_name)
        elif archetype == "thread_pool_future":
            self._generate_thread_pool(buf, sanity, class_name)
        elif archetype == "lockfree_tagged_stack":
            self._generate_lockfree_stack(buf, sanity, class_name)
        elif archetype == "state_machine_variant":
            self._generate_state_machine(buf, sanity, class_name)
        elif archetype == "custom_allocator_pmr":
            self._generate_pmr_allocator(buf, sanity, class_name)
        elif archetype == "expression_templates":
            self._generate_expr_templates(buf, sanity, class_name)
        else:
            self._generate_signals_slots(buf, sanity, class_name)

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

        buf.write("    template<typename... Args>\n")
        buf.write("    auto foldSum(Args... args) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        return (... + args);\n")
        buf.write("    }\n\n")

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

    def _generate_coroutines(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit C++20 stackless coroutines with generator handles."""
        buf.write("#include <coroutine>\n\n")
        buf.write(f"struct {class_name}Generator {{\n")
        buf.write("    struct promise_type {\n")
        buf.write("        int current_value;\n")
        buf.write(f"        {class_name}Generator get_return_object() {{\n")
        buf.write(f"            return {class_name}Generator{{std::coroutine_handle<promise_type>::from_promise(*this)}};\n")
        buf.write("        }\n")
        buf.write("        std::suspend_always initial_suspend() noexcept { return {}; }\n")
        buf.write("        std::suspend_always final_suspend() noexcept { return {}; }\n")
        buf.write("        std::suspend_always yield_value(int value) noexcept {\n")
        buf.write("            current_value = value;\n")
        buf.write("            return {};\n")
        buf.write("        }\n")
        buf.write("        void return_void() noexcept {}\n")
        buf.write("        void unhandled_exception() { std::terminate(); }\n")
        buf.write("    };\n")
        buf.write("    std::coroutine_handle<promise_type> handle;\n")
        buf.write(f"    explicit {class_name}Generator(std::coroutine_handle<promise_type> h) : handle(h) {{}}\n")
        buf.write(f"    ~{class_name}Generator() {{ if (handle) handle.destroy(); }}\n")
        buf.write("};\n")

    def _generate_thread_pool(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit multi-threaded worker pool with packaged_task and condition_variable."""
        buf.write("#include <queue>\n#include <thread>\n#include <future>\n#include <condition_variable>\n\n")
        buf.write(f"class {class_name}ThreadPool {{\n")
        buf.write("    std::vector<std::thread> workers;\n")
        buf.write("    std::queue<std::packaged_task<void()>> tasks;\n")
        buf.write("    std::mutex queue_mutex;\n")
        buf.write("    std::condition_variable cv;\n")
        buf.write("    bool stop = false;\n\n")
        buf.write("public:\n")
        buf.write(f"    explicit {class_name}ThreadPool(size_t threads = 4) {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        (void)threads;\n")
        buf.write("    }\n")
        buf.write(f"    ~{class_name}ThreadPool() {{\n")
        buf.write("        stop = true;\n")
        buf.write("        cv.notify_all();\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_lockfree_stack(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit lock-free atomic stack with CAS loop."""
        buf.write("#include <atomic>\n\n")
        buf.write(f"template<typename T>\nclass {class_name}LockFreeStack {{\n")
        buf.write("    struct Node {\n")
        buf.write("        T data;\n")
        buf.write("        Node* next;\n")
        buf.write("        Node(T val) : data(val), next(nullptr) {}\n")
        buf.write("    };\n")
        buf.write("    std::atomic<Node*> head{nullptr};\n\n")
        buf.write("public:\n")
        buf.write("    void push(T val) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        Node* new_node = new Node(val);\n")
        buf.write("        new_node->next = head.load(std::memory_order_relaxed);\n")
        buf.write("        while (!head.compare_exchange_weak(new_node->next, new_node, std::memory_order_release, std::memory_order_relaxed));\n")
        buf.write("    }\n")
        buf.write("};\n")

    def _generate_state_machine(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit std::variant finite state machine with overloaded lambdas."""
        buf.write("struct StateIdle {};\nstruct StateActive { int transactions; };\nstruct StateHalted {};\n\n")
        buf.write(f"using {class_name}State = std::variant<StateIdle, StateActive, StateHalted>;\n\n")
        buf.write("template<class... Ts> struct Overloaded : Ts... { using Ts::operator()...; };\n")
        buf.write("template<class... Ts> Overloaded(Ts...) -> Overloaded<Ts...>;\n\n")
        buf.write(f"inline std::string describeState(const {class_name}State& s) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    return std::visit(Overloaded{\n")
        buf.write('        [](const StateIdle&) { return "IDLE"; },\n')
        buf.write('        [](const StateActive& a) { return "ACTIVE:" + std::to_string(a.transactions); },\n')
        buf.write('        [](const StateHalted&) { return "HALTED"; }\n')
        buf.write("    }, s);\n")
        buf.write("}\n")

    def _generate_pmr_allocator(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit C++17 Polymorphic Memory Resource (PMR) buffer manager."""
        buf.write("#include <memory_resource>\n\n")
        buf.write(f"class {class_name}PmrBuffer {{\n")
        buf.write("    char buffer[2048];\n")
        buf.write("    std::pmr::monotonic_buffer_resource pool;\n")
        buf.write("public:\n")
        buf.write(f"    {class_name}PmrBuffer() : pool(buffer, sizeof(buffer)) {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("    }\n")
        buf.write("    std::pmr::memory_resource* resource() { return &pool; }\n")
        buf.write("};\n")

    def _generate_expr_templates(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit lazy linear algebra expression templates."""
        buf.write("template<typename L, typename R>\n")
        buf.write("struct VecAdd {\n")
        buf.write("    const L& lhs; const R& rhs;\n")
        buf.write("    VecAdd(const L& l, const R& r) : lhs(l), rhs(r) {}\n")
        buf.write("    auto operator[](size_t i) const { return lhs[i] + rhs[i]; }\n")
        buf.write("};\n\n")
        buf.write(f"struct {class_name}Vector {{\n")
        buf.write("    double data[4] = {1.0, 2.0, 3.0, 4.0};\n")
        buf.write("    double operator[](size_t i) const { return data[i]; }\n")
        buf.write("};\n")

    def _generate_signals_slots(self, buf: StringIO, sanity: float, class_name: str) -> None:
        """Emit type-safe multicast signal/slot observer."""
        buf.write("#include <functional>\n\n")
        buf.write(f"class {class_name}Signal {{\n")
        buf.write("    std::vector<std::function<void(const std::string&)>> slots;\n")
        buf.write("public:\n")
        buf.write("    void connect(std::function<void(const std::string&)> slot) {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        slots.push_back(slot);\n")
        buf.write("    }\n")
        buf.write("    void emit(const std::string& msg) {\n")
        buf.write("        for (auto& s : slots) s(msg);\n")
        buf.write("    }\n")
        buf.write("};\n")
