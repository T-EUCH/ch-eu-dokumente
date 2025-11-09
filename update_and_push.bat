@echo off
setlocal
title Update & Push ch-eu-dokumente

REM 0) Ins Repo-Root wechseln (dieses .bat liegt dort)
cd /d "%~dp0"

echo [1/4] Baue Manifest & Index mit Python...
python --version >nul 2>nul
if errorlevel 1 (
  echo [FEHLER] Python wurde nicht gefunden. Bitte Python installieren oder PATH setzen.
  pause
  exit /b 1
)

python generate_indexes.py
if errorlevel 1 (
  echo [FEHLER] generate_indexes.py ist fehlgeschlagen.
  pause
  exit /b 1
)

echo [2/4] Pruefe, ob git verfuegbar ist...
where git >nul 2>nul
if errorlevel 1 (
  echo [HINWEIS] Git ist nicht im PATH. Ich kann nicht automatisch committen/pushen.
  echo          -> Oeffne GitHub Desktop und mache:
  echo             "Commit to main"  und danach  "Push origin".
  echo          -> Alternativ Git for Windows installieren: https://git-scm.com/download/win
  echo ===========================
  echo Manifest/Index sind gebaut.
  echo Test: https://t-euch.github.io/ch-eu-dokumente/manifest.json
  echo ===========================
  pause
  exit /b 0
)

echo [3/4] Aenderungen fuer Commit vormerken...
git add -A

echo [3.1/4] Commit nur wenn noetig...
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Update indexes and manifest"
) else (
  echo [INFO] Keine Aenderungen – nichts zu committen.
)

echo [4/4] Push nach GitHub...
git push
if errorlevel 1 (
  echo [FEHLER] Push fehlgeschlagen (kein Internet? keine Rechte?).
  pause
  exit /b 1
)

echo.
echo =========================================
echo  Fertig: Manifest/Index aktualisiert.
echo  Startseite:  https://t-euch.github.io/ch-eu-dokumente/
echo  Manifest:    https://t-euch.github.io/ch-eu-dokumente/manifest.json
echo =========================================
pause
endlocal
