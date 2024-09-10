import json
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        prog="postprocess",
        description="Postprocesses the edited dataset to obtain the final version",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the input dataset file",
        default=os.path.join("data", "top_down.json"),
    )
    arguments = parser.parse_args()

    with open(
        arguments.input_file, "r", encoding="utf8"
    ) as input_file:
        dataset = json.load(input_file)

    dataset = [
        record
        for record in dataset
        if record["category"] != "unknown"
    ]
    record_count = len(dataset)

    with open(
        os.path.join(
            "output",
            f"prodata_instruct_{record_count}.json"
        ),
        "w",
        encoding="utf8",
    ) as output_file:
        print(
            json.dumps(dataset, indent=4, ensure_ascii=False),
            file=output_file,
        )


if __name__ == "__main__":
    main()
