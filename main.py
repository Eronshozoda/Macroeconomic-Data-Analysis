import argparse
import sys
from tabulate import tabulate
from reports import REPORTS

def main():
    parser = argparse.ArgumentParser(description="Macroeconomic data analysis")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)

    args = parser.parse_args()

    if args.report not in REPORTS:
        print(f"Unknown report: {args.report}")
        sys.exit(1)

    try:
        table = REPORTS[args.report](args.files)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

   

    print(
    tabulate(
        table,
        headers=["country", "gdp"],
        showindex=range(1, len(table) + 1),
        tablefmt="psql"
    )
)



if __name__ == "__main__":
    main()