from foxify_cli.config.startup import startup
from foxify_cli.core.argparser import ArgParser
import sys

def main():
    startup()
    parser = ArgParser(sys.argv[1:])
    parser.run_args()

if __name__ == "__main__":
    main()