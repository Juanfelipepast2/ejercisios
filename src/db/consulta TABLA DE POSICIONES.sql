WITH STATS AS (
SELECT EQUIPO.IDEQUIPO,
       EQUIPO.NOMBREEQUIPO,
       COUNT(DISTINCT PARTIDOCOMPLETO.IDPARTIDO) AS PJ,
       COUNT(DISTINCT CASE WHEN ( (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL AND 
                                   PARTIDOCOMPLETO.GOLESLOCAL > PARTIDOCOMPLETO.GOLESVISITANTE) OR 
                                  (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOVISITANTE AND 
                                   PARTIDOCOMPLETO.GOLESVISITANTE > PARTIDOCOMPLETO.GOLESLOCAL) ) THEN EQUIPO.IDEQUIPO END) AS PG,
       COUNT(DISTINCT CASE WHEN ( (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL OR 
                                   EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOVISITANTE) AND 
                                  PARTIDOCOMPLETO.GOLESLOCAL = PARTIDOCOMPLETO.GOLESVISITANTE) THEN EQUIPO.IDEQUIPO END) AS PE,
       COUNT(DISTINCT CASE WHEN ( (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL AND 
                                   PARTIDOCOMPLETO.GOLESLOCAL < PARTIDOCOMPLETO.GOLESVISITANTE) OR 
                                  (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOVISITANTE AND 
                                   PARTIDOCOMPLETO.GOLESVISITANTE < PARTIDOCOMPLETO.GOLESLOCAL) ) THEN EQUIPO.IDEQUIPO END) AS PP,
       SUM(CASE WHEN EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL THEN PARTIDOCOMPLETO.GOLESLOCAL ELSE PARTIDOCOMPLETO.GOLESVISITANTE END) AS GF,
       SUM(CASE WHEN EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL THEN PARTIDOCOMPLETO.GOLESVISITANTE ELSE PARTIDOCOMPLETO.GOLESLOCAL END) AS GC
  FROM EQUIPO
       LEFT JOIN
       EQUIPOTEMPORADA ON EQUIPO.IDEQUIPO = EQUIPOTEMPORADA.IDEQUIPO
       INNER JOIN
       PARTIDOCOMPLETO ON ( (EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOLOCAL OR 
                             EQUIPO.IDEQUIPO = PARTIDOCOMPLETO.IDEQUIPOVISITANTE) AND 
                            (EQUIPOTEMPORADA.IDTEMPORADA = PARTIDOCOMPLETO.IDTEMPORADA) )        
 GROUP BY EQUIPO.IDEQUIPO
)

SELECT *, GF - GC as DG, (((PG * 3) + PE)/(PJ * 3))*100 as RENDIMIENTO, (PG * 3) + PE AS PTS FROM STATS 
ORDER BY PTS DESC, DG DESC, GF DESC, GC ASC
