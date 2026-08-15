# import os

# from dotenv import load_dotenv
# from neo4j import GraphDatabase

# load_dotenv()

# NEO4J_URI = os.getenv("NEO4J_URI")
# NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
# NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


# def get_driver():
#     return GraphDatabase.driver(
#         NEO4J_URI,
#         auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
#     )

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


# =========================================================
# COGNODB CONFIGURATION
# =========================================================

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME", "cognodb")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")
COGNODB_DATABASE = os.getenv("COGNODB_DATABASE", "neo4j")


# =========================================================
# VALIDATE CONFIGURATION
# =========================================================

if not COGNODB_URI:
    raise RuntimeError(
        "COGNODB_URI is missing from .env"
    )

if not COGNODB_PASSWORD:
    raise RuntimeError(
        "COGNODB_PASSWORD is missing from .env"
    )


# =========================================================
# DRIVER
# =========================================================

def get_driver():
    return GraphDatabase.driver(
        COGNODB_URI,
        auth=(
            COGNODB_USERNAME,
            COGNODB_PASSWORD
        ),
    )


# =========================================================
# CONNECTION TEST
# =========================================================

def test_connection():

    driver = get_driver()

    try:

        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                "RETURN 1 AS connected"
            )

            record = result.single()

            if record and record["connected"] == 1:
                return {
                    "status": "success",
                    "message": "Connected to CognoDB"
                }

            return {
                "status": "error",
                "message": "CognoDB connection test failed"
            }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }

    finally:
        driver.close()


