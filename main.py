import io
import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

from modules.config_loader import ConfigLoader
from modules.email_sender import EmailSender
from modules.html_builder import build_html_email
from modules.train_scraper import TrainScraper
from modules.utils import (get_next_n_saturdays, parse_duration_to_hours,
                           send_notification)

# Setup encoding and dotenv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()  # load .env file if present

def main():
    config_loader = ConfigLoader("config.yaml")
    config = config_loader.load_config()

    train_scraper = TrainScraper()
    cheap_connections = []

    # Determine base date
    if not config.get("data_wyjazdu"):
        base_date = datetime.today()
    else:
        base_date = datetime.strptime(config["data_wyjazdu"], "%d-%m-%Y")

    tryb_szukania = config.get("tryb_szukania", "weekend").lower()

    if tryb_szukania == "weekend":
        num_weekends = int(config.get("liczba_weekendów_wyszukiwania", 4))
        searching_period = get_next_n_saturdays(base_date, num_weekends)
    elif tryb_szukania == "codziennie":
        dni_do_szukania = int(config.get("dni_szukania", 14))
        searching_period = [base_date + timedelta(days=i) for i in range(dni_do_szukania)]
    else:
        print("⚠️ Nieznany tryb szukania. Używam domyślnego (weekend).")
        num_weekends = int(config.get("liczba_weekendów_wyszukiwania", 4))
        searching_period = get_next_n_saturdays(base_date, num_weekends)

    max_duration = float(config.get("max_czas_przejazdu", 24))

    for date in searching_period:
        data_wyjazdu = date.strftime("%d-%m-%Y")
        godzina_wyjazdu = config["godzina_wyjazdu"]
        max_price = float(config["cena_maksymalna"])
        return_after_days = int(config["nocy_na_miejscu"])

        url_wyjazd = f"https://koleo.pl/rozklad-pkp/{config['przejazd_do']}/{config['przejazd_z']}/{data_wyjazdu}_{godzina_wyjazdu}/all/all"
        print(f"\n🔍 URL wyszukiwania (wyjazd): {url_wyjazd}")
        polaczenia_wyjazd = train_scraper.find_connections(url_wyjazd)

        date_connections = []

        for polaczenie in polaczenia_wyjazd:
            try:
                price = float(str(polaczenie["price"]).replace("zł", "").replace(",", ".").strip())
                czas_przejazdu_h = parse_duration_to_hours(polaczenie['travel_time'])

                if price < max_price and czas_przejazdu_h <= max_duration:
                    msg = f"📅 {data_wyjazdu} - Wyjazd: {price:.2f} zł, {polaczenie['departure_time']} → {polaczenie['arrival_time']} ({polaczenie['travel_time']})"
                    send_notification(msg)
                    date_connections.append(msg)

                    data_powrotu = (date + timedelta(days=return_after_days)).strftime("%d-%m-%Y")
                    godzina_powrotu = "20:00"
                    url_powrot = f"https://koleo.pl/rozklad-pkp/{config['przejazd_z']}/{config['przejazd_do']}/{data_powrotu}_{godzina_powrotu}/all/all"
                    print(f"🔁 URL wyszukiwania (powrót): {url_powrot}")
                    polaczenia_powrot = train_scraper.find_connections(url_powrot)

                    for polacenie_powrot in polaczenia_powrot:
                        try:
                            price_return = float(str(polacenie_powrot["price"]).replace("zł", "").replace(",", ".").strip())
                            czas_powrotu_h = parse_duration_to_hours(polacenie_powrot['travel_time'])

                            if price_return < max_price and czas_powrotu_h <= max_duration:
                                msg_return = f"↩️ {data_powrotu} - Powrót: {price_return:.2f} zł, {polacenie_powrot['departure_time']} → {polacenie_powrot['arrival_time']} ({polacenie_powrot['travel_time']})"
                                send_notification(msg_return)
                                date_connections.append(msg_return)
                        except Exception as e:
                            print(f"Błąd podczas parsowania ceny (powrót): {e}")
            except Exception as e:
                print(f"Błąd podczas parsowania ceny (wyjazd): {e}")

        if date_connections:
            cheap_connections.append(f"🗓️ {data_wyjazdu}:\n" + "\n".join(date_connections) +
                                     f"\n🌐 Linki:\n➡️ {url_wyjazd}\n⬅️ {url_powrot}\n")

    train_scraper.close()

    if cheap_connections:
        html_body = build_html_email(cheap_connections)

        gmail_user = os.getenv("GMAIL_ACCOUNT")
        gmail_password = os.getenv("GMAIL_PASSWORD")

        if not gmail_user or not gmail_password:
            print("❌ Brakuje zmiennych środowiskowych: GMAIL_ACCOUNT i/lub GMAIL_PASSWORD")
            return

        email_sender = EmailSender(gmail_user=gmail_user, gmail_password=gmail_password)
        email_sender.send_email(
            to_email=gmail_user,
            subject="🚆 Tanie połączenia kolejowe",
            body=html_body
        )
    else:
        print("❌ Nie znaleziono żadnych tanich połączeń.")

if __name__ == "__main__":
    main()
