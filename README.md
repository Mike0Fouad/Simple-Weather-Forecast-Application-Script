
# Simple Weather Forecast Application 🧭

A command-line Python application that fetches and displays current weather using user-selected input (IP-based location, city/country, or latitude & longitude) via the OpenWeatherMap API and PyOWM.

---
## 🛠️ Skills Used

- Python (core language)
- API Integration (OpenWeatherMap, geolocation services)
- Environment management (`python-dotenv`)
- Error handling & logging (Python’s `logging`)
- Third-party libraries (e.g. `pyowm`, `geocoder`, `country_converter`)
- Command-line application development
- Version control (Git & GitHub)
- Data parsing & processing
- User input validation
- Software documentation (docstrings, inline comments)
---
## 📦 Features

- **Auto-detect location** via IP address (using `geocoder.ip`)  
- **City + country lookup**, supporting either ISO2 code or full country name  
- **Geographic coordinates** input (latitude & longitude)  
- **Interactive menu loop** with clean exit option  
- **Current weather display**, including:
  - Weather status (e.g., "Clear", "Rain")
  - Temperature (current, min, max in °C)

---

## 🛠️ Prerequisites

- Python **3.7+**
- A **virtual environment** (see setup below)
- **OpenWeatherMap** API key — free tier suffices  
- Install dependencies:
  ```bash
  pip install pyowm geocoder country_converter python-dotenv


* `pyowm`: Python wrapper for OpenWeatherMap ([github.com][1], [github.com][2])
* `geocoder`: IP-based location lookup
* `country_converter`: Country name ↔ ISO2 conversion
* `python-dotenv`: Load `.env` environment variables

---

## 🧪 Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/Mike0Fouad/Simple-Weather-Forecast-Application-Script.git
cd Simple-Weather-Forecast-Application-Script
```

### 2. Create & activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

*(If `requirements.txt` doesn’t exist, manually install the packages listed above.)*

### 4. Set your API key

Create a `.env` file in the project root:

```dotenv
API_KEY=your_openweathermap_api_key
```

### 5. Run the application

```bash
python main.py
```

Follow the interactive prompts to:

1. Get weather for your **current location**
2. Enter **city & country**
3. Enter **latitude & longitude**
4. **Exit**

Example flow:

```
Welcome to the Weather App!
Choose:
1. get Current Weather
2. get specific weather
3. get weather by coordinates
4. Exit
Enter your choice: 2
Enter the two-letter country code: United States
Enter the City name: Cairo
Getting weather for Cairo...
Today's weather in Cairo:
Status: Clear
Temperature: 30°C
Max Temperature: 32°C
Min Temperature: 28°C
```

---

## 🧩 Code Overview

**`Weather` class (`weather.py`)**

* Configures logging, loads `.env`, and initializes PyOWM
* `input_data()`: interactive menu to select input method
* `get_weather()`: fetches weather via PyOWM
* `print_weather()`: displays formatted output

**`main()` function (`main.py`)**

* Bootstraps the app, loops until user exits
* Handles exceptions and clean termination

---

## 🚀 Extend & Contribute

* Enhance output styling (e.g., color-coded status)
* Add optional forecast or hourly data
* Package as a console script (e.g. `entry_points` in `setup.py`)
* Switch to OpenWeatherMap’s **OneCall API** via PyOWM for forecasts ([github.com][3], [pyowm.readthedocs.io][4])

Pull requests and suggestions welcome!

---

## 🧾 Troubleshooting

* **Missing API key**: App exits with error prompting `.env` setup
* **Invalid country input**: `country_converter` raises error, and user is prompted again
* **Geo/IP lookup fails**: asks user for manual location
* **PyOWM Errors**: caught and re-prompts user

---

## ✅ License & Attribution

MIT License.
Uses:

* **PyOWM** - Python wrapper around OpenWeatherMap APIs ([github.com][5], [github.com][1])
* **geocoder** - for IP-based city lookup
* **country\_converter** - for converting country names/codes
* **python-dotenv** - for `.env` support

---

Enjoy using the Weather App! 🌤️

---



[1]: https://github.com/csparpa/pyowm/blob/master/README.md?utm_source=chatgpt.com "pyowm/README.md at master · csparpa/pyowm · GitHub"
[2]: https://github.com/sir-zech/WeatherApp?utm_source=chatgpt.com "GitHub - sir-zech/WeatherApp: A simple and stylish weather application ..."
[3]: https://github.com/CodeByFelix/pysimplegui-desktop-weather-app?utm_source=chatgpt.com "CodeByFelix/pysimplegui-desktop-weather-app - GitHub"
[4]: https://pyowm.readthedocs.io/en/latest/index.html?utm_source=chatgpt.com "PyOWM — pyowm documentation - Read the Docs"
[5]: https://github.com/ramakaknayt/Weather-Forecast?utm_source=chatgpt.com "GitHub - ramakaknayt/Weather-Forecast: A Simple Weather Forecast App ..."
