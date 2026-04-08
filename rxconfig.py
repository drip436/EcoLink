import os
import reflex as rx
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="ecolink",
    db_url=os.environ["DATABASE_URL"],
    port=3000,
    state_auto_setters=True,
)
