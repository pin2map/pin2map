# ADR-008 – Konkrete Routing-Grenzanalyse (Bestandsaufnahme)

Stand: 2026-11-05. Grundlage: `main/index.html` v10.12.71; Zeilen sind ungefähre Fundstellen. Keine Änderung der Produktivdatei.

## Belegte Kandidaten für fachliche Funktionen

| Funktion | Fundstelle | Ist-Abhängigkeit | Vorläufige Einordnung |
|---|---:|---|---|
| `formatRouteDuration(sec)` | ~4348 | Zahlen und Stringformatierung | Domain-Kandidat; isoliert testbar |
| `routeLegColor(i,total)` | ~4125 | Farbpaletten/Präsentation | Frontend/Design, **nicht** Domain |
| `decodeValhallaPolyline(str)` | ~4363 | Zeichenkette → Koordinaten | Netzwerk-/Geometrie-Adapter-Kandidat |
| `routeAirDistance(a,b)` | ~4559 | `a._pinLayer.getLatLng()`, `b._pinLayer.getLatLng()` | Vermischung: Fachberechnung greift direkt auf Leaflet-Layer zu |
| `valhallaTripResult(d,routeItems)` | ~4560 | externe Valhalla-Struktur und Decoder | Adapter-Kandidat; Transformation und Validierung trennen |
| `optimizeRouteOrder()` | ~4565 | globaler Routingzustand, Leaflet-Koordinaten, DOM-/Button-Updates und `fetch` | **ADR-008-Verflechtung**, nicht als reine Domain klassifizierbar |
| `parse(s)` | ~2649 | Textparser und Hilfsfunktion `color()` | Domain-Kandidat nach Prüfung/Entkopplung der Hilfsfunktion |

## Konkrete Grenze, die heute nicht eingehalten ist

`routeAirDistance(a,b)` entnimmt Koordinaten aus Leaflet-Pinlayern. Eine reine Domain-Signatur sollte stattdessen primitive Eingaben wie `{lat,lng}` verwenden. Die Umwandlung von Leaflet-Layern zu Koordinaten gehört in den Adapter.

`optimizeRouteOrder()` verbindet in einer Funktion (a) Wegpunkt-Reihenfolge, (b) den Zugriff auf `_pinLayer`, (c) Netzwerkaufrufe zur Valhalla-Optimierung, (d) globalen Zustand und (e) UI-Aktualisierungen. Eine ADR-008-konforme Aufteilung braucht getrennte pure Optimierungs-/Validierungsfunktionen, Routingservice-Adapter und UI-Controller.

`calculateRoute()` (ca. Zeile 4590) kombiniert Netzwerkaufrufe, Ergebnisvalidierung, UI-Status und Leaflet-Zeichnung. Die erfolgreichen Browsertests sichern beobachtetes Verhalten ab, ersetzen aber keine Schichtentrennung.

## Kontrolllücken

- `quality/domain_modules.json` enthält `{"modules":[]}`. Der bestehende Scanner überprüft **null** Produktions-Domainmodule. Ein grüner CI-Status ist daher kein ADR-008-Nachweis.
- `quality/adr007_components.json` ist `[]`; es existiert noch kein geprüftes Altkomponenten-Löschinventar.
- Der vorhandene Regex-Scanner ist nur eine ergänzende Schranke, keine vollständige Abhängigkeitsanalyse. Auch seine derzeitige Verbotsliste deckt nicht sämtliche Browser-/Netzwerkzugriffe ab.
- Der Branch `qs-setup` ist QS-Vorbereitung. `main` darf ohne explizite Eigentümerfreigabe nicht geändert werden.

## Nächste Umsetzungsetappe (erfordert separate Produktionsfreigabe)

1. Ein klar abgegrenztes Routing-Domainmodul mit expliziten Koordinaten-Datentypen und isolierten Unit-Tests entwerfen.
2. Leaflet- und Netzwerkadapter definieren, bestehende Aufrufstellen mit Vorher/Nachher-Inventar dokumentieren.
3. Die Domainmodule tatsächlich in `quality/domain_modules.json` registrieren; erst danach sind die Grenztests für diese Module aussagekräftig.
4. Browser-Regressionen (Erfolg, 503, NoRoute, ungültiges JSON, Recovery, verspätete Antwort) als unverzichtbares Gate beibehalten.
5. Für einen UI-Ersatz nach ADR-007 zunächst Alt-HTML, CSS, JS-Handler, Renderer und Brücken explizit inventarisieren und ihre Entfernung nachweisen.

**Ergebnis:** belegte Architekturverflechtung und dokumentierte Migrationskandidaten; **keine** ADR-007-/ADR-008-Zertifizierung.
