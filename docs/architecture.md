# The Better Credit — Architecture

## Overview
India's smartest credit card reward optimizer. 
Given a transaction, the system recommends the best credit card to use for maximum rewards.

## Stack
- **Backend:** FastAPI + PostgreSQL (Supabase) + SQLAlchemy
- **Chrome Extension:** React + TypeScript + Manifest V3
- **Mobile App:** Flutter + Dart + Riverpod

## Folder Structure
The-Better-Credit/
├── backend/          # FastAPI server
│   ├── routers/      # URL endpoints (one file per feature)
│   ├── models/       # Database tables (SQLAlchemy)
│   ├── schemas/      # Data shapes for validation (Pydantic)
│   └── database.py   # DB connection
├── rules/            # JSON reward rules per card
├── app/              # Flutter mobile app
├── extension/        # Chrome extension
└── docs/             # Architecture documentation
## Core Logic Flow
1. User inputs a merchant + amount
2. Rule engine checks all user's cards
3. Each card is scored based on reward rules
4. API returns ranked list with explanation

## Phases
- Phase 1 — Cards API (current)
- Phase 2 — Database + SQLAlchemy
- Phase 3 — Rule Engine
- Phase 4 — JWT Auth
- Phase 5 — Chrome Extension
- Phase 6 - Flutter App