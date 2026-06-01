def save_answer(
    question,
    answer,
    evaluation,
    responses
):

    responses.append(
        {
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        }
    )

    return responses


def delete_answer(
    index,
    responses
):

    if 0 <= index < len(responses):

        responses.pop(index)

    return responses


def clear_answers():

    return []


def get_all_answers(
    responses
):

    return responses