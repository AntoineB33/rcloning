@echo off
:: Change these variables to match your setup
set "LOCALFOLDER=C:\."
set "REMOTE=gdrive:/backup-folder"
set "FILTERFILE=C:\Users\N6506\Home\computer\rcloning\data\sync-filter.txt"

:: Run rclone with proper quoting
rclone sync "%LOCALFOLDER%" "%REMOTE%" --filter-from "%FILTERFILE%" --create-empty-src-dirs --progress

pause
