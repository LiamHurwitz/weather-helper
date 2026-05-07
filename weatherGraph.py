import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generateWeatherGraphs(town_name: str):
    weather_dataframe = pd.read_csv(f"Hourly_Weather_Data_{town_name}.csv")
    weather_dataframe["Hour"] = np.arange(
        1, 25
    )  # Add prettier hours so reduce graph clutter

    # Do some plotting with subplots -- FOR NOW I AM NOT INCLUDING CLOUD COVER I LEGIT DONT KNOW HOW TO DO IT AND DONT FEEL LIKE LOOKING
    fig, ax = plt.subplots(2, 3)
    ax[0, 0].plot(weather_dataframe["Hour"], weather_dataframe["temperature_2m"])
    ax[0, 0].set_title("Temperature (F)")
    ax[0, 1].plot(weather_dataframe["Hour"], weather_dataframe["relative_humidity_2m"])
    ax[0, 1].set_title("Relative Humidity")
    ax[0, 2].plot(
        weather_dataframe["Hour"], weather_dataframe["precipitation_probability"]
    )
    ax[0, 2].set_title("Precipitation Probability")
    ax[1, 0].plot(weather_dataframe["Hour"], weather_dataframe["precipitation"])
    ax[1, 0].set_title("Precipitation (in)")
    ax[1, 1].plot(weather_dataframe["Hour"], weather_dataframe["wind_speed_10m"])
    ax[1, 1].set_title("Wind Speed (mph)")
    ax[1, 2].plot(weather_dataframe["Hour"], weather_dataframe["uv_index"])
    ax[1, 2].set_title("UV Index")

    plt.show()


# Testing REMOVE LATER
town = "Duvall"
generateWeatherGraphs(town)
