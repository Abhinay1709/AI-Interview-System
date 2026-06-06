SKIP_WORDS = [
    "",
    "-",
    "no",
    "n/a",
    "na",
    "skip",
    "skipped",
    "none"
]


def save_answer(
    question,
    answer,
    answers_dict
):

    answers_dict[question] = answer

    return answers_dict


def get_answer(
    question,
    answers_dict
):

    return answers_dict.get(
        question,
        ""
    )


def update_answer(
    question,
    answer,
    answers_dict
):

    answers_dict[question] = answer

    return answers_dict


def delete_answer(
    question,
    answers_dict
):

    if question in answers_dict:

        del answers_dict[question]

    return answers_dict


def clear_all_answers():

    return {}


def clear_answers():

    return {}


def is_skipped_answer(
    answer
):

    if answer is None:

        return True

    cleaned = (
        str(answer)
        .strip()
        .lower()
    )

    return cleaned in SKIP_WORDS


def get_answered_count(
    answers_dict
):

    count = 0

    for answer in answers_dict.values():

        if not is_skipped_answer(
            answer
        ):

            count += 1

    return count


def get_skipped_count(
    questions,
    answers_dict
):

    skipped = 0

    for question in questions:

        answer = answers_dict.get(
            question,
            ""
        )

        if is_skipped_answer(
            answer
        ):

            skipped += 1

    return skipped


def get_attempted_questions(
    questions,
    answers_dict
):

    attempted = []

    for question in questions:

        answer = answers_dict.get(
            question,
            ""
        )

        if not is_skipped_answer(
            answer
        ):

            attempted.append(
                question
            )

    return attempted


def get_skipped_questions(
    questions,
    answers_dict
):

    skipped = []

    for question in questions:

        answer = answers_dict.get(
            question,
            ""
        )

        if is_skipped_answer(
            answer
        ):

            skipped.append(
                question
            )

    return skipped


def get_interview_statistics(
    questions,
    answers_dict
):

    total_questions = len(
        questions
    )

    answered_questions = (
        get_answered_count(
            answers_dict
        )
    )

    skipped_questions = (
        get_skipped_count(
            questions,
            answers_dict
        )
    )

    completion_percentage = 0

    if total_questions > 0:

        completion_percentage = round(
            (
                answered_questions
                /
                total_questions
            ) * 100,
            2
        )

    return {

        "total_questions":
            total_questions,

        "answered_questions":
            answered_questions,

        "skipped_questions":
            skipped_questions,

        "completion_percentage":
            completion_percentage
    }


def validate_answers(
    questions,
    answers_dict
):

    missing_questions = []

    for question in questions:

        if question not in answers_dict:

            missing_questions.append(
                question
            )

    return {

        "is_valid":
            len(
                missing_questions
            ) == 0,

        "missing_questions":
            missing_questions
    }