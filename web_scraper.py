import tkinter as tk
import tkinter.simpledialog as simpledialog
from html.parser import HTMLParser
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class HtmlParser(HTMLParser):
    """
    This class represents html parser. It provides functionality of parsing html
    based on specific elements, it could be comments, id or a class.
    It takes url as an argument, makes request to it and store html content in
    self.html variable.
    """

    def __init__(self, url="") -> None:
        """
        Constructor for HtmlParser Class
        Params:
            url: str
        Returns:
            None
        """
        super().__init__()
        if url == "":
            raise Exception("Url is required")
        self.url = url
        self.html = HtmlParser.fetch(url)
        self.specific_elem = ""  # if specific element needs to be scrapped
        self.specific_class = ""  # if element with specific class needs to be scrapped
        self.specific_id = ""  # element with specific id needs to be scrapped
        self.comments_only = False  # if only comments needs to be scrapped
        self.data_inside_div = []  # Stores data that is inside of specific element
        self.data = []  # stores all data
        self.inside_tag = False  # Flag for checking if we are inside of specific element

    def handle_starttag(self, tag, attrs) -> None:
        """
        This is helper method for extracting html start tags
        using this helper we are going to utilize our options
        based scrap

        Params:
            tag: str
            attrs: [str]
        Returns:
            None
        """
        if self.specific_elem and tag == self.specific_elem:
            self.inside_tag = True

        elif self.specific_class:
            if (self.compare_attr(attrs, "class", self.specific_class)):
                self.inside_tag = True
                self.specific_class = tag

        elif self.specific_id:
            if (self.compare_attr(attrs, "id", self.specific_id)):
                self.inside_tag = True
                self.specific_id = tag

    def handle_comment(self, data) -> None:
        """
        This function is responsible for extracting comments
        Params:
            data: str
        Returns:
            None
        """

        if self.comments_only:
            self.data = data.strip()

    def handle_data(self, data: str) -> None:
        """
        This function is responsible for extracting data
        Params:
            data: str
        Returns:
            None
        """
        if self.inside_tag and data.strip() != '':
            self.data_inside_div.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        """
        This function is responsible for handling closing tag
        Params:
            tag: str
        Returns:
            None
        """
        if self.inside_tag and (self.specific_elem == tag or self.specific_class == tag or self.specific_id == tag):
            self.inside_tag = False
            self.data.append(self.data_inside_div)
            self.data_inside_div = []

    def is_scrapable(self):
        """
        Helper function for checking if site is scrapable
        Params:
            None
        Returns:
            None
        """
        return True if "data" in self.html.keys() else False

    def scrap(self, specific_elem="", specific_class="", specific_id="", comments_only=False, feed="") -> None:
        """
        This function is responsible for scrapping html content
        Params:
            None
        Returns:
            None
        """
        if not self.is_scrapable():
            return None
        if specific_elem:
            self.specific_elem = specific_elem
        elif specific_class:
            self.specific_class = specific_class
        elif specific_id:
            self.specific_id = specific_id
        else:
            self.comments_only = comments_only
        self.feed(feed if feed else str(self.html['data']))
        self.dump_results()

    @staticmethod
    def fetch(url) -> None:
        """
        Fetches html content from url
        and returns html content
        Params:
            None
        Returns:
            str
        """
        if not url:
            raise Exception("Url is required")

        try:
            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                if response_text and response.getcode() == 200:
                    return {"success": True, "data": response_text}
                else:
                    raise Exception("Error making the request")

        except Exception as e:
            return {"success": False, "error": e}

    # Helper Methods

    def compare_attr(self, attrs, key, value) -> bool:
        """
        Compares attribute with value
        Params:
            attrs: [(str, str)]
            value: str
        Returns:
            bool
        """

        for attr in attrs:
            if attr[0].strip().lower() == key and attr[1].strip().lower() == value:
                return True
        return False

    def dump_results(self, file=""):
        """
        This helper function dumps results to a file
        Params:
            file: str
        Returns:
            None
        """
        file = "results.txt" if not file else file
        with open(file, "w") as f:
            f.write(str(self.data))


