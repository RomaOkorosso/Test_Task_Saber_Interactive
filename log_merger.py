import argparse
import json
import os
import time
from datetime import datetime

filename = ""
first_path = ""
second_path = ""
output_path = ""


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="merge logs in one file")

    parser.add_argument(
        "input_path",
        type=str,
        help="paths to dir with generated logs",
        nargs=2,
    )

    parser.add_argument("-o", "--output", dest="output_path", nargs=1)

    return parser.parse_args()


def merge_logs():
    global filename, first_path, second_path

    filename = output_path[0].split("/")[-1]

    if len(filename) == 0:
        raise Exception("please enter the filename for output file")

    if os.path.exists(output_path[0]):
        Exception("file already exists, delete it and try again")

    first = open(first_path, "r")
    second = open(second_path, "r")
    lines = True
    first_file_line = first.readline()
    second_file_line = second.readline()

    with open(output_path[0], "w") as output:
        while lines:
            if not second_file_line or not first_file_line:
                if not first_file_line:
                    output.write(second_file_line)
                    second_file_line = second.readline()
                    while lines and second_file_line:
                        output.write(second_file_line)
                        second_file_line = second.readline()
                    lines = False
                else:
                    output.write(first_file_line)
                    first_file_line = first.readline()
                    while lines and first_file_line:
                        output.write(first_file_line)
                        first_file_line = first.readline()
                    lines = False
            else:
                first_file_line_json = json.loads(first_file_line)
                second_file_line_json = json.loads(second_file_line)
                first_time = datetime.strptime(
                    first_file_line_json["timestamp"], "%Y-%m-%d %H:%M:%S"
                )
                second_time = datetime.strptime(
                    second_file_line_json["timestamp"], "%Y-%m-%d %H:%M:%S"
                )
                if first_time > second_time:
                    output.write(second_file_line)
                    second_file_line = second.readline()
                else:
                    output.write(first_file_line)
                    first_file_line = first.readline()


if __name__ == "__main__":
    args = _parse_args()

    first_path, second_path = args.input_path
    output_path = args.output_path

    if not os.path.exists(first_path):
        raise Exception(f"{first_path} dir or file does not exist")
    if not os.path.exists(second_path):
        raise Exception(f"{second_path} dir or file does not exist")
    start = time.time()
    merge_logs()
    stop = time.time()
    print(f"OK\nTime spent: {round(float(stop - start), 5)}")
