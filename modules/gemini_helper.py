import google.generativeai as genai
import time


def generate_with_retry(
    model,
    prompt,
    retries=3
):

    for attempt in range(retries):

        try:

            response = model.generate_content(
                prompt
            )

            return response.text

        except Exception:

            if attempt < retries - 1:

                time.sleep(2)

            else:

                return (
                    "Evaluation unavailable. "
                    "Please try again later."
                )