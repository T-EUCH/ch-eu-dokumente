@echo off
setlocal
REM Ein-Klick: Manifest + Indizes neu bauen, committen, pushen

REM Ins Repo-Root wechseln (dieses .bat liegt dort)
cd /d "%~dp0"

REM 1) Indizes/Manifest erzeugen
python generate_indexes.py
if errorlevel 1 (
  echo Fehler beim Erzeugen der Indizes.
  pause
  exit /b 1
)

REM 2) Git-Status prüfen und ggf. committen
git add -A
REM Wenn es nichts zu committen gibt, bricht git commit mit Errorlevel 1 ab – abfangen:
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Update indexes and manifest"
) else (
  echo Nichts zu committen.
)

REM 3) Pushen
git push
if errorlevel 1 (
  echo Fehler beim Push.
  pause
  exit /b 1
)

echo ================================
echo Fertig: Manifest/Index aktualisiert und gepusht.
echo ================================
pause
endlocal
