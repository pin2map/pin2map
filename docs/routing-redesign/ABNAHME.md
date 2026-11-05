# Abnahmecheckliste – neuer Routing-Dialog

**Status:** Prüfplan, keine Abnahme. Quelle: `ANFORDERUNGEN.md` und Referenzregister `SCREENSHOTS.md`.

| ID | Prüffall | Soll |
|---|---|---|
| UI-01 | Jede Routing-Art, Auswahl geschlossen | Nur aktiver grauer Routing-Button in Titelzeile |
| UI-02 | Aktiven Routing-Button antippen | Vier Modi sichtbar; aktiver Button blau |
| UI-03 | Anderen Modus wählen | Wechsel sofort; Auswahl zu; neuer Button grau |
| UI-04 | ÖPNV-Eingaben | Abfahrt/Ankunft, Datum, Uhrzeit in genau einer Zeile |
| UI-05 | ÖPNV, zwei Vorschläge | Genau zwei Zeilen; Etappen direkt mit kleinem Abstand darunter |
| UI-06 | ÖPNV, fünf Vorschläge | Fünf nummerierte Zeilen, keine künstliche Leerfläche |
| UI-07 | Aktive Verbindung | Rote Schrift, roter Nummernkreis mit weißer Zahl, roter Haken |
| UI-08 | Anderen Vorschlag antippen | Sofortiger Karten-/Etappenwechsel, keine Bestätigung |
| UI-09 | ÖPNV-Etappen | Darstellung und bestehende Bedienung unverändert |
| UI-10 | ÖPNV-DB-Button | Nicht sichtbar, aber DB-Navigator-Funktion nicht gelöscht |
| UI-11 | Desktop rechts | Umkehren, Beenden (rot), Schließen ×; gleiche rechteckige Größe |
| UI-12 | iPhone rechts | Drei runde Lucide-Icons rechts untereinander, fest beim Scrollen |
| UI-13 | iPhone-Dialog | Bestehende Größe und Rechtsversatz; Zoom-Buttons nicht überdeckt |
| UI-14 | Mobil scrollen | Inhaltsbereich scrollt, Aktionsbuttons bleiben stehen |
| UI-15 | Auto/Fahrrad/Fuß | ALL/FIX/OPT und Apple direkt unter Titel, Funktionen erhalten |
| UI-16 | Auto/Fahrrad/Fuß | Konstante bisherige Dialoghöhe; mehr sichtbare Etappen |
| UI-17 | Wechsel Desktop↔Mobil | Kein Überlauf/Überdecken, alle Bedienelemente bedienbar |
| UI-18 | Fehler/Leerlauf | Keine blockierten Buttons oder kaputten Zustände; konkrete Texte noch offen |
| UI-19 | Projekt speichern/laden | Route, aktive Auswahl und Etappen entsprechend Bestand erhalten |
| UI-20 | GPX und Karteninteraktion | Keine Regressionen der vorhandenen Funktionen |
| UI-21 | Icon-System | Lucide zentral und versioniert; keine Emoji-Bediensymbole im neuen Dialog |
| UI-22 | Schließen/Beenden | Vorherige Semantik exakt erhalten |
| UI-23 | Tastatur/Touch | Bedienbar, Fokus sichtbar, zugängliche Namen der Symbolbuttons |
| UI-24 | Browser-Konsole | Keine neuen Fehler |

## Prüfmatrix

- Desktop: Chromium und mindestens ein zweiter Browser, mit tatsächlichem Leaflet und vollständiger `index.html`.
- Mobil: iPhone-Viewport-Emulation **und** abschließende Prüfung auf einem realen iPhone.
- Routing-Arten: Auto, Fahrrad, Fuß, ÖPNV.
- ÖPNV-Verbindungen: 0, 1, 2, 5 und >5 Vorschläge (Anzahl >5 und Nullzustand noch zu spezifizieren).
- Referenz-Screenshots: visueller Vergleich mit S01–S18, unter Berücksichtigung der verbindlichen Änderungen.
- Kein Test gilt als bestanden, bevor er tatsächlich ausgeführt und protokolliert ist.

## Freigabegates

1. Alle verbindlichen Anforderungen erfüllt, offene Fragen entschieden.
2. Keine ersetzte alte UI-Struktur im DOM/CSS/JS zurückgelassen (ADR-007).
3. RoutingView, Controller und Fachlogik mit klaren Schnittstellen (ADR-008).
4. Reale Browser- und Mobiltests, Regressionen und manuelle Sichtprüfung bestanden.
5. Ausdrückliche Freigabe des Projektinhabers vor `main`.
