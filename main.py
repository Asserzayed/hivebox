#!/usr/bin/env python3

import argparse

# Tool version
TOOL_VERSION = "0.0.1"

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="HiveBox DevOps CLI tool.",
                                    epilog="Use '%(prog)s <command> --help' to get help on a specific command.")
    
    # Add the --version flag
    parser.add_argument("--version", "-v",
                        action="version",
                        version=f"HiveBox v{TOOL_VERSION}",
                        help="Shows tool version.")

    # Parse arguments
    args = parser.parse_args()
    
    # Testing #
    # Show logic route
    # print(args)

    # Print help if no args are passed
    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()
