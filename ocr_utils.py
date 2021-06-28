import pytesseract
from PIL import Image


def correct_ethnicities(ethnicities):
    ethnicities = list(filter(None, ethnicities))
    ethnicities = [x.strip() for x in ethnicities]
    # Rudimentary OCR corrections
    errors = {
        "Filipino": ["Filipi", "Filipir"],
        "Hawaiian": ["Hawe", "Haw:", "Hawai", "Hawaiia", "Hawaiie", "Hav"],
        "Samoan": ["Sar", "Samoar", "Samoi", "Sarr"],
        "Hispanic": ["Hispani", "Hispani:", "Hispanir"],
        "Other": ["Othe", "Othe:", "Other Pac. Isl", "Other Pac. Isl:", "Other P", "Other Asian"],
        "Unknown": ["H", "C", "Unkr"],
        "Indian": ["India"],
        "Japanese": ["Japa", "Japane:", "Japan", "Japai", "Japanes"],
        "Native American": ["Native Americ", "Native"],
        "Chinese": ["Chin"],
        "Tongan":  ["Ton", "Tong"],
        "Micronesian": ["Micr"],
        "Laotian": ["Laotia"],
        "Middle Eastern": ["Middle Easter", "Middle Easter:"]
    }
    corrected_ethnicities = []

    for x in ethnicities:
        inserted = False
        for y in errors:
            if x in errors[y]:
                corrected_ethnicities.append(y)
                inserted = True
        if not inserted:
            corrected_ethnicities.append(x)

    return corrected_ethnicities

def read_text(path):
    return pytesseract.image_to_string(Image.open(path))
