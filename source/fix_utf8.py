import json
import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="fix_utf8",
        description="Fix UTF-8 encoding of the JSON file",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the input JSON file",
        default=os.path.join("output", "translated.json"),
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path of the output JSON file",
        default=os.path.join(
            "output", "translated_utf8_fixed.json"
        ),
    )
    arguments = parser.parse_args()

    with open(arguments.input_file, "r") as input_file:
        json_string = input_file.read()

    dictionary = json.loads(json_string)

    with open(
        arguments.output_file, "w", encoding="utf8"
    ) as output_file:
        print(
            json.dumps(dictionary, indent=4, ensure_ascii=False),
            file=output_file,
        )


if __name__ == "__main__":
    main()
