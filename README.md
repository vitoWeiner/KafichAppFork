# KafichApp
## izradili: Antonio Delač i Vito Weiner
Web aplikacija koja olakšava upravljanje kafićem.


UPDATE - PORUKA ZA 4 PRAKTIČNI ZADATAK:
implementirani su REST API endpointi te im se može pristupiti nakon prijave korisnika u aplikaciji putem slijedećih authentifikacijskih podataka:


username: admin
password: admin

Otvara se izbornik, te se pod stavkom "lista pića (REST)" nalazi GUI sučelje za pozivanje endpointova.

Zahtjevi

Da biste pokrenuli aplikaciju, potrebno je imati instalirane slijedeće pakete:

    - Django (verzija 5.1.1 ili novija)
    - Django Filter (django-filter)
    - Django REST framework




Nakon pokretanja aplikacije, prva stranica je namjenjena za log in, tamo se može odabrati opcija za registraciju novih računa za novog admina ili novog korisnika
ili se mogu upotrijebiti podaci za log in već postojećih admina i korisnika:

ADMIN
username: admin
password: admin12345

USER
username: user
password: user12345 
