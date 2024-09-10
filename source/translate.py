import argparse
import json
import os
import translators
import termcolor
import time
import requests


def update_provider_index(provider_index, providers):
    return (provider_index + 1) % len(providers)


def main():
    parser = argparse.ArgumentParser(
        prog="translate",
        description="Translates the input dataset",
    )
    parser.add_argument(
        "-i",
        "--input_file_path",
        help="Path of the input JSON file",
        default=os.path.join("output", "preprocessed.json"),
    )
    parser.add_argument(
        "-o",
        "--output_file_path",
        help="Path of the output JSON file",
        default=os.path.join("output", "translated.json"),
    )
    parser.add_argument(
        "--preaccelerate",
        action=argparse.BooleanOptionalAction,
        help="Whether to preaccelerate or not",
    )
    arguments = parser.parse_args()

    with open(arguments.input_file_path, "r") as input_file:
        records = json.load(input_file)

    providers = [
        "google",
        "yandex",
        "deepl",
        "bing",
        "alibaba",
        "baidu",
    ]
    provider_index = 0
    termcolor.cprint(
        f"Starting translation, current provider is {providers[provider_index]}",
        "blue",
    )
    translated_records = list()
    if arguments.preaccelerate:
        translators.preaccelerate_and_speedtest()
    for i, record in enumerate(records):
        new_record = dict()
        could_translate = False
        fail_count = 0
        fail_count_limit = 20
        short_sleep = 10
        while not could_translate:
            try:
                for key in ["instruction", "answer"]:
                    new_record[key] = translators.translate_text(
                        record[key],
                        translator=providers[provider_index],
                        from_language="en",
                        to_language="az",
                    )
                could_translate = True
            except (
                requests.exceptions.HTTPError,
                TypeError,
            ) as error:
                fail_count += 1
                termcolor.cprint(
                    f"Encountered {type(error)}, trying again",
                    "magenta",
                )
                if fail_count < fail_count_limit:
                    time.sleep(short_sleep)
                else:
                    provider_index = update_provider_index(
                        provider_index, providers
                    )
                    termcolor.cprint(
                        f"Failed {fail_count} times, changing provider to {providers[provider_index]}",
                        "magenta",
                    )
            except IndexError as error:
                fail_count += 1
                termcolor.cprint(
                    f"Encountered {type(error)}, trying again",
                    "magenta",
                )
                record["answer"] = "Answer is " + record["answer"]
            except translators.server.TranslatorError as error:
                fail_count += 1
                termcolor.cprint(
                    f"Encountered {type(error)}, trying again",
                    "magenta",
                )
                provider_index = update_provider_index(
                    provider_index, providers
                )
        print(f"Record {i}: [{new_record}]\n\n")
        translated_records.append(new_record)

    termcolor.cprint(
        "Translation completed. Writing the output file", "blue"
    )
    with open(arguments.output_file_path, "w") as output_file:
        print(
            json.dumps(translated_records, indent=4),
            file=output_file,
        )


if __name__ == "__main__":
    main()
