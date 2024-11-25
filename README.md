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

### **Step 1: Add the Custom Repository to HACS**
1. **Install HACS**:  
   If you don’t have HACS installed yet, follow the [HACS Installation Guide](https://hacs.xyz/docs/installation/installation).

2. **Add the Repository**:  
   - Open **HACS** in Home Assistant.
   - Go to **"Integrations"**.
   - Click the three dots in the top-right and select **"Custom repositories"**.
   - Add the following repository:
     ```
     https://github.com/AutoH-cloud/ha_wtime
     ```
   - Select **"Integration"** as the category and click **"Add"**.

3. **Install Wtime**:  
   - Locate **Wtime** in the HACS Integrations section.
   - Click **"Install"** and follow the instructions.

4. **Restart Home Assistant**:  
   - Restart Home Assistant to activate the integration.

---

### **Step 2: Set Up the Wtime Integration**

1. **Add Integration**:  
   - Go to **Settings** > **Devices & Services** > **Integrations**.
   - Click **"Add Integration"** and search for **Wtime**.
   - Follow the prompts to complete the setup.
