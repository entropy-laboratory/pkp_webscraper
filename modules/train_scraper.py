from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

class TrainScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def parse_duration_to_hours(self, duration_string):
        try:
            parts = duration_string.lower().replace(" ", "").replace("min", "").replace("h", "h").split("h")
            hours = int(parts[0]) if parts[0] else 0
            minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 0
            return hours + minutes / 60
        except Exception as e:
            print(f"Błąd przy parsowaniu czasu przejazdu '{duration_string}': {e}")
            return float('inf')  # domyślnie odrzuć połączenie

    def find_connections(self, url, max_duration=None):
        self.driver.get(url)
        time.sleep(5)  # Wait for the page to load
        connections = []

        # Nowe selektory CSS dla nowej struktury strony
        train_segments = self.driver.find_elements(By.CSS_SELECTOR, "a.search-result")

        for segment in train_segments:
            try:
                # Cena
                price_element = segment.find_element(By.CSS_SELECTOR, ".search-result-price__price")
                price_text = price_element.text.replace("zł", "").replace(",", ".").replace("&nbsp;", "").strip()
                price = float(price_text)

                # Czas odjazdu
                departure_time = segment.find_element(By.CSS_SELECTOR, ".search-result-time--origin .search-result-time__scheduled").text.strip()
                
                # Czas przyjazdu
                arrival_time = segment.find_element(By.CSS_SELECTOR, ".search-result-time--destination .search-result-time__scheduled").text.strip()

                # Czas podróży
                travel_time_element = segment.find_element(By.CSS_SELECTOR, ".search-result-main__duration")
                travel_time = travel_time_element.text.replace("Czas podróży", "").strip()

                # Sprawdzenie czasu przejazdu
                duration_hours = self.parse_duration_to_hours(travel_time)
                if max_duration is not None and duration_hours > max_duration:
                    continue  # pomiń zbyt długi przejazd

                # Liczba przesiadek
                changes_element = segment.find_element(By.CSS_SELECTOR, ".search-result-main__changes")
                changes = changes_element.text.strip()

                connections.append({
                    "price": price,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "travel_time": travel_time,
                    "changes": changes
                })
            except Exception as e:
                print(f"Błąd podczas parsowania segmentu: {e}")
                continue

        return connections

    def close(self):
        self.driver.quit()