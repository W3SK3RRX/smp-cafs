#!/bin/bash

# Diretório onde os backups serão armazenados
BACKUP_DIR="/home/suporte/Documentos/smp-cafs/backups"

# Nome do arquivo de backup (inclui a data atual)
BACKUP_FILE="backup_$(date +%Y-%m-%d_%H-%M-%S).sql"

# Executa o backup usando pg_dump
docker exec -t db pg_dump -U smpcafs smpcafs > "$BACKUP_DIR/$BACKUP_FILE"