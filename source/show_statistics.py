import json
import argparse
import os
import pandas


def main():
    parser = argparse.ArgumentParser(
        prog="show_statistics",
        description="Shows dataset statistics",
    )
    parser.add_argument(
        "-d",
        "--dataset_path",
        help="Path of the dataset",
        default=os.path.join("data", "top_down.json"),
    )
    parser.add_argument(
        "-c",
        "--categories_file",
        help="Path of the categories file",
        default=os.path.join("data", "categories.json"),
    )
    arguments = parser.parse_args()

    with open(arguments.categories_file, "r") as categories_file:
        categories = json.load(categories_file)

    with open(arguments.dataset_path, "r") as dataset_file:
        records = json.load(dataset_file)

    for category in categories:
        category["count"] = 0

    for record in records:
        is_valid_category = False
        for category in categories:
            if record["category"] == category["name"]:
                category["count"] += 1
                is_valid_category = True
        if not is_valid_category:
            print(f"'{record['category']}' is not a valid category")
            assert False

    category_dataframe = pandas.DataFrame(
        {
            "name": [category["name"] for category in categories],
            "count": [
                category["count"] for category in categories
            ],
            "completion_rate": [
                (
                    category["count"]
                    / category["desired_count"]
                    * 100
                    if category["name"] != "unknown"
                    else pandas.NA
                )
                for category in categories
            ],
            "desired_count": [
                category["desired_count"]
                for category in categories
            ],
        }
    )

    without_unknown = category_dataframe[
        ~category_dataframe["name"].str.contains("unknown")
    ]

    pandas.options.display.float_format = "{:,.2f}%".format
    print(without_unknown)
    print(f"Total count: {without_unknown['count'].sum()}")


if __name__ == "__main__":
    main()
