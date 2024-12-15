# **WTime**

## **Custom Integration for Home Assistant**

**WTime** is a custom integration for Home Assistant that provides a variety of sensors related to time and dates, including Daylight Saving Time (DST) status, current seasons, and more. It's perfect for displaying time-based information on your Home Assistant dashboard and creating automations based on DST status or seasons.

---

## **Available Sensors**

- **Clock**: Displays the current time in a 12 and in 24-hour format, with and without seconds (updated in real time).
- **Date**: Displays the current date (e.g., December 1, 2024).
- **Date (Short)**: Displays the current date in numeric format (e.g., 12/01/24).
- **Current Month**: Displays the current month (useful for automations).
- **DST Status**: Indicates whether Daylight Saving Time (DST) is currently active.
- **Current Season**: Displays the current season (Spring, Summer, Fall, Winter).
- **Weekday**: Displays the full name of the current day (e.g., Sunday).
- **Weekday (Short)**: Displays the abbreviated name of the current day (e.g., Sun).

---

## **Installation Instructions**

### **Add Repository to HACS**

1. Open the **HACS** section in Home Assistant.
2. Navigate to **Settings > Custom Repositories**.
3. Enter the following URL into the **Repository URL** field:
     ```
     https://github.com/AutoH-cloud/ha_wtime
     ```
4. Set the category to **Integration** and click **Add**.
5. Return to the **Integrations** page and install **WTime** from the list.
6. Restart Home Assistant when prompted.

---

### **Set Up the WTime Integration**

1. Go to **Settings > Devices & Services > Integrations**.
2. Click **Add Integration** and search for **WTime**.
3. Follow the on-screen instructions to complete the setup.

---

## **Automation Examples**

### **Example 1: Notify When DST Changes**
This automation sends a notification whenever Daylight Saving Time (DST) status changes.

```yaml
alias: Notify DST Change
description: "Send a notification when DST status changes"
trigger:
- platform: state
 entity_id: sensor.Wtime_dst_status
condition: []
action:
- service: notify.mobile_app
 data:
   title: "DST Status Changed"
   message: >
     Daylight Saving Time is now {{ states('sensor.wtime_dst_status') }}.
mode: single
```

### **Example 2: Adjust Thermostat Based on Season**
This automation adjusts the thermostat based on the current season.
```yaml
alias: Adjust Thermostat by Season
description: "Set thermostat settings based on the current season"
trigger:
  - platform: state
    entity_id: sensor.wtime_current_season
condition: []
action:
  - choose:
      - conditions:
          - condition: state
            entity_id: sensor.wtime_current_season
            state: "Winter"
        sequence:
          - service: climate.set_temperature
            target:
              entity_id: climate.home_thermostat
            data:
              temperature: 22
      - conditions:
          - condition: state
            entity_id: sensor.wtime_current_season
            state: "Summer"
        sequence:
          - service: climate.set_temperature
            target:
              entity_id: climate.home_thermostat
            data:
              temperature: 24
      - conditions:
          - condition: state
            entity_id: sensor.wtime_current_season
            state: "Spring"
        sequence:
          - service: climate.set_temperature
            target:
              entity_id: climate.home_thermostat
            data:
              temperature: 21
      - conditions:
          - condition: state
            entity_id: sensor.wtime_current_season
            state: "Fall"
        sequence:
          - service: climate.set_temperature
            target:
              entity_id: climate.home_thermostat
            data:
              temperature: 20
mode: single
```

To disable recording history and lookback for the clock sensors, add the below in the ```configuration.yaml``` file.
```
recorder:
  exclude:
    entities:
      - sensor.wtime_12hr_clock
      - sensor.wtime_12hr_clock_with_seconds
      - sensor.wtime_24hr_clock
      - sensor.wtime_24hr_clock_with_seconds
      - sensor.wtime_date
      - sensor.wtime_date_short
      - sensor.wtime_weekday
      - sensor.wtime_weekday_short
```

  # Support
If you found this project helpful and would like to support its development, consider buying me a coffee! ☕

<div align="center"> <a href="https://buymeacoffee.com/yoely0966" target="_blank"> <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee" style="height: 50px; width: auto;"> </a> </div>
