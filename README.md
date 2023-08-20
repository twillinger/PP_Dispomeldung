# Python MSSQL-Datenbank-Integration

Dieses Skript enthält Funktionen zur Interaktion mit einer MSSQL-Datenbank. Es liest Konfigurationsdaten aus einer XML-Datei, stellt eine Verbindung zur Datenbank her und fügt Daten in eine spezifische Tabelle ein.

## Abhängigkeiten

- `openpyxl`
- `pyodbc`
- `datetime`
- `xml.etree.ElementTree`

## Hauptfunktionen

- **get_value_from_xml(xml_file, key)**: Liest Werte aus einer XML-Datei.
- **establish_connection(server, user, password)**: Stellt eine Verbindung zur MSSQL-Datenbank her.
- **update_value_in_xml(xml_file, key, new_value)**: Aktualisiert einen Wert in der XML-Datei.
- **aufgabe_pp()**: Hauptfunktion, die Daten aus der Datenbank abruft und die Datenverarbeitung und -insertion steuert.
- **auf_anlegen()**: Fügt Daten in die `TERORGANISATION`-Tabelle der Datenbank ein.

## Benutzung

1. Stellen Sie sicher, dass Sie alle benötigten Abhängigkeiten installiert haben.
2. Aktualisieren Sie die `settings.xml`-Datei mit den richtigen Konfigurationsdaten.
3. Führen Sie das Skript aus, um die Datenbank zu aktualisieren.

## Hinweise

Bevor Sie das Skript in einer Produktionsumgebung ausführen, stellen Sie sicher, dass Sie alle notwendigen Sicherungen Ihrer Datenbank durchgeführt haben. 

---
