import datasets
import pandas
import argparse
import os
import termcolor


def main():
    parser = argparse.ArgumentParser(
        prog="preprocess",
        description="Preprocesses the input dataset",
    )
    parser.add_argument(
        "-o",
        "--output_file_path",
        help="Path of the output JSON file",
        default=os.path.join("output", "preprocessed.json"),
    )
    arguments = parser.parse_args()

    termcolor.cprint("Loading the dataset", "blue")
    alpaca_dataset = datasets.load_dataset(
        "tatsu-lab/alpaca", split="train"
    )

    termcolor.cprint("Preprocessing the dataset", "blue")
    alpaca_dataframe = alpaca_dataset.to_pandas()
    alpaca_dataframe["instruction"] = alpaca_dataframe.apply(
        lambda row: (
            row["instruction"]
            if row["input"] == ""
            else f"{row['instruction']}: {row['input']}"
        ),
        axis=1,
    )
    alpaca_dataframe = alpaca_dataframe.drop(
        ["input", "text"], axis=1
    ).rename(columns={"output": "answer"})

    termcolor.cprint("Writing output files", "blue")
    os.makedirs(
        os.path.dirname(arguments.output_file_path), exist_ok=True
    )
    with open(arguments.output_file_path, "w") as output_file:
        print(
            alpaca_dataframe.to_json(indent=4, orient="records"),
            file=output_file,
        )


if __name__ == "__main__":
    main()
