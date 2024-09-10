from datasets import load_dataset
import json
import os
import argparse
import numpy


def main():
    parser = argparse.ArgumentParser(
        prog="convert_reference_to_json",
        description="""Converts reference dataset to JSON format""",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path of the output JSON file",
        default=os.path.join("output", "reference.json"),
    )
    arguments = parser.parse_args()

    dolly = load_dataset("w95/databricks-dolly-15k-az")[
        "train"
    ].to_pandas()
    dolly["id"] = numpy.arange(len(dolly))

    with open(
        arguments.output_file, "w", encoding="utf8"
    ) as output_file:
        dolly_json = dolly.to_json(
            orient="records", force_ascii=False, indent=4
        )
        print(dolly_json, file=output_file)


if __name__ == "__main__":
    main()
