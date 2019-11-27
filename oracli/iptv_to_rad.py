#!/usr/bin/python
import sys, os
import datetime
import psycopg2



PG_HOST=os.environ.get('PG_HOST', '127.0.0.1')
PG_USER=os.environ.get('PG_USER', 'snmpuser')
PG_PASS=os.environ.get('PG_PASSWORD', 'snmpuser')
PG_DATABASE=os.environ.get('PG_DATABASE', 'snmpdb')


connpg = psycopg2.connect(dbname=PG_DATABASE, user=PG_USER, password=PG_PASS, host=PG_HOST)
cursor = connpg.cursor()



print 'start: ', datetime.datetime.now()

daybefore = datetime.datetime.now() - datetime.timedelta(days=1)


try:
  import cx_Oracle
except ImportError,info:
  print "Import Error:",info
  sys.exit()

try:
  with cx_Oracle.connect('ap/ap@10.6.0.104/onyma') as conn:
    try:

      cur = conn.cursor()
      q="""
           SELECT DISTINCT 
           replace(REGEXP_SUBSTR(MM.SITENAME,'[0-9]+'),'','') as cid,
           AP."VALUE" AS mac,
           to_char(DS.BEGDATE, 'yyyy-mm-dd') as date1,
           to_char(DS.ENDDATE, 'yyyy-mm-dd') as date2,
           DS.DMID as sid,
           AP.CLOSED as status 
           FROM MAP_MAIN MM 
           LEFT JOIN DOG_SERV DS ON MM.DMID = DS.DMID 
           LEFT JOIN MAP_MAIN MM2 ON mm.dogid = mm2.dogid 
           JOIN AUTH_SPEC_PARAMS AP On AP.DMID = MM2.DMID 
           WHERE (MM.sitename LIKE 'tv%' OR MM.sitename LIKE 'iptv%') 
           AND MM.deldate IS NULL 
           AND MM2.deldate IS NULL 
           AND DS.ENDDATE IS NULL 
           AND AP.ATTRCOD = 205 
           AND DS.BEGDATE < SYSDATE 
           AND (DS.ENDDATE > SYSDATE OR DS.ENDDATE is null) 
           AND AP.CLOSED!=4 
           AND AP."VALUE" IS NOT NULL 
           AND AP.repl_id = (SELECT max(A.repl_id) FROM AUTH_SPEC_PARAMS A WHERE A.ATTRCOD=205 AND A.clsrv=AP.clsrv)
        """

      cur.execute(q)





      cursor.execute("TRUNCATE TABLE circuit")
      for col1, col2, col3, col4, col5, col6 in cur.fetchall():
          if col2 != None:
              #print col1, col2, col3, col4, col5, col6 
              cursor.execute("""INSERT INTO circuit (cid,circuit_id,date1,date2,sid,status) VALUES (%s,%s,%s,%s,%s,%s)""", (col1, col2, col3, col4, col5, col6))

      connpg.commit()


      cur.close()
      connpg.close()

    except cx_Oracle.DatabaseError, info:
      print "DB Error:", info
      cur.close()
      exit(0)

  print 'end:   ', datetime.datetime.now()

except cx_Oracle.DatabaseError, info:
  print "Logon Error:", info
  exit(0)
