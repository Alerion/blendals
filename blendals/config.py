from dataclasses import dataclass


@dataclass
class Settings:
    LIVE_SET_CONTROLS_COLLECTION: str = "LiveSetControls"


settings = Settings()
