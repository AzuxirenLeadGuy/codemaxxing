"""Unit tests for codemaxxing synthetic code generators.

Verifies that all 16 language generators produce diverse, non-empty, and unpredictable
code outputs across different sanity levels.
"""

import unittest
from codemaxxing.config import GenerationConfig
from codemaxxing.generator import generate
from codemaxxing.generators import ALL_GENERATORS, LANG_MAP, get_generators


class TestGenerators(unittest.TestCase):
    """Test suite ensuring all language generators function reliably and unpredictably."""

    def test_all_generators_instantiated(self) -> None:
        """Verify that all 16 generators are registered."""
        self.assertEqual(len(ALL_GENERATORS), 16)

    def test_generators_generate_content_across_sanity(self) -> None:
        """Verify each generator produces valid GeneratedFile objects across sanity levels."""
        sanity_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
        for gen in ALL_GENERATORS:
            for sanity in sanity_levels:
                result = gen.generate(sanity=sanity, file_index=42)
                self.assertTrue(result.filename, f"Generator {gen.name} produced empty filename")
                self.assertGreater(len(result.content), 20, f"Generator {gen.name} produced too little content")
                self.assertGreater(result.line_count, 0, f"Generator {gen.name} reported 0 lines")
                self.assertTrue(
                    result.filename.endswith(gen.extension) or result.filename.endswith(".ts") or result.filename.endswith(".js"),
                    f"Generator {gen.name} filename {result.filename} does not match expected extension",
                )

    def test_unpredictability_and_diversity(self) -> None:
        """Verify repeated generation produces diverse and randomized content."""
        for gen in ALL_GENERATORS:
            contents = set()
            for i in range(5):
                res = gen.generate(sanity=0.5, file_index=i)
                contents.add(res.content)
            # Ensure at least 4 out of 5 outputs are distinct
            self.assertGreaterEqual(
                len(contents), 4,
                f"Generator {gen.name} produced too repetitive outputs across 5 runs",
            )

    def test_get_generators_mapping(self) -> None:
        """Verify language mapping returns correct generators."""
        self.assertEqual(get_generators("java")[0].name, "enterprise_java")
        self.assertEqual(get_generators("python")[0].name, "enterprise_python")
        self.assertEqual(get_generators("rust")[0].name, "rust_enterprise")
        self.assertEqual(get_generators("go")[0].name, "go_slop")
        self.assertEqual(len(get_generators("all")), 16)

    def test_full_generate_orchestrator(self) -> None:
        """Verify the main orchestrator satisfies line count targets."""
        config = GenerationConfig(lines=500, sanity=0.5, lang="all")
        files = generate(config)
        total_lines = sum(f.line_count for f in files)
        self.assertGreaterEqual(total_lines, 500)
        self.assertGreaterEqual(len(files), 16)


if __name__ == "__main__":
    unittest.main()
