@echo off
cd /d "%~dp0"
echo ==============================================
echo Compilation de CCNA-Spotlight.exe
echo ==============================================
python -m PyInstaller --noconsole --onefile --icon="assets/icon.ico" --name="CCNA-Spotlight" --add-data "data;data" --add-data "extracted_images;extracted_images" --add-data "assets;assets" mini_app.py
if exist "dist\CCNA-Spotlight.exe" (
    copy /y "dist\CCNA-Spotlight.exe" "CCNA-Spotlight.exe"
    echo.
    echo Succes : CCNA-Spotlight.exe a ete genere a la racine du dossier !
) else (
    echo.
    echo Erreur lors de la compilation.
)
pause
