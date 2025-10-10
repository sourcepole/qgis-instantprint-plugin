@echo off
SET QGIS_ROOT=C:\Program Files\QGIS 3.22.7
call "%QGIS_ROOT%"\bin\o4w_env.bat
call "%QGIS_ROOT%"\apps\grass\grass78\etc\env.bat
@echo off
path %PATH%;%QGIS_ROOT%\apps\qgis\bin
path %PATH%;%QGIS_ROOT%\apps\grass\grass78\lib
path %PATH%;%QGIS_ROOT%\apps\Qt6\bin
path %PATH%;%QGIS_ROOT%\apps\Python39\Scripts
set PYTHONPATH=%PYTHONPATH%;%QGIS_ROOT%\apps\qgis-ltr\python
set PYTHONHOME=%QGIS_ROOT%\apps\Python39
cmd.exe
pyside6-rcc -o resources.py resources.qrc
