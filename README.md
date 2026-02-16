<div align="center">

# 🤖 Telegram to Google Calendar Bridge

### AI-Powered Natural Language Event Assistant

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram API](https://img.shields.io/badge/Telegram_Bot_API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Calendar_API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

<br>

<a href="#english">🇬🇧 English</a> | <a href="#italiano">🇮🇹 Italiano</a>

</div>

---

<h2 id="english">🇬🇧 English</h2>

### 📖 About The Project
A powerful Telegram bot that integrates seamlessly with Google Calendar, allowing users to manage events through natural language. By leveraging Google's Generative AI (Gemini), the bot intelligently parses conversational input, extracts event details, and automatically schedules them into your calendar.

### 🚀 Key Features
* **🧠 Natural Language Processing:** Add events using everyday conversational language without strict formatting rules.
* **📅 Multi-Calendar Support:** Manage multiple calendars and automatically route events based on custom categories.
* **⚡ Smart Event Parsing:** Automatically extracts dates, times, durations, and contextual details.
* **🔄 Real-time Updates:** Immediate two-way synchronization with your Google Calendar.
* **🎨 Customizable Categories:** Automatic color-coding for different event types to keep your schedule visually organized.

### 🛠️ Tech Stack
* **Backend:** Python 3.12
* **APIs:** Google Calendar API, Telegram Bot API, Google Generative AI
* **Core Libraries:**
  * `python-telegram-bot` (Telegram framework)
  * `google-api-python-client` (Calendar integration)
  * `google-genai` (NLP and AI parsing)
  * `python-dotenv` (Environment management)

### 🎥 Live Demo
Here's the bot in action, parsing natural language and adding an event on the fly:

<div align="center">
  <img src="assets/demo_bot.gif" alt="Bot Demo" width="80%" />
</div>

### ⚡ Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/gizano/telegram-to-calendar.git
cd telegram-to-calendar
```

**2. Set up environment**
```bash
cp .env.example .env
# Edit .env with your personal credentials
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Google Cloud**
* Enable the Google Calendar API in your GCP Console.
* Create a Service Account and download credentials as `credentials.json`.
* Share your target Google Calendar with the service account email.

**5. Run the bot**
```bash
python main.py
```

### 📝 Configuration Parameters
* `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (from BotFather)
* `GOOGLE_AI_API_KEY`: Google Generative AI API key
* `GOOGLE_EMAIL`: Your primary Google account email
* `CALENDAR_ID`: Default Google Calendar ID

### 📚 Documentation Links
* [Google Calendar API Guide](https://developers.google.com/calendar/api/guides/overview)
* [python-telegram-bot Documentation](https://python-telegram-bot.org/)
* [Google Generative AI Docs](https://ai.google.dev/)

---

<h2 id="italiano">🇮🇹 Italiano</h2>

### 📖 Riepilogo del Progetto
Un potente bot Telegram che si integra perfettamente con Google Calendar, permettendo agli utenti di gestire gli eventi utilizzando il linguaggio naturale. Sfruttando l'AI generativa di Google (Gemini), il bot interpreta in modo intelligente i messaggi conversazionali, estrae i dettagli dell'evento e li pianifica automaticamente nel calendario.

### 🚀 Funzionalità Principali
* **🧠 Elaborazione del Linguaggio Naturale:** Aggiungi eventi usando frasi colloquiali senza regole di formattazione rigide.
* **📅 Supporto Multi-Calendario:** Gestisci più calendari e indirizza automaticamente gli eventi in base a categorie personalizzate.
* **⚡ Parsing Intelligente:** Estrazione automatica di date, orari, durate e dettagli contestuali.
* **🔄 Sincronizzazione in Tempo Reale:** Aggiornamento immediato e bidirezionale con il tuo Google Calendar.
* **🎨 Categorie Personalizzabili:** Codifica a colori automatica per distinguere visivamente i vari tipi di eventi.

### 🛠️ Stack Tecnologico
* **Backend:** Python 3.12
* **API:** Google Calendar API, Telegram Bot API, Google Generative AI
* **Librerie Core:**
  * `python-telegram-bot` (Framework Telegram)
  * `google-api-python-client` (Integrazione Calendar)
  * `google-genai` (NLP e Parsing AI)
  * `python-dotenv` (Gestione variabili d'ambiente)

### 🎥 Demo
Ecco il bot in azione mentre interpreta una frase colloquiale e aggiunge un evento al volo:

<div align="center">
  <img src="assets/demo_bot.gif" alt="Demo del Bot" width="80%" />
</div>

### ⚡ Avvio Rapido

**1. Clona il repository**
```bash
git clone https://github.com/gizano/telegram-to-calendar.git
cd telegram-to-calendar
```

**2. Configura l'ambiente**
```bash
cp .env.example .env
# Modifica il file .env con le tue credenziali
```

**3. Installa le dipendenze**
```bash
pip install -r requirements.txt
```

**4. Configurazione Google Cloud**
* Abilita l'API di Google Calendar dalla tua console GCP.
* Crea un Service Account e scarica le credenziali nel file `credentials.json`.
* Condividi il tuo calendario di destinazione con l'indirizzo email del Service Account.

**5. Avvia il bot**
```bash
python main.py
```

### 📝 Parametri di Configurazione
* `TELEGRAM_BOT_TOKEN`: Il token del tuo bot Telegram (fornito da BotFather)
* `GOOGLE_AI_API_KEY`: Chiave API per Google Generative AI (Gemini)
* `GOOGLE_EMAIL`: La tua email principale dell'account Google
* `CALENDAR_ID`: ID del calendario Google predefinito

### 📚 Riferimenti Ufficiali
* [Guida API Google Calendar](https://developers.google.com/calendar/api/guides/overview)
* [Documentazione python-telegram-bot](https://python-telegram-bot.org/)
* [Documentazione Google Generative AI](https://ai.google.dev/)

---
<div align="center">
  
  **Developed by [GiZano](https://giovanni-zanotti.is-a.dev)**
  
</div>
