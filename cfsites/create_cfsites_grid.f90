PROGRAM create_cfsites_grid

  USE xios
  ! USE netcdf

  IMPLICIT NONE
  INCLUDE "mpif.h"
  ! INTEGER,PARAMETER :: ncell=2
  INTEGER,PARAMETER :: ncell=121
  DOUBLE PRECISION                     :: delta_lat, delta_lon
  DOUBLE PRECISION, DIMENSION(ncell)   :: cfsites_lat, cfsites_lon
  DOUBLE PRECISION, DIMENSION(4,ncell) :: cfsites_bounds_lon,cfsites_bounds_lat
  REAL, DIMENSION(ncell) :: cfsites_field
  INTEGER :: ierr,ncid,varid
  INTEGER :: comm,i,j,fact
  TYPE(xios_duration) :: dtime
  TYPE(xios_context) :: ctx_hdl

  open(unit=7, file='cmip6-cfsites-locations.txt')
  !cfsites_field(1)=0. ;   cfsites_lat(1)=45. ;   cfsites_lon(1)=0.
  !cfsites_field(1)=0. ;   cfsites_lat(2)=35. ;   cfsites_lon(2)=0.
  delta_lat=0.01
  delta_lon=0.01
  
  do i=1,ncell
     read (7,*) j,cfsites_lon(i),cfsites_lat(i)
     cfsites_field(i)=i
     fact=1 ; if (cfsites_lat(i) <= 0.) fact=-1
     cfsites_bounds_lat(1,i)=cfsites_lat(i)-fact*delta_lat
     cfsites_bounds_lat(2,i)=cfsites_lat(i)+fact*delta_lat
     cfsites_bounds_lat(3,i)=cfsites_lat(i)+fact*delta_lat
     cfsites_bounds_lat(4,i)=cfsites_lat(i)-fact*delta_lat
     
     cfsites_bounds_lon(1,i)=cfsites_lon(i)-delta_lon
     cfsites_bounds_lon(2,i)=cfsites_lon(i)-delta_lon
     cfsites_bounds_lon(3,i)=cfsites_lon(i)+delta_lon
     cfsites_bounds_lon(4,i)=cfsites_lon(i)+delta_lon
  enddo

  CALL xios_initialize("create_cfsites_grid",return_comm=comm)
  CALL xios_context_initialize("create_cfsites_grid",comm)
  CALL xios_set_domain_attr("cfsites_domain", nvertex=4, ni_glo=ncell, ni=ncell, ibegin=0,&
       latvalue_1d=cfsites_lat, lonvalue_1d=cfsites_lon)
  CALL xios_set_domain_attr("cfsites_domain", bounds_lon_1d=cfsites_bounds_lon, bounds_lat_1d=cfsites_bounds_lat)

  dtime%second = 3600
  CALL xios_set_timestep(dtime)
  CALL xios_close_context_definition()
  
  CALL xios_update_calendar(1)
  CALL xios_send_field("cfsites_field",cfsites_field)
 
  CALL xios_context_finalize()
  CALL xios_finalize()

END PROGRAM create_cfsites_grid
