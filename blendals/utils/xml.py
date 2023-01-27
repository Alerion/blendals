from lxml import etree
from lxml.etree import _Element as Element
from rich import print


def print_xml(element: Element) -> None:
    print(etree.tostring(element, pretty_print=True).decode("utf-8"))


def save_xml_to_file(content: Element, file_path: str) -> None:
    with open(f"xml/{file_path}", "wb") as file:
        file.write(etree.tostring(content, pretty_print=True))
