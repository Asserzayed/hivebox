#!/usr/bin/env python3

import argparse

# Tool version
TOOL_VERSION = "0.0.1"

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="HiveBox DevOps CLI tool.")
    
    # Add the --version flag
    parser.add_argument("--version", "-v", action="version", version=f"HiveBox v{TOOL_VERSION}", help="Shows tool version.")

    # Parse arguments
    args = parser.parse_args()
    # Show logic route # Testing
    # print(args)

if __name__ == "__main__":
    main()
