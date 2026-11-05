# pin2map – verbindliche Qualitätspolitik

## Geltung
Für jede zukünftige Änderung an pin2map. Keine Entwicklung oder Veröffentlichung ohne nachweisbare Prüfungen.

## ADR-007 – Ersatz und Entfernung
Bei einer Neuentwicklung des Frontends sind die ersetzten HTML-Strukturen, CSS-Regeln, Renderer, Eventhandler und Kompatibilitätsbrücken vollständig zu entfernen. Kein Verstecken alter UI, kein Proxy-Klick, keine MutationObserver-Brücke. Fachlogik und bestehende Funktionen bleiben erhalten. Für jede Änderung wird ein Lösch-/Beibehaltungsinventar mit konkret benannten Altstrukturen geführt. Die vollständige Entfernung muss mit projektspezifischen Sperrtests nachgewiesen werden.

## ADR-008 – Schichtentrennung
Fachlogik (Backend im Browser) darf keine DOM-/HTML-/CSS- oder Leaflet-Abhängigkeiten enthalten. Frontend übernimmt Darstellung und Benutzerinteraktion, nicht Berechnung oder externe Services. Adapter kapseln Leaflet, Netzwerk, Dateisystem und andere technische Integrationen. Keine Mischfunktionen. Schnittstellen müssen explizit sein.

## Freigaberegel
Ein fehlender, nicht ausführbarer oder fehlgeschlagener Pflicht-Test ist kein PASS. Eine erfolgreiche Syntaxprüfung ersetzt keine Browserprüfung. Freigabe nur nach Architektur-, Funktions-, Regressions- und erforderlichen echten Browsertests sowie menschlicher Zustimmung.

## Schutz der Prüfregeln
Änderungen an quality/, tests/ und .github/workflows/ müssen gesondert geprüft und vom Projektinhaber ausdrücklich genehmigt werden. Der Entwickler darf Prüfungen nicht abschwächen, überspringen oder löschen, um eine Freigabe zu erhalten. Für echte Erzwingung sind GitHub-Branchregeln / Rulesets und gegebenenfalls unabhängige Reviews erforderlich.

## Status
IN ARBEIT / NICHT GEPRÜFT / GESPERRT / FREIGEGEBEN. FREIGEGEBEN nur bei vollständig belegtem Gate-Ergebnis.

## Initiale Baseline
Die bestehende produktive index.html ist historischer Code und erfüllt die Zielarchitektur noch nicht nachweislich. Der QS-Aufbau führt zunächst einen Smoke-Test und eine Prüfung des QS-Systems selbst aus. Diese Baseline ist ausdrücklich KEINE Architekturfreigabe und keine Freigabe der Anwendung.
