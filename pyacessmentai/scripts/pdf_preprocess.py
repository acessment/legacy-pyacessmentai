import weasyprint
from weasyprint.formatting_structure.boxes import LineBox, TextBox, InlineBox
import xml.etree.ElementTree as ET

def weasyprint_element_to_etree(element):
    """
    Converts a WeasyPrint element to an ElementTree element.
    """
    if element.element is not None:
        # Create an ElementTree element with the same tag and attributes
        etree_element = ET.Element(element.element.tag, attrib=element.element.attrib)
    else:
        # If the element has no tag (e.g., a text node), create a placeholder
        etree_element = ET.Element("div")

    # If the element is a TextBox, add its text content
    if isinstance(element, TextBox):
        etree_element.text = element.text

    # Recursively convert children
    for child in element.all_children():
        etree_child = weasyprint_element_to_etree(child)
        etree_element.append(etree_child)

    return etree_element

def weasyprint_document_to_etree(doc):
    """
    Converts a WeasyPrint document to an ElementTree object.
    """
    root = ET.Element("root")  # Create a root element for the ElementTree

    for page in doc.pages:
        for box in page._page_box.all_children():
            body = box.all_children()[0].all_children()
            for el in body:
                etree_element = weasyprint_element_to_etree(el)
                root.append(etree_element)

    return ET.ElementTree(root)


def get_element_by_render_id(doc: weasyprint.document.Document, target_id: str):
    """
    Traverses the entire WeasyPrint document tree from the root to find an element by render_id.
    
    Why not use id? because the render queue can have multiple documents, thus creating duplicate ids.
    """
    def find_element_by_render_id(element, target_id):
        """
        Recursively searches for an element with the specified target_id.
        """
        # Check if the current element has the target id
        if (
            element.element is not None
            and element.element.attrib.get("render_id") == target_id
        ):
            print(element.element.attrib)
            return element

        # Recursively search through all children
        for child in element.all_children():
            result = find_element_by_render_id(child, target_id)
            if result is not None:
                return result

        return None
    # Start traversal from the document root
    for page in doc.pages:
        # Traverse the page's _page_box (root box for the page)
        result = find_element_by_render_id(page._page_box, target_id)
        if result is not None:
            return result

    return None


def get_line_number(doc: weasyprint.document.Document, element_render_id: str) -> list[str]:
    """
    This function will return a list of strings that is ordered line by line according to the layout in the pdf file.
    You can input the class name of a particular parent element and the function will return the line number information of the child elements. 
    Note that the child elements should be text element such as "p", "h1", "span", "div" etc., other elements such as "img" or "table" will not be supported.
    
    Returns:
        list[str]: List of text strings, each representing a line in the document
    """
    target_element = get_element_by_render_id(doc, element_render_id)
    if target_element is None:
        print(f"Element with render id '{element_render_id}' not found")
        return []

    text_lines = []
    line_number = 0
    
    def extract_text_recursively(box):
        """
        Recursively extract text from any box type, handling arbitrary nesting levels
        """
        if isinstance(box, TextBox):
            return box.text
            
        text = ""
        # Process all children recursively regardless of box type
        for child in box.all_children():
            text += extract_text_recursively(child)
            
        return text
    
    # Traverse the target element to find line boxes
    for block_box in target_element.all_children():
        for box in block_box.all_children():
            if isinstance(box, LineBox):
                line_number += 1
                line_text = extract_text_recursively(box)
                
                if line_text.strip():  # Only add non-empty lines
                    print(f"Line {line_number}: {line_text}")
                    text_lines.append(line_text)
    
    return text_lines
