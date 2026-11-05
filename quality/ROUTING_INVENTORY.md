# Routing-Dialog: Bestandsaufnahme aus main/index.html

Stand: 2026-11-05. Quelle: GitHub-Repository pin2map/pin2map, Branch main, index.html.
Dies ist ein **Ist-Inventar** und KEINE Liste bereits zu löschender Strukturen.

## Aktuelle UI-Strukturen (HTML ca. Zeilen 2495–2505)
- `#routeInfo`: Container des Routing-Dialogs.
- `#routeSummary`: Routen-Zusammenfassung.
- `#routePanelHide`: Dialog ausblenden.
- `[data-route-mode]`: Auto, Fahrrad, Fußweg und ÖPNV.
- `#routeClear`: Route beenden.
- `#routeVisiblePins`: sichtbare Pins als Zwischenziele hinzufügen.
- `#routeOrderToggle`, `#routeOrderOptimal`: Reihenfolge fest/optimiert.
- `#routeReverse`: Reihenfolge umkehren.
- `#routeDetailsToggle`, `#routeLegs`: Teilstrecken.
- `#transitTimeControls`, `#transitTimeMode`, `#transitDateTime`: ÖPNV-Einstellungen.
- `#p2mTransitDateTimePair`, `#p2mTransitDate`, `#p2mTransitClock`: Datums-/Zeiteingabe.
- `#p2mDbNavigator`, `#openAppleMaps`: externe Navigation.
- `#routeAvoid`, `#routeEndpoints`, `#routeEdit`, `#routeHint`: Routing-Teilbereiche.

## Vorhandene CSS- und JS-Verknüpfungen
- `#routePanelToggle`: CSS ab ca. Zeile 160, weitere Regeln u.a. 443, 718, 1446.
- `setRoutePanelHidden`: JS ca. Zeile 4205.
- `syncRoutePanelToggle`: JS ca. Zeile 4217.
- `renderRouteEditor`: JS ca. Zeile 4229.
- `updateRouteModeButtons`: JS ca. Zeile 4360.
- `routePanelToggle.onclick`: JS ca. Zeile 4637.

## Bewertung
Der Dialog hat zahlreiche gekoppelte HTML-, CSS- und JS-Elemente.
Eine zukünftige Ersetzung nach ADR-007 muss für **jedes betroffene Element**
festlegen: entfernen, ersetzen oder begründet behalten. Ein globales
Verbot dieser Bezeichner wäre jetzt falsch: Sie gehören zur aktuellen
Produktionsversion. Deshalb bleibt `adr007_components.json` zunächst leer.

## Nächster Nachweis
1. Exakte Grenzen der zu ersetzenden Komponente schriftlich festlegen.
2. Alte Bezeichner und alle Verwendungsstellen vollständig erfassen.
3. Neue DOM-/Event-Struktur implementieren und alte vollständig entfernen.
4. Die *tatsächlich entfernten* Tokens im ADR-007-Manifest registrieren.
5. Browser-Interaktionen und Fachlogik-Regressionsfälle nachweisen.

Ohne diese Schritte keine ADR-007-Zertifizierung.
