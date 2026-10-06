Kinoprojekti backend
Backendi teeme Pythonis ja andmebaasiks kasutame PostgreSQL-i. Python sai valitud sellepärast, et kood on üsna lihtsalt loetav ja API tegemiseks on olemas head tööriistad. Teeme projekti kahekesi, nii et tahame jõuda ka rakenduse valmis, mitte kulutada enamikku aega raamistiku õppimisele.
Võrdlesime kolme varianti. Meie jaoks loeb eriti see, kuidas nendega valmis SQL-tabeleid kasutada, sest andmebaasi skeemi teeme enne backendit.
FastAPI ja SQLModel
Selles variandis teeb FastAPI API osa ja SQLModel seob Pythoni klassid andmebaasi tabelitega. Pydantic v2 kontrollib päringuga saadetud andmeid ning Alembicuga muudame hiljem tabelite struktuuri. PostgreSQL on toetatud.
Meie kinoprojekti jaoks on hea see, et näiteks filmi lisamine ja seansside otsimine ei vaja väga palju koodi. FastAPI teeb ka API dokumentatsiooni, kus saab päringuid proovida. See aitab enne frontendiga ühendamist näha, kas backend töötab. FastAPI ja SQLModeli juhendites on nende koos kasutamise näited, nii et alustamiseks on materjal olemas.
Miinus on see, et SQLModel ei tee meie valmis andmebaasist ise mudeliklasse. Need peame tabelite järgi kirjutama ja kontrollima, et väljad ning seosed klapiksid. Ka Alembicu pakutud migratsioonid tuleb üle vaadata. Keerulisemate päringute korral võib vaja minna SQLAlchemy juhendeid, sest SQLModel kasutab seda enda all.
FastAPI ja SQLAlchemy
Siin kasutaksime SQLModeli asemel otse SQLAlchemyt. FastAPI, Pydantic ja Alembic jääksid samaks. Ka see variant toetab PostgreSQL-i.
SQLAlchemy eelis on meie puhul olemasoleva andmebaasi struktuuri lugemine ehk reflection. Automap saab selle põhjal tabelid ORM-iga siduda. Kuna kirjutame SQL-i enne valmis, oleks sellest kasu. Samuti on SQLAlchemy dokumentatsioonis palju võimalusi seotud andmete päringuteks, mida võib vaja minna seansside ja broneeringute juures.
Samas tuleks API andmemudelid eraldi kirjutada ja osa välju korduks eri klassides. Õppida oleks rohkem, sest tuleb aru saada sessioonidest ja seoste kasutamisest. Meie projekti tavalisemate lisamise ning otsimise funktsioonide jaoks tundub SQLModel lihtsam. Struktuurimuudatusteks kasutaksime siin samuti Alembicut.
Django
Kolmas variant oleks Django koos selle ORM-i ja Django REST Frameworkiga, millega saab API teha. PostgreSQL on toetatud ning migratsioonid on Djangos endas olemas.
Django juures oleks meile kasulik valmis haldusliides. Sellega saaks filme ja seansse hallata, ilma et peaksime kohe kõik haldusvaated ise tegema. Olemasolevatest tabelitest saab käsuga inspectdb mudelite algversiooni luua. Djangol on ka palju juhendeid ja suur kogukond.
Meie jaoks oleks miinus see, et peaksime õppima nii Django ülesehitust kui ka REST Frameworki. Valmis SQL-tabelite puhul tuleb genereeritud mudelid üle kontrollida ja seadistada, kas Django hakkab nende struktuuri haldama. Väikese, eraldi frontendiga projekti jaoks tundub see praegu rohkem tööd, kui meil vaja on.
Mida kasutame
Jääme FastAPI ja SQLModeli juurde. Lisaks kasutame Pydantic v2-te, Alembicut ning PostgreSQL-i. See tundub meie projekti jaoks piisav ja mudelite kirjutamine on lihtsam kui otse SQLAlchemyga.
Kirjutame mudelid valmis SQL-skeemi järgi ja paneme Alembicus paika sellele vastava algversiooni. Edasised tabelimuudatused teeme migratsioonidega. Broneerimisel peame lisaks API kontrollidele kasutama andmebaasi piiranguid ja tehinguid, et sama seansi sama kohta ei saaks kaks inimest korraga broneerida.
Ülesandes on kirjas MySQL/MariaDB. Kui see on kohustuslik, tuleb meie PostgreSQL-i valik õpetajaga kokku leppida.
Allikad: FastAPI, SQLModel, SQLAlchemy Automap, Alembic, Django ja Django REST Framework.