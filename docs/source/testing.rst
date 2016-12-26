Konventionen
------------

- Unittests (unittest)
  Testen einzelner Funktionen

- Funktionstests (webdriver)
  Testen mehrerer Funktionen im Zusammenspiel

- Integratonstests (selenium)
  Usecases mit phantomjs durchgespielt

- Ordnerstruktur:
  - tests/unit/models
     - dateiname_des_model.py (z.B. "web_user.py")
  - tests/unit/views
      - dateiname_des_view.py (z.B. "page.py")
  - tests/functional/
      - konzept.py (z.B. "login.py")
  - tests/integration
      - usecase.py (z.B. "musician.py")


ado-do Taks
-----------

Die Tests werden über einen ado-do Task ausgeführt.

Man erstellt separat ein Datenbank-Template (ado-do create-test-db),
dessen Kopie für die Tests dann beim Ausführen (ado-do run-tests)
verwendet wird, um nicht jedes mal die DB neu initialisieren und die
scenario_master_data.txt ausführen zu müssen.

Man kann sämtliche Parameter für nosetests an den ado-do Task
weiterreichen, sowie auch wie gewohnt den Pfad (auch mit Klasse und
Methode). Falls kein Pfad angegeben wird, werden alle Tests inklusive
aller Plugins ausgeführt. Beim Schreiben der Tests sollte man zuerst in
den Container wechseln, damit die Container nicht immer neu erstellt und
die Pakete installiert werden müssen. Die Tests von außen anzustoßen
macht hauptsächlich nur für Continous Integration Sinn.

Zu Bedienung siehe hier:

  https://github.com/C3S/c3s.ado/tree/develop#testing

Details in ado-do.py:

  create-test-db
  https://github.com/C3S/c3s.ado/blob/develop/ado/ado-do#L185

  run-tests
  https://github.com/C3S/c3s.ado/blob/develop/ado/ado-do#L244


Pfade
-----

- Screenshots werden in ado/tmp/screenshots gelöscht & gespeichert
  (der Pfad ist in der Testframework Konfiguration definiert)
- Tryton-Dateien (Upload) werden in ado/tmp/files gelöscht & gespeichert
  (der Pfad ist in ado-do definiert)


Konfiguration
-------------

Konfiguration des Testframeworks in (portal)/tests/config.py


https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/config.py

Die .ini des Pyramid-Servers wird (1) als settings "environment" in der
Testframework Konfiguration definiert (derzeit 'testing'), und kann bei
Bedarf (2) für alle Tests dort überschrieben werden, sowie (3) in jeder
Klasse über die Klassenmethode 'settings'.

  (1) environment

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/config.py#L11

  (2) settings: {}

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/config.py#L13

  (3) settings() return {}

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/base.py#L88


Server/Client
-------------

Die Erstellung der Server/Client Objekte, mit denen getestet wird, läuft
zentral in einer Klasse Net ab, die sowohl für webdriver
(wrapper=TestApp) als auch selenium (wrapper=StopableWSGIServer)
verwendet werden kann. Server ist die App (TestApp/StopableWSGIServer),
Client ein PhantomJs. Mit dem zentralen Zusammenbauen des Servers werden
die Tests auch weitaus übersichtlicher.

  Net

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/base.py#L23


Basisklassen
------------

Basisklassen für die Tests in (portal)/tests/base.py:

  Unittests

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/base.py#L112

  Funktionstests

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/base.py#L123

  Integratonstests

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/base.py#L144

Mit diesen stehen die benötigten Server/Client Objekte und ein paar
weiter Hilfsfunktionen zu Verfügung. Außerdem wird die Testbeschreibung
bei der Konsolenausgabe automatisch mit Plugin, Testtyp, Klasse prefixt.

Server/Client leben derzeit eine Klasse lang. Mit self.session() kann
zwischen oder innerhalb der Funktionen eine neue Session gestartet werden.

Für Tests mit notwendiger Reihenfolge (wahrscheinlich nur bei
Integrationstests) müssen die Funktionsnamen lexikographisch sortiert
werden können (test_001_X, test_002_Y, ...)


Pageobjects
-----------

Um bei Integrationstests den Testcode sauber zu halten, bietet sich das
'Page Object Pattern' an, bei dem man für die logischen Objekte der
Webseite eine API bastelt, welche sich dann unter der Haube um das
Herauspicken der jeweiligen Interaktionselemente kümmert.

 siehe z.B. http://martinfowler.com/bliki/PageObject.html

