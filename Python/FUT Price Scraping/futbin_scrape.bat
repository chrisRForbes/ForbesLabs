call workon webscraping

@echo off
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%b-%%a)

echo %mydate%
mkdir .\%mydate%

python .\futbin_main.py 90 98 %mydate%\90_98 %*
python .\futbin_main.py 70 90 %mydate%\70_90 %*
python .\futbin_main.py 55 70 %mydate%\55_70 %*
python .\futbin_main.py 45 55 %mydate%\45_55 %*

copy .\%mydate%\*.csv .\%mydate%\all_players.csv