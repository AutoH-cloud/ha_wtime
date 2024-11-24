# const.py

# Domain for the integration
DOMAIN = "WTime"

# Default settings for the integration (if any)
DEFAULT_NAME = "WTime"

# Example of default sensor configurations
DEFAULT_SENSORS = ["date", "time", "dst", "jewish_weekday"]

# Translation keys
CONF_SENSORS = "sensors"

# Supported sensors (can be extended based on your custom sensors)
SENSOR_TYPES = {
    "date": "Date",
    "time": "Time",
    "dst": "DST Status",
    "jewish_weekday": "Jewish Weekday",
    "jewish_weekday_full": "Jewish Full Weekday",
}

# Some other constants that might be useful
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # in seconds
