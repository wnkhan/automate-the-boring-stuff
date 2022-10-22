@echo off 

if "%1" NEQ "" (
    python3 %USERPROFILE%\Repos\automate-the-boring-stuff\cli_tools\tasklist-sort.py --sort %1
) else (
        python3 %USERPROFILE%\Repos\automate-the-boring-stuff\cli_tools\tasklist-sort.py
    )

