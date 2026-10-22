import argparse

from codemaxxing.archetypes import DEFAULT_ARCHETYPES, LANGUAGE_ARCHETYPES
from codemaxxing.config import GenerationConfig

ALL_LANGS = [
    "all",
    "java",
    "python",
    "js",
    "javascript",
    "go",
    "generic",
    "rust",
    "csharp",
    "cs",
    "kotlin",
    "php",
    "ruby",
    "haskell",
    "hs",
    "c",
    "cpp",
    "c++",
    "swift",
    "zig",
    "lua",
]


def _base_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codemaxxing",
        description="Maximize your lines of code. Because quantity IS quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  codemaxxing --lines 10000 --sanity 100\n"
            "  codemaxxing --lines 50000 --sanity 0 --lang java\n"
            "  codemaxxing --lines 100000 --turbo --sanity 50\n"
            "  codemaxxing --lines 1000 --enterprise\n"
            "  codemaxxing --lines 15000 --lang java --java-archetype gateway\n"
            "  codemaxxing --lines 20000 --lang python --python-archetype metaclass\n"
            "  codemaxxing --lang all --archetype hybrid\n"
            "  codemaxxing --turbo --forever --push-every 50 --batch-size 30\n"
        ),
    )

    parser.add_argument("--lines", type=int, default=10000, help="Target number of lines to generate (default: 10000)")
    parser.add_argument("--sanity", type=int, default=50, choices=range(101), metavar="0-100", help="Chaos level. 100=corporate cringe, 0=full unhinged (default: 50)")
    parser.add_argument("--lang", type=str, default="all", choices=ALL_LANGS, help="Target language(s) for generated slop (default: all)")
    parser.add_argument("--output", type=str, default="./output", help="Output directory (default: ./output)")
    parser.add_argument("--turbo", action="store_true", help="Turbo mode: generate -> git add -> commit -> repeat")
    parser.add_argument("--enterprise", action="store_true", help="Enterprise mode: 10x line multiplier because enterprise")
    parser.add_argument("--batch-size", type=int, default=15, help="Files per commit in turbo mode (default: 15, higher = more lines/commit)")
    parser.add_argument("--push-every", type=int, default=0, help="Auto-push every N commits (default: 0 = manual push)")
    parser.add_argument("--forever", action="store_true", help="Run indefinitely until interrupted (ignores --lines)")
    parser.add_argument("--branch", type=str, default="", help="Use this branch instead of creating slop/session-* (useful for CI)")
    parser.add_argument(
        "--archetype",
        type=str,
        default="enterprise",
        choices=sorted({archetype for profiles in LANGUAGE_ARCHETYPES.values() for archetype in profiles}),
        help="Default generator archetype to use when the user does not specify a language-specific override.",
    )

    for language in [lang for lang in ALL_LANGS if lang != "all"]:
        archetypes = LANGUAGE_ARCHETYPES.get(language, [DEFAULT_ARCHETYPES.get(language, "enterprise")])
        parser.add_argument(
            f"--{language}-archetype",
            type=str,
            default=DEFAULT_ARCHETYPES.get(language, "enterprise"),
            choices=archetypes,
            help=f"{language.title()} generator archetype (default: {DEFAULT_ARCHETYPES.get(language, 'enterprise')})",
        )

    return parser


def build_config(args: argparse.Namespace) -> GenerationConfig:
    overrides: dict[str, str] = {}

    if args.lang == "all":
        for language in [lang for lang in ALL_LANGS if lang != "all"]:
            overrides[language] = getattr(args, f"{language}-archetype", DEFAULT_ARCHETYPES.get(language, "enterprise"))
    else:
        overrides[args.lang] = getattr(args, f"{args.lang}-archetype", DEFAULT_ARCHETYPES.get(args.lang, "enterprise"))

    if args.archetype != "enterprise":
        for language in [lang for lang in ALL_LANGS if lang != "all"]:
            overrides.setdefault(language, args.archetype)

    return GenerationConfig(
        lines=args.lines,
        sanity=args.sanity / 100.0,
        lang=args.lang,
        output_dir=args.output,
        turbo=args.turbo,
        enterprise=args.enterprise,
        batch_size=args.batch_size,
        push_every=args.push_every,
        forever=args.forever,
        branch=args.branch,
        archetypes=overrides,
    )


def main() -> None:
    parser = _base_parser()
    args = parser.parse_args()
    config = build_config(args)

    if config.turbo:
        from codemaxxing.turbo import run_turbo

        run_turbo(config)
    else:
        from codemaxxing.generator import generate, write_files

        print(f"Generating {config.lines:,} lines of pure slop...")
        print(f"Sanity: {config.sanity:.0%} | Lang: {config.lang} | Output: {config.output_dir}")
        print()

        files = generate(config)
        total = write_files(files, config.output_dir)

        print(f"Done! Generated {total:,} lines across {len(files)} files.")
        print(f"Output: {config.output_dir}/")


if __name__ == "__main__":
    main()
