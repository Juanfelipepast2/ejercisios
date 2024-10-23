SELECT partido.IDPARTIDO,
       partido.IDTEMPORADA,
       partido.FECHAPARTIDO,
       -- ----------------------------------------------------
       local.nombreequipo AS EQUIPOLOCAL,
       PARTIDO.IDEQUIPOLOCAL,
       PARTIDO.IDTECNICOLOCAL,
       DTLOCAL.NOMBRETECNICO || ' ' || DTLOCAL.APELLIDOTECNICO AS NOMBREDTLOCAL,-- NOMBRE DEL TECNICO LOCAL
       /* ---------------------------------------- */
       COUNT(DISTINCT glocal.idgol) AS GOLESLOCAL,
       count(DISTINCT gvisitante.idgol) GOLESVISITANTE,
       -- -----------------------
       visitante.nombreequipo AS EQUIPOVISITANTE,
       PARTIDO.IDEQUIPOVISITANTE,
       PARTIDO.IDTECNICOVISITANTE,
       DTVISITANTE.NOMBRETECNICO || ' ' || DTVISITANTE.APELLIDOTECNICO AS NOMBREDTVISITANTE,-- NOMBRE DEL TECNICO LOCAL
       paRtido.amarillaslocalpartido AS AMARILLASLOCAL,
       partido.AMARILLASVISITANTEPARTIDO AS AMARILLASVISITANTE,
       PARTIDO.ROJASLOCALPARTIDO AS ROJASLOCAL,
       PARTIDO.ROJASLOCALPARTIDO AS ROJASVISITANTE
  FROM (
           (
               (
                   partido
                   LEFT JOIN
                   equipo AS local ON partido.IDEQUIPOLOCAL = local.idequipo
               )
               LEFT JOIN
               equipo AS visitante ON partido.IDEQUIPOVISITANTE = visitante.idequipo
           )
           LEFT JOIN
           gol AS glocal ON (glocal.idpartido = partido.IDPARTIDO AND 
                             glocal.idequipo = local.idequipo) 
           LEFT JOIN
           gol AS gvisitante ON gvisitante.idpartido = partido.IDPARTIDO AND 
                                gvisitante.idequipo = visitante.idequipo
       )
       LEFT JOIN
       tecnico AS DTLOCAL ON PARTIDO.IDTECNICOLOCAL = DTLOCAL.IDTECNICO
       LEFT JOIN
       tecnico AS DTVISITANTE ON PARTIDO.IDTECNICOVISITANTE = DTVISITANTE.IDTECNICO
 GROUP BY partido.IDPARTIDO;
;
