async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Wtime sensors based on a config entry."""
    async_add_entities([
        DateSensor(),
        TimeSensor(),
        JewishDateSensor(),
        DSTSensor()
    ])
