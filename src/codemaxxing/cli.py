"""CLI entrypoint alias for codemaxxing.

Delegates directly to `codemaxxing.__main__.main` to support package script hooks.
"""

from codemaxxing.__main__ import main

if __name__ == "__main__":
    main()
