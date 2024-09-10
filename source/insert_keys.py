import json
import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="insert_keys",
        description="Insert key named 'category' to all of the dictionaries in the JSON list",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the input JSON file",
        default=os.path.join(
            "output", "translated_utf8_fixed.json"
        ),
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path of the output JSON file",
        default=os.path.join("output", "with_extra_keys.json"),
    )
    arguments = parser.parse_args()

    with open(
        arguments.input_file, "r", encoding="utf8"
    ) as input_file:
        json_string = input_file.read()

    records = json.loads(json_string)

    for record in records:
        record["category"] = "unknown"

    with open(
        arguments.output_file, "w", encoding="utf8"
    ) as output_file:
        print(
            json.dumps(records, indent=4, ensure_ascii=False),
            file=output_file,
        )


if __name__ == "__main__":
    main()