Da wir über Colander/Deform schon eine wohldefinierte, maschinenlesbare
Struktur besitzen, aus der der HTML-Code erst generiert wird, liegt es
nahe, die API automatisch bauen zu lassen. Ich habe das für ein paar
Deform Widgets umgesetzt.

Die Basisklasse für ein Element, welche die Grundlegende API definiert:

  base.py

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/integration/pageobjects/base.py

Einige Elemente für Deform Widgets, die anhand eines locators (meist id,
manchmal name HTML-Attribut) das jeweilige Element aus dem HTML-Code
extrahieren können:

  elements.py

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/integration/pageobjects/elements.py

Und hier das Object, welches eine Deform Form automatisch parsen kann:

  objects.py

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/integration/pageobjects/objects.py#L21

Dafür wird zum einen die Form benötigt, welche bei unseren Formularen
immer am Ende der Datei über eine Funktion generiert wird, sowie leider
(noch) die id des Formulars, welche dem Klassennamen des FormControlles
entspricht (falls nicht manuell definiert).

Man holt sich also in der Testklasse das DeformFormObject, füttert es
mit dem zu testenden Formular (+id) und bekommt automatisch eine
übersichtliche API, um das Formular testen zu können.
Bei Änderungen der Struktur des Formulars kann man den Test ohne
Umschweife direkt entsprechend anpassen. Bei Änderungen von ids muss man
die Tests nicht anpassen.


Beispiele
---------


  Unittest (portal)/tests/unit/models/base.py:

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/unit/models/base.py#L10


  Funktionstest (portal)/tests/functional/login.py:

https://github.com/C3S/collecting_society.portal/blob/develop/collecting_society_portal/tests/functional/login.py#L7


  Integrationstest (imp)/tests/integration/web_user.py:

https://github.com/C3S/collecting_society.portal.imp/blob/develop/collecting_society_portal_imp/tests/integration/web_user.py#L15

  PageObject (imp)/tests/integration/web_user.py:

https://github.com/C3S/collecting_society.portal.imp/blob/develop/collecting_society_portal_imp/tests/integration/web_user.py#L24



Offene Punkte
-------------

- Derzeit wird postgres als Test Datenbank verwendet. Ich hatte
versucht, sqlite zu benutzen, im Code ist es implementiert. Leider ist
das derzeit noch weitaus langsamer. Womöglich hängt das mit dem
zugewiesenen mem des containers zusammen, anders kann ich es mir nicht
erklären. Außerdem scheinen manche wichtige Funktionen über sqlite nicht
zu funktionieren - das müsste man sich irgendwann nochmal anschauen.
Optimal wäre es, wenn man die sqlite im RAM laufen könnte, allerdings
wüsste ich nicht, wie man den Speicher über verschiedene subprocess
hinweg behalten könnte.

- Es ist noch unklar, wo welche Tests hinsollen. Funktions- und
Integrationstests sind für Portal nicht ohne weiteres umsetzbar, da im
Standardzustand keine Webseite angezeigt wird. Vielleicht könnte man das
mit DummyTemplates lösen, was auch dem Gedanken entgegenkommt,
Funktionen/Konzepte unabhägig voneinander zu testen.

- Die scenario_master_data.txt sollte bei Gelegenheit aufgeteilt werden
in Minimalsetup (Production/Autotests) und Testsetup (für manuelle Tests),

- Da das starten des Servers (App) Zeit braucht, könnte man auch
versuchen, für einen Testlauf zwei Server zu starten
(TestApp/StopableWSGIServer) und nur in den Tests einen neuen zu
starten, falls nötig.

- Man könnte die testing.ini kicken, wenn man in der pyramid __main__
die Tdb Daten über os.environ holt. Der einzige Unterschied derzeit zu
production ist der Name der trytond.conf. Da die settings für alle Tests
in der Testframework Konfiguration überschrieben werden können, hat die
eigene ini keinen Sinn.

- Die restlichen Deform Widgets müssten als Elemente umgesetzt werden

- Die id eines Formulars sollte zum parsen maschinenlesbar werden. Das
ist nicht ganz trivial, zumal die id manuell überschrieben werden kann.
