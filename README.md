# MehrFaden

MehrFaden ist ein Server-Projekt, das Mehrfach-Threading (Multithreading) nutzt, um parallele Prozesse effizient zu verwalten.

## Installation

**Repository klonen:**
   ```bash
   git clone https://github.com/Adyrem/MehrFaden.git
   cd MehrFaden
   ```

**Insomnia installieren**

https://docs.insomnia.rest/insomnia/install


## Nutzung

Der Server kann mit folgendem Befehl gestartet werden:
```bash
python Server.py
```

## API-Endpunkte

Der Server stellt eine einfache API bereit, die mit **Insomnia** getestet werden kann.

### GET-Anfrage
Abrufen eines gespeicherten Werts:
```http
GET /?user=<username>&key=<key>
```
Antwort:
- **200 OK**: Gibt den gespeicherten Wert zurück.
- **404 Not Found**: Falls kein Wert für den angegebenen Benutzer vorhanden ist.

### POST-Anfrage
Speichern eines neuen Werts:
```http
POST /
Content-Type: application/json

{
  "user": "<username>",
  "key": "<key>",
  "value": "<value>"
}
```
Antwort:
- **200 OK**: Gibt die gespeicherten Daten zurück.




