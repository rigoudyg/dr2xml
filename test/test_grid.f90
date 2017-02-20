PROGRAM test_grid

  USE xios
  USE mod_wait
  IMPLICIT NONE
  INCLUDE "mpif.h"

  INTEGER,PARAMETER :: il_unit=10
  INTEGER :: comm, rank, size_loc, ierr
  INTEGER :: ni,ibegin,iend,nj,jbegin,jend
  INTEGER :: i,j,l,ts,n, nb_pt, il_run
  DOUBLE PRECISION :: sypd, timestep_in_seconds, simulated_seconds_per_seconds, elapsed_per_timestep
  CHARACTER(len=*),PARAMETER :: id="client"
  CHARACTER(1000):: duration, timestep
  TYPE(xios_date) :: cdate, edate
  TYPE(xios_duration)  :: dtime
  TYPE(xios_context) :: ctx_hdl
  REAL :: ilon,ilat
  DOUBLE PRECISION,ALLOCATABLE :: lon_glo(:,:),lat_glo(:,:),lval(:)
  DOUBLE PRECISION,ALLOCATABLE :: field_A_glo (:,:,:), pressure_glo (:,:,:), height_glo (:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: bounds_lon_glo(:,:,:),bounds_lat_glo(:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: pressure (:,:,:), height (:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: lon(:,:),lat(:,:),lonvalue(:,:)
  DOUBLE PRECISION,ALLOCATABLE :: bounds_lon(:,:,:),bounds_lat(:,:,:) 
  DOUBLE PRECISION,ALLOCATABLE :: field_atm_2D(:,:),field_atm_3D(:,:,:),field_srf_2D(:),field_srf_3D(:,:)
  DOUBLE PRECISION,ALLOCATABLE :: field_oce_2D(:,:),field_oce_3D(:,:,:)
  INTEGER, ALLOCATABLE :: kindex(:)

  INTEGER :: ni_glo, nj_glo,llm

  NAMELIST /param_toy/ ni_glo, nj_glo,llm,timestep,duration,sypd

!!! MPI Initialization

  CALL MPI_INIT(ierr)

  CALL init_wait

!!! Lecture des parametres du run

  OPEN(unit=il_unit, file='param.def',status='old',iostat=ierr)
  READ (il_unit, nml=param_toy)
  !PRINT *, ni_glo, nj_glo,llm,duration

!!! XIOS Initialization (get the local communicator)

  CALL xios_initialize(id,return_comm=comm)

  CALL MPI_COMM_RANK(comm,rank,ierr)
  CALL MPI_COMM_SIZE(comm,size_loc,ierr)


!!! Initialisation et allocation des coordonnées globales et locales pour la grille régulière

  ALLOCATE (lon_glo(ni_glo,nj_glo),lat_glo(ni_glo,nj_glo))
  ALLOCATE(bounds_lon_glo(4,ni_glo,nj_glo))
  ALLOCATE(bounds_lat_glo(4,ni_glo,nj_glo))
  ALLOCATE (field_A_glo(ni_glo,nj_glo,llm))
  ALLOCATE (pressure_glo(ni_glo,nj_glo,llm))
  ALLOCATE (height_glo(ni_glo,nj_glo,llm))
  ALLOCATE (lval(llm))

  DO j=1,nj_glo
    DO i=1,ni_glo

      ilon=i-0.5
      ilat=j-0.5

      lat_glo(i,j)= 90-(ilat*180./ni_glo)
      lon_glo(i,j)= (ilon*360./nj_glo)

      bounds_lat_glo(1,i,j)= 90-((ilat-0.5)*180./ni_glo)
      bounds_lon_glo(1,i,j)=((ilon-0.5)*360./nj_glo)

      bounds_lat_glo(2,i,j)= 90-((ilat-0.5)*180./ni_glo)
      bounds_lon_glo(2,i,j)=((ilon+0.5)*360./nj_glo)

      bounds_lat_glo(3,i,j)= 90-((ilat+0.5)*180./ni_glo)
      bounds_lon_glo(3,i,j)=((ilon+0.5)*360./nj_glo)

      bounds_lat_glo(4,i,j)= 90-((ilat+0.5)*180./ni_glo)
      bounds_lon_glo(4,i,j)=((ilon-0.5)*360./nj_glo)

      DO l=1,llm
         field_A_glo(i,j,l)=(i-1)+(j-1)*ni_glo+10000*l
         ! pressure at half levels. First index is high altitude, low pressure
         pressure_glo(i,j,l)=((l-0.)/llm)*100000 + (ilat -nj_glo/2.)/nj_glo * 10000
         height_glo(i,j,l)=(llm-l+0.5)/llm * 15000 + ilat * 100
      ENDDO
    ENDDO
  ENDDO
  ni=ni_glo ; ibegin=0

  jbegin=0
  DO n=0,size_loc-1
    nj=nj_glo/size_loc
    IF (n<MOD(nj_glo,size_loc)) nj=nj+1
    IF (n==rank) exit
    jbegin=jbegin+nj
  ENDDO

  iend=ibegin+ni-1 ; jend=jbegin+nj-1

  ALLOCATE(lon(ni,nj),lat(ni,nj),lonvalue(ni,nj))
  ALLOCATE(bounds_lon(4,ni,nj))
  ALLOCATE(bounds_lat(4,ni,nj))
  lon(:,:)=lon_glo(ibegin+1:iend+1,jbegin+1:jend+1)
  lat(:,:)=lat_glo(ibegin+1:iend+1,jbegin+1:jend+1)
  bounds_lon(:,:,:)=bounds_lon_glo(:,ibegin+1:iend+1,jbegin+1:jend+1)
  bounds_lat(:,:,:)=bounds_lat_glo(:,ibegin+1:iend+1,jbegin+1:jend+1)


  DO i=1,llm
    lval(i)=i
 ENDDO
 

  
!###########################################################################
! Contexte ATM
!###########################################################################
 ALLOCATE(field_atm_2D(0:ni+1,-1:nj+2),field_atm_3D(0:ni+1,-1:nj+2,llm))
 ALLOCATE(pressure(0:ni+1,-1:nj+2,llm))
 ALLOCATE(height(0:ni+1,-1:nj+2,llm))
  field_atm_2D(1:ni,1:nj)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,1)
  field_atm_3D(1:ni,1:nj,:)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)
  pressure(1:ni,1:nj,:)=pressure_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)
  height(1:ni,1:nj,:)=height_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)

  CALL xios_context_initialize("arpsfx",comm)
  !write(0,*) 'atm context initialized' ; call flush(0)
  CALL xios_get_handle("arpsfx",ctx_hdl)
  CALL xios_set_current_context(ctx_hdl)

  CALL xios_set_axis_attr("axis_atm",n_glo=llm ,value=lval) ;

  CALL xios_set_domain_attr("domain_atm",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, &
       ni=ni,jbegin=jbegin,nj=nj, type='rectilinear')
  CALL xios_set_domain_attr("domain_atm",data_dim=2, data_ibegin=-1, &
       data_ni=ni+2, data_jbegin=-2, data_nj=nj+4)
  CALL xios_set_domain_attr("domain_atm",lonvalue_2D=lon,latvalue_2D=lat)
  CALL xios_set_domain_attr("domain_atm", nvertex=4, bounds_lon_2d=bounds_lon, bounds_lat_2d=bounds_lat)


