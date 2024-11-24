# WTime

# **Wtime Custom Integration for Home Assistant**
### *Still in Beta - Use at your own discretion!*

Welcome to the **Wtime** custom integration for Home Assistant! This integration provides various sensors related to time and dates, including support for Jewish calendar days, daylight savings status, and more. It is perfect for displaying various time-based information on your Home Assistant dashboard.

#### **Key Features**:
- **Current Date**: Displays the current date in a user-friendly format.
- **Time**: Displays the current time, which updates in real-time.
- **Jewish Week Date**: Displays the current Jewish weekday in Hebrew, perfect for Jewish-themed dashboards.
- **DST Status**: Shows whether the current time is before or after Daylight Saving Time (DST).
- **Customizable**: Easily adjust the date and time formats to suit your preferences.

---

### **Warning: This Integration is Still in Beta**
Please note that **Wtime** is still in beta, and while it’s functional, some features may be subject to changes. We appreciate your understanding and feedback as we continue to improve this integration.

---

## **Installation Instructions**
To get started, follow these steps:

### **Step 1: Add the Custom Repository to HACS**

1. **Install Home Assistant Community Store (HACS)**:  
   If you don’t have HACS installed yet, follow the [HACS Installation Guide](https://hacs.xyz/docs/installation/installation) to get it set up on your Home Assistant instance.

2. **Add Custom Repository to HACS**:
   - Open Home Assistant and go to **HACS** (you’ll find it in the left-hand menu).
   - Click on **"Integrations"**.
   - In the top-right corner, click on the three dots (overflow menu) and select **"Custom repositories"**.
   - Paste the URL of this repository into the **"Repository"** field. (Replace with your actual repo link)
     ```
     https://github.com/AutoH-cloud/ha_wdate
     ```
   - Select **"Integration"** as the category and click **"Add"**.
   
3. **Install the Integration**:
   - Now, go back to the **"Integrations"** page in HACS, and you should see **Wtime** listed there.
   - Click **"Install"** to install the integration.

4. **Restart Home Assistant**:
   - After installation, restart Home Assistant to allow the integration to load correctly.

---

### **Step 2: Set Up the Wtime Integration**

1. **Add the Integration**:
   - Go to **Settings** > **Devices & Services** > **Integrations**.
   - Click **"Add Integration"** and search for **Wtime**.
   - Select **Wtime** and follow the prompts to complete the setup.

2. **Configure the Sensors**:
   - The integration will automatically create several sensors. You can modify these sensors using the `configuration.yaml` file or through the **UI** if you prefer.
   - The available sensors include:
     - **Date**: Displays the current date.
     - **Time**: Displays the current time.
     - **Jewish Week Date**: Displays the current Jewish day (in Yiddish).
     - **DST Status**: Displays the DST status (Before or After DST).
  
   Example of how you can configure these sensors in `configuration.yaml` (if needed):
   ```yaml
   sensor:
     - platform: wtime
       name: "Jewish Week Date"
     - platform: wtime
       name: "DST Status"
________________________________________________

