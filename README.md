# 🚆 Cheap Train Finder & Email Notifier

This script searches for **cheap and time-efficient train connections** based on your preferences, and automatically sends you an email summary of the best round-trip options.

---

## ✨ Features

- Scrapes **KOLEO** train connections
- Supports **weekend** or **daily** travel searches
- Filters by:
  - Maximum ticket price
  - Maximum travel duration
- Sends a **styled HTML email** with results
- Fully configurable via `config.yaml` and `.env`

---

## 📁 Project Structure

```
.
├── main.py # Main script
├── config.yaml # User configuration (travel preferences)
├── .env # Email credentials
├── modules/ # Utility modules
│ ├── config_loader.py
│ ├── email_sender.py
│ ├── html_builder.py
│ ├── train_scraper.py
│ └── utils.py
```

---

## ⚙️ Configuration

### 🔐 .env

GMAIL_ACCOUNT=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

> 💡 Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if you have 2FA enabled on your Google account.

---

### 📄 config.yaml

```yaml
data_wyjazdu: ""                # Leave empty for today
tryb_szukania: "weekend"       # Options: "weekend", "codziennie"
liczba_weekendów_wyszukiwania: 4
dni_szukania: 10
przejazd_do: "warszawa"
przejazd_z: "krakow"
cena_maksymalna: 80
nocy_na_miejscu: 2
godzina_wyjazdu: "07:00"
max_czas_przejazdu: 5.5


🚀 Usage
Run the script:
```

python main.py

```

If matching connections are found, an email is sent with a detailed list of round-trip options.


📬 Sample Output
An example email contains:
Travel date
Departure and return details
Duration and price
Direct links to the KOLEO search results



🧪 Notes
If no results match the filters, no email is sent.
Connection data is scraped using dynamic URLs per travel date.
Assumes proper Polish formatting of prices and times (zł, HH:MM).



✅ Requirements
Python 3.8+

Required modules:
dotenv
requests
beautifulsoup4
smtplib (built-in)
email (built-in)

You can install requirements with:
```

pip install -r requirements.txt

```


📧 Final Note
This tool is ideal for weekend getaways, budget travel planning, or even automated monitoring of train deals.
```
