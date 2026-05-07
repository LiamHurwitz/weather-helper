import tkinter as tk
from tkinter import Frame, Menu, Tk, messagebox

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

import openmeteoToCsv as meteoCSV


def main():
    # Generate CSV data for Duvall
    meteoCSV.fetchData(47.7423, -121.9857, "Duvall")


if __name__ == "__main__":
    main()
