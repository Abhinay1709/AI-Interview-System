from datetime import datetime


def log_error(error):

    with open(
        "error_log.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"\n\n[{datetime.now()}]\n"
        )

        file.write(
            str(error)
        )

        file.write("\n")