@echo off
echo ============================================
echo   README Updater - KonetiBalaji Profile
echo ============================================
echo.
echo Updating README.md with latest repositories...
echo.
python update_readme.py
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] README updated!
) else (
    echo [FAILED] See errors above.
)
echo.
pause
