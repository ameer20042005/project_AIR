# Project AIR - CO2, Temperature, and Humidity Monitoring System

## Overview
Project AIR is an Arduino-based system that measures CO2 levels, temperature, and humidity. The collected data is sent to a Python script, which logs it into an Excel file for analysis and monitoring.

## Repository
GitHub Repository: [Project AIR](https://github.com/ameer20042005/project_AIR.git)

## Components
- **Arduino Board** (e.g., Arduino Uno)
- **CO2 Sensor** (e.g., MH-Z19, MQ135)
- **DHT11/DHT22 Sensor** for temperature and humidity
- **USB Cable** for data transfer
- **Computer with Python Installed**

## Installation & Setup
### Arduino Setup
1. Connect the CO2 sensor and DHT sensor to the Arduino.
2. Upload the provided Arduino code (`arduino_code.ino`) using the Arduino IDE.
3. Select the correct COM port and board type in the Arduino IDE.

### Python Setup
1. Install Python (if not already installed).
2. Install required dependencies:
   ```sh
   pip requirements.txt
   ```
3. Run the Python script to start logging data:
   ```sh
   python fff.py
   ```

## How It Works
1. The Arduino collects CO2, temperature, and humidity data from sensors.
2. The data is transmitted via the serial port to the computer.
3. The Python script reads the incoming data and saves it into an Excel file.

## Data Format
The data is logged in an Excel file in the following format:

| Timestamp | CO2 (ppm) | Temperature (°C) | Humidity (%) |
|-----------|----------|-----------------|--------------|
| 2025-03-12 12:00:00 | 450 | 25.3 | 60 |

## Features
- Real-time monitoring of air quality.
- Data logging in Excel for further analysis.
- Easy to set up and integrate with additional sensors.

## Future Improvements
- Implement real-time visualization using Matplotlib.
- Cloud integration for remote monitoring.
- Mobile app for remote access to data.

## License
This project is open-source under the MIT License.

## Contribution
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Contact
For any questions or suggestions, please contact the project owner through the GitHub repository.
