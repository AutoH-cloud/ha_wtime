# WTime

## **Wtime Custom Integration for Home Assistant**
### *Still in Beta - Use at your own discretion!*

Welcome to the **Wtime** custom integration for Home Assistant! This integration provides various sensors related to time and dates, including support for daylight savings status, seasons, and more. It is perfect for displaying various time-based information on your Home Assistant dashboard.

---

## **Key Features**
- **Current Date**: Displays the current date in a user-friendly format.
- **Time**: Displays the current time, which updates in real-time.
- **DST Status (Binary Sensor)**: Indicates whether the current time is during Daylight Saving Time (DST).
- **Current Season**: Displays the current season (Spring, Summer, Fall, or Winter).
- **Customizable**: Easily adjust the date, time, and season formats to suit your preferences.

---

## **Installation Instructions**

### **Option 1: Use the Quick Install Button**
Click the button below to open Home Assistant and navigate directly to the **HACS > Custom Repositories** page. Add the repository URL and select "Integration."

[![Open HACS Repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?repository_url=https://github.com/AutoH-cloud/ha_wtime&category=integration)

---

### **Option 2: Manual Installation via HACS**
1. Open the **HACS** section of Home Assistant.
2. In **Integrations**, click the **"Explore & Add Repositories"** button in the bottom-right corner.
3. Search for **"Wtime"** in the search bar.
4. If it doesn’t appear, add the repository manually:
   - Go to **Settings > Custom Repositories**.
   - Paste the following URL into the **Repository URL** field:
     ```
     https://github.com/AutoH-cloud/ha_wtime
     ```
   - Select **"Integration"** as the category and click **Add**.
5. Once added, return to the **Integrations** page and install **Wtime**.
6. Restart Home Assistant when prompted.

---

### **Step 3: Set Up the Wtime Integration**

1. **Add Integration**:  
   - Go to **Settings** > **Devices & Services** > **Integrations**.
   - Click **"Add Integration"** and search for **Wtime**.
   - Follow the prompts to complete the setup.

2. **Sensors Configuration (Optional)**:  
   Add the following to your `configuration.yaml` for additional customization:

   ```yaml
   sensor:
     - platform: wtime
       name: "Current Date"
     - platform: wtime
       name: "Current Time"
     - platform: wtime
       name: "Current Season"

   binary_sensor:
     - platform: wtime
       name: "DST Status"