!!! Definition du timestep

  CALL xios_get_start_date(cdate)
  edate=cdate+xios_duration_convert_from_string(duration)
  dtime=xios_duration_convert_from_string(timestep)
  CALL xios_set_timestep(timestep=dtime)

!!! Fin de la definition du contexte

  !CALL xios_close_context_definition()

!!! Calcul de temps elaps par seconde pour respecter le SYPD (hyp : pas de délai d'I/O)
  
  timestep_in_seconds=xios_date_convert_to_seconds(cdate+dtime) - xios_date_convert_to_seconds(cdate)
  simulated_seconds_per_seconds=sypd * 365 
  elapsed_per_timestep=timestep_in_seconds/simulated_seconds_per_seconds ! in seconds

!###########################################################################
! Contexte SRF
!###########################################################################

!!! Initialisation des coordonnées globales et locales pour la grille indexee (1 point sur 2)

    nb_pt=ni*nj/2
    ALLOCATE(kindex(nb_pt),field_srf_2D(nb_pt),field_srf_3D(nb_pt,llm))
    DO i=1,nb_pt
      kindex(i)=2*i-1
    ENDDO
    field_srf_2D(1:nb_pt)=RESHAPE(field_A_glo(ibegin+1:iend+1:2,jbegin+1:jend+1,1),(/ nb_pt /))
    field_srf_3D(1:nb_pt,:)=RESHAPE(field_A_glo(ibegin+1:iend+1:2,jbegin+1:jend+1,:),(/ nb_pt,llm /))

  !CALL xios_context_initialize("surface",comm)
  !CALL xios_get_handle("surface",ctx_hdl)
  !CALL xios_set_current_context(ctx_hdl)

  CALL xios_set_axis_attr("axis_srf",n_glo=llm ,value=lval)
  CALL xios_set_domain_attr("domain_srf",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, ni=ni,jbegin=jbegin,nj=nj, type='rectilinear')
  CALL xios_set_domain_attr("domain_srf",data_dim=1, data_ibegin=0, data_ni=nb_pt)
  CALL xios_set_domain_attr("domain_srf",data_i_index=kindex)
  CALL xios_set_domain_attr("domain_srf",lonvalue_2D=lon,latvalue_2D=lat)
  CALL xios_set_domain_attr("domain_srf", nvertex=4, bounds_lon_2d=bounds_lon, bounds_lat_2d=bounds_lat)

!!! Definition du timestep

  !dtime%second=timestep
  !dtime=xios_duration_convert_from_string(timestep)
  !CALL xios_set_timestep(timestep=dtime)

!!! Fin de la definition du contexte SRF

  CALL xios_close_context_definition()
  write(0,*) 'srf context def closed' ; call flush(0)

!###########################################################################
! Contexte OCE
!###########################################################################
  ALLOCATE(field_oce_2D(0:ni+1,-1:nj+2),field_oce_3D(0:ni+1,-1:nj+2,llm))
  field_oce_2D(1:ni,1:nj)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,1)
  field_oce_3D(1:ni,1:nj,:)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)

  CALL xios_context_initialize("nemo",comm)
  CALL xios_get_handle("nemo",ctx_hdl)
  CALL xios_set_current_context(ctx_hdl)

  CALL xios_set_axis_attr("axis_oce",n_glo=llm ,value=lval) ;

  CALL xios_set_domain_attr("domain_oce",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, ni=ni,jbegin=jbegin,nj=nj, type='curvilinear')
  CALL xios_set_domain_attr("domain_oce",data_dim=2, data_ibegin=-1, data_ni=ni+2, data_jbegin=-2, data_nj=nj+4)
  CALL xios_set_domain_attr("domain_oce",lonvalue_2D=lon,latvalue_2D=lat)


