import speech_recognition as sr


def listen_and_convert():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

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

        return "No speech detected."

    except sr.UnknownValueError:

        return "Could not understand audio."

    except sr.RequestError:

        return "Speech service unavailable."

    except Exception as e:

        return f"Error: {str(e)}"