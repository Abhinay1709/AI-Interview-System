def save_answer(
    question,
    answer,
    evaluation,
    responses
):
    """
    Save a response record.

    Parameters:
        question (str)
        answer (str)
        evaluation (str)
        responses (list)

    Returns:
        list
    """

    response_data = {
        "question": question,
        "answer": answer,
        "evaluation": evaluation
    }

    responses.append(response_data)

    return responses


def delete_answer(
    index,
    responses
):
    """
    Delete response by index.

    Parameters:
        index (int)
        responses (list)

    Returns:
        list
    """

    if (
        index >= 0
        and index < len(responses)
    ):
        responses.pop(index)

    return responses


def clear_answers():
    """
    Remove all responses.

    Returns:
        list
    """

    return []


def get_all_answers(
    responses
):
    """
    Return all responses.

    Parameters:
        responses (list)

    Returns:
        list
    """

    return responses