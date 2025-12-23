#!/bin/bash

if [ ! -d logs ]; then
  mkdir logs
  touch logs/logfile
fi

if [ ! -f .env ]; then
    cp .env.example .env

    read -p "Enter RETAIL_CRM_API_KEY: " api_key
    read -p "Enter RETAIL_CRM_HOST: " host

    sed -i "s|RETAIL_CRM_API_KEY=.*|RETAIL_CRM_API_KEY=\"$api_key\"|" .env
    sed -i "s|RETAIL_CRM_HOST=.*|RETAIL_CRM_HOST=\"$host\"|" .env
fi
