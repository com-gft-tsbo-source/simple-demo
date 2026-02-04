#!/bin/sh
set -eu

TARGET_VALUE="${TARGET:-http://localhost:8081/temperature}"
export TARGET="$TARGET_VALUE"

envsubst '$TARGET' < /opt/frontend/config.template.js > /opt/frontend/config.js
