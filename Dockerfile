# stage to get the latest ergast db if not yet available
FROM python:3.10-alpine as ergastdata

VOLUME [ "/data" ]

RUN pip install python-dateutil requests
COPY get_latest_ergast_db.py /get_latest_ergast_db.py

RUN  ["/usr/local/bin/python","/get_latest_ergast_db.py"]

FROM mariadb:latest
COPY --from=ergastdata /data/ergast_f1db.sql.gz /docker-entrypoint-initdb.d/


