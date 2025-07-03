from datetime import datetime, timedelta

def send_notification(message):
    print(message)

def get_next_n_saturdays(start_date, n):
    days_until_saturday = (5 - start_date.weekday()) % 7
    first_saturday = start_date + timedelta(days=days_until_saturday)
    return [first_saturday + timedelta(weeks=i) for i in range(n)]

def parse_duration_to_hours(duration_string):
    try:
        parts = duration_string.lower().replace(" ", "").replace("min", "").replace("h", "h").split("h")
        hours = int(parts[0]) if parts[0] else 0
        minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 0
        return hours + minutes / 60
    except Exception as e:
        print(f"Błąd przy parsowaniu czasu przejazdu '{duration_string}': {e}")
        return float('inf')  # domyślnie odrzuć połączenie