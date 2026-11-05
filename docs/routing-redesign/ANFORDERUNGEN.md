# Routing-Dialog: verbindliche Anforderungen (Übertragung 05.11.2026)

**Status:** Anforderungen aus pin2map8 im Chat pin2map9 übertragen; **noch nicht implementiert / nicht abgenommen**. Keine stillschweigende Erweiterung der Vorgaben. Quelle: direkte Nutzeranweisungen und 15 Referenzbilder vom 05.11.2026. Bilder sind im lokalen Übergabepaket nummeriert (siehe `SCREENSHOTS.md`); die Bilddateien müssen noch binär in dieses Repository übernommen werden.

## Architekturentscheidungen

- **Fachlogik unabhängig von Darstellungs-/Oberflächenlogik** (im Projekt als „Backend“/„Frontend“ bezeichnet, kein separater Server erforderlich).
- Ziel: RoutingDomain, RoutingController, RoutingView, getrennte Karten-, Netzwerk- und Projektadapter. Der bestehende ADR-008-Entwicklungsbranch enthält erst **Teilbereiche** dieser Trennung; kein fertiges Backend/Frontend behaupten.
- **Lucide** (https://lucide.dev/icons/) als zentrale, versionsgebundene Symbolbibliothek für die **gesamte** Anwendung; Migration beginnt beim Routing-Dialog. Vorhandene Emoji-Bediensymbole im Routing-Dialog ersetzen, andere Funktionen vorerst unverändert. Konkrete Icon-Auswahl noch offen.

## R01 – Routing-Art-Auswahl in der Titelzeile

- In der Titelzeile links statt statischem Emoji ein bedienbarer Routing-Art-Button (Auto/Fahrrad/Fuß/ÖPNV), rechts die zugehörigen Routeninformationen.
- Geschlossen: **nur** aktuelle Routing-Art als **grauer** Button sichtbar.
- Klick auf aktuellen Button: **blau**, alle vier Routing-Arten sichtbar.
- Klick auf andere Art: Wechsel der Routing-Art, Auswahl klappt zu, nur der neu gewählte **graue** Button sichtbar. Die anderen bleiben verborgen, bis erneut geöffnet.
- Die bisherige gesonderte Gruppe „Routing für“ mit vier permanent sichtbaren Buttons entfällt. Deren Platz wird frei.
- Die neue Titelzeile zeigt je nach Routing-Art andere Informationen; bei ÖPNV Referenz Start/Ziel, bei Auto Distanz/Dauer. Exakte Texte/Datenlogik gesondert prüfen.
- Beim Aufklappen auf iPhone keine Kollision mit Informationen/Aktionsbuttons; Vorschlag: temporäre Überlagerung ohne Höhenänderung (noch nicht bestätigt).

## R02 – ÖPNV: eine Eingabezeile

- Direkt unter Titelzeile genau **drei** Felder in **einer** Zeile: (1) Abfahrt/Ankunft, (2) Datum, (3) Uhrzeit.
- Vorher fünf Felder in zwei Zeilen plus DB-Button: Bahn-/Bus-Präferenzfeld entfällt aus Oberfläche; fachliche Entbehrlichkeit noch prüfen.
- Verlängerung der Umsteigezeit entfällt **vorläufig** aus Oberfläche; fachliche Notwendigkeit offen. Falls weiterhin erforderlich: späteres Konfigurationsmenü.
- Runder **DB-Button entfällt aus dem Dialog**, aber die Funktion zur Übergabe an DB Navigator **muss erhalten bleiben**; neuer Ort später festlegen.

## R03 – ÖPNV: Verbindungsvorschläge

- Direkt unter Eingabezeile eine **nummerierte Liste** verfügbarer Verbindungen.
- Jede Zeile: Abfahrt–Ankunft, Gesamtdauer, Umstiege.
- Aktive Verbindung: **rote Schrift**, **roter Nummernkreis mit weißer Ziffer**, **roter Haken links**.
- Klick/Tipp auf Vorschlag: **sofortige Aktivierung** der Verbindung einschließlich zugehöriger ÖPNV-Route auf Karte; kein zusätzlicher Bestätigungsbutton.
- Liste hat **dynamische Höhe**: z.B. bei zwei Ergebnissen nur zwei Zeilen, keine Reservierung für fünf.
- Nach letztem Vorschlag folgt mit kleinem, konstantem Abstand die **bestehende Etappenanzeige**, deren Darstellung und Funktion **unverändert** bleiben müssen.
- Verhalten bei null Ergebnissen, Fehlern und Laden noch spezifizieren.

## R04 – Rechte Aktionsbuttons, Desktop

- Gemeinsame rechte Spalte für **alle** Routing-Arten.
- Von oben nach unten: **Umkehren** (bisher A→B), **Beenden** (rot), **Schließen ×** (bisher runder X-Button).
- **Überholt durch Nutzerentscheidung vom 05.11.2026:** Auch auf Desktop sind alle drei Buttons **rund und ausschließlich mit Symbol**. Beenden bleibt rot mit weißem Symbol. Desktop und iPhone sollen grundsätzlich ähnlich aussehen.
- Positionierung wie ÖPNV-Gesamtansicht Referenz.
- **Bestehende Semantik** von Schließen vs. Beenden erhalten; exakt im Bestand überprüfen.

## R05 – iPhone / Mobil

- **Bisherige Breite, Höhe und leicht nach rechts versetzte Position** des Routing-Dialogs bleiben erhalten, damit Zoom-Buttons frei bleiben.
- Rechte Aktionsbuttons **fest**, **rechts untereinander**, **rund und nur mit Symbol**: oben Umkehren ↩ (hell), mittig Beenden roter Kreis mit weißem X, unten Schließen ✔ (hell). Diese Symbolformen sind Referenzabsicht; konkrete Lucide-Icons noch festlegen.
- Aktionsbuttons dürfen beim Scrollen **nicht mitscrollen**.
- Verbindungsliste/Etappen in scrollbarem Inhaltsbereich; Dialog/Bedienbuttons bleiben an Position.
- Desktop- und iPhone-Varianten sind in der grundlegenden Darstellung **ähnlich**; insbesondere sind die drei Aktionsbuttons auf beiden Geräten rund und ausschließlich mit Symbolen. Keine ungetestete Änderung von Größe/Position oder Überdeckung.

## R06 – Auto/Fahrrad/Fuß

- Gleiche neue Titelzeile und Routing-Art-Auswahl wie ÖPNV.
- Direkt darunter der **bestehende** Multi-Pin-Routing-Block **ALL / FIX / OPT** und **Apple**-Button; Größen/Funktionen zunächst beibehalten, nur nach oben versetzen.
- Dadurch mehr Platz für darunterliegende Etappen; mehrere Etappen gleichzeitig sichtbar, soweit Platz.
- **Dialoghöhe bleibt konstant wie bisher** (Auto/Fahrrad/Fuß).
- Rechte Aktionsbuttons wie R04/R05.
- Etappenbereich scrollt; Titelzeile, Optionen und rechte Buttons bleiben stehen (Vorschlag des Assistenten, noch gesondert bestätigen).
- Bestehende Routing-Funktionalität nicht verändern.

## R07 – Abnahme und Qualität

- Alle Screenshots mit eindeutigen IDs als Referenzen erhalten und den Anforderungen zuordnen.
- Für jede Routing-Art Desktop und iPhone prüfen: geschlossene/geöffnete Auswahl, Moduswechsel, Eingaben, Verbindungswahl, Etappen, Scrollen, Aktionsbuttons, Projekt-/GPX-Rückwärtsverhalten, keine Überlagerung von Zoom-Buttons.
- Etappenanzeige bei ÖPNV **nicht neu gestalten**.
- Tests mit echtem Leaflet und vollständiger Anwendung; isolierte Node-/Chromium-Smoke-Tests sind **keine** vollständige Freigabe.
- Keine Produktionsänderung ohne ausdrückliche Freigabe; bestehende `main`- und `qs-setup`-Branches unverändert.

## Noch offen (nicht eigenmächtig entscheiden)

1. Konkrete Lucide-Icons für Auto, Fahrrad, Fuß, ÖPNV, Umkehren, Beenden, Schließen und Apple-Integration.
2. Was passiert mit Bahn-/Bus-Präferenz auf Fachlogik-/API-Ebene?
3. Wird die Verlängerung der Umsteigezeit benötigt? Falls ja, Gestaltung späteres Konfigurationsmenü.
4. Neuer Zugang zur **erhaltenen** DB-Navigator-Funktion.
5. Fehler-/Lade-/Nullergebnis-Zustände der ÖPNV-Verbindungsauswahl.
6. Exakte Titelinhalte je Routing-Art und Verhalten bei fehlenden Routen.
7. Mobile Überlagerung bei geöffneter Routing-Art-Auswahl und konkrete Scrollgrenzen.
8. Bestandssemantik von „Schließen“ vs. „Beenden“ vor Implementierung verifizieren.

## Historie und Verbindlichkeit

Die Punkte R01–R06 beruhen auf Nutzeranweisungen und Screenshots. Als „Vorschlag“ oder „offen“ bezeichnete Punkte sind **nicht** automatisch freigegeben. Diese Datei ist eine konsolidierte Spezifikation; die Bilddateien und das Chat-Original bleiben eigenständige Belege.

## Nachtrag – Vereinheitlichung Desktop/iPhone (05.11.2026)

**Neueste verbindliche Entscheidung hat Vorrang vor älteren Screenshots und R04:** Die rechte Aktionsspalte besteht **auf Desktop und iPhone gleichermaßen aus drei runden, ausschließlich ikonbasierten Buttons** in der Reihenfolge Umkehren, Beenden, Schließen. Keine rechteckigen Desktop-Textbuttons. Die bisherigen Lucide-/Farbvorgaben gelten weiterhin. Sonstige Unterschiede der verfügbaren Fläche und Abmessungen bleiben responsiv.

## Nachtrag – kompakte, geräteübergreifend ähnliche Dialogbreite (05.11.2026)

**Verbindliche Nutzerentscheidung:** Der Routing-Dialog soll auf Desktop und iPhone annähernd gleich schmal/breit erscheinen; auf großen Bildschirmen darf er nicht zu einem wesentlich breiteren Dialog anwachsen. Maßgeblicher Ausgangspunkt ist die bestehende iPhone-Dialogbreite. Die bestehende iPhone-Position (leicht nach rechts versetzt, Zoom-Buttons frei) und Höhe bleiben erhalten. Auf beiden Geräten dieselbe grundlegende Elementanordnung und drei runde Icon-only-Aktionsbuttons rechts. **Keinen frei erfundenen festen Pixelwert festlegen**: zunächst reale Bestandsmaße aus CSS und Referenzbildern bestimmen, dann geräteübergreifende Breitenbegrenzung festlegen und im Browser messen. Bei sehr kleinen Viewports darf die Oberfläche nicht abgeschnitten werden.
