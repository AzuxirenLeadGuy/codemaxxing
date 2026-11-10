"""Rust enterprise code generator.

Synthesizes rich Rust source files spanning multiple distinct archetypes:
Tokio async actors with message channels, compile-time typestate builders,
custom thread-safe Iterator/Stream pipelines, and unsafe macro metaprogramming.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class RustEnterpriseGenerator(SlopGenerator):
    """Enterprise Rust code generator.

    Emits safe and idiomatic Rust source code spanning async actors,
    typestate builders, custom iterators, and macro-expanded abstractions.
    """

    name = "rust_enterprise"
    language = "rust"
    extension = ".rs"

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

        archetype = random.choice([
            "tokio_async_actor",
            "typestate_builder",
            "custom_iterator",
            "unsafe_macro_slop",
        ])

        if archetype == "tokio_async_actor":
            self._generate_async_actor(buf, sanity, struct_name)
        elif archetype == "typestate_builder":
            self._generate_typestate(buf, sanity, struct_name)
        elif archetype == "custom_iterator":
            self._generate_iterator(buf, sanity, struct_name)
        else:
            self._generate_macro_slop(buf, sanity, struct_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"rust/{module_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_async_actor(self, buf: StringIO, sanity: float, struct_name: str) -> None:
        """Emit async actor pattern with custom error handling."""
        err_name = f"{struct_name}Error"
        buf.write(f"#[derive(Debug, Clone)]\n")
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
