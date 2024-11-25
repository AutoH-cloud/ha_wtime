"""Constants for WTime integration."""

DOMAIN = "wtime"
DEFAULT_NAME = "WTime"

# Sensor types
SENSOR_TYPES = {
    "wtime_date": "Date",
    "wtime_time": "Time",
    "wtime_dst": "DST Status",
}

CONF_SENSORS = "sensors"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # Default update interval in seconds
