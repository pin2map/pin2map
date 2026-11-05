# RoutingView – Schnittstellenvertrag (Entwurf)

**Status:** Entwicklungsgerüst, keine Freigabe. Gilt für `src/routing/routing-view.js` auf `dev/adr008-routing-integration`.

## Prinzip

`P2MRoutingView.createRoutingView({ document, mount, onAction, createIcon })` ist eine DOM-Oberflächenkomponente. Sie darf keine Routing-Anbieter anfragen, keine Strecken berechnen, keine GPX-Daten verwalten und keine Karte direkt manipulieren. Das übernimmt der Routing-Controller mit Fachlogik und Adaptern.

### Eingaben

- `document`: DOM-Dokument.
- `mount`: exklusiver Container der RoutingView.
- `onAction(type, payload?)`: Controller-Callback. Aktuell: `mode`, `selectAlternative`, `reverse`, `end`, `close`.
- `createIcon(lucideName, document)`: zentraler, anwendungsweit wiederverwendbarer Lucide-Renderer. Noch nicht implementiert.
- `view.update({ mode, expanded, alternatives, selectedId, summary, legsNode })`: aktuell nur ein **provisorisches** State-Format. `mode` ist `car|bike|walk|transit`; `alternatives` sind `{id,times,duration,transfers}`-Objekte.

### Rückgaben

- `view.getState()`: flache Kopie des aktuellen View-Zustands.
- `view.destroy()`: leert den Mount-Container.

### Integrationsregeln

1. Der Controller ist Quelle der Wahrheit für Modus, aktive Verbindung, Routenberechnung und Etappen.
2. Bei Verbindungsauswahl sendet die View nur `selectAlternative(id)`; Controller aktiviert Route und Etappen, danach aktualisiert er die View.
3. `reverse`, `end` und `close` bleiben getrennte Aktionen mit **bestehender** Semantik.
4. Die bestehenden ALL/FIX/OPT-, Apple-, Datum-/Uhrzeit- und Abfahrt-/Ankunft-Bedienelemente sind noch **nicht** angeschlossen. Die gegenwärtigen Slots sind Platzhalter.
5. Die bestehende Etappenanzeige darf bei der Integration nicht neu gestaltet werden.
6. Lucide wird zentral und versionsgebunden eingebunden. Im Gerüst vorhandene Icon-Text-Fallbacks und Unicode-Haken sind **noch nicht abnahmekonform**.
7. Eine DOM-Neuerzeugung bei `update` ist aktuell nur eine Prototyp-Entscheidung. Vor Integration müssen Fokus, Eingabezustände, Scrollposition, bestehende Event-Handler und Map-Interaktionen erhalten bleiben.
8. Responsive CSS allein beweist nicht, dass iPhone-Dialoggröße und Rechtsversatz dem Bestand entsprechen. Messungen und Screenshotvergleich sind Pflicht.

## Nächste technische Schritte

1. Ist-Zustand des produktiven Dialogs vollständig inventarisieren: Funktionen, DOM, CSS, Eventhandler, Abhängigkeiten.
2. Konkrete Lucide-Symbole anhand der Vorgaben auswählen und zentralen Icon-Renderer aufbauen.
3. Controller-View-Adapter definieren und alle Aktionen über bestehende Logik anbinden.
4. Kontrollslots durch echte Eingabefelder/Buttons ersetzen, ohne Fachlogik zu duplizieren.
5. Visuelle Desktop- und iPhone-Prüfungen gegen S01–S18 sowie Regressionstests.
6. Keine Änderung an `main` ohne ausdrückliche Freigabe.

## Teststatus

Es existieren neun Node-Tests und eine GitHub-Actions-Workflowdatei. **Kein bestandener CI-Lauf wurde hier nachgewiesen**; ein GitHub-Commit-Statusaufruf lieferte keine Statusmeldungen. Daher kein grüner Teststatus behaupten.
