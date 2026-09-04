# ==============================================================================
# config.py - Secure Configuration
# ==============================================================================
# Secrets are loaded ONLY from environment variables.
# Never put API_HASH, BOT_TOKEN, STRING_SESSION, or MongoDB credentials
# directly in this file or commit them to GitHub.
# ==============================================================================

import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):

        # ==========================================================================
        # TELEGRAM API
        # ==========================================================================
        self.API_ID: int = self._get_int("8708079238", 0)
        self.API_HASH: str = os.getenv("54e664524248ecc195bd3d731725396d", "").strip()

        # Bot token must come from environment variables.
        self.BOT_TOKEN: str = os.getenv("8974679127:AAFXY5MvPGqzG2W7E8pH5gPGRGQV06ZA-a0", "").strip()

        self.LOGGER_ID: int = self._get_int("5476060006", 0)
        self.OWNER_ID: int = self._get_int("8708079238", 0)

        # ==========================================================================
        # DATABASE
        # ==========================================================================
        self.MONGO_URL: str = os.getenv("MONGO_DB_URI", "").strip()

        # ==========================================================================
        # MUSIC BOT LIMITS
        # ==========================================================================
        self.DURATION_LIMIT: int = (
            self._get_int("DURATION_LIMIT", 300) * 60
        )

        self.QUEUE_LIMIT: int = self._get_int("QUEUE_LIMIT", 30)

        self.PLAYLIST_LIMIT: int = self._get_int("PLAYLIST_LIMIT", 20)

        self.PLAYLIST_MAX: int = self._get_int("PLAYLIST_MAX", 60)

        # ==========================================================================
        # SPOTIFY - OPTIONAL
        # ==========================================================================
        self.SPOTIFY_CLIENT_ID: str = (
            os.getenv("SPOTIFY_CLIENT_ID")
            or os.getenv("SPOTIPY_CLIENT_ID")
            or ""
        ).strip()

        self.SPOTIFY_CLIENT_SECRET: str = (
            os.getenv("SPOTIFY_CLIENT_SECRET")
            or os.getenv("SPOTIPY_CLIENT_SECRET")
            or ""
        ).strip()

        # ==========================================================================
        # ASSISTANT SESSIONS
        # ==========================================================================
        self.SESSION1: str = os.getenv("STRING_SESSION", "").strip()
        self.SESSION2: str = os.getenv("STRING_SESSION2", "").strip()
        self.SESSION3: str = os.getenv("STRING_SESSION3", "").strip()

        # ==========================================================================
        # SUPPORT
        # ==========================================================================
        self.SUPPORT_CHANNEL: str = os.getenv(
            "SUPPORT_CHANNEL",
            "https://t.me/hasiimusic"
        ).strip()

        self.SUPPORT_CHAT: str = os.getenv(
            "SUPPORT_CHAT",
            "https://t.me/TheInfinityAI"
        ).strip()

        # ==========================================================================
        # EXCLUDED CHATS
        # ==========================================================================
        self.EXCLUDED_CHATS: List[int] = self._parse_excluded_chats()

        # ==========================================================================
        # FEATURE FLAGS
        # ==========================================================================
        self.QUEUE_END_MESSAGE: bool = self._str_to_bool(
            os.getenv("QUEUE_END_MESSAGE", "False")
        )

        self.AUTO_LEAVE: bool = self._str_to_bool(
            os.getenv("AUTO_LEAVE", "False")
        )

        self.THUMB_GEN: bool = self._str_to_bool(
            os.getenv("THUMB_GEN", "True")
        )

        # ==========================================================================
        # VIDEO
        # ==========================================================================
        self.VIDEO_MAX_HEIGHT: int = self._parse_video_height()

        # ==========================================================================
        # YOUTUBE COOKIES
        # ==========================================================================
        self.COOKIES_URL: List[str] = self._parse_cookies()

        # ==========================================================================
        # IMAGES
        # ==========================================================================
        self.DEFAULT_THUMB: str = os.getenv(
            "DEFAULT_THUMB",
            "https://files.catbox.moe/kgrs8f.png"
        ).strip()

        self.PING_IMG: str = os.getenv(
            "PING_IMG",
            "https://files.catbox.moe/djilyq.png"
        ).strip()

        self.START_IMG: str = os.getenv(
            "START_IMG",
            "https://files.catbox.moe/7jihmf.png"
        ).strip()

        self.RADIO_IMG: str = os.getenv(
            "RADIO_IMG",
            "https://files.catbox.moe/t03fzk.png"
        ).strip()

        # ==========================================================================
        # MODERATION
        # ==========================================================================
        self.EXCLUDED_USERNAMES: List[str] = (
            os.getenv("EXCLUDED_USERNAMES", "").split()
        )

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    @staticmethod
    def _get_int(name: str, default: int = 0) -> int:
        """Safely read an integer environment variable."""
        value = os.getenv(name, str(default)).strip()

        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _parse_video_height(self) -> int:
        """Clamp video height to a safe range."""

        default_height = 480
        height = self._get_int(
            "VIDEO_MAX_HEIGHT",
            default_height
        )

        # 0 or negative = unlimited
        if height <= 0:
            return 0

        # Keep between 360p and 1080p
        return max(360, min(height, 1080))

    def _parse_excluded_chats(self) -> List[int]:
        """Parse comma-separated Telegram chat IDs."""

        value = os.getenv("EXCLUDED_CHATS", "").strip()

        if not value:
            return []

        chat_ids: List[int] = []

        for item in value.split(","):
            item = item.strip()

            if item.lstrip("-").isdigit():
                chat_ids.append(int(item))

        return chat_ids

    def _parse_cookies(self) -> List[str]:
        """Parse allowed cookie URLs."""

        value = os.getenv("COOKIE_URL", "").strip()

        if not value:
            return []

        valid_sources = (
            "batbin.me",
            "pastebin.com",
            "paste.ee",
            "rentry.co",
        )

        return [
            url.strip()
            for url in value.split()
            if url.strip()
            and any(source in url for source in valid_sources)
        ]

    @staticmethod
    def _str_to_bool(value: str) -> bool:
        """Convert common environment values to boolean."""

        return value.strip().lower() in (
            "true",
            "1",
            "yes",
            "y",
            "on",
        )

    # ==========================================================================
    # CONFIGURATION VALIDATION
    # ==========================================================================

    def check(self) -> None:
        """Validate required environment variables."""

        required_vars = {
            "API_ID": self.API_ID,
            "API_HASH": self.API_HASH,
            "BOT_TOKEN": self.BOT_TOKEN,
            "MONGO_DB_URI": self.MONGO_URL,
            "LOGGER_ID": self.LOGGER_ID,
            "OWNER_ID": self.OWNER_ID,
            "STRING_SESSION": self.SESSION1,
        }

        missing = [
            name
            for name, value in required_vars.items()
            if not value
            or (isinstance(value, int) and value == 0)
        ]

        if missing:
            raise SystemExit(
                "❌ Missing required environment variables: "
                + ", ".join(missing)
                + "\n"
                "Please configure them in your hosting provider's "
                "Environment Variables / Secrets."
            )


# Create configuration object
Config = Config()
