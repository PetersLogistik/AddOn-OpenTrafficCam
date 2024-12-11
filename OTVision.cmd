@echo off
setlocal
cd %~dp0\OTVision
echo start OTVision
call \venv\Scripts\activate
echo Fall 0: python rename.py 
echo Fall I: python convert.py -p "/to/your/h264 files" 
echo Fall II: python detect.py -p "/to/video" --expected_duration "video duration [sec]" 
echo Fall III: python track.py -p "/to/otdet@video"
pause
cmd
deactivate
endlocal
exit /b