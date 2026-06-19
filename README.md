# Trading Platform

## auth-service (microservice)

    - configure .env.local (using host.docker.internal instead of localhost cause only able to use postgresql inside docker)
    - install docker in windows
    - create .venv for each service and install dependencies (activate and deactivate)
        - python -m venv .venv
        - .venv/Scripts/activate
        - python -m pip install -r requirements-dev.txt
    - create postgresql instance inside docker container
        - docker run --name postgres-trading -e POSTGRES_USER=trading -e POSTGRES_PASSWORD=trading -e POSTGRES_DB=trading_platform -p 5432:5432 -d postgres
        - docker start postgres-trading
        - docker stop postgres-trading
    - verify docker container and connect DB
        - docker ps
        - docker exec -it postgres-trading psql -U trading -d trading_platform
        - CREATE DATABASE trading_platform; (if necessary)
        - docker rm -f postgres-trading (deletes container)
    - alembic process migration
        - alembic init migrations
        - alembic revision --autogenerate -m "create users table" (check files generated, add schema if necessary)
        - alembic upgrade head
    - after create protos, generate grpcs in protos directory
        - python -m grpc_tools.protoc -I . --python_out=generated --grpc_python_out=generated auth.proto
    - create test DB inside docker container
        - CREATE DATABASE trading_platform_test;
    - generate encrypted key, copy into .env.local
        - python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    - run tests (if running integration tests from gateway api, target database url to DB test)
        - pytest tests/unit, pytest tests/integration, pytest tests/grpc
    - run auth-service
        - python -m main
        
## gateway-api (microservice)

    - configure .env.local
    - test certificate and generate it in microservice root
        - openssl genrsa -out ca.key 4096
        - openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out cert.pem -subj "//CN=Local-CA"
        - create msauth folder
        - openssl req -new -nodes -newkey rsa:2048 -keyout msauth/key.pem -out msauth/ms1.csr -subj "//CN=msauth"
        - openssl x509 -req -in msauth/ms1.csr -CA cert.pem -CAkey ca.key -CAcreateserial -out msauth/cert.pem -days 365 -sha256
        - keep only ca.key and cert.pem (move files from msauth to MS root)
        - set AUTH_SERVICE_SECURE to true in .env.local
    - copy auth.proto from auth_service to gateway-api and generate stubs
        - python -m grpc_tools.protoc -I . --python_out=generated --grpc_python_out=generated auth.proto
    - run tests
        - pytest tests/unit, pytest tests/integration
    - run gateway-api
        - python -m main

## run with docker

    - docker-compose down -v
    - docker-compose up --build
    - docker exec -it trading_postgres psql -U trading -d trading_platform
    - create test DB inside docker container
        - CREATE DATABASE trading_platform_test;
    - enter container
        - docker exec -it auth_service bash

## signal-service (microservice)

    - alembic process migration
        - alembic init migrations
        - alembic revision --autogenerate -m "create configurations and signals tables"
        - alembic upgrade head

## web (React + TypeScript + Vite)

    - install dependencies
        - npm config set strict-ssl false / true (avoid ssl verification)
        - npm create vite@latest web
        - npm install
        - npm install react-router-dom axios
        - npm install @tanstack/react-query
        - npm install react-hook-form
        - npm install zod
        - npm install @hookform/resolvers
        - npm install uuid
        - npm install react-hot-toast
        - npm install --save-dev @types/react

## SQL commands for DB structure (do not run, alembic does migrations)

    - create schemas
        - CREATE SCHEMA auth;
        - CREATE SCHEMA signals;
    - create tables
        - CREATE TABLE auth.users (
            id UUID PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            telegram_token TEXT,
            telegram_chat_id TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP NULL
          );
        - CREATE TABLE signals.configurations (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            symbols JSONB NOT NULL,
            strategies JSONB NOT NULL,
            params JSONB,
            trend_timeframe VARCHAR(10) NOT NULL,
            context_timeframe VARCHAR(10) NULL,
            entry_timeframe VARCHAR(10) NOT NULL,
            enabled BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
        - CREATE TABLE signals.signals (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            symbol TEXT NOT NULL,
            strategy TEXT NOT NULL,
            signal TEXT NOT NULL,
            trend_timeframe VARCHAR(10) NOT NULL,
            context_timeframe VARCHAR(10) NULL,
            entry_timeframe VARCHAR(10) NOT NULL,
            price NUMERIC,
            signal_time TIMESTAMP NOT NULL,
            candle_time TIMESTAMP NOT NULL,
            dedup_key TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
    - create indexes
        - CREATE INDEX idx_signals_user_id ON signals.signals(user_id);
        - CREATE INDEX idx_signals_user_time ON signals.signals(user_id, signal_time DESC);
        - CREATE INDEX idx_signals_symbol ON signals.signals(symbol);
        - CREATE INDEX idx_signals_time ON signals.signals(signal_time);
        - CREATE UNIQUE INDEX uq_signals_dedup ON signals.signals(user_id, dedup_key, candle_time);
