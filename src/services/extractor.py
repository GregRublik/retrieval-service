from bs4 import BeautifulSoup
from schemas.websearch import RawPage, ExtractedDocument

class ExtractService:

    @staticmethod
    def extract(page: RawPage) -> ExtractedDocument:
        soup = BeautifulSoup(page.html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string if soup.title else ""

        text = " ".join(soup.stripped_strings)

        return ExtractedDocument(
            url=page.url,
            title=title,
            text=text
        )