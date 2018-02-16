import xml.etree.ElementTree as ET


def get_romset(mamexml, blacklist):
    tree = ET.parse(mamexml)
    root = tree.getroot()

    romset = dict()
    for child in root:
        driver = child.find("driver")
        if (driver is None):
            continue

        status = driver.get("status")
        if ((status != "good") and (status !="imperfect")):
            continue

        cloneof = child.get("cloneof")
        if (not cloneof):
            cloneof = child.get("name")

        if (cloneof.startswith(blacklist)):
            continue
        
        if (cloneof not in romset):
            romset[cloneof.lower()] = list()

        romset[cloneof].append(child)
    
    return romset


if __name__ == "__main__":
    romset = get_romset("mame.xml", blacklist)
