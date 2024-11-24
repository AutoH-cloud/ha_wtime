# custom_components/WTime/const.py

DOMAIN = "WTime"

DEFAULT_NAME = "WTime"

# Define available sensor types
SENSOR_TYPES = {
    "wtime_date": "Date",
    "wtime_time": "Time",
    "wtime_dst": "DST Status",  # Added DST status
}

CONF_SENSORS = "sensors"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # in seconds
