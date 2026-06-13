# Trading Platform

## Local environment

    - install docker in windows
    - run postgresql instance inside docker
        - docker run --name postgres-trading -e POSTGRES_USER=trading -e POSTGRES_PASSWORD=trading -e POSTGRES_DB=trading_platform -p 5432:5432 -d postgres
    - verify docker container and connect DB
        - docker ps
        - docker exec -it postgres-trading psql -U trading -d trading_platform
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
        - CREATE TABLE signals.configs (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            symbols JSONB NOT NULL,
            strategies JSONB NOT NULL,
            params JSONB,
            timeframes JSONB NOT NULL,
            enabled BOOLEAN DEFAULT TRUE,
            execution_interval INTEGER DEFAULT 60,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
          );
        - CREATE TABLE signals.signals (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            symbol TEXT NOT NULL,
            strategy TEXT NOT NULL,
            signal TEXT NOT NULL,
            timeframes TEXT NOT NULL,
            price NUMERIC,
            time TIMESTAMP NOT NULL,
            candle_time TIMESTAMP NOT NULL,
            dedup_key TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE SET NULL
          );
        - CREATE TABLE signals.logs (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
    - create indexes
        - CREATE INDEX idx_signals_user_id ON signals.signals(user_id);
        - CREATE INDEX idx_signals_user_time ON signals.signals(user_id, time DESC);
        - CREATE INDEX idx_signals_symbol ON signals.signals(symbol);
        - CREATE INDEX idx_signals_time ON signals.signals(time);
        - CREATE UNIQUE INDEX uq_signals_dedup ON signals.signals(user_id, dedup_key, candle_time);
    - create .venv for each service and install dependencies (activate and deactivate)
        - python -m venv .venv
        - .venv/Scripts/activate
        - python -m pip install -r requirements-dev.txt
        