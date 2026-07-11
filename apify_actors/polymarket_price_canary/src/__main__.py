"""Entry point wiring, per Apify Python Actor convention (`python3 -m src`)."""

import asyncio

from .main import main

if __name__ == "__main__":
    asyncio.run(main())
