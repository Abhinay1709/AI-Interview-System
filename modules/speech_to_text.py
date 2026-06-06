import speech_recognition as sr


def listen_and_convert():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print(
                "Listening..."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(

                source,

                timeout=15,

                phrase_time_limit=60
            )

        text = recognizer.recognize_google(

            audio,

            language="en-US"
        )

        return text.strip()

    except sr.WaitTimeoutError:

        return (
            "No speech detected."
        )

    except sr.UnknownValueError:

        return (
            "Could not understand audio."
        )

    except sr.RequestError:

        return (
            "Speech recognition service unavailable."
        )

    except Exception as e:

        return (
            f"Speech Recognition Error: "
            f"{str(e)}"
        )


# --------------------------------------------------
# CONTINUOUS LISTENING
# --------------------------------------------------

def listen_long_answer():

    recognizer = sr.Recognizer()

    complete_text = ""

    try:

        with sr.Microphone() as source:

            print(
                "Listening..."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            while True:

                try:

                    audio = recognizer.listen(

                        source,

                        timeout=5,

                        phrase_time_limit=30
                    )

                    text = recognizer.recognize_google(
                        audio
                    )

                    complete_text += (
                        text + " "
                    )

                except sr.WaitTimeoutError:

                    break

        return complete_text.strip()

    except Exception as e:

        return (
            f"Error: {str(e)}"
        )


# --------------------------------------------------
# VALIDATE SPEECH RESULT
# --------------------------------------------------

def is_valid_speech(
    text
):

    invalid_responses = [

        "",

        "No speech detected.",

        "Could not understand audio.",

        "Speech recognition service unavailable."
    ]

    return text not in invalid_responses


# --------------------------------------------------
# CLEAN SPEECH TEXT
# --------------------------------------------------

def clean_speech_text(
    text
):

    if not text:

        return ""

    text = text.strip()

    text = " ".join(
        text.split()
    )

    return text


# --------------------------------------------------
# SKIP DETECTION
# --------------------------------------------------

def is_skipped_speech(
    text
):

    if not text:

        return True

    skip_words = [

        "-",

        "no",

        "n a",

        "n slash a",

        "skip",

        "skipped",

        "none"
    ]

    return (
        text.lower().strip()
        in skip_words
    )