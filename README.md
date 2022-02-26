# BEST2022
Rešitev za identifikacijo anomalij pri merjenjo količine kurilnega olja. Sistem podatke o meritvah prejme, jih obdela, poišče morebitne napake in jih popravi. O najdenih napakah tudi obvesti preko email sporočila. Podatke za največjo kompatibilnost z že obstoječimi sistemi shranjuje naravnost v access podatkovno zbirko, kjer so pripravljeni tudi izpisi. Access podatkovna zbirka je povezana tudi z powerBI, ki omogoča boljši pregled.

![slika](https://user-images.githubusercontent.com/33715779/155846810-f04b6a36-2bf7-4bc2-a177-d9c22f377c4c.png)

## Konfiguracija
Konfiguracijske nastavitve sistema se nahajajo v datoteki `.env` v mapi `/backend`. Te se lahko spremenijo za namene testiranja sistema. Ta vsebuje naslednje vrednosti:
- MAIL_PASSWORD - geslo email računa s katerega se pošiljajo obvestila
- MAIL_USERNAME - email računa s katerega se pošiljajo obvestila
- MAX_CONSUMPTION - največja dovoljena poraba (v kubičnih metrih)
- WARNING_RECIPIENT - email naslov, kamor se bodo opozorila pošiljala

## Zahteve
 - Python 3^
 - Windows OS
 - [Access driver](https://www.microsoft.com/en-US/download/details.aspx?id=13255)

## Navodila za uporabo
- odprite `/backend` mapo
- dvakrat kliknite na `run_virtualenv_DEV.bat`
- počakajte da se vse namesti (če to počnete prvič)
- aplikacija je zagnana in dostopna na naslovu http://127.0.0.1:5000/

## Končne točke aplikacije
- http://127.0.0.1:5000/import - sproži simulacijo branja novih txt datotek z meritvami
- http://127.0.0.1:5000/email - sproži simulacijo obvestila o dolivanju goriva
- http://127.0.0.1:5000/emailc - sproži simulacijo obvestila o preveliki porabi
