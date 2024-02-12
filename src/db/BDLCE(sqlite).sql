/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     5/02/2024 10:54:52 p. m.                     */
/*==============================================================*/

drop table if exists EQUIPO;

drop table if exists EQUIPOTEMPORADA;

drop table if exists GOL;

drop table if exists JUGADOR;

drop table if exists JUGADORTEMPORADA;

drop table if exists NEGOCIOS;

drop table if exists PAIS;

drop table if exists PARTIDO;

drop table if exists POSICION;

drop table if exists RRESET;

drop table if exists STATS;

drop table if exists TECNICO;

drop table if exists TECNICOTEMPORADA;

drop table if exists TEMPORADA;

/*==============================================================*/
/* Table: EQUIPO                                                */
/*==============================================================*/
create table EQUIPO 
(
   IDEQUIPO             INTEGER PRIMARY KEY,
   IDRESET              INTEGER              not null,
   IDTECNICO INTEGER NOT NULL,
   NOMBREEQUIPO         varchar(20)         not null,
   ESCUDOEQUIPO         BLOB,
   PRESUPUESTOINICIAL   int not null,
   constraint FK_EQUIPO_EQUIPO_A__RRESET foreign key (IDRESET)
      references RRESET (IDRESET),
	constraint FK_PRIMER_DT foreign key (IDTECNICO)
      references TECNICO (IDTECNICO) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: EQUIPOTEMPORADA                                       */
/*==============================================================*/
create table EQUIPOTEMPORADA
(
   IDEQUIPO             int not null,
   IDTEMPORADA          int not null,
   PRESUPUESTO          int not null,
   primary key (IDTEMPORADA, IDEQUIPO),
   constraint FK_EQUIPOTEMPORADA foreign key (IDTEMPORADA)
      references TEMPORADA (IDTEMPORADA) on delete restrict on update restrict,
	constraint FK_EQUIPOTEMPORADA2 foreign key (IDEQUIPO)
      references EQUIPO (IDEQUIPO) on delete restrict on update restrict
	  
);

/*==============================================================*/
/* Table: GOL                                                   */
/*==============================================================*/
create table GOL
(
   IDGOL                INTEGER PRIMARY KEY,
   IDPARTIDO            int not null,
   IDJUGADOR            int not null,
   IDTEMPORADA          int not null,
   IDEQUIPO             int not null,
   constraint FK_ANOTADOR foreign key (IDJUGADOR, IDTEMPORADA, IDEQUIPO)
      references JUGADORTEMPORADA (IDJUGADOR, IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict,
	constraint FK_SE_ANOTO_EN foreign key (IDPARTIDO)
      references PARTIDO (IDPARTIDO) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: JUGADOR                                               */
/*==============================================================*/
create table JUGADOR
(
   IDJUGADOR            INTEGER PRIMARY KEY,
   IDPAIS               int not null,
   NOMBREJUGADOR        varchar(20) not null,
   APELLIDOJUGADOR      varchar(20) not null,
   FECHANACIMIENTOJUGADOR date not null,
   LINKTRANSFERMRKTJUGADOR varchar(200) not null,
   PIEJUGADOR           bool not null,
   ESTATURAJUGADOR      int not null
   constraint CKC_ESTATURAJUGADOR_JUGADOR check (ESTATURAJUGADOR between 130 and 300),
   FOTOJUGADOR          longblob,
   ESTADOJUGADOR        bool not null,
   BANDAJUGADOR         char(3)
   constraint CKC_BANDAJUGADOR_JUGADOR check (BANDAJUGADOR is null or (BANDAJUGADOR in ('IZQ','DER','AMB'))),
   constraint FK_ES_CIUDADANO_DE foreign key (IDPAIS)
      references PAIS (IDPAIS) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: JUGADORTEMPORADA                                      */
/*==============================================================*/
create table JUGADORTEMPORADA
(
   IDJUGADOR            int not null,
   IDTEMPORADA          int not null,
   IDEQUIPO             int not null,
   primary key (IDJUGADOR, IDTEMPORADA, IDEQUIPO),
   constraint FK_JUGO_TEMPORADA foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict,
	constraint FK_TUVO_A_JUGADOR foreign key (IDTEMPORADA, IDEQUIPO)
      references EQUIPOTEMPORADA (IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: NEGOCIOS                                              */
/*==============================================================*/
create table NEGOCIOS
(
   IDNEGOCIO            INTEGER PRIMARY KEY,
   ESTADONEGOCIO        bool not null,
   MONTONEGOCIANTE1     int not null default 0,
   MONTONEGOCIANTE2     int not null default 0
);

/*==============================================================*/
/* Table: PAIS                                                  */
/*==============================================================*/
create table PAIS
(
   IDPAIS               INTEGER PRIMARY KEY,
   NOMBREPAIS           varchar(20) not null,
   BANDERAPAIS          longblob not null
);

/*==============================================================*/
/* Table: PARTIDO                                               */
/*==============================================================*/
create table PARTIDO
(
   IDPARTIDO            INTEGER PRIMARY KEY,
   IDTECNICOLOCAL       int not null,
   IDEQUIPOLOCAL        int not null,
   IDTECNICOVISITANTE   int not null,
   IDEQUIPOVISITANTE    int not null,
   IDTEMPORADA          int not null,
   FECHAPARTIDO         smallint not null,
   AMARILLASLOCALPARTIDO smallint not null default 0,
   ROJASLOCALPARTIDO    smallint not null default 0,
   AMARILLASVISITANTEPARTIDO smallint not null default 0,
   ROJASVISITANTEPARTIDO smallint not null default 0,
   FASEPARTIDO          char(3) not null,
   constraint CKC_FASEPARTIDO_PARTIDO check (FASEPARTIDO in ('tct','cp8','cp4','cps','cpf','pr4','prs','prf','po4','pos','pof','sp4','sps','spf')),
   constraint FK_LOCAL_DIRIGE foreign key (IDTECNICOLOCAL, IDEQUIPOLOCAL)
      references TECNICOTEMPORADA (IDTECNICO, IDEQUIPO) on delete restrict on update restrict,
	constraint FK_SE_JUGO_EN foreign key (IDTEMPORADA)
      references TEMPORADA (IDTEMPORADA) on delete restrict on update restrict,
	constraint FK_VISITANTE_DIRIGE foreign key (IDTECNICOVISITANTE, IDEQUIPOVISITANTE)
      references TECNICOTEMPORADA (IDTECNICO, IDEQUIPO) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: POSICION                                              */
/*==============================================================*/
create table POSICION
(
   ABREVIATURAPOSICION  varchar(3) not null
   constraint CKC_ABREVIATURAPOSICI_POSICION check (ABREVIATURAPOSICION in ('PO','LIB','CT','CA','LA','CCD','CC','VOL','EXT','SD')),
   IDJUGADOR            int not null,
   POSICIONPRINCIPAL    bool not null,
   primary key (ABREVIATURAPOSICION, IDJUGADOR),
   constraint FK_RELATIONSHIP_16 foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: RRESET                                                */
/*==============================================================*/
create table RRESET
(
   IDRESET              INTEGER PRIMARY KEY,
   NOMBRERESET          varchar(20) not null,
   FECHAINICIORESET     date not null,
   FECHAFINRESET        date
);

/*==============================================================*/
/* Table: STATS                                                 */
/*==============================================================*/
create table STATS
(
	IDJUGADOR            int              not null,
   ATAQUESTAT           SMALLINT             default 50 not null
      constraint CKC_ATAQUESTAT_STATS check (ATAQUESTAT between 0 and 100),
   DEFENSASTAT          SMALLINT             default 50 not null
      constraint CKC_DEFENSASTAT_STATS check (DEFENSASTAT between 0 and 100),
   ESTABILIDADSTATS     SMALLINT             default 50 not null
      constraint CKC_ESTABILIDADSTATS_STATS check (ESTABILIDADSTATS between 0 and 100),
   RESISTENCIASTATS     SMALLINT             default 50 not null
      constraint CKC_RESISTENCIASTATS_STATS check (RESISTENCIASTATS between 0 and 100),
   VELMAXIMASTATS       SMALLINT             default 50 not null
      constraint CKC_VELMAXIMASTATS_STATS check (VELMAXIMASTATS between 0 and 100),
   ACELERACIONSTATS     SMALLINT             default 50 not null
      constraint CKC_ACELERACIONSTATS_STATS check (ACELERACIONSTATS between 0 and 100),
   RESPUESTASTATS       SMALLINT             default 50 not null
      constraint CKC_RESPUESTASTATS_STATS check (RESPUESTASTATS between 0 and 100),
   AGILIDADSTATS        SMALLINT             default 50 not null
      constraint CKC_AGILIDADSTATS_STATS check (AGILIDADSTATS between 0 and 100),
   PRECISIONCONDUCCIONSTATS SMALLINT             default 50 not null
      constraint CKC_PRECISIONCONDUCCI_STATS check (PRECISIONCONDUCCIONSTATS between 0 and 100),
   VELCONDUCCIONSTATS   SMALLINT             default 50 not null
      constraint CKC_VELCONDUCCIONSTAT_STATS check (VELCONDUCCIONSTATS between 0 and 100),
   PRECPASECORTOSTATS   SMALLINT             default 50 not null
      constraint CKC_PRECPASECORTOSTAT_STATS check (PRECPASECORTOSTATS between 0 and 100),
   VELPASECORTOSTATS    SMALLINT             default 50 not null
      constraint CKC_VELPASECORTOSTATS_STATS check (VELPASECORTOSTATS between 0 and 100),
   PRECPASELARGOSTATS   SMALLINT             default 50 not null
      constraint CKC_PRECPASELARGOSTAT_STATS check (PRECPASELARGOSTATS between 0 and 100),
   VELPASELARGOSTATS    SMALLINT             default 50 not null
      constraint CKC_VELPASELARGOSTATS_STATS check (VELPASELARGOSTATS between 0 and 100),
   PRECTIROSTATS        SMALLINT             default 50 not null
      constraint CKC_PRECTIROSTATS_STATS check (PRECTIROSTATS between 50 and 100),
   POTTIROSTATS         SMALLINT             default 50 not null
      constraint CKC_POTTIROSTATS_STATS check (POTTIROSTATS between 0 and 100),
   TECDISPAROSTATS      SMALLINT             default 50 not null
      constraint CKC_TECDISPAROSTATS_STATS check (TECDISPAROSTATS between 0 and 100),
   PRECSAQFALTASTATS    SMALLINT             default 50 not null
      constraint CKC_PRECSAQFALTASTATS_STATS check (PRECSAQFALTASTATS between 0 and 100),
   EFECTOSTATS          SMALLINT             default 50 not null
      constraint CKC_EFECTOSTATS_STATS check (EFECTOSTATS between 0 and 100),
   CABEZAZOSTATS        SMALLINT             default 50 not null
      constraint CKC_CABEZAZOSTATS_STATS check (CABEZAZOSTATS between 0 and 100),
   SALTOSTATS           SMALLINT             default 50 not null
      constraint CKC_SALTOSTATS_STATS check (SALTOSTATS between 0 and 100),
   TECNICASTATS         SMALLINT             default 50 not null
      constraint CKC_TECNICASTATS_STATS check (TECNICASTATS between 0 and 100),
   AGRESIVIDADSTATS     SMALLINT             default 50 not null
      constraint CKC_AGRESIVIDADSTATS_STATS check (AGRESIVIDADSTATS between 0 and 100),
   MENTALIDADSTATS      SMALLINT             default 50 not null
      constraint CKC_MENTALIDADSTATS_STATS check (MENTALIDADSTATS between 0 and 100),
   CUALIDADESPORTEROSTATS SMALLINT             default 50 not null
      constraint CKC_CUALIDADESPORTERO_STATS check (CUALIDADESPORTEROSTATS between 0 and 100),
   TRAEQUIPOSTATS       SMALLINT             default 50 not null
      constraint CKC_TRAEQUIPOSTATS_STATS check (TRAEQUIPOSTATS between 0 and 100),
   ESTADOFORMASTATS     SMALLINT             default 4 not null
      constraint CKC_ESTADOFORMASTATS_STATS check (ESTADOFORMASTATS between 0 and 8),
   PRECPIEMALOSTATS     SMALLINT             default 4 not null
      constraint CKC_PRECPIEMALOSTATS_STATS check (PRECPIEMALOSTATS between 0 and 8),
   FRECPIEMALOSTATS     SMALLINT             default 4 not null
      constraint CKC_FRECPIEMALOSTATS_STATS check (FRECPIEMALOSTATS between 0 and 8),
   RESISTENCIALESIONESSTATS SMALLINT             default 4 not null
      constraint CKC_RESISTENCIALESION_STATS check (RESISTENCIALESIONESSTATS between 0 and 8),
   HABREGATESTATS       bool not null,
   HABREGATEHABILSTATS  bool not null,
   HABCAPPOSICIONSTATS  bool not null,
   HABREACCIONSTATS     bool not null,
   HABCAPMANDOSTATS     bool not null,
   HABPASESTATS         bool not null,
   HABGOLEADORASTATS    bool not null,
   HABGOL1A1STATS       bool not null,
   HABJUGADORPOSTESTATS bool not null,
   HABLINEASSTATS       bool not null,
   HABDISPARIOSMEDIOSSTATS bool not null,
   HABLADOSTATS         bool not null,
   HABCENTROSTATS       bool not null,
   HABLANZAPENALESSTATS bool not null,
   HABPASE1TOQUESTATS   bool not null,
   HANEXTERIORSTATS     bool not null,
   HABMARCARHOMBRESTATS bool not null,
   HABBARRIDASTATS      bool not null,
   HABMARCAJESTATS      bool not null,
   HABLINEADEFENSASTATS bool not null,
   HABPORTEROPENALESSTATS bool not null,
   HABPORTERO1V1STATS   bool not null,
   HABSAQUELARGO        bool not null default 50,
   primary key (IDJUGADOR),
   constraint FK_JUGADOR_STATS foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: TECNICO                                               */
/*==============================================================*/
create table TECNICO
(
   IDTECNICO            INTEGER PRIMARY KEY,
   IDPAIS               int not null,
   NOMBRETECNICO        varchar(20) not null,
   APELLIDOTECNICO      varchar(20) not null,
   CONTRASENATECNICO    varchar(30) not null,
   ADMINTECNICO         bool not null,
   OWNERTECNICO         bool not null,
   constraint FK_TIENE_COMO_NACIONALIDAD foreign key (IDPAIS)
      references PAIS (IDPAIS) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: TECNICOTEMPORADA                                      */
/*==============================================================*/
create table TECNICOTEMPORADA
(
   IDTECNICO            int not null,
   IDEQUIPO             int not null,
   IDTEMPORADA          int not null,
   primary key (IDTECNICO, IDEQUIPO, IDTEMPORADA),
   constraint FK_DIRIGE_TEMPORADA foreign key (IDTECNICO)
      references TECNICO (IDTECNICO) on delete restrict on update restrict,
   constraint FK_EQUIPO_POR_TEMPORADA foreign key (IDTEMPORADA, IDEQUIPO)
      references EQUIPOTEMPORADA (IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: TEMPORADA                                             */
/*==============================================================*/
create table TEMPORADA
(
   IDTEMPORADA          INTEGER PRIMARY KEY,
   IDRESET              int not null,
   NOMBRETEMPORADA      varchar(15) not null,
   FECHAINICIOTEMPORADA date not null,
   FECHAFINTEMPORADA    date,
   constraint FK_PERTENECE foreign key (IDRESET)
      references RRESET (IDRESET) on delete restrict on update restrict
);

/*alter table EQUIPO
   add constraint FK_EQUIPO_EQUIPO_A__RRESET foreign key (IDRESET)
      references RRESET (IDRESET);
*/
/*
alter table EQUIPOTEMPORADA add constraint FK_EQUIPOTEMPORADA foreign key (IDTEMPORADA)
      references TEMPORADA (IDTEMPORADA) on delete restrict on update restrict;
*/

/*
alter table EQUIPOTEMPORADA add constraint FK_EQUIPOTEMPORADA2 foreign key (IDEQUIPO)
      references EQUIPO (IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table GOL add constraint FK_ANOTADOR foreign key (IDJUGADOR, IDTEMPORADA, IDEQUIPO)
      references JUGADORTEMPORADA (IDJUGADOR, IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table GOL add constraint FK_SE_ANOTO_EN foreign key (IDPARTIDO)
      references PARTIDO (IDPARTIDO) on delete restrict on update restrict;
*/

/*
alter table JUGADOR add constraint FK_ES_CIUDADANO_DE foreign key (IDPAIS)
      references PAIS (IDPAIS) on delete restrict on update restrict;
*/

/*
alter table JUGADORTEMPORADA add constraint FK_JUGO_TEMPORADA foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict;
*/

/*
alter table JUGADORTEMPORADA add constraint FK_TUVO_A_JUGADOR foreign key (IDTEMPORADA, IDEQUIPO)
      references EQUIPOTEMPORADA (IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table PARTIDO add constraint FK_LOCAL_DIRIGE foreign key (IDTECNICOLOCAL, IDEQUIPOLOCAL)
      references TECNICOTEMPORADA (IDTECNICO, IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table PARTIDO add constraint FK_SE_JUGO_EN foreign key (IDTEMPORADA)
      references TEMPORADA (IDTEMPORADA) on delete restrict on update restrict;
*/

/*
alter table PARTIDO add constraint FK_VISITANTE_DIRIGE foreign key (IDTECNICOVISITANTE, IDEQUIPOVISITANTE)
      references TECNICOTEMPORADA (IDTECNICO, IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table POSICION add constraint FK_RELATIONSHIP_16 foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict;
*/

/*
alter table STATS add constraint FK_JUGADOR_STATS foreign key (IDJUGADOR)
      references JUGADOR (IDJUGADOR) on delete restrict on update restrict;
*/

/*
alter table TECNICO add constraint FK_TIENE_COMO_NACIONALIDAD foreign key (IDPAIS)
      references PAIS (IDPAIS) on delete restrict on update restrict;
*/

/*
alter table TECNICOTEMPORADA add constraint FK_DIRIGE_TEMPORADA foreign key (IDTECNICO)
      references TECNICO (IDTECNICO) on delete restrict on update restrict;
*/

/*
alter table TECNICOTEMPORADA add constraint FK_EQUIPO_POR_TEMPORADA foreign key (IDTEMPORADA, IDEQUIPO)
      references EQUIPOTEMPORADA (IDTEMPORADA, IDEQUIPO) on delete restrict on update restrict;
*/

/*
alter table TEMPORADA add constraint FK_PERTENECE foreign key (IDRESET)
      references RRESET (IDRESET) on delete restrict on update restrict;
*/
