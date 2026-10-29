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

Arvutis peavad olemas olema [Docker Desktop](https://www.docker.com/products/docker-desktop/), [uv](https://docs.astral.sh/uv/) ja [Node.js](https://nodejs.org/).

Kõik käsud käivita projekti põhikaustast (`Kino`).

## Esimene käivitamine

### 1. Tee seadete failid

```bash
echo "POSTGRES_PASSWORD=change_me" > Database/.env
echo "DATABASE_URL=postgresql+psycopg://kino:change_me@localhost:5432/kino" > Backend/.env
```

### 2. Käivita andmebaas

```bash
cd Database
docker compose up -d
cd ..
```

### 3. Käivita backend

Ava uus terminal ja jäta see lahti:

```bash
cd Backend
uv sync
uv run alembic upgrade head
uv run python -m backend.seed
uv run fastapi dev main.py --port 8471
```

Backend töötab aadressil http://127.0.0.1:8471. API dokumentatsioon on aadressil http://127.0.0.1:8471/docs.

### 4. Käivita frontend

Ava teine terminal ja jäta ka see lahti:

```bash
cd Frontend
npm install
npm run dev
```

Ava brauseris http://localhost:5173.

## Järgmised käivitamised

Igaüks oma terminalis:

```bash
cd Database && docker compose up -d
```

```bash
cd Backend && uv run fastapi dev main.py --port 8471
```

```bash
cd Frontend && npm run dev
```

## Andmebaasi nullimine

See kustutab kõik andmed ja loob uued demoandmed:

```bash
cd Database
docker compose down -v
docker compose up -d
cd ../Backend
uv run alembic upgrade head
uv run python -m backend.seed
```

Allikad
FastAPI, SQLModel, SQLAlchemy Automap, Alembic, Django ja Django REST Framework.
