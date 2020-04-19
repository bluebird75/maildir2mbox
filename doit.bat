@echo off
@set BUIILD_IT=
if "%1" == "upload_test" (
	set OTHER_ARGS=--repository-url https://test.pypi.org/legacy/
) else if "%1" == "upload_pypi" (
	set OTHER_ARGS=
) else if "%1" == "build" (
	set BUIILD_IT=yes
) else (
	echo You must supply either "upload_test" or "upload_pypi" or "build"
	exit /b 1
)
@echo on

@if "%BUIILD_IT%" == "yes" (
	python setup.py bdist_wheel sdist 
	@if errorlevel 1 exit /b 1
	exit /b 0
)

python -m twine upload -u __token__ %OTHER_ARGS%  dist/*
@if errorlevel 1 exit /b 1

@echo Uploaded successfully