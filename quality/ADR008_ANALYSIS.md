# ADR-008 – Ist-Analyse und Zielgrenzen

Stand 2026-11-05. Quelle: `main/index.html` (ca. 8.675 Zeilen).
Alle Zahlen sind zeilenbasierte Suchtreffer, keine geprüften AST-Abhängigkeitszahlen.

## Messwerte
- DOM-API-Muster `document.getElementById/querySelector/createElement/addEventListener`: 529 Trefferzeilen.
- Leaflet-Konstruktor-Muster `L.map/marker/polyline/geoJSON/tileLayer`: 20 Trefferzeilen.
- `fetch(`: 17 Trefferzeilen.
- Funktionsdefinitionen mit Route/route im Namen: 48 Trefferzeilen.
- `quality/domain_modules.json` enthält derzeit `modules: []`. Daher prüft die bestehende ADR-008-Grenzprüfung keine echten Domain-Module.

## Konkrete Verflechtungspunkte
- `ensureMap` (ca. Zeile 2672): `L.map` – Leaflet-Adapter.
- `drawRouteGeometry` (ca. Zeile 4126): Kartenlayer und Geometriedarstellung – Leaflet-Adapter.
- `renderRouteEditor` (ca. Zeile 4229): DOM-Manipulation – Frontend.
- `setRoutePanelHidden` (ca. Zeile 4205): DOM-Manipulation – Frontend.
- `syncRoutePanelToggle` (ca. Zeile 4217): DOM-Manipulation – Frontend.
- `updateRouteModeButtons` (ca. Zeile 4360): DOM-Manipulation – Frontend.
- `fetch` im Routingbereich (ca. Zeilen 4521, 4573, 4601, 4616): Netzwerk-Adapter.
- `routeStartItem`, `routeTargetItem`, `routeWaypoints` (ca. Zeile 4122): gemeinsamer Routingzustand; Eigentümerschaft der Fachschicht ist zu klären.

## Zielmodell (eine auslieferbare HTML-Datei bleibt möglich)
1. **Domain**: reine Eingaben/Ausgaben; Reihenfolge, Wegpunkte, Routevalidierung, Zustandsübergänge, Persistenz-Datenmodell. Keine DOM-, Leaflet-, fetch- oder Browser-APIs.
2. **Frontend**: DOM-Rendering, Eingaben, Schaltflächen, modale Dialoge. Nutzt Domain über definierte Schnittstellen.
3. **Adapter**: Leaflet, Netzwerkanfragen, GPX/Datei-IO und lokale Speicherung. Übersetzen externe Daten für die Domain.
4. **Bootstrap/Composition**: verbindet Module, ohne Fachlogik zu duplizieren.

## QS-Nachweis vor Freigabe
- Tatsächliche Domain-Module in `domain_modules.json` registrieren; leere Liste darf niemals als Architektur-Zertifikat gelten.
- Domänenfunktionen in Isolation testen (ohne `window`, `document`, `L`, `fetch`).
- Frontend-Interaktionen in Chromium testen (Desktop und mobil).
- Netzwerk-/Leaflet-Adapter mit kontrollierten Testdoubles prüfen.
- ADR-007-Löschinventar und End-to-End-Regressionsfälle nachweisen.

**Status:** Analyse, nicht ADR-008-Zertifizierung. Keine Änderung an `main`.
