# Bentota Divisional Secretariat Development Project System 📊

A cloud-native web application built to digitize, monitor, and query development programs and infrastructure projects for the Bentota Divisional Secretariat Division. This application migrates localized spreadsheets into a scalable relational data infrastructure to streamline project lifecycle tracking and statutory administrative reporting.

---

## 🛠️ Tech Stack & Key Architectures

* **Backend Framework:** Python Flask 3.0.2 (WSGI standard routing)
* **Production Server:** Gunicorn 21.2.0 (Sync worker engine)
* **Cloud Relational Database:** Neon PostgreSQL (Serverless cluster instance)
* **Containerization:** Docker (Debian-slim base environment layer)
* **Frontend Engine:** Jinja2 Template Layout + Native Vanilla JavaScript (Excel export, dynamic variant switching)

---

## 🏗️ System Architecture & Data Directory

The codebase implements a strict separation of concerns engineered for low-overhead container environments:

```text
Website/
│
├── templates/
│   └── index.html          # Unified Jinja2 layout for forms, editing, and reports
│
├── app.py                  # Main operational controller & HTTP request router
├── models.py               # Structural database mapping layers & input choices
├── requirements.txt        # Deterministic Python environment dependency manifest
├── Dockerfile              # Multi-layer container system configuration
└── .gitignore              # Access token control filter tracking files
