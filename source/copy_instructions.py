from datasets import load_dataset
import json
import os
import argparse
import numpy
import pandas


def main():
    parser = argparse.ArgumentParser(
        prog="copy_instructions",
        description="""Copies some of the instructions from the
                        reference dataset to the current dataset""",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the input dataset file",
        default=os.path.join("output", "manually_edited.json"),
    )
    parser.add_argument(
        "-r",
        "--reference_file",
        help="Path of the reference dataset file",
        default=os.path.join("data", "dolly.json"),
    )
    parser.add_argument(
        "--ids",
        help="""Path of the file containing
                IDs of instructions that are copied""",
        default="data/dolly_ids.csv",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path of the output dataset file",
        default=os.path.join("output", "copy_augmented.json"),
    )
    arguments = parser.parse_args()

    with open(
        arguments.reference_file, "r", encoding="utf8"
    ) as reference_file:
        reference = json.load(reference_file)

    with open(arguments.ids, "r") as ids_file:
        ids = pandas.read_csv(
            arguments.ids, header=None
        ).to_numpy()[:, 0]

    with open(
        arguments.input_file, "r", encoding="utf8"
    ) as input_file:
        dataset = json.load(input_file)

    for id_ in ids:
        new_record = {}
        found_instruction = False
        for record in reference:
            if (
                record["id"] == id_
                and record["category"] != "general_qa"
            ):
                new_record["instruction"] = (
                    f"{record['instruction']}"
                )
                if len(record["context"]) > 0:
                    new_record["instruction"] += (
                        "\n" + record["context"]
                    )
                new_record["answer"] = record["response"]
                category = record["category"]
                if category == "information_extraction":
                    new_record["category"] = "extraction"
                elif category == "creative_writing":
                    new_record["category"] = "writing"
                elif category == "closed_qa":
                    new_record["category"] = "closed"
                elif category == "open_qa":
                    new_record["category"] = "open"
                else:
                    new_record["category"] = category
                found_instruction = True
                break
        if found_instruction:
            dataset.append(new_record)

    with open(
        arguments.output_file, "w", encoding="utf8"
    ) as output_file:
        print(
            json.dumps(dataset, indent=4, ensure_ascii=False),
            file=output_file,
        )


if __name__ == "__main__":
    main()
