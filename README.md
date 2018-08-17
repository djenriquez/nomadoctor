# Nomadoctor
Simple, dockerized way to backup and restore your Nomad jobs

## Backup:
```sh
NOMAD_ENDPOINT=http://10.0.1.1:4646
JOBS_FILE=my_backup

docker run --rm \
djenriquez/nomadoctor:v0.1.0 \
--backup \
$NOMAD_ENDPOINT > $JOBS_FILE
```

## Restore:
Assuming that you are running the restore in the working directory that contains `$BACKUP_FILE`
```sh
NOMAD_ENDPOINT=http://10.0.1.1:4646
JOBS_FILE=my_backup

docker run --rm \
-v `pwd`:/restore \
djenriquez/nomadoctor:v0.1.0 \
--restore $JOBS_FILE \
$NOMAD_ENDPOINT
```