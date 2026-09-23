#!/bin/bash

###############################################################################
# Bash скрипт для создания нового контейнера pysite-cont
# и перезапуска с именем pysite-cont-app
# Использование: sudo ./restart.sh
###############################################################################

set -e  # Выход при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции для вывода
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

###############################################################################
# ПРОВЕРКИ
###############################################################################

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
    log_error "Этот скрипт должен быть запущен с правами sudo"
    exit 1
fi

# Проверка ОС
if ! grep -qi debian /etc/os-release && ! grep -qi ubuntu /etc/os-release; then
    log_error "Этот скрипт работает только на Debian/Ubuntu"
    exit 1
fi

log_info "Начало установки и настройки сайта..."

sudo docker rm -f pysite-cont-app
sudo docker build -t pysite-cont .
sudo docker run -d --name=pysite-cont-app --restart=unless-stopped -p 127.0.0.1:8000:8000 --read-only --tmpfs /tmp --cap-drop=ALL pysite-cont
