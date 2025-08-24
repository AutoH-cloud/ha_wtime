"""Constants for WTime integration."""

DOMAIN = "wtime"
DEFAULT_NAME = "WTime"

# (legacy keys you already had)
SENSOR_TYPES = {
    "wtime_date": "Date",
    "wtime_time": "Time",
    "wtime_dst": "DST Status",
}
CONF_SENSORS = "sensors"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # seconds

# --- Auto-purge options (NEW) ---
CONF_AUTOPURGE_ENABLED = "autopurge_enabled"
CONF_AUTOPURGE_ENTITY_IDS = "autopurge_entities"
CONF_AUTOPURGE_INTERVAL = "autopurge_interval"  # seconds

DEFAULT_AUTOPURGE_INTERVAL = 60  # every minute
DEFAULT_AUTOPURGE_ENTITY_IDS = [
    "sensor.wtime_12hr_clock",
    "sensor.wtime_12hr_clock_with_seconds",
    "sensor.wtime_24hr_clock",
    "sensor.wtime_24hr_clock_with_seconds",
]
