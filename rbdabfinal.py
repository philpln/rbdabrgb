from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json
import requests

# Optionen für Headless-Modus
options = Options()
options.add_argument("--headless")  # Headless-Modus aktivieren

# Firefox WebDriver starten mit Optionen
driver = webdriver.Firefox(options=options)

try:
    # Öffne die Website
    driver.get("https://www.kleinanzeigen.de/s-anzeige:angebote/roy-bianco-regensburg/k0")

    # Warte kurz, bis die Seite geladen ist
    time.sleep(2)

    # Cookie-Banner akzeptieren
    try:
        grdp = driver.find_element(By.ID, "gdpr-banner-accept")
        grdp.click()
    except:
        print("Kein Cookie-Banner gefunden.")

    # Suche nach dem UL-Element
    ul_element = driver.find_element(By.ID, "srchrslt-adtable")

    # Alle LI-Elemente innerhalb des UL-Tags suchen
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    
    # Anzeigen-Daten aus JSON-Datei laden
    with open("anzeigen.json", 'r') as jsonFile:
        data = json.load(jsonFile)
    
    # Neue Anzeigen in die JSON-Daten hinzufügen
    for li in li_elements:
        try:
            # <a>-Tag innerhalb des LI-Elements finden
            a_tag = li.find_element(By.CSS_SELECTOR, "a.ellipsis")  # CSS-Selektor für den <a>-Tag
            href = a_tag.get_attribute("href")  # HREF-Attribut extrahieren
            
            # Überprüfen, ob die Anzeige bereits vorhanden ist
            if href not in data["anzeigen"]:
                print(f"Neue Anzeige gefunden: {href}")
                data["anzeigen"].append(href)
                # Ntfy-Benachrichtigung senden
                requests.post("https://ntfy.sh/rbdabrgb",
                    data=href,
                    headers={
                        "Title": "neue Tickets gefunden",
                        "Priority": "urgent",
                        "Tags": "warning"
                    })

        except:
            # Falls kein <a>-Tag vorhanden ist
            print("Kein <a>-Tag in diesem <li> gefunden")
    
    # Geänderte JSON-Daten in die Datei zurückschreiben
    with open("anzeigen.json", 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)

    print("Neue Anzeigen wurden gespeichert.")

finally:
    # Browser schließen
    driver.quit()