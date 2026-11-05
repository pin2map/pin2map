# Routing-Integration – Ist-Befund und verbindliche nächste Schritte

Stand: 05.11.2026. **Keine fertige Integration; keine Freigabe.**

## Tatsächlich am Entwicklungsstand geprüft

Quelle: `index.html` im Zweig `dev/adr008-routing-integration` (GitHub-Blob `8d904c3ceb841bd2ef4c0049216e7b91c638f21e`), Quelltextsuche.

- Der bestehende Routingdialog liegt im HTML bei `#routeInfo` und enthält `.route-main`, `#routeSummary`, `#routePanelHide`.
- Die bestehende Aktionsleiste enthält `#routeReverse`; weitere Steuerungen liegen in `.route-toolbar-row`, `.route-toolbar-secondary`.
- Für ÖPNV existieren `#transitTimeControls`, `#transitTimeMode` und `#p2mTransitDateTimePair`.
- Für Multi-Pin-Routing existieren `#routeOrder`, `#routeOrderToggle` sowie ein ALL-Button im HTML.
- Die Apple-Karten-Übergabe hängt an `#openAppleMaps`.
- Der Dialog ist mit `#routePanelToggle` und `.route-panel-hidden` an die bestehende Kartenoberfläche gekoppelt.
- `renderRouteEditor()` und `updateRouteLegColorButton()` sind bestehende JavaScript-Funktionen.
- Das HTML enthält zahlreiche historische CSS-Überschreibungen, darunter `!important`-Regeln für Routing. Die neue Oberfläche darf nicht nur als zusätzliche CSS-Schicht darübergelegt werden.

## Zu integrierender Stand

Die zuletzt vom Nutzer akzeptierte Richtung ist Vorschau **V5**:
1. Desktop und iPhone ähnlich kompakt; rechte Aktionsspalte auf beiden Geräten mit drei runden Symbolbuttons.
2. Die vier Modusbuttons **überdecken** beim Öffnen den vorhandenen Kopftext; sie verschieben ihn nicht.
3. ÖPNV-Alternativen genau **zwei Zeilen**: Zeile 1 „Von–bis“, Zeile 2 „Dauer · Anzahl Umstiege“.
4. Keine horizontalen Scrollbalken; aktive Alternative nur rot, **ohne Haken**.
5. Bestehende Etappen und Fachfunktionen unverändert erhalten.

## Integrationsstrategie

1. Vollständige Abhängigkeitsinventur von `#routeInfo`, sämtlichen Buttons, Zustandsvariablen und Listenern erstellen. Kein altes HTML entfernen, solange es noch von Fachlogik referenziert wird.
2. Neue RoutingView als **separaten DOM-Baum** in den bestehenden Dialog einhängen; einen Controller-Adapter verwenden. Kein bloßes Nachstylen des Alt-Dialogs.
3. Eingabefelder und ALL/FIX/OPT/Apple an die vorhandenen Aktionen anschließen. Transit-Alternativen müssen echte Karte und Etappen umschalten.
4. Zentrale, versionsgebundene Lucide-Icons für Routing bereitstellen.
5. Desktop/iPhone-Messungen gegen Screenshots, alle Anforderungen und mehrfache Funktionstests ausführen.
6. Erst nach bestandenen Prüfungen eine vollständig testbare HTML-Version bereitstellen; **`main` nicht verändern**.

## Teststatus

Derzeit nur Prototyp und isolierte Tests vorhanden. Die neue RoutingView ist **nicht** in die produktive Anwendung integriert. Weder die vollständige Funktion noch eine fehlerfreie Browserprüfung der Integration sind nachgewiesen.
