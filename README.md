# 🎬 Movie Web App (Flask)

Eine kleine, moderne Web-App zum Verwalten von Lieblingsfilmen — inkl. User-Management, OMDb-Anbindung, dynamischen Seiten, Templates, Flash-Nachrichten, und einer responsiven UI.

Dieses Projekt wurde mit **Flask**, **SQLAlchemy**, **OMDb API**, **HTML/Jinja2** und **CSS** erstellt.

---

## 🚀 Features

- 👤 **Benutzerverwaltung** (User anlegen, anzeigen)
- 🎞️ **Filmverwaltung pro Benutzer**
- 🌐 **Automatisches Laden von Filmdaten über OMDb API**
- 🖼️ **Poster, Titel, Jahr, Regisseur – direkt aus OMDb**
- 🗑️ Update & Delete mit Sicherheits-Abfrage
- 🔔 Flash-Nachrichten (Erfolg, Fehler, Warnung)
- 🎨 Einheitliches Design mit `base.html`
- 📁 Saubere Projektstruktur mit Templates & Static Files
- ⚠️ Custom Fehlerseiten (404 & 500)

---

## 📁 Projektstruktur

```
MovieProjectWebApp/
│
├── app.py
├── data_manager.py
├── models.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── movies.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── style.css
│   └── img/
│       └── movie-web-app-logo.png
│
├── data/
│   └── movies.db
│
├── .env
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Repository klonen
```bash
git clone <your-repo-url>
cd MovieProjectWebApp
```

### 2. Virtuelle Umgebung erstellen
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependencies installieren
```bash
pip install flask flask_sqlalchemy python-dotenv requests
```

### 4. `.env` erstellen
```
API_KEY=DEIN_OMDB_API_KEY
SECRET_KEY=irgendein_geheimer_schluessel
```

### 5. Datenbank anlegen
```python
    with app.app_context():
        db.create_all()
```

### 6. App starten
```bash
    python app.py
```

App läuft danach unter:
```
http://localhost:5000
```

---

## 🔌 Wichtige Endpunkte

| Endpoint | Methode | Beschreibung |
|---------|---------|--------------|
| `/` | GET | Liste aller Benutzer |
| `/users` | POST | Neuen Benutzer anlegen |
| `/users/<id>/movies` | GET | Alle Filme eines Benutzers anzeigen |
| `/users/<id>/movies` | POST | Film hinzufügen (inkl. OMDb-Fetch) |
| `/users/<id>/movies/<movie_id>/update` | POST | Film aktualisieren |
| `/users/<id>/movies/<movie_id>/delete` | POST | Film löschen (mit Confirm) |

---

## 🧩 Technologien

- **Python 3.9+**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **OMDb API**
- **Jinja2**
- **CSS**

---

## 📄 Lizenz

Dieses Projekt ist Open Source. Du kannst es frei erweitern, verbessern oder anpassen.

---

## ✨ Hinweis

Wenn du Fragen hast oder neue Features einbauen möchtest (Login-System, Favoriten, Suchfunktion, Pagination, API-Version, Test-Suite etc.) helfe ich dir jederzeit gerne weiter.
