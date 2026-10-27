"""Registry and factory lookup for language-specific synthetic code generators.

Provides mappings from language names and alias identifiers to instantiated
`SlopGenerator` subclasses covering 16 supported programming language styles.
"""

from codemaxxing.generators.enterprise_java import EnterpriseJavaGenerator
from codemaxxing.generators.enterprise_python import EnterprisePythonGenerator
from codemaxxing.generators.javascript import JavaScriptGenerator
from codemaxxing.generators.go_slop import GoSlopGenerator
from codemaxxing.generators.generic import GenericGenerator
from codemaxxing.generators.c_slop import CSlopGenerator
from codemaxxing.generators.csharp_enterprise import CSharpEnterpriseGenerator
from codemaxxing.generators.cpp_enterprise import CppEnterpriseGenerator
from codemaxxing.generators.haskell_chaos import HaskellChaosGenerator
from codemaxxing.generators.kotlin_enterprise import KotlinEnterpriseGenerator
from codemaxxing.generators.lua_chaos import LuaChaosGenerator
from codemaxxing.generators.php_enterprise import PhpEnterpriseGenerator
from codemaxxing.generators.ruby_chaos import RubyChaosGenerator
from codemaxxing.generators.rust_enterprise import RustEnterpriseGenerator
from codemaxxing.generators.swift_enterprise import SwiftEnterpriseGenerator
from codemaxxing.generators.zig_enterprise import ZigEnterpriseGenerator

ALL_GENERATORS = [
    EnterpriseJavaGenerator(),
    EnterprisePythonGenerator(),
    JavaScriptGenerator(),
    GoSlopGenerator(),
    GenericGenerator(),
    RustEnterpriseGenerator(),
    CSharpEnterpriseGenerator(),
    KotlinEnterpriseGenerator(),
    PhpEnterpriseGenerator(),
    RubyChaosGenerator(),
    HaskellChaosGenerator(),
    CSlopGenerator(),
    CppEnterpriseGenerator(),
    SwiftEnterpriseGenerator(),
    ZigEnterpriseGenerator(),
    LuaChaosGenerator(),
]

LANG_MAP = {
    "java": [EnterpriseJavaGenerator()],
    "python": [EnterprisePythonGenerator()],
    "js": [JavaScriptGenerator()],
    "javascript": [JavaScriptGenerator()],
    "go": [GoSlopGenerator()],
    "generic": [GenericGenerator()],
    "rust": [RustEnterpriseGenerator()],
    "csharp": [CSharpEnterpriseGenerator()],
    "cs": [CSharpEnterpriseGenerator()],
    "kotlin": [KotlinEnterpriseGenerator()],
    "php": [PhpEnterpriseGenerator()],
    "ruby": [RubyChaosGenerator()],
    "haskell": [HaskellChaosGenerator()],
    "hs": [HaskellChaosGenerator()],
    "c": [CSlopGenerator()],
    "cpp": [CppEnterpriseGenerator()],
    "c++": [CppEnterpriseGenerator()],
    "swift": [SwiftEnterpriseGenerator()],
    "zig": [ZigEnterpriseGenerator()],
    "lua": [LuaChaosGenerator()],
    "all": ALL_GENERATORS,
}


def get_generators(lang: str) -> list:
    """Retrieve generator instances matching a target language identifier or alias.

    Args:
        lang: Target language name (e.g. 'java', 'rust', 'csharp', 'js') or 'all'.
            Case-sensitive language identifier or shorthand alias.

    Returns:
        A list of `SlopGenerator` instances configured for the requested language,
        or all available generators if `lang` is 'all' or unrecognized.
    """
    return LANG_MAP.get(lang, ALL_GENERATORS)
