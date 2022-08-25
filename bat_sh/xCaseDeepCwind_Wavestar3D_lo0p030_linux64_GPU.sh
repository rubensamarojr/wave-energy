#!/bin/bash 

fail () { 
 echo Execution aborted. 
 read -n1 -r -p "Press any key to continue..." key 
 exit 1 
}

# "name" and "dirout" are named according to the testcase

export name=CaseDeepCwind_Wavestar3D_lo0p030
export dirout=${name}_out
export diroutdata=${dirout}/data

# "executables" are renamed and called from their directory

export dirbin=../../../bin/linux
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${dirbin}
export gencase="${dirbin}/GenCase_linux64"
export dualsphysicscpu="${dirbin}/DualSPHysics5.0CPU_linux64"
export dualsphysicsgpu="${dirbin}/DualSPHysics5.0_linux64"
export boundaryvtk="${dirbin}/BoundaryVTK_linux64"
export partvtk="${dirbin}/PartVTK_linux64"
export partvtkout="${dirbin}/PartVTKOut_linux64"
export measuretool="${dirbin}/MeasureTool_linux64"
export computeforces="${dirbin}/ComputeForces_linux64"
export isosurface="${dirbin}/IsoSurface_linux64"
export flowtool="${dirbin}/FlowTool_linux64"
export floatinginfo="${dirbin}/FloatingInfo_linux64"

option=-1
 if [ -e $dirout ]; then
 while [ "$option" != 1 -a "$option" != 2 -a "$option" != 3 ] 
 do 

	echo -e "The folder "${dirout}" already exists. Choose an option.
  [1]- Delete it and continue.
  [2]- Execute post-processing.
  [3]- Abort and exit.
"
 read -n 1 option 
 done 
  else 
   option=1 
fi 

if [ $option -eq 1 ]; then
# "dirout" to store results is removed if it already exists
if [ -e ${dirout} ]; then rm -r ${dirout}; fi

# CODES are executed according the selected parameters of execution in this testcase

# Executes GenCase to create initial files for simulation.
${gencase} ${name}_Def ${dirout}/${name} -save:all 
if [ $? -ne 0 ] ; then fail; fi

# Executes DualSPHysics to simulate SPH method.
${dualsphysicsgpu} -gpu ${dirout}/${name} ${dirout} -dirdataout data -svres -stable
if [ $? -ne 0 ] ; then fail; fi

fi

if [ $option -eq 2 -o $option -eq 1 ]; then
# Executes PartVTK to create VTK files with particles.
export dirout2=${dirout}/floatinginfo

${floatinginfo} -dirin ${diroutdata} -filein PartFloatMotion.fbi4 -onlymk:60 -savemotion -savedata %dirout2%/FloatingMotion 
if [ $? -ne 0 ] ; then fail; fi

#${floatinginfo} -dirin ${diroutdata} -filein PartDeepCwindMotion.fbi4 -onlymk:60 -savemotion -savedata ${dirout2}/DeepCwindMotion 
#if [ $? -ne 0 ] ; then fail; fi
#${floatinginfo} -dirin ${diroutdata} -filein PartWavestar1Motion.fbi4 -onlymk:61 -savemotion -savedata ${dirout2}/Wavestar1Motion 
#if [ $? -ne 0 ] ; then fail; fi
#${floatinginfo} -dirin ${diroutdata} -filein PartWavestar2Motion.fbi4 -onlymk:62 -savemotion -savedata ${dirout2}/Wavestar2Motion 
#if [ $? -ne 0 ] ; then fail; fi
#${floatinginfo} -dirin ${diroutdata} -filein PartWavestar3Motion.fbi4 -onlymk:63 -savemotion -savedata ${dirout2}/Wavestar3Motion 
#if [ $? -ne 0 ] ; then fail; fi

${computeforces} -dirin ${diroutdata} -savecsv ${dirout2}/_DeepCwindForce -savevtk  ${dirout2}/DeepCwindForce -csvsep:1 -onlymk:60 -momentaxis:0:0.1:0.0:0:-0.1:0.0
if [ $? -ne 0 ] ; then fail; fi
${computeforces} -dirin ${diroutdata} -savecsv ${dirout2}/_Wavestar1Force -savevtk  ${dirout2}/Wavestar1Force -csvsep:1 -onlymk:61 -momentaxis:0:0.1:0.0:0:-0.1:0.0
if [ $? -ne 0 ] ; then fail; fi
${computeforces} -dirin ${diroutdata} -savecsv ${dirout2}/_Wavestar2Force -savevtk  ${dirout2}/Wavestar2Force -csvsep:1 -onlymk:62 -momentaxis:0.1:0.1:0.0:-0.1:-0.1:0.0
if [ $? -ne 0 ] ; then fail; fi
${computeforces} -dirin ${diroutdata} -savecsv ${dirout2}/_Wavestar3Force -savevtk  ${dirout2}/Wavestar3Force -csvsep:1 -onlymk:63 -momentaxis:-0.1:0.1:0.0:0.1:-0.1:0.0
if [ $? -ne 0 ] ; then fail; fi

export dirout2=${dirout}/particles
${partvtk} -dirin ${diroutdata} -savevtk ${dirout2}/PartFluid -onlytype:-all,+fluid -vars:+vel,+rhop,+press,+idp,+type
if [ $? -ne 0 ] ; then fail; fi

#${partvtk} -dirin ${diroutdata} -savevtk ${dirout2}/PartMoving -onlytype:-all,+moving -vars:+vel,+rhop,+press,+idp,+type
#if [ $? -ne 0 ] ; then fail; fi

${partvtk} -dirin ${diroutdata} -savevtk ${dirout2}/PartFloating -onlytype:-all,+floating -vars:+vel,+rhop,+press,+idp,+type
if [ $? -ne 0 ] ; then fail; fi

export dirout2=${dirout}/boundary
${boundaryvtk} -loadvtk ${dirout}/${name}_Tank_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/Tank.vtk -onlymk:10
if [ $? -ne 0 ] ; then fail; fi

${boundaryvtk} -loadvtk ${dirout}/${name}_DeepCwind_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/MotionDeepCwind -onlymk:60
if [ $? -ne 0 ] ; then fail; fi

${boundaryvtk} -loadvtk ${dirout}/${name}_Wavestar1_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/MotionWavestar1 -onlymk:61
if [ $? -ne 0 ] ; then fail; fi

${boundaryvtk} -loadvtk ${dirout}/${name}_Wavestar2_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/MotionWavestar2 -onlymk:62
if [ $? -ne 0 ] ; then fail; fi

${boundaryvtk} -loadvtk ${dirout}/${name}_Wavestar3_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/MotionWavestar3 -onlymk:63
if [ $? -ne 0 ] ; then fail; fi

#${boundaryvtk} -loadvtk ${dirout}/${name}_Piston_Dp.vtk -motiondata ${diroutdata} -savevtkdata ${dirout2}/MotionPiston -onlymk:20
#if [ $? -ne 0 ] ; then fail; fi

#export dirout2=${dirout}/surface
#${isosurface} -dirin ${diroutdata} -saveiso ${dirout2}/Surface -vars:+vel,+rhop,+press
#if [ $? -ne 0 ] ; then fail; fi

fi
if [ $option != 3 ];then
 echo All done
 else
 echo Execution aborted
fi

read -n1 -r -p "Press any key to continue..." key
