@REM @echo off
@REM cd C:\Users\Asus\Documents\work\source\bot
@REM python crypto_forecast.py

@echo off
:: Load environment variables from sendgrid.env
for /f "tokens=1,2 delims==" %%a in (sendgrid.env) do (
    set %%a=%%b
)

:: Verify that the environment variable is set
if "%SENDGRID_API_KEY%"=="" (
    echo SENDGRID_API_KEY is not set.
    exit /b 1
) else (
    echo SENDGRID_API_KEY is set.
)

:: Run the Python script
python crypto_forecast.py

:: Pause the command line window if you want to see the output
pause
