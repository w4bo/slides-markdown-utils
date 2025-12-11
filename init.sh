#!/bin/bash
set -xo
[ ! -f publish.sh ] && cp utils/publish.sh.example publish.sh
# ln -s utils/_quarto.yml _quarto.yml
[ ! -f _quarto.yml ] && cp utils/_quarto.yml _quarto.yml
[ ! -f docker-compose.yml ] && cp utils/docker-compose.yml docker-compose.yml