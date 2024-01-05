# Web Scraper

This Python script, `web_scraper.py`, is a web scraping tool that fetches and parses HTML content from a given URL. It provides a simple GUI for user interaction and allows users to specify the type of data they want to scrape.

## Main Components

### HtmlParser Class

This class is responsible for fetching and parsing HTML content from a given URL. It extends the `HTMLParser` class from Python's `html.parser` module. The main functionalities of this class include:

- Fetching HTML content from a specified URL.
- Parsing the HTML content based on user-specified criteria (e.g., specific HTML elements, classes, IDs, or comments).
- Storing the parsed data and optionally writing it to a file.

### ScrapMe Class

This class provides a simple GUI for user interaction. It extends the `Tk` class from Python's `tkinter` module. The main functionalities of this class include:

- Creating and managing UI widgets (e.g., labels, entry fields, radio buttons, and buttons).
- Handling user input and feedback.
- Invoking the `HtmlParser` class to scrape data based on user input.

### Main Function

The main function of this script initializes an instance of the `ScrapMe` class and starts the Tkinter event loop. This launches the GUI and allows the user to interact with the application.

## Usage

When run, the script opens a GUI window where the user can enter a URL and choose a scraping option. The options include scraping comments, specific HTML elements, elements with a specific class, or elements with a specific ID. After the user clicks the "Scrape" button, the script fetches and parses the HTML content from the specified URL, stores the parsed data, and writes it to a file named `results.txt`.




<img width="298" alt="GUI" src="https://github.com/usaeedcs/Webscraper-python/assets/85361194/301cc378-396c-4bbc-9b94-2f468d9f490a">
