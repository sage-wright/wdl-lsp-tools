"""Entry point for the zipapp: `python wdl-lsp-tools.pyz <command> [args]`.

Commands are named like the console scripts the package installs, so an editor
can run either form with the same arguments."""
import sys

from . import __version__

USAGE = "usage: wdl-lsp-tools {wdl-command-lint,sprocket-filtered} [args...]"


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    # Leave the remaining arguments in sys.argv for the command, as if it had
    # been run through its own console script.
    sys.argv = [command, *sys.argv[2:]]
    if command == "wdl-command-lint":
        from .command_lint import main as run
    elif command == "sprocket-filtered":
        from .sprocket_filtered import main as run
    elif command in ("--version", "-V"):
        print(f"wdl-lsp-tools {__version__}")
        return
    else:
        sys.exit(USAGE)
    run()


if __name__ == "__main__":
    main()
