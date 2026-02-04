# Overview

The goal of this project was to develop a Weather Dashboard application to enhance my skills in software development, API integration, and cloud database usage. As a software engineer, this project allowed me to learn how to fetch live data from an external API, store it in a cloud database, and present it in an interactive GUI with real-time updates and historical trends.

The software is a Python-based GUI application that lets users select or add weather stations using ZIP codes, fetch the latest weather from the OpenWeatherMap API, and store readings in Firebase Firestore. The dashboard displays current temperature, humidity, wind speed, and weather description, and includes a historical graph of temperature readings for each station. Users can dynamically add new stations, and the data is stored in the cloud for persistence.

To use the program, run the Python script, select a station from the dropdown (or add a new one with a ZIP code), and click “Update Weather” to fetch the latest readings. The dashboard will display the current weather and update the historical temperature graph automatically.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

The cloud database used in this project is Firebase Firestore. It is a NoSQL cloud database that allows real-time updates and easy integration with Python via the Firebase Admin SDK.

The database structure for this project is as follows:

weatherStations (collection)
 ├── StationName (document, e.g., Madison-Wisconsin)
 │    └── readings (subcollection)
 │         ├── timestamp_document (document, e.g., 20260203120000)
 │         │    ├── temperature
 │         │    ├── humidity
 │         │    ├── windSpeed
 │         │    ├── description
 │         │    └── timestamp
 └── AnotherStation (document)
      └── readings (subcollection)
           └── ...


Each station has its own document, and each reading is stored as a timestamped sub-document. This structure allows storing multiple readings over time and generating historical graphs.

# Development Environment

The software was developed using Python 3 in VS Code as the IDE.

Libraries and tools used:

Tkinter – for creating the GUI.

Requests – for calling the OpenWeatherMap API.

Firebase Admin SDK – to connect and write to Firebase Firestore.

Matplotlib – to display historical temperature graphs inside the GUI.

Datetime – for managing timestamped readings.

This setup allowed seamless integration between live weather data, cloud storage, and interactive visualization in the dashboard.

# Useful Websites

OpenWeatherMap API Documentation
 – for understanding weather API endpoints and parameters.

Firebase Firestore Python SDK
 – for Python integration with Firestore.

Matplotlib Documentation
 – for plotting historical weather data.

Tkinter Tutorial
 – for GUI design in Python.

# Future Work

Add options to plot humidity and wind speed trends in addition to temperature.

Implement automatic periodic updates so the dashboard refreshes weather readings every hour.

Improve GUI styling and usability, including color-coded alerts for extreme weather.

Enable user authentication and personalized station lists.