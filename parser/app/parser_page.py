from html.parser import HTMLParser


class ParserPage(HTMLParser):

    def __init__(self):
        super().__init__()
        self._links = []

    def handle_starttag(self, tag, attrs):
        """Search url to csv files

        :param tag:
        :param attrs:
        """
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and '.csv?' in value:
                    self._links.append(value)

    def get_files_links(self, html_page: str) -> list[str]:
        """Parsing HTML data

        :param html_page:
        :return:
        """
        self._links = []
        self.feed(html_page)
        return self._links
