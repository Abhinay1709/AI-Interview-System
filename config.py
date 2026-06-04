import os
from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    raise ValueError(
        """
        GEMINI_API_KEY not found.

        Create a .env file and add:

        GEMINI_API_KEY=your_api_key_here
        """
    )