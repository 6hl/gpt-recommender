MAX_USER_INPUT_LENGTH = 2048 * 2

CAROT_SYSTEM = """<|system|>
{system_prompt}<|end|>"""

CAROT_USER = """
<|user|>
{user_prompt}<|end|>"""

CAROT_ASSISTANT = """
<|assistant|>
{assistant_prompt}<|end|>"""

CAROT_END_TEMPLATE = """
<|assistant|> """

MODEL_MESSAGE_FORMAT_MAPPING = {
    "Phi-3-mini-4k-instruct.Q4_0.gguf": {
        "system": CAROT_SYSTEM,
        "user": CAROT_USER,
        "assistant": CAROT_ASSISTANT,
        "end": CAROT_END_TEMPLATE,
    },
}

MAX_PAGES_TO_SCRAPE = 5

# url constants
GOOD_READS_USER_BASE = (
    "https://www.goodreads.com/review/list/{user_id}?page={page_num}&shelf=read"
)
LETTERBOXD_USER_BASE = (
    "https://letterboxd.com/{user_id}/films/by/rated-date/page/{page_num}/"
)

GOOGLE_SEARCH_BASE = "https://www.google.com/search"

COOKIE_INFORMATION = {
    "CONSENT": "PENDING+987",
    "SOCS": "CAESHAgBEhIaAB",
}