class ScrapMe(tk.Tk):
    """
    This class represents a simple GUI for scraping data from a website.
    """

    def __init__(self, geometry="400x250"):
        """
        Constructor for ScrapingApp class
        Params:
            geometry: string
        Returns:
            None
        """
        super().__init__()  # calling super class constructor
        self.title("Scrap Me")
        self.geometry(geometry)
        self.create_widgets()

    def create_widgets(self):
        """
        Helper function to create UI widgets
        Params:
            None
        Returns:
            None
        """
        self.url_label = tk.Label(self, text="Enter URL:")  # url label
        self.url_label.pack()  # packing url label
        self.url_entry = tk.Entry(self, width=40)  # adding url field
        self.url_entry.pack()

        # Now let's add radio buttons for scraping options
        self.scrap_option = tk.IntVar()
        self.scrap_option.set(0)

        self.radio_frame = tk.Frame(self)
        self.radio_frame.pack(pady=10)

        options = [
            ("Scrap Comments", 1),
            ("Scrap specific element", 2),
            ("Scrap by specific class", 3),
            ("Scrap by specific ID", 4)
        ]

        for text, value in options:
            tk.Radiobutton(self.radio_frame, text=text, variable=self.scrap_option,
                           value=value).pack(anchor="w")

       # Let's add a label for feedback message
        self.feedback_label = tk.Label(self, text="", fg="blue")
        self.feedback_label.pack(pady=5)

        # Let's now add scrap button
        self.scrape_button = tk.Button(
            self, text="Scrape", command=self.scrape_data)
        self.scrape_button.pack(pady=10)

    def scrape_data(self):
        """
        This is helper function for scraping data from a website
        we will be utilising HtmlParser class for this purpose
        Params:
            None
        Returns:
            None
        """
        url = self.url_entry.get()
        if not url:
            tk.messagebox.showwarning("Error", "Please enter a URL.")
            return

        option = self.scrap_option.get()

        if option == 0:
            tk.messagebox.showwarning(
                "Error", "Please choose a scraping option.")
            return

        specific_input = ""
        if option in (2, 3, 4):
            specific_input = simpledialog.askstring(
                "Input", "Enter the name of the specific element, class, or ID:")
            if not specific_input:
                tk.messagebox.showwarning(
                    "Error", "Please enter name of the specific element, class, or ID:")
                return

         # Display feedback message while scraping is in progress
        self.feedback_label.config(text="Scraping in progress...", fg="blue")
        self.feedback_label.update()

        # Let's instantiate HtmlParser class
        parser = HtmlParser(url)

        if parser.is_scrapable():
            # Now let's call scrap method based on the option
            if option == 1:  # Scrap Comments
                parser.scrap(comments_only=True)
            elif option == 2:  # Scrap specific element
                parser.scrap(specific_elem=specific_input)
            elif option == 3:  # Scrap by specific class
                parser.scrap(specific_class=specific_input)
            elif option == 4:  # Scrap by specific ID
                parser.scrap(specific_id=specific_input)

            # Save the scraped data to a file (optional)
            parser.dump_results("results.txt")

            # Update the feedback message with success
            self.feedback_label.config(
                text=f"Scraping completed. Results saved to results.txt.", fg="green"
            )

            # Show a simple dialog box for the result
            tk.messagebox.showinfo(
                "Scraping Result", "Scraping completed. Results saved to 'results.txt'.")
        else:
            # Update the feedback message with success
            self.feedback_label.config(
                text=f"Failed", fg="red"
            )
            tk.messagebox.showinfo(
                "Application Error", str(parser.html['error']))


if __name__ == "__main__":
    app = ScrapMe()
    app.mainloop()
