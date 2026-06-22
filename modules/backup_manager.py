import shutil
from datetime import datetime


def backup_database():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        f"backup_{timestamp}.db"
    )

    shutil.copy(
        "interview_data.db",
        backup_file
    )

    return backup_file