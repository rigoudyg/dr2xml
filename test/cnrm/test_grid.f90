PROGRAM test_grid

  USE xios
  USE mod_wait
  IMPLICIT NONE
  INCLUDE "mpif.h"

  INTEGER,PARAMETER :: il_unit=10
  INTEGER :: comm, rank, size_loc, ierr
  INTEGER :: ni,ibegin,iend,nj,jbegin,jend, nicosp
  INTEGER :: i,j,l,ts,n, nb_pt, il_run
  DOUBLE PRECISION :: sypd, timestep_in_seconds, simulated_seconds_per_seconds, elapsed_per_timestep
  CHARACTER(len=*),PARAMETER :: id="client"
  CHARACTER(100) :: atmid,srfid,oceid
  CHARACTER(10) :: startdate
  CHARACTER(1000):: duration, timestep
  TYPE(xios_date) :: cdate, edate
  TYPE(xios_duration)  :: dtime
  TYPE(xios_context) :: ctx_hdl
  REAL :: ilon,ilat
  DOUBLE PRECISION,ALLOCATABLE :: cfsites_grid_field(:)
  DOUBLE PRECISION,ALLOCATABLE :: lon_glo(:,:),lat_glo(:,:),lval(:)
  DOUBLE PRECISION,ALLOCATABLE :: field_A_glo (:,:,:), pressure_glo (:,:,:), height_glo (:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: bounds_lon_glo(:,:,:),bounds_lat_glo(:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: pressure (:,:,:), height (:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: lon(:,:),lat(:,:),lonvalue(:,:)
  DOUBLE PRECISION,ALLOCATABLE :: bounds_lon(:,:,:),bounds_lat(:,:,:) 
  DOUBLE PRECISION,ALLOCATABLE :: field_atm_2D(:,:),field_atm_3D(:,:,:),field_srf_2D(:),field_srf_3D(:,:)
  DOUBLE PRECISION,ALLOCATABLE :: other_field_atm_3D(:,:,:)
  DOUBLE PRECISION,ALLOCATABLE :: field_atm_2D_miss(:,:)
  DOUBLE PRECISION,ALLOCATABLE :: field_oce_2D(:,:),field_oce_3D(:,:,:)
  INTEGER, ALLOCATABLE :: kindex(:)
  !
  INTEGER,PARAMETER            :: nmax_transects=1000
  CHARACTER(100)               :: transect_names(nmax_transects)
  INTEGER                      :: ntransects, ibegin_transects, itransects_size
  DOUBLE PRECISION,ALLOCATABLE :: transects_field(:)
  !
  INTEGER :: ni_glo, nj_glo,llm

  NAMELIST /param_toy/ ni_glo, nj_glo,llm,timestep,duration,sypd,atmid,srfid,oceid,startdate,transect_names

!!! MPI Initialization

  CALL MPI_INIT(ierr)

  CALL init_wait

  atmid="atmosphere"
  srfid="surface"
  oceid="ocean"
  startdate="1950-01-01"
  transect_names=(/("", i=1,nmax_transects)/)
  
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

      lat_glo(i,j)= -90+(ilat*180./nj_glo)
      lon_glo(i,j)= (ilon*360./ni_glo)

      bounds_lat_glo(1,i,j)= -90+((ilat-0.5)*180./nj_glo)
      bounds_lon_glo(1,i,j)=((ilon-0.5)*360./ni_glo)

      bounds_lat_glo(2,i,j)= -90+((ilat-0.5)*180./nj_glo)
      bounds_lon_glo(2,i,j)=((ilon+0.5)*360./ni_glo)

      bounds_lat_glo(3,i,j)= -90+((ilat+0.5)*180./nj_glo)
      bounds_lon_glo(3,i,j)=((ilon+0.5)*360./ni_glo)

      bounds_lat_glo(4,i,j)= -90+((ilat+0.5)*180./nj_glo)
      bounds_lon_glo(4,i,j)=((ilon-0.5)*360./ni_glo)

      DO l=1,llm
         field_A_glo(i,j,l)=(i-1)+(j-1)*ni_glo+10000*l
         ! pressure at half levels. First l index is high altitude, low pressure
         pressure_glo(i,j,l)=((l-1.)/(llm-1.))*100000 + (ilat -nj_glo/2.)/nj_glo * 10000
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
 
!!! Count transects number and init transects field to sequential integers from 1
 ntransects=0
 do i=1,nmax_transects
     if (trim(transect_names(i)) /= "") ntransects=i
  enddo
  ALLOCATE (transects_field(ntransects))
  transects_field=(/(i, i=1,ntransects)/)
  
!!! compute transects local range (in case we actually distribute this axis)
  ibegin_transects=0
  DO n=0,size_loc-1
    itransects_size=ntransects/size_loc
    IF (n<MOD(ntransects,size_loc)) itransects_size=itransects_size+1
    IF (n==rank) exit
    ibegin_transects=ibegin_transects+itransects_size
  ENDDO

  
!###########################################################################
! Contexte ATM
!###########################################################################
 ALLOCATE(field_atm_2D(0:ni+1,-1:nj+2),field_atm_3D(0:ni+1,-1:nj+2,llm))
 ALLOCATE(other_field_atm_3D(0:ni+1,-1:nj+2,llm))
 ALLOCATE(field_atm_2D_miss(0:ni+1,-1:nj+2))
 ALLOCATE(pressure(0:ni+1,-1:nj+2,llm))
 ALLOCATE(height(0:ni+1,-1:nj+2,llm))
  field_atm_2D(1:ni,1:nj)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,1)
  field_atm_2D_miss(1:ni,1:nj)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,1)
  field_atm_3D(1:ni,1:nj,:)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)
  pressure(1:ni,1:nj,:)=pressure_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)
  height(1:ni,1:nj,:)=height_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)

  CALL xios_context_initialize(trim(atmid),comm)
  !write(0,*) 'atm context initialized' ; call flush(0)
  CALL xios_get_handle(trim(atmid),ctx_hdl)
  CALL xios_set_current_context(ctx_hdl)

  CALL xios_set_axis_attr("axis_atm",n_glo=llm ,value=lval) ;

  CALL xios_set_domain_attr("domain_atm",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, &
       ni=ni,jbegin=jbegin,nj=nj, type='rectilinear')
  CALL xios_set_domain_attr("domain_atm",data_dim=2, data_ibegin=-1, &
       data_ni=ni+2, data_jbegin=-2, data_nj=nj+4)
  !CALL xios_set_domain_attr("domain_atm",lonvalue_2D=lon,latvalue_2D=lat)
  CALL xios_set_domain_attr("domain_atm",lonvalue_1D=lon(:,1),latvalue_1D=lat(1,:))
  ! Don't set bounds for a rectilinear domain
  !CALL xios_set_domain_attr("domain_atm", nvertex=4, bounds_lon_2d=bounds_lon, bounds_lat_2d=bounds_lat)

  
!!! Definition de la start date et du timestep

  call xios_set_start_date(xios_date_convert_from_string(startdate//" 00:00:00"))
  dtime=xios_duration_convert_from_string(timestep)
  CALL xios_set_timestep(timestep=dtime)

!!! Fin de la definition du contexte

  if (trim(atmid) /= trim(srfid))  then 
     write(0,*) 'closing context '//trim(atmid) ; call flush(0)
     print*,'closing_context_definition for '//trim(atmid)
     CALL xios_close_context_definition()
  endif


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

    if (trim(atmid) /= trim(srfid))  then 
       CALL xios_context_initialize(trim(srfid),comm)
       CALL xios_get_handle(trim(srfid),ctx_hdl)
       CALL xios_set_current_context(ctx_hdl)
    endif

  CALL xios_set_axis_attr("axis_srf",n_glo=llm ,value=lval)
  CALL xios_set_domain_attr("domain_srf",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, ni=ni,jbegin=jbegin,nj=nj, type='rectilinear')
  CALL xios_set_domain_attr("domain_srf",data_dim=1, data_ibegin=0, data_ni=nb_pt)
  CALL xios_set_domain_attr("domain_srf",data_i_index=kindex)
  CALL xios_set_domain_attr("domain_srf",lonvalue_1D=lon(:,1),latvalue_1D=lat(1,:))

!!! Definition de la start date et du timestep

  if (trim(atmid) /= trim(srfid))  then
     call xios_set_start_date(xios_date_convert_from_string(startdate//" 00:00:00"))
     CALL xios_set_timestep(timestep=dtime)
  endif
  
!!! Fin de la definition du contexte SRF (ou ATM si = SRF)
  print*,'closing_context_definition for '//trim(srfid)
  CALL xios_close_context_definition()

  ! If config file describes an input field for cosp sites grid, read it
  if (.FALSE. .AND. xios_is_valid_field("cfsites_field")) then 
     CALL xios_set_current_context(trim(atmid))
     CALL xios_update_calendar(0)
     call xios_get_domain_attr("cfsites_domain", ni=nicosp)
     allocate(cfsites_grid_field(nicosp))
     call xios_recv_field("cfsites_field", cfsites_grid_field)
  endif

!!! Calcul de temps elaps par seconde pour respecter le SYPD (hyp : pas de délai d'I/O)
  
  CALL xios_get_start_date(cdate)
  edate=cdate+xios_duration_convert_from_string(duration)
  timestep_in_seconds=xios_date_convert_to_seconds(cdate+dtime) - xios_date_convert_to_seconds(cdate)
  simulated_seconds_per_seconds=sypd * 365 
  elapsed_per_timestep=timestep_in_seconds/simulated_seconds_per_seconds ! in seconds

!###########################################################################
! Contexte OCE
!###########################################################################
  ALLOCATE(field_oce_2D(0:ni+1,-1:nj+2),field_oce_3D(0:ni+1,-1:nj+2,llm))
  field_oce_2D(1:ni,1:nj)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,1)
  field_oce_3D(1:ni,1:nj,:)=field_A_glo(ibegin+1:iend+1,jbegin+1:jend+1,:)

  CALL xios_context_initialize(trim(oceid),comm)
  CALL xios_get_handle(trim(oceid),ctx_hdl)
  CALL xios_set_current_context(ctx_hdl)

  CALL xios_set_axis_attr("axis_oce",n_glo=llm ,value=lval) ;

  CALL xios_set_domain_attr("domain_oce",ni_glo=ni_glo, nj_glo=nj_glo, ibegin=ibegin, ni=ni,jbegin=jbegin,nj=nj, type='curvilinear')
  CALL xios_set_domain_attr("domain_oce",data_dim=2, data_ibegin=-1, data_ni=ni+2, data_jbegin=-2, data_nj=nj+4)
  CALL xios_set_domain_attr("domain_oce",lonvalue_2D=lon,latvalue_2D=lat)
  CALL xios_set_domain_attr("domain_oce",nvertex=4, bounds_lon_2d=bounds_lon, bounds_lat_2d=bounds_lat)

  if (xios_is_valid_axis("transect_axis")) then
     CALL xios_set_axis_attr("transect_axis",n_glo=ntransects)

     ! Version with a distributed transect axis
     ! CALL xios_set_axis_attr("transect_axis",begin=ibegin_transects,n=itransects_size)
     ! CALL xios_set_axis_attr("transect_axis",label=transect_names(ibegin_transects:ibegin_transects+itransects_size))

     ! Version with a non-distributed transect axis
     print *,'initalizing labels for transect_axis to:',transect_names
     CALL xios_set_axis_attr("transect_axis",value=(/(1.0D0*I, i=1,ntransects)/))
     CALL xios_set_axis_attr("transect_axis",label=transect_names(1:ntransects))
     CALL xios_set_axis_attr("transect_axis",name="oline")
     CALL xios_set_axis_attr("transect_axis",standard_name="Region")
     CALL xios_set_axis_attr("transect_axis",long_name="ocean passage")
  endif

  
!!! Definition de la start date et du timestep

  call xios_set_start_date(xios_date_convert_from_string(startdate//" 00:00:00"))
  dtime=xios_duration_convert_from_string(timestep)
  CALL xios_set_timestep(timestep=dtime)

  print*,'closing_context_definition for '//trim(oceid)

  CALL xios_close_context_definition()

!!! Sending a test field on axis 'transect'
  


!####################################################################################
!!! Boucle temporelle
!####################################################################################
  ts=1
  cdate=cdate+dtime
  DO while ( cdate <= edate )

     print*,'ts=',ts
!     print*,'cdate=',cdate
!     print*,'edate=',edate
      CALL xios_get_handle(trim(atmid),ctx_hdl)
      CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

      CALL xios_update_calendar(ts)

!!! On donne la valeur du champ atm

!      print *,'sending field_atm_2d at timestep',ts
      CALL xios_send_field("field_atm_scalar",field_atm_2D(1,1)+ts)
!print*,'step0' ; call flush(6)
      CALL xios_send_field("field_atm_1D",field_atm_3D(1,1,:)+ts)
      CALL xios_send_field("field_atm_2D",field_atm_2D+ts)
!print*,'step1' ; call flush(6)
      other_field_atm_3D(:,:,:)=field_atm_3D(:,:,:)+ts
      CALL xios_send_field("field_atm_3D",other_field_atm_3D)
      ! CALL xios_send_field("field_atm_3D",field_atm_3D)
!print*,'step2' ; call flush(6)
      CALL xios_send_field("pressure" ,pressure)
!print*,'step2.0' ; call flush(6)
      CALL xios_send_field("height"   ,height)
      if (mod(ts,2)==0) then
         CALL xios_send_field("field_sub",field_atm_2D+ts)
      endif
!print*,'step2.1' ; call flush(6)
      !! On crée un champ avec des missings qui bougent
      !! dans le temps : un bande verticale de 1 à ni-3
      field_atm_2D_miss(:,:)= field_atm_2D(:,:)+ts
!print*,'step2.2' ; call flush(6)
      field_atm_2D_miss(mod(ts,ni-3)+1,:)=1.e+20
!print*,'step2.3' ; call flush(6)
      CALL xios_send_field("field_miss",field_atm_2D_miss)
!print*,'step2.4' ; call flush(6)
      
!!! On change de contexte

      if (trim(atmid) /= trim(srfid))  then 
         CALL xios_get_handle(trim(srfid),ctx_hdl)
         CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

         CALL xios_update_calendar(ts)
      endif

!!! On donne la valeur du champ srf

      CALL xios_send_field("field_srf_2D",field_srf_2D)
      CALL xios_send_field("field_srf_3D",field_srf_3D)

!print*,'step3' ; call flush(6)
!!! On change de contexte

      CALL xios_get_handle(trim(oceid),ctx_hdl) 
     CALL xios_set_current_context(ctx_hdl)

!!! Mise a jour du pas de temps

      CALL xios_update_calendar(ts)

!!! On donne la valeur des champs oce

      CALL xios_send_field("field_oce_scalar",field_oce_2D(1,1)+ts)
      CALL xios_send_field("field_oce_2D",field_oce_2D)
      CALL xios_send_field("field_oce_3D",field_oce_3D)
      if (xios_is_valid_axis("transect_axis")) then
         ! Version with a distributed transect axis
         !call xios_send_field("transect_field",transects_field(ibegin_transects:ibegin_transects+itransects_size))
         ! Version with a non-distributed transect axis
         call xios_send_field("transect_field",transects_field(1:ntransects))
      endif

      CALL wait_us(int(elapsed_per_timestep*1.e6))   ! micro-secondes
      cdate=cdate+dtime
      ts=ts+1

   ENDDO

!####################################################################################
!!! Finalisation
!####################################################################################

!!! Fin des contextes

    print*,'context_finalize for'//trim(oceid)
    CALL xios_context_finalize()
    CALL xios_get_handle(trim(atmid),ctx_hdl)
    CALL xios_set_current_context(ctx_hdl)
    print*,'context_finalize for'//trim(atmid)
    CALL xios_context_finalize()
    if (trim(atmid) /= trim(srfid))  then 
       print*,'context_finalize for'//trim(srfid)
       CALL xios_get_handle(trim(srfid),ctx_hdl)
       CALL xios_set_current_context(ctx_hdl)
       CALL xios_context_finalize()
    endif

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






