"""
Conversation states used by the Telegram client.

The state names are intentionally simple strings because they are
also stored in context.user_data during conversations.
"""

# ==========================================================
# CREATE RECORD
# ==========================================================

ESTIMATED_AGE = "estimated_age"
REPORTED_NAME = "reported_name"
REPORTED_LOCATION = "reported_location"
SOURCE = "source"
RECOGNITION_FEATURES = "recognition_features"

REVIEW = "review"
SUBMIT = "submit"


# ==========================================================
# CREATE RECORD (Animals)
# ==========================================================

ANIMAL_SPECIES = "animal_species"
ANIMAL_SIZE = "animal_size"
ANIMAL_BREED_TYPE = "animal_breed_type"
ANIMAL_BREED_TEXT = "animal_breed_text"


# ==========================================================
# SEARCH RECORD
# ==========================================================

SEARCH_TYPE = "search_type"

# Person search

SEARCH_REPORTED_NAME = "search_reported_name"
SEARCH_ESTIMATED_AGE = "search_estimated_age"
SEARCH_LOCATION = "search_location"
SEARCH_SOURCE = "search_source"
SEARCH_RECOGNITION_FEATURES = "search_recognition_features"

# Animal search

SEARCH_ANIMAL_SPECIES = "search_animal_species"
SEARCH_ANIMAL_NAME = "search_animal_name"
SEARCH_ANIMAL_SIZE = "search_animal_size"
SEARCH_ANIMAL_BREED_TEXT = "search_animal_breed_text"
SEARCH_ANIMAL_LOCATION = "search_animal_location"
SEARCH_ANIMAL_FEATURES = "search_animal_features"

SEARCH_RESULTS = "search_results"
SEARCH_EXPLAIN = "search_explain"


# ==========================================================
# EDIT FLOW
# ==========================================================

EDIT_TEXT = "edit_text"


# ==========================================================
# GENERAL ACTIONS
# ==========================================================

CANCEL = "cancel"
EDIT = "edit"
CONFIRM = "confirm"
BACK = "back"
