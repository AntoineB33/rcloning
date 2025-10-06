@echo off
:: Change these variables to match your setup
set "LOCALFOLDER=C:\."
set "REMOTE=gdrive:/backup-folder"
set "FILTERFILE=C:\Users\N6506\Home\computer\rcloning\data\sync-filter.txt"
set "LOGFILE=C:\Users\N6506\Home\computer\rcloning\data\preview_list.txt"

:: Create log folder if it doesn't exist
if not exist "%~dp0data" mkdir "%~dp0data"

echo ============================
echo Starting Rclone dry-run copy
echo Log file: %LOGFILE%
echo ============================

REM Clear the log file to ensure overwrite
echo. > "%LOGFILE%"

:: Run rclone and log both normal output and errors
rclone copy "%LOCALFOLDER%" "%REMOTE%" ^
  --filter-from "%FILTERFILE%" ^
  --create-empty-src-dirs ^
  --progress ^
  --dry-run ^
  --log-file="%LOGFILE%" ^
  --log-level NOTICE

echo.
echo Rclone dry-run complete. Log written to:
echo %LOGFILE%
pause
