---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Email Triage OpenEnv

A real-world email triage environment where AI agents classify, prioritize, and respond to emails.

## Tasks
- **spam_detection** (easy): Classify emails as spam or not_spam
- **priority_sorting** (medium): Label urgency and assign priority 1-3
- **full_triage** (hard): Label + prioritize + detect phishing + draft replies

## API Endpoints
- POST /reset
- POST /step  
- GET /state