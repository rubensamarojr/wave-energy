@echo off
setlocal EnableDelayedExpansion
rem Don't remove the two jump line after than the next line [set LF=^]
set NL=^


set /p DpType="Choose the particle distance DpType.!NL!  [1]- lo=0.030m.!NL!  [2]- lo=0.020m.!NL!"
if "!DpType!" == "1" set Dp=0p030
if "!DpType!" == "2" set Dp=0p020

echo Hello %Dp%!

rem "name" and "dirout" are named according to the testcase

set name=CaseDeepCwind3D_ModelScale_lo%Dp%_01
set dirout=%name%_out
set diroutdata=%dirout%\data

rem "executables" are renamed and called from their directory

set dirbin=bin\windows
set gencase="%dirbin%/GenCase_win64.exe"
set dualsphysicscpu="%dirbin%/DualSPHysics5.0CPU_win64.exe"
set dualsphysicsgpu="%dirbin%/DualSPHysics5.0_win64.exe"
set boundaryvtk="%dirbin%/BoundaryVTK_win64.exe"
set partvtk="%dirbin%/PartVTK_win64.exe"
set partvtkout="%dirbin%/PartVTKOut_win64.exe"
set measuretool="%dirbin%/MeasureTool_win64.exe"
set computeforces="%dirbin%/ComputeForces_win64.exe"
set isosurface="%dirbin%/IsoSurface_win64.exe"
set flowtool="%dirbin%/FlowTool_win64.exe"
set floatinginfo="%dirbin%/FloatingInfo_win64.exe"

:menu
if exist %dirout% ( 
	set /p option="The folder "%dirout%" already exists. Choose an option.!NL!  [1]- Save floatinfo data.!NL!  [2]- Save vtk files.!NL!  [3]- Save surface mesh.!NL!  [4]- Abort and exit.!NL!"
	if "!option!" == "1" goto floatinfo else (
		if "!option!" == "2" goto vtk else (
			if "!option!" == "3" goto surface else (
				if "!option!" == "4" goto fail else ( 
					goto menu
				)
			)
		)
	)
)

:floatinfo
set dirout2=%dirout%\floatinginfo
%floatinginfo% -dirin %diroutdata% -filein PartFloatMotion.fbi4 -onlymk:60 -savemotion -savedata %dirout2%/FloatingMotion 
if not "%ERRORLEVEL%" == "0" goto fail

set dirout2=%dirout%\floatinginfo
%floatinginfo% -dirin %diroutdata% -csvsep:1 -onlymk:60 -savedata %dirout2%/FloatMot
if not "%ERRORLEVEL%" == "0" goto fail

set dirout2=%dirout%\floatinginfo
%computeforces% -dirin %diroutdata% -savecsv %dirout2%/_FloatingForce -savevtk %dirout2%/FloatingForce -csvsep:1 -onlymk:60 -momentaxis:6.402:0.1:4.694:6.402:-0.1:4.694
if not "%ERRORLEVEL%" == "0" goto fail

echo All done
goto end


:vtk
set dirout2=%dirout%\particles
%partvtk% -dirin %diroutdata% -savevtk %dirout2%/PartFluid -onlytype:-all,+fluid -vars:+vel,+rhop,+press,+idp,+type
if not "%ERRORLEVEL%" == "0" goto fail
%partvtk% -dirin %diroutdata% -savevtk %dirout2%/PartMoving -onlytype:-all,+moving 
if not "%ERRORLEVEL%" == "0" goto fail
%partvtk% -dirin %diroutdata% -savevtk %dirout2%/PartFloating -onlytype:-all,+floating -vars:+vel,+rhop,+press,+idp,+type
if not "%ERRORLEVEL%" == "0" goto fail

set dirout2=%dirout%\boundary
%boundaryvtk% -loadvtk %dirout%/%name%_Tank_Dp.vtk -motiondata %diroutdata% -savevtkdata %dirout2%/Tank.vtk -onlymk:10
if not "%ERRORLEVEL%" == "0" goto fail
%boundaryvtk% -loadvtk %dirout%/%name%_Floater_Dp.vtk -motiondata %diroutdata% -savevtkdata %dirout2%/MotionFloating -onlymk:60
if not "%ERRORLEVEL%" == "0" goto fail
%boundaryvtk% -loadvtk %dirout%/%name%_Piston_Dp.vtk -motiondata %diroutdata% -savevtkdata %dirout2%/MotionPiston -onlymk:20
if not "%ERRORLEVEL%" == "0" goto fail

echo All done
goto end


:surface
set dirout2=%dirout%\surface
%isosurface% -dirin %diroutdata% -saveiso %dirout2%/Surface -vars:+vel,+rhop,+press
if not "%ERRORLEVEL%" == "0" goto fail


:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause
