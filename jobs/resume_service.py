from pypdf import PdfReader


def extract_resume_text(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


# import re

import re


def extract_candidate_name(text):
    """
    Extract candidate name from the beginning of a resume.
    Handles formats such as:

    YUGENDER THONTI Software Engineer | Python Developer
    RAHUL KUMAR
    Name: Rahul Kumar
    FULL NAME - Rahul Kumar
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    # --------------------------------------------------
    # 1. Explicit name labels
    # --------------------------------------------------

    for line in lines[:15]:

        match = re.match(
            r"^(?:name|full\s*name)\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match:
            name = match.group(1).strip()

            # Remove anything after common separators
            name = re.split(
                r"\||\s{2,}|software engineer|developer|"
                r"python|react|django|java|sql",
                name,
                flags=re.IGNORECASE
            )[0].strip()

            return name

    # --------------------------------------------------
    # 2. Resume header:
    #    "YUGENDER THONTI Software Engineer | ..."
    # --------------------------------------------------

    for line in lines[:10]:

        # Only look at the beginning of the line
        first_part = re.split(
            r"\||\s+Software\s+Engineer|\s+Software\s+Developer|"
            r"\s+Developer|\s+Engineer",
            line,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0].strip()

        # Remove unwanted symbols
        first_part = re.sub(
            r"[^A-Za-z .'-]",
            "",
            first_part
        ).strip()

        words = first_part.split()

        # A normal person's name is usually 2-4 words
        if 2 <= len(words) <= 4:

            if all(
                word.replace("-", "").replace("'", "").isalpha()
                for word in words
            ):
                return " ".join(
                    word.capitalize()
                    for word in words
                )

    # --------------------------------------------------
    # 3. Standalone name line
    # --------------------------------------------------

    for line in lines[:10]:

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line
        ).strip()

        words = cleaned.split()

        if 2 <= len(words) <= 4:

            if all(
                word.replace("-", "").replace("'", "").isalpha()
                for word in words
            ):
                return " ".join(
                    word.capitalize()
                    for word in words
                )

    return None