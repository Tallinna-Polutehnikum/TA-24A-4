# Kinoprojekt

Kinorakenduse projekt.

## Kasutatavad tehnoloogiad

- FastAPI
- SQLModel
- Pydantic v2
- Alembic
- PostgreSQL
- Docker
- Faker


## Backendi valik

Backendi teeme Pythonis ja andmebaasiks kasutame PostgreSQL-i. Python sai valitud sellepärast, et kood on üsna lihtsalt loetav ja API tegemiseks on olemas head tööriistad.

Teeme projekti kahekesi, nii et tahame jõuda ka rakenduse valmis, mitte kulutada enamikku aega raamistiku õppimisele.

Võrdlesime kolme varianti. Meie jaoks loeb eriti see, kuidas nendega valmis SQL-tabeleid kasutada, sest andmebaasi skeemi tegime enne backendit.


### FastAPI ja SQLModel

Selles variandis teeb FastAPI API osa ja SQLModel seob Pythoni klassid andmebaasi tabelitega.

Pydantic v2 kontrollib päringuga saadetud andmeid ning Alembicuga muudame hiljem tabelite struktuuri. PostgreSQL on toetatud.

Meie kinoprojekti jaoks on hea see, et näiteks filmi lisamine ja seansside otsimine ei vaja väga palju koodi.

FastAPI teeb ka API dokumentatsiooni, kus saab päringuid proovida. See aitab enne frontendiga ühendamist näha, kas backend töötab.

Miinus on see, et SQLModel ei tee meie valmis andmebaasist ise mudeliklasse. Need peame tabelite järgi kirjutama ja kontrollima, et väljad ning seosed klapiksid.

Ka Alembicu pakutud migratsioonid tuleb üle vaadata. Keerulisemate päringute korral võib vaja minna SQLAlchemy juhendeid, sest SQLModel kasutab seda enda all.


### FastAPI ja SQLAlchemy

Siin kasutaksime SQLModeli asemel otse SQLAlchemyt.

FastAPI, Pydantic ja Alembic jääksid samaks. Ka see variant toetab PostgreSQL-i.

SQLAlchemy eelis on olemasoleva andmebaasi struktuuri lugemine ehk reflection.

Automap saab selle põhjal tabelid ORM-iga siduda. Kuna kirjutasime SQL-i enne valmis, oleks sellest kasu.

Samas tuleks API andmemudelid eraldi kirjutada ja osa välju korduks eri klassides.

Õppida oleks rohkem, sest tuleb aru saada sessioonidest ja seoste kasutamisest.

Meie projekti tavalisemate lisamise ning otsimise funktsioonide jaoks tundub SQLModel lihtsam.


### Django

Kolmas variant oleks Django koos selle ORM-i ja Django REST Frameworkiga, millega saab API teha.

PostgreSQL on toetatud ning migratsioonid on Djangos endas olemas.

Django juures oleks kasulik valmis haldusliides. Sellega saaks filme ja seansse hallata ilma, et peaksime kohe kõik haldusvaated ise tegema.

Olemasolevatest tabelitest saab käsuga `inspectdb` mudelite algversiooni luua.

Meie jaoks oleks miinus see, et peaksime õppima nii Django ülesehitust kui ka REST Frameworki.

Väikese, eraldi frontendiga projekti jaoks tundub see rohkem tööd, kui meil vaja on.


## Mida kasutame

Jääme FastAPI ja SQLModeli juurde.

Lisaks kasutame:

- Pydantic v2
- Alembic
- PostgreSQL

Kirjutame mudelid SQL-skeemi järgi ja paneme Alembicus paika sellele vastava algversiooni.

Edasised tabelimuudatused teeme migratsioonidega.

Broneerimisel peame lisaks API kontrollidele kasutama andmebaasi piiranguid ja tehinguid, et sama seansi sama kohta ei saaks kaks inimest korraga broneerida.


# Projekti käivitamine

## 1. Environment failid

Tee `Database/.env.example` põhjal uus fail:
Database/.env
Näiteks:
POSTGRES_PASSWORD=change_me

Seejärel tee Backendi jaoks fail:
Backend/.env

Näiteks:
DATABASE_URL=postgresql+psycopg://kino:change_me@localhost:5432/kino

Mõlemas failis peab olema sama PostgreSQL parool.
2. PostgreSQL käivitamine Dockeriga
Mine Database kausta:
cd Database

Käivita andmebaas:
docker compose up -d

Kontrolli, kas andmebaas töötab:
docker compose ps

Andmebaasi status peaks olema healthy.
3. Backendi dependency'd
Mine Backend kausta:
cd ../Backend

Installi vajalikud dependency'd:
python -m uv sync

4. Migratsioonid
Käivita Alembic migratsioonid:
python -m uv run alembic upgrade head

See loob PostgreSQL andmebaasi vajalikud tabelid.
5. Demoandmed
Käivita seeder:
python -m uv run python -m backend.seed

Seeder lisab andmebaasi demoandmeid:
- kinod
- saalid
- istekohad
- filmid
- kasutajad
- seansid
- piletid
- arvustused
Seeder loob näiteks:
- 120 seanssi
- 300 piletit
- 300 istekohta
- 50 arvustust
Andmebaasi kontrollimine
Mine Database kausta:
cd ../Database

Ava PostgreSQL terminal:
docker compose exec db psql -U kino -d kino

Näiteks saab kontrollida andmete arvu:
SELECT COUNT(*) FROM sessions;
SELECT COUNT(*) FROM tickets;
SELECT COUNT(*) FROM seats;
SELECT COUNT(*) FROM reviews;

PostgreSQL terminalist väljumiseks:
\q

Andmebaasi täielik nullimine
Kui tahad andmebaasi täiesti puhtaks teha:
docker compose down -v

Seejärel käivita uuesti:
docker compose up -d

Mine Backend kausta:
cd ../Backend

Rakenda migratsioonid:
python -m uv run alembic upgrade head

Lisa demoandmed:
python -m uv run python -m backend.seed

Allikad
FastAPI, SQLModel, SQLAlchemy Automap, Alembic, Django ja Django REST Framework.


## Andmebaasi indeksid

Projektis kasutame andmebaasi indekseid veergudel, mille järgi rakendus teeb otsinguid, filtreerimist või seotud andmete päringuid.

Indeksid aitavad PostgreSQL-il vajalikke andmeid kiiremini leida. Indekseid ei lisata igale veerule, sest need võtavad lisaruumi ja võivad muuta andmete lisamise ning muutmise natuke aeglasemaks.

Kasutatavad indeksid:

- `movies.name`
  - filmi nime järgi otsimiseks

- `movie_genres.genre`
  - filmide žanri järgi filtreerimiseks

- `cinema_halls.location_id`
  - kindla kino saalide leidmiseks

- `sessions.movie_id`
  - konkreetse filmi seansside leidmiseks

- `sessions.hall_id`
  - kindlas saalis toimuvate seansside leidmiseks

- `sessions.start_time`
  - seansside kuupäeva ja kellaaja järgi filtreerimiseks ning sorteerimiseks

- `seats.hall_id`
  - kindla saali istekohtade leidmiseks

- `tickets.session_id`
  - konkreetse seansi piletite leidmiseks

- `tickets.user_id`
  - kasutaja piletite ja broneeringute leidmiseks

- `tickets.seat_id`
  - istekoha broneeringute kontrollimiseks

- `reviews.user_id`
  - kasutaja arvustuste leidmiseks

- `reviews.movie_id`
  - konkreetse filmi arvustuste leidmiseks

`users.email` on unikaalne väli. PostgreSQL loob unikaalsuse kontrollimiseks sellele juba indeksi, seega eraldi indeksit ei ole vaja lisada.

## Vahemälu plaan

Praegu ei ole rakenduses vahemälu veel realiseeritud. Tulevikus võiks kasutada järgmist vahemälu plaani.

### Filmide nimekiri

Vahemälu kestus: 5 minutit.

Filmide nimekiri muutub harva, seega võib seda hoida vahemälus pikemalt.

Vahemälu tühistatakse, kui:

- lisatakse uus film
- filmi andmeid muudetakse
- film kustutatakse
- filmi žanre muudetakse

### Filmi detailandmed

Vahemälu kestus: 5 minutit.

Vahemälu tühistatakse, kui:

- filmi andmeid muudetakse
- filmi žanre muudetakse

### Seansid

Vahemälu kestus: 1 minut.

Seansside andmed võivad muutuda sagedamini kui filmi põhiandmed.

Vahemälu tühistatakse, kui:

- lisatakse uus seanss
- seansi aega muudetakse
- seanss kustutatakse
- seansi saali muudetakse

### Istekohtade saadavus

Vahemälu kestus: maksimaalselt 10 sekundit või seda ei salvestata vahemällu.

Istekohtade saadavus võib broneeringute tõttu kiiresti muutuda.

Vahemälu tühistatakse kohe, kui:

- luuakse uus broneering või pilet
- broneering tühistatakse
- istekoha saadavus muutub

### Piletid ja broneeringud

Piletite ja broneeringute puhul ei kasutata pikka vahemälu, sest kasutajale peab kuvama võimalikult värsket infot.

Kui vahemälu kasutatakse, tühistatakse see kohe pärast:

- pileti loomist
- broneeringu loomist
- broneeringu muutmist
- broneeringu tühistamist