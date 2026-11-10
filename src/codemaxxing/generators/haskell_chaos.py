"""Haskell chaos code generator.

Synthesizes rich functional Haskell source files across multiple distinct archetypes:
Monad transformer pipelines with do-notation, Generalized Algebraic Data Types (GADTs),
van Laarhoven lens combinators with point-free compositions, and lazy infinite fixpoint streams.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class HaskellChaosGenerator(SlopGenerator):
    """Haskell language code generator.

    Emits pure functional Haskell constructs spanning monad transformers,
    GADTs, lenses, and lazy stream combinators.
    """

    name = "haskell_chaos"
    language = "haskell"
    extension = ".hs"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Haskell source file (.hs).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Haskell source code.
        """
        buf = StringIO()
        module_name = naming.class_name(sanity)

        buf.write(f"-- {comments.comment(sanity)}\n")
        buf.write(f"module {module_name} where\n\n")
        buf.write("import Control.Monad\nimport Control.Applicative\nimport Data.Maybe\nimport Data.Either\n\n")

        archetype = random.choice([
            "monad_transformers",
            "gadt_category",
            "lens_combinators",
            "lazy_fixpoint_stream",
        ])

        if archetype == "monad_transformers":
            self._generate_monad_transformer(buf, sanity, module_name)
        elif archetype == "gadt_category":
            self._generate_gadt(buf, sanity, module_name)
        elif archetype == "lens_combinators":
            self._generate_lenses(buf, sanity, module_name)
        else:
            self._generate_lazy_stream(buf, sanity, module_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"haskell/{module_name}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_monad_transformer(self, buf: StringIO, sanity: float, mod_name: str) -> None:
        """Emit Monad transformer pipeline with do-notation."""
        data_name = f"{mod_name}Env"
        buf.write(f"data {data_name} = {data_name} {{ envId :: String, envQuota :: Int }}\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"{mname} :: {data_name} -> Maybe String -> Either String String\n")
        buf.write(f"{mname} env input = do\n")
        buf.write(f"    -- {comments.comment(sanity)}\n")
        buf.write("    val <- maybe (Left \"missing input\") Right input\n")
        buf.write("    when (envQuota env <= 0) (Left \"quota exhausted\")\n")
        buf.write("    Right (val ++ \"_ACK_\" ++ envId env)\n")

    def _generate_gadt(self, buf: StringIO, sanity: float, mod_name: str) -> None:
        """Emit Generalized Algebraic Data Type (GADT) syntax."""
        buf.write("{-# LANGUAGE GADTs #-}\n\n")
        expr_name = f"{mod_name}Expr"
        buf.write(f"data {expr_name} a where\n")
        buf.write(f"    LitInt  :: Int -> {expr_name} Int\n")
        buf.write(f"    LitStr  :: String -> {expr_name} String\n")
        buf.write(f"    Add     :: {expr_name} Int -> {expr_name} Int -> {expr_name} Int\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"{mname} :: {expr_name} a -> a\n")
        buf.write(f"{mname} (LitInt n) = n\n")
        buf.write(f"{mname} (LitStr s) = s\n")
        buf.write(f"{mname} (Add x y)  = {mname} x + {mname} y\n")

    def _generate_lenses(self, buf: StringIO, sanity: float, mod_name: str) -> None:
        """Emit van Laarhoven lens combinators."""
        buf.write(f"type Lens s t a b = forall f. Functor f => (a -> f b) -> s -> f t\n\n")
        buf.write(f"-- {comments.comment(sanity)}\n")
        buf.write(f"lens :: (s -> a) -> (s -> b -> t) -> Lens s t a b\n")
        buf.write("lens getter setter f s = fmap (setter s) (f (getter s))\n")

    def _generate_lazy_stream(self, buf: StringIO, sanity: float, mod_name: str) -> None:
        """Emit lazy infinite streams and fixpoints."""
        mname = naming.method_name(sanity)
        buf.write(f"-- {comments.comment(sanity)}\n")
        buf.write(f"{mname} :: [String]\n")
        buf.write(f"{mname} = iterate (++ \"!\") \"slop\"\n")
