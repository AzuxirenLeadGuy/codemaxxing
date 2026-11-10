"""JavaScript and TypeScript synthetic code generator.

Synthesizes modern JavaScript and TypeScript source files across diverse archetypes:
TypeScript reactive observable streams, React hook components, Node.js stream microservices,
and metaprogramming proxy interceptor traps.
"""

import random
from io import StringIO

from codemaxxing.generators.base import SlopGenerator, GeneratedFile
from codemaxxing import naming, comments


class JavaScriptGenerator(SlopGenerator):
    """JavaScript/TypeScript code generator.

    Emits JavaScript or TypeScript source files spanning reactive observables,
    hook-driven components, Node.js streams, and dynamic proxy traps.
    """

    name = "javascript"
    language = "javascript"
    extension = ".js"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic JavaScript or TypeScript source file (.js or .ts).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized JavaScript or TypeScript code.
        """
        buf = StringIO()
        use_ts = random.random() < 0.6  # 60% TypeScript for rich type syntax
        ext = ".ts" if use_ts else ".js"
        module_name = naming.class_name(sanity)

        archetype = random.choice([
            "ts_reactive_stream",
            "react_hook_component",
            "node_stream_service",
            "chaos_proxy_trap",
        ])

        buf.write(f"// {comments.comment(sanity)}\n")
        buf.write("'use strict';\n\n")

        if archetype == "ts_reactive_stream":
            self._generate_reactive_stream(buf, sanity, module_name, use_ts)
        elif archetype == "react_hook_component":
            self._generate_hook_component(buf, sanity, module_name, use_ts)
        elif archetype == "node_stream_service":
            self._generate_node_service(buf, sanity, module_name, use_ts)
        else:
            self._generate_proxy_trap(buf, sanity, module_name, use_ts)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"js/{module_name}_{file_index}{ext}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_reactive_stream(self, buf: StringIO, sanity: float, module_name: str, use_ts: bool) -> None:
        """Emit TypeScript reactive observable stream with generics and operators."""
        if use_ts:
            buf.write("export type Action<T = unknown> = { type: string; payload: T; timestamp: number };\n")
            buf.write("export type Operator<T, R> = (source: AsyncIterable<T>) => AsyncIterable<R>;\n\n")

        buf.write(f"export class {module_name}Stream {{\n")
        buf.write("  constructor() {\n")
        buf.write("    this._handlers = new Map();\n")
        buf.write("    this._isTerminated = false;\n")
        buf.write("  }\n\n")

        # Subscribe method
        buf.write("  subscribe(eventType, callback) {\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    if (!this._handlers.has(eventType)) {\n")
        buf.write("      this._handlers.set(eventType, new Set());\n")
        buf.write("    }\n")
        buf.write("    this._handlers.get(eventType).add(callback);\n")
        buf.write("    return () => this._handlers.get(eventType).delete(callback);\n")
        buf.write("  }\n\n")

        # Dispatch method
        mname = naming.method_name(sanity)
        buf.write(f"  async {mname}(event) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    const listeners = this._handlers.get(event.type) || [];\n")
        buf.write("    const results = await Promise.allSettled(\n")
        buf.write("      Array.from(listeners).map(fn => fn(event))\n")
        buf.write("    );\n")
        buf.write("    return results.filter(r => r.status === 'fulfilled').map(r => r.value);\n")
        buf.write("  }\n\n")

        # Async generator pipe
        buf.write("  async *pipe(items, ...operators) {\n")
        buf.write("    let current = items;\n")
        buf.write("    for (const op of operators) {\n")
        buf.write("      current = op(current);\n")
        buf.write("    }\n")
        buf.write("    for await (const val of current) {\n")
        buf.write("      yield val;\n")
        buf.write("    }\n")
        buf.write("  }\n")
        buf.write("}\n")

    def _generate_hook_component(self, buf: StringIO, sanity: float, module_name: str, use_ts: bool) -> None:
        """Emit a modern React hook and UI component pattern."""
        buf.write("// Mock React Hooks ecosystem\n")
        buf.write("const useState = (init) => [init, (v) => v];\n")
        buf.write("const useEffect = (cb, deps) => { cb(); };\n")
        buf.write("const useMemo = (fn, deps) => fn();\n")
        buf.write("const useRef = (init) => ({ current: init });\n\n")

        hook_name = f"use{module_name}"
        buf.write(f"export function {hook_name}(initialConfig = {{}}) {{\n")
        buf.write("  const [state, setState] = useState({ loading: false, data: null, error: null });\n")
        buf.write("  const renderCount = useRef(0);\n\n")
        buf.write("  useEffect(() => {\n")
        buf.write("    renderCount.current += 1;\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    const timer = setTimeout(() => {\n")
        buf.write("      setState({ loading: false, data: { status: 'ONLINE', count: renderCount.current }, error: null });\n")
        buf.write("    }, 50);\n")
        buf.write("    return () => clearTimeout(timer);\n")
        buf.write("  }, []);\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"  const {mname} = useMemo(() => () => {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    return { rendered: renderCount.current, timestamp: Date.now() };\n")
        buf.write("  }}, [state]);\n\n")
        buf.write(f"  return {{ state, {mname} }};\n")
        buf.write("}\n\n")

        buf.write(f"export function {module_name}Component(props) {{\n")
        buf.write(f"  const {{ state, {mname} }} = {hook_name}(props);\n")
        buf.write("  return {\n")
        buf.write("    type: 'div',\n")
        buf.write("    props: { className: 'enterprise-container', children: state.data ? 'Ready' : 'Loading' },\n")
        buf.write("  };\n")
        buf.write("}\n")

    def _generate_node_service(self, buf: StringIO, sanity: float, module_name: str, use_ts: bool) -> None:
        """Emit Node.js microservice router with middleware and EventEmitter."""
        buf.write("const EventEmitter = require('events');\n\n")
        buf.write(f"export class {module_name}Service extends EventEmitter {{\n")
        buf.write("  constructor(options = {}) {\n")
        buf.write("    super();\n")
        buf.write("    this.options = options;\n")
        buf.write("    this.middlewares = [];\n")
        buf.write("  }\n\n")

        buf.write("  use(fn) {\n")
        buf.write("    this.middlewares.push(fn);\n")
        buf.write("    return this;\n")
        buf.write("  }\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"  async {mname}(ctx) {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    let index = -1;\n")
        buf.write("    const dispatch = async (i) => {\n")
        buf.write("      if (i <= index) throw new Error('next() called multiple times');\n")
        buf.write("      index = i;\n")
        buf.write("      const fn = this.middlewares[i];\n")
        buf.write("      if (!fn) return;\n")
        buf.write("      return fn(ctx, () => dispatch(i + 1));\n")
        buf.write("    };\n")
        buf.write("    await dispatch(0);\n")
        buf.write(f"    this.emit('{mname}:complete', ctx);\n")
        buf.write("    return ctx;\n")
        buf.write("  }\n")
        buf.write("}\n")

    def _generate_proxy_trap(self, buf: StringIO, sanity: float, module_name: str, use_ts: bool) -> None:
        """Emit dynamic Proxy metaprogramming traps with reflection."""
        buf.write(f"export function create{module_name}Proxy(target = {{}}) {{\n")
        buf.write("  const shadowStore = new Map();\n\n")
        buf.write("  return new Proxy(target, {\n")
        buf.write("    get(obj, prop, receiver) {\n")
        buf.write("      if (prop === 'isProxy') return true;\n")
        buf.write("      if (shadowStore.has(prop)) return shadowStore.get(prop);\n")
        buf.write(f"      // {comments.comment(sanity)}\n")
        buf.write("      if (typeof prop === 'string' && prop.startsWith('get')) {\n")
        buf.write("        return () => Reflect.get(obj, prop.slice(3).toLowerCase(), receiver);\n")
        buf.write("      }\n")
        buf.write("      return Reflect.get(obj, prop, receiver);\n")
        buf.write("    },\n\n")
        buf.write("    set(obj, prop, value, receiver) {\n")
        buf.write(f"      // {comments.comment(sanity)}\n")
        buf.write("      shadowStore.set(prop, value);\n")
        buf.write("      return Reflect.set(obj, prop, value, receiver);\n")
        buf.write("    },\n")
        buf.write("  });\n")
        buf.write("}\n")
