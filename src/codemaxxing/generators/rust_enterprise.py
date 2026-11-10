"""Rust enterprise code generator.

Synthesizes rich Rust source files across 11 distinct archetypes:
Tokio async actors with message channels, compile-time typestate builders,
custom thread-safe Iterator/Stream pipelines, unsafe macro metaprogramming,
Tower/Axum middleware services with poll_ready, zero-copy lifetime slice parsers,
syn/quote procedural derive macro AST generators, lock-free AtomicPtr queues,
handwritten pin-projected Future state machines, Entity Component Systems (ECS),
and generational arena index allocators.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class RustEnterpriseGenerator(SlopGenerator):
    """Enterprise Rust code generator.

    Emits safe and idiomatic Rust source code spanning async actors,
    typestate builders, custom iterators, Tower services, zero-copy parsers,
    lock-free queues, and generational memory arenas.
    """

    name = "rust_enterprise"
    language = "rust"
    extension = ".rs"

    ARCHETYPES = [
        "tokio_async_actor",
        "typestate_builder",
        "custom_iterator",
        "unsafe_macro_slop",
        "tower_middleware_service",
        "zero_copy_slice_parser",
        "proc_macro_ast_derive",
        "lockfree_atomic_queue",
        "pin_projected_future",
        "ecs_component_system",
        "generational_arena",
    ]

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Rust source file (.rs).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Rust source code.
        """
        buf = StringIO()
        module_name = naming.class_name(sanity)
        struct_name = naming.class_name(sanity)

        buf.write(f"//! {comments.docstring(sanity, module_name)}\n\n")
        buf.write("use std::fmt::{self, Display, Formatter};\n")
        buf.write("use std::sync::atomic::{AtomicU64, Ordering};\n")
        buf.write("use std::sync::{Arc, RwLock};\n\n")

        archetype = random.choice(self.ARCHETYPES)

        if archetype == "tokio_async_actor":
            self._generate_async_actor(buf, sanity, struct_name)
        elif archetype == "typestate_builder":
            self._generate_typestate(buf, sanity, struct_name)
        elif archetype == "custom_iterator":
            self._generate_iterator(buf, sanity, struct_name)
        elif archetype == "unsafe_macro_slop":
            self._generate_macro_slop(buf, sanity, struct_name)
        elif archetype == "tower_middleware_service":
            self._generate_tower_service(buf, sanity, struct_name)
        elif archetype == "zero_copy_slice_parser":
            self._generate_slice_parser(buf, sanity, struct_name)
        elif archetype == "proc_macro_ast_derive":
            self._generate_proc_macro_ast(buf, sanity, struct_name)
        elif archetype == "lockfree_atomic_queue":
            self._generate_lockfree_queue(buf, sanity, struct_name)
        elif archetype == "pin_projected_future":
            self._generate_pin_future(buf, sanity, struct_name)
        elif archetype == "ecs_component_system":
            self._generate_ecs(buf, sanity, struct_name)
        else:
            self._generate_generational_arena(buf, sanity, struct_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"rust/{module_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_async_actor(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit async actor pattern with custom error handling."""
        err_name = f"{struct_name}Error"
        buf.write("#[derive(Debug, Clone)]\n")
        buf.write(f"pub enum {err_name} {{\n")
        buf.write("    ChannelClosed,\n    Timeout,\n    ValidationFailed(String),\n")
        buf.write("}\n\n")

        buf.write(f"impl Display for {err_name} {{\n")
        buf.write("    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {\n")
        buf.write('        write!(f, "{:?}", self)\n')
        buf.write("    }\n")
        buf.write("}\n\n")
        buf.write(f"impl std::error::Error for {err_name} {{}}\n\n")

        buf.write(f"pub struct {struct_name}Actor {{\n")
        buf.write("    processed_count: Arc<AtomicU64>,\n")
        buf.write("}\n\n")

        buf.write(f"impl {struct_name}Actor {{\n")
        buf.write("    pub fn new() -> Self {\n")
        buf.write("        Self { processed_count: Arc::new(AtomicU64::new(0)) }\n")
        buf.write("    }\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    pub fn {mname}(&self, payload: &str) -> Result<u64, {err_name}> {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        if payload.is_empty() {\n")
        buf.write(f'            return Err({err_name}::ValidationFailed("empty payload".into()));\n')
        buf.write("        }\n")
        buf.write("        let prev = self.processed_count.fetch_add(1, Ordering::SeqCst);\n")
        buf.write("        Ok(prev + 1)\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_typestate(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit zero-cost typestate builder."""
        buf.write("use std::marker::PhantomData;\n\n")
        buf.write("pub struct Uninitialized;\n")
        buf.write("pub struct Configured;\n\n")

        buf.write(f"pub struct {struct_name}Builder<State> {{\n")
        buf.write("    endpoint: Option<String>,\n")
        buf.write("    _state: PhantomData<State>,\n")
        buf.write("}\n\n")

        buf.write(f"impl {struct_name}Builder<Uninitialized> {{\n")
        buf.write("    pub fn new() -> Self {\n")
        buf.write("        Self { endpoint: None, _state: PhantomData }\n")
        buf.write("    }\n\n")
        buf.write(f"    pub fn with_endpoint(self, ep: impl Into<String>) -> {struct_name}Builder<Configured> {{\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write(f"        {struct_name}Builder {{\n")
        buf.write("            endpoint: Some(ep.into()),\n")
        buf.write("            _state: PhantomData,\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n\n")

        buf.write(f"impl {struct_name}Builder<Configured> {{\n")
        buf.write("    pub fn build(self) -> String {\n")
        buf.write('        self.endpoint.unwrap_or_else(|| "default".into())\n')
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_iterator(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit custom Iterator with thread-safe lock."""
        buf.write(f"pub struct {struct_name}Iter {{\n")
        buf.write("    data: Arc<RwLock<Vec<u32>>>,\n")
        buf.write("    cursor: usize,\n")
        buf.write("}\n\n")

        buf.write(f"impl Iterator for {struct_name}Iter {{\n")
        buf.write("    type Item = u32;\n\n")
        buf.write("    fn next(&mut self) -> Option<Self::Item> {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        let guard = self.data.read().ok()?;\n")
        buf.write("        if self.cursor < guard.len() {\n")
        buf.write("            let val = guard[self.cursor];\n")
        buf.write("            self.cursor += 1;\n")
        buf.write("            Some(val)\n")
        buf.write("        } else {\n")
        buf.write("            None\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_macro_slop(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit declarative macro and unsafe block."""
        buf.write("macro_rules! enterprise_eval {\n")
        buf.write("    ($val:expr) => {\n")
        buf.write("        $val.trim().to_uppercase()\n")
        buf.write("    };\n")
        buf.write("}\n\n")

        buf.write(f"pub fn compute_{struct_name.lower()}(input: &str) -> String {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    enterprise_eval!(input)\n")
        buf.write("}\n")

    def _generate_tower_service(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit Tower/Axum async middleware service."""
        buf.write("pub struct Request<T> { pub payload: T }\n")
        buf.write("pub struct Response<T> { pub body: T }\n\n")

        buf.write(f"pub struct {struct_name}Service<S> {{\n")
        buf.write("    inner: S,\n")
        buf.write("}\n\n")

        buf.write(f"impl<S> {struct_name}Service<S> {{\n")
        buf.write("    pub fn new(inner: S) -> Self {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        Self { inner }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_slice_parser(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit Nom-style zero-copy byte slice parser."""
        buf.write(f"pub struct {struct_name}Slice<'a> {{\n")
        buf.write("    pub header: &'a [u8],\n")
        buf.write("    pub payload: &'a [u8],\n")
        buf.write("}\n\n")

        buf.write(f"pub fn parse_{struct_name.lower()}<'a>(input: &'a [u8]) -> Option<{struct_name}Slice<'a>> {{\n")
        buf.write(f"    // {comments.comment(sanity)}\n")
        buf.write("    if input.len() < 4 { return None; }\n")
        buf.write(f"    Some({struct_name}Slice {{\n")
        buf.write("        header: &input[..4],\n")
        buf.write("        payload: &input[4..],\n")
        buf.write("    })\n")
        buf.write("}\n")

    def _generate_proc_macro_ast(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit Syn/Quote derive macro AST node model."""
        buf.write(f"#[derive(Debug, Clone)]\n")
        buf.write(f"pub struct {struct_name}AstNode {{\n")
        buf.write("    pub ident: String,\n")
        buf.write("    pub attributes: Vec<String>,\n")
        buf.write("    pub is_generic: bool,\n")
        buf.write("}\n\n")

        buf.write(f"impl {struct_name}AstNode {{\n")
        buf.write("    pub fn parse_ident(raw: &str) -> Self {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        Self {\n")
        buf.write("            ident: raw.trim().to_string(),\n")
        buf.write("            attributes: vec![\"enterprise\".to_string()],\n")
        buf.write("            is_generic: raw.contains('<'),\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_lockfree_queue(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit AtomicPtr based lock-free concurrent queue stub."""
        buf.write("use std::sync::atomic::{AtomicPtr, Ordering};\n")
        buf.write("use std::ptr;\n\n")

        buf.write(f"pub struct {struct_name}AtomicQueue<T> {{\n")
        buf.write("    head: AtomicPtr<T>,\n")
        buf.write("}\n\n")

        buf.write(f"impl<T> {struct_name}AtomicQueue<T> {{\n")
        buf.write("    pub fn new() -> Self {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        Self { head: AtomicPtr::new(ptr::null_mut()) }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_pin_future(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit handwritten Pin-projected Future implementation."""
        buf.write("use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll};\n\n")

        buf.write(f"pub struct {struct_name}PollFuture {{\n")
        buf.write("    remaining_ticks: usize,\n")
        buf.write("}\n\n")

        buf.write(f"impl Future for {struct_name}PollFuture {{\n")
        buf.write("    type Output = usize;\n")
        buf.write("    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        if self.remaining_ticks == 0 {\n")
        buf.write("            Poll::Ready(0)\n")
        buf.write("        } else {\n")
        buf.write("            self.remaining_ticks -= 1;\n")
        buf.write("            Poll::Pending\n")
        buf.write("        }\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_ecs(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit Entity Component System (ECS) sparse storage."""
        buf.write(f"pub struct {struct_name}World {{\n")
        buf.write("    entities: Vec<u32>,\n")
        buf.write("    transforms: Vec<f32>,\n")
        buf.write("}\n\n")

        buf.write(f"impl {struct_name}World {{\n")
        buf.write("    pub fn spawn_entity(&mut self, transform: f32) -> u32 {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        let id = self.entities.len() as u32;\n")
        buf.write("        self.entities.push(id);\n")
        buf.write("        self.transforms.push(transform);\n")
        buf.write("        id\n")
        buf.write("    }\n")
        buf.write("}\n")

    def _generate_generational_arena(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit generational arena slot allocator."""
        buf.write(f"#[derive(Copy, Clone, Debug, PartialEq, Eq)]\n")
        buf.write("pub struct Index { pub index: usize, pub generation: u64 }\n\n")

        buf.write(f"pub struct {struct_name}Arena<T> {{\n")
        buf.write("    items: Vec<Option<(T, u64)>>,\n")
        buf.write("    generation: u64,\n")
        buf.write("}\n\n")

        buf.write(f"impl<T> {struct_name}Arena<T> {{\n")
        buf.write("    pub fn new() -> Self {\n")
        buf.write(f"        // {comments.comment(sanity)}\n")
        buf.write("        Self { items: Vec::new(), generation: 1 }\n")
        buf.write("    }\n")
        buf.write("}\n")