!!! Definition du timestep

  dtime=xios_duration_convert_from_string(timestep)
  CALL xios_set_timestep(timestep=dtime)

  CALL xios_close_context_definition()

!####################################################################################
!!! Boucle temporelle
!####################################################################################
  ts=1
  cdate=cdate+dtime
  DO while ( cdate <= edate )

      CALL xios_get_handle("arpsfx",ctx_hdl)
      CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

      CALL xios_update_calendar(ts)

!!! On donne la valeur du champ atm

      print *,'sending field_atm_2d at timestep',ts
      CALL xios_send_field("field_atm_scalar",field_atm_2D(1,1)+ts)
      CALL xios_send_field("field_atm_1D",field_atm_3D(1,1,:)+ts)
      CALL xios_send_field("field_atm_2D",field_atm_2D+ts)
      CALL xios_send_field("field_atm_3D",field_atm_3D+ts)
      CALL xios_send_field("pressure" ,pressure)
      CALL xios_send_field("height"   ,height)
      if (mod(ts,2)==0) then
         CALL xios_send_field("field_sub",field_atm_2D+ts)
      endif
      
!!! On change de contexte

      !CALL xios_get_handle("surface",ctx_hdl)
      !CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

      !CALL xios_update_calendar(ts)

!!! On donne la valeur du champ srf

      CALL xios_send_field("field_srf_2D",field_srf_2D)
      CALL xios_send_field("field_srf_3D",field_srf_3D)

!!! On change de contexte

      CALL xios_get_handle("nemo",ctx_hdl)
      CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

      CALL xios_update_calendar(ts)

!!! On donne la valeur du champ oce

      CALL xios_send_field("field_oce_scalar",field_oce_2D(1,1)+ts)
      CALL xios_send_field("field_oce_grid_2D",field_oce_2D)
      CALL xios_send_field("field_oce_grid_3D",field_oce_3D)

      CALL wait_us(int(elapsed_per_timestep*1.e6))   ! micro-secondes
      cdate=cdate+dtime
      ts=ts+1

   ENDDO

!####################################################################################
!!! Finalisation
!####################################################################################

!!! Fin des contextes

    CALL xios_context_finalize()
    CALL xios_get_handle("arpsfx",ctx_hdl)
    CALL xios_set_current_context(ctx_hdl)
    CALL xios_context_finalize()
    !CALL xios_get_handle("surface",ctx_hdl)
    !CALL xios_set_current_context(ctx_hdl)
    !CALL xios_context_finalize()

    DEALLOCATE(lon, lat, lonvalue, field_atm_2D, field_atm_3D)
    DEALLOCATE(pressure,height,pressure_glo,height_glo)
    DEALLOCATE(kindex, field_srf_2D, field_srf_3D)
    DEALLOCATE(field_oce_2D, field_oce_3D)
    DEALLOCATE(lon_glo,lat_glo,field_A_glo,lval)

!!! Fin de XIOS

    CALL MPI_COMM_FREE(comm, ierr)
      
    CALL xios_finalize()

  CALL MPI_FINALIZE(ierr)

END PROGRAM test_grid






