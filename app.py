#import openpyxl
import pyodbc
import datetime
import xml.etree.ElementTree as ET
import datetime
from datetime import datetime

def get_value_from_xml(xml_file, key):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for elem in root:
        if elem.attrib.get('key') == key:
            return elem.text
    return None

# Usage:
xml_path = 'settings.xml'
v_server = get_value_from_xml(xml_path, 'B6')
v_database = get_value_from_xml(xml_path, 'B9')
v_firma = get_value_from_xml(xml_path, 'B18')
s = get_value_from_xml(xml_path, 'B19')
row_hist_letzte = get_value_from_xml(xml_path, 'B20')
betr = get_value_from_xml(xml_path, 'B21')
mitbez = get_value_from_xml(xml_path, 'C19')
v_user = "PASST"
v_password = "HidHd4M"

def get_value_from_excel(sheet, cell_address):
    return sheet[cell_address].value

def establish_connection(server, user, password):
    connection_string = f"DRIVER={{SQL Server}};SERVER={server};UID={user};PWD={password}"
    cnxn = pyodbc.connect(connection_string)
    return cnxn

def update_value_in_xml(xml_file, key, new_value):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    element_found = False

    for elem in root:
        if elem.attrib.get('key') == key:
            elem.text = str(new_value)
            element_found = True
            break
    
    if not element_found:
        new_elem = ET.SubElement(root, 'Value', key=key)
        new_elem.text = str(new_value)
    
    tree.write(xml_file)

def aufgabe_pp():
    mit = s
    cnxn = establish_connection(v_server, v_user, v_password)
    cursor = cnxn.cursor()
    
    db = f"[{v_database}]"
    cursor.execute(f"USE {db}")
    
    cursor.execute(f"SELECT * FROM BESDIS WHERE ROWBESDIS > '{row_hist_letzte}' ORDER BY ROWBESDIS ASC")
    rows = cursor.fetchall()
    
    if not rows:
        row_hist_db = row_hist_letzte
    else:
        for row in rows:
            dispo = row.DISPO
            bezeichnung = row.BEZEICHNUNG
            datum = row.DATUM
            datum = datum.strftime('%d.%m.%Y')
            
            sachbearbeiter_dispo = row.SACHBEARBEITER
            row_hist_db = row.ROWBESDIS
            
            #art_liste = f"DISPO: {dispo} -\nBez: {bezeichnung} -\nDatum: {datum} -\nSachb-Dispo: {sachbearbeiter_dispo}"
            #art_liste = f"DISPO: {dispo} -" + CHAR(13) + CHAR(10) + f"Bez: {bezeichnung} -" + CHAR(13) + CHAR(10) + f"Datum: {datum} -" + CHAR(13) + CHAR(10) + f"Sachb-Dispo: {sachbearbeiter_dispo}"
            art_liste = f"DISPO: {dispo} -\r\nBez: {bezeichnung} -\r\nDatum: {datum} -\r\nSachb-Dispo: {sachbearbeiter_dispo}"


            #print(art_liste)
            
            # Call the Auf_anlegen function
            auf_anlegen(None, mit, None, None, datum, art_liste, None, None, None, mitbez, cursor, v_database, v_firma)
    
    # Usage:
    update_value_in_xml(xml_path, 'B20', row_hist_db)
    cnxn.close()

def auf_anlegen(vorgang, mit, bestellung, bes_betreff, datum, art_liste, vorg_betreff, adr, adr_kurzname, mitbez, cursor, v_database, v_firma):
    #v_server = get_value_from_excel(settings_sheet, 'B6')

    # Erstellen Sie ein datetime-Objekt für das aktuelle Datum und die aktuelle Uhrzeit
    jetzt = datetime.now()

    # Formatieren Sie das Datum im deutschen Format
    beginnam_datt = datetime.now()
    beginnam_dat = beginnam_datt.strftime('%d.%m.%Y')

    #formatted_datetime = beginnam_dat.strftime('%Y-%m-%d %H:%M:%S')

    erfass_dat = datetime.now()
    bis_dat = None 
    zeit_von = None
    status = "In Bearbeitung"
    prio = "Normal"
    notiz = ""
    orgtyp = '2'

    #print(beginnam_dat)
    protokoll = f"{erfass_dat} Erfasst: {mit} {erfass_dat} Zuständig: {mit}"
    
    cursor.execute(f"SELECT MAX(ROWORGANISATION) AS ID FROM TERORGANISATION")
    id_row = cursor.fetchone()
    id_val = int(id_row.ID) + 1

    #print(mit)


   
    query = """
        INSERT INTO TERORGANISATION (ROWORGANISATION, FIRMA, ORGTYP, DATUMVON, DATUMBIS, KURZTEXT, TEXT, ADRESSE, MITARBEITER, ZEITVON, STATUSTEXT, PRIO, VONMITARBEITER, BETREFF, ERFASSER, ERFASSDAT, PROTOKOLL, NOTIZ, VORGANG, VORGBETREFF, ADRKURZNAME, MITKURZNAME)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    parameters = (id_val, v_firma, orgtyp, beginnam_dat, bis_dat, betr, art_liste, adr, mit, zeit_von, status, prio, mit, betr, mit, beginnam_dat, protokoll, notiz, vorgang, vorg_betreff, adr_kurzname, mitbez)


    #print(query, parameters)  # Print the query string
    #print(id_val)
    try:
        cursor.execute(query, parameters)
        cursor.commit()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    
    print(id_val)
    queryZaehl = "UPDATE ZAEHLERTABELLE SET ROWZAEHL = ? WHERE NAME = 'TERORGANISATION'"
    parametersZaehl = (id_val,)
    print(queryZaehl, parametersZaehl)
    try:
        cursor.execute(queryZaehl, parametersZaehl)
        cursor.commit()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
# To execute the function
aufgabe_pp()
