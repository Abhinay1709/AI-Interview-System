import speech_recognition as sr


def listen_and_convert():
    """
    Record audio from microphone and
    convert speech to text.

    Returns:
        str: Recognized text or error message
    """

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("Listening...")

            # Reduce background noise
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

        return text

    except sr.WaitTimeoutError:

        return (
            "No speech detected. "
            "Please try again."
        )

    except sr.UnknownValueError:

        return (
            "Could not understand the audio."
        )

    except sr.RequestError:

        return (
            "Speech recognition service "
            "is unavailable."
        )

    except OSError:

        return (
            "Microphone not found. "
            "Please connect a microphone."
        )

    except Exception as e:

        return f"Error: {str(e)}"