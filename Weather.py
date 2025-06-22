from pyowm import OWM
from pyowm.utils.config import get_config_from
import geocoder
import country_converter as coco
from dotenv import load_dotenv
import os
import logging
# Set Up the OpenWeatherMap API

## Load environment variables from .env file
class Weather:
    def __init__(self):
        """
        Initializes the Weather class by setting up logging, loading environment variables, and configuring the OpenWeatherMap (OWM) API client.
        - Configures logging to the INFO level.
        - Loads environment variables from a .env file.
        - Retrieves the API key for OWM from environment variables.
        - Initializes the country converter for country name/code conversions.
        - Raises a ValueError if the API key is not found or if OWM initialization fails.
        - Initializes various instance variables for input and returned weather data.
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO)

        # Get the OpenWeatherMap API key
        load_dotenv()
        self._API_KEY = os.getenv('API_KEY')

        # Check if the API key is set
        if not self._API_KEY:
            logging.error("OWM_API_KEY not found in environment variables. Please set it in the .env file.")
            raise ValueError("OWM_API_KEY not found in environment variables. Please set it in the .env file.")
        
        # Initialize the OWM client
        try:
            self.owm = OWM(self._API_KEY)
        except Exception as e:
            logging.error(f"Error initializing OWM: {e}")
            raise ValueError(f"Error initializing OWM: {e}")
        
        # Initialize the country converter
        self.converter = coco.CountryConverter()


        # Inputed Data
        self.choice = None
        self.valid= False
        self.location = None
        self.time = None

        #Returned Data
        self.location = None
        self.weather = None
        self.weather_status = None
        self.temperature = None
        self.max_temp = None
        self.min_temp = None
        

    def input_data(self):
        """
        Handles user input for selecting weather data retrieval options.
        Prompts the user to choose between:
            1. Getting current weather based on their IP location.
            2. Getting weather for a specific city and country.
            3. Getting weather by entering latitude and longitude coordinates.
            4. Exiting the application.
        Depending on the user's choice:
            - For option 1, attempts to determine the user's location via IP and convert the country name to an ISO2 code.
            - For option 2, prompts for a city and country (accepts both country name and ISO2 code), converting if necessary.
            - For option 3, prompts for latitude and longitude, ensuring numeric input.
            - For option 4, sets location to None and exits.
            - Handles invalid inputs and prompts the user to try again.
        Returns:
            str or tuple or int or None: The location string (city,country), coordinates tuple (lat, lon), 0 for current location, or None for exit.
        """
        

        if self.choice is None or self.choice not in ['1', '2', '3', '4']:
            print("Choose:")
            print("1. get Current Weather")
            print("2. get specific weather")
            print("3. get weather by coordinates")
            print("4. Exit")
            self.choice = input("Enter your choice: ")
        
        if self.choice == '1':
            # Get the user's current location
            g = geocoder.ip('me')
            if g.ok:
                try:
                    country2code = self.converter.convert(g.country, to='ISO2')
                    self.location = g.city + ',' + country2code
                except ValueError as e:
                    logging.error(f"Error converting country name to ISO2 code: {e}")
                    print("Invalid country name. Please try again.")
                    return self.input_data()
            else:
                logging.error("Could not determine your current location.")
                print("Could not determine your current location. Please enter a city and country code.")
                return self.input_data()
            
            return 0
        elif self.choice == '2':
            # Get specific weather for a city and country
            country = input("Enter the two-letter country code: ")
            city = input("Enter the City name: ")
            if len(country) != 2:
                try:
                    country = self.converter.convert(country, to='ISO2')
                except ValueError as e:
                    logging.error(f"Error converting country name to ISO2 code: {e}")
                    print("Invalid country name. Please try again.")
                    return self.input_data()
            self.location = f"{city},{country}"
            print(f"Getting weather for {city}...")
            return self.location
        elif self.choice == '3':
            # Get weather by coordinates
            try:
                lat = input("Enter latitude: ")
                lon = input("Enter longitude: ")
                lat = float(lat)  # Convert to float
                lon = float(lon)  # Convert to float
            except ValueError:
                logging.error("Invalid input. Please enter numeric values for latitude and longitude.")
                return self.input_data()
            self.location = (lat, lon)
            print(f"Getting weather for coordinates {lat}, {lon}...")
            return self.location
        elif self.choice == '4':
            # Exit the program
            self.location = None
            self.choice = '4'
            return self.location
        else:
            print("Invalid choice. Please try again.")
            self.input_data()

    def get_weather(self):
        """
        Fetches and updates the current weather information based on the user's selected input method.
        Depending on the value of `self.choice`, retrieves weather data either by place name or by geographic coordinates
        using the OpenWeatherMap API. Updates instance attributes with the latest weather details, including location name,
        weather status, and temperature information (current, max, and min in Celsius).
        If an error occurs during the fetch, logs the error, prompts the user for new input, and retries fetching the weather.
        Raises:
            Exception: If there is an error fetching weather data from the API.
        """
        
        
        mgr = self.owm.weather_manager()
        try:
            if self.choice is None:
                self.input_data()
            elif self.choice == '1' or self.choice == '2':
                weather_details= mgr.weather_at_place(self.location)
            elif self.choice == '3':
                # If the location is a tuple, it means we are using coordinates
                weather_details = mgr.weather_at_coords(self.location[0], self.location[1])
            else:
                self.choice = '1'
                weather_details = mgr.weather_at_place(self.location)
            self.location= weather_details.location.name
            self.weather = weather_details.weather
            self.weather_status = self.weather.status
            self.temperature = self.weather.temperature('celsius')
            self.max_temp = self.temperature['temp_max']
            self.min_temp = self.temperature['temp_min']
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}")
            print("An error occurred while fetching the weather data. Please try again.")
            self.input_data()
            self.get_weather()
        

        

    def print_weather(self):
        """
        Prints the current weather information for the specified location.
        Outputs the following details to the console:
            - Location name
            - Weather status/description
            - Current temperature (in Celsius)
            - Maximum temperature (in Celsius)
            - Minimum temperature (in Celsius)
        Assumes that the following instance attributes are defined:
            - self.location (str): Name of the location.
            - self.weather_status (str): Description of the weather.
            - self.temperature (dict): Dictionary containing temperature data with key 'temp'.
            - self.max_temp (float or int): Maximum temperature.
            - self.min_temp (float or int): Minimum temperature.
        """
        print(f"Today's weather in {self.location}:")
        print(f"Status: {self.weather_status}")
        print(f"Temperature: {self.temperature['temp']}°C")
        print(f"Max Temperature: {self.max_temp}°C")
        print(f"Min Temperature: {self.min_temp}°C")


def main():
    """
    Main entry point for the Weather App.
    This function welcomes the user and provides an interactive loop to fetch weather information.
    Users can choose to get weather data for their current location, a specified city, or by coordinates.
    The loop continues until the user selects the exit option.
    Handles exceptions by logging errors and notifying the user of any issues during weather retrieval.
    """
    print("Welcome to the Weather App!")
    print("This app provides weather information for your current location or a specified city.")
    print("You can also get weather information by coordinates.")

    try:
        again= True
        while again:
            weather = Weather()
            weather.input_data()
            if weather.choice == '4':
                print("Exiting the program.")
                again = False
                break
            weather.get_weather()
            weather.print_weather()
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("An error occurred while fetching the weather. Please try again later.")
    
   

if __name__ == "__main__":
    # Run the main function
    main()
