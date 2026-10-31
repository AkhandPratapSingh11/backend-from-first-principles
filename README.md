# Backend from First Principles

> Comprehensive master notes, architectural diagrams, and tooling derived from the complete **Backend from first principles** curriculum.

---

## 📖 Overview

This repository contains comprehensive, production-grade learning notes and reference documentation covering the entire spectrum of modern backend systems engineering. Every concept is distilled from foundational principles—ranging from raw network packets and operating system syscalls to distributed storage, real-time protocols, and container orchestration.

In addition to the master study notes, this repository includes an automated Python pipeline for extracting, cleaning, and compiling video transcripts from any YouTube playlist.

---

## 📂 Repository Structure

```
.
├── notes/
│   └── COMPLETE_BACKEND_NOTES.md      # Master 31-Chapter backend guide (2,500+ lines, 57 diagrams)
├── get_playlist_transcripts.py        # Automated YouTube playlist transcript downloader & merger
├── requirements.txt                   # Dependencies for playlist transcript extractor
├── .gitignore                         # Python, venv, and local transcript ignores
└── README.md                          # Repository documentation
```

---

## 📚 Curriculum & Notes Outline

The master guide in [`notes/COMPLETE_BACKEND_NOTES.md`](notes/COMPLETE_BACKEND_NOTES.md) covers 8 core architectural modules across 31 in-depth chapters:

### Module 1: Foundations, Architecture & The HTTP Protocol
- **Chapter 01 (Video 001):** The 28 Architectural Pillars of Modern Backend Systems
- **Chapter 02 (Video 002):** Mindset & The 3 Learning Phases (Philosophy → Polyglot Code → Production Systems)
- **Chapter 03 (Video 003):** Physical Request Flow (DNS → Security Group → Nginx → Node/PM2 → DB), State Centralization, and Why Frontends Cannot Be Backends
- **Chapter 04 (Video 004):** The ROI of Learning Backend Engineering from First Principles
- **Chapter 05 (Video 005):** Deep Dive into HTTP (L4 TCP vs L7 HTTP, HTTP/1.0 through HTTP/3 QUIC, Head-of-Line Blocking, Headers, Methods & Idempotency, CORS Preflight Flow, Status Codes, Caching & ETags)

### Module 2: Core Web API Mechanics & Application Architecture
- **Chapter 06 (Video 006):** Routing Tables `(METHOD, PATH)`, Dynamic Segments, Query vs Path Parameters, Nesting, and API Versioning
- **Chapter 07 (Video 007):** Serialization & Deserialization across Heterogeneous Runtimes, Text (JSON/XML) vs Binary (Protobuf), and JSON Grammar Limits
- **Chapter 08 (Video 008):** AuthN vs AuthZ, Historical Evolution, Stateful Sessions vs Stateless JWTs, Cookies (`HttpOnly`, `Secure`, `SameSite`), OAuth 2.0 / OIDC Delegation, RBAC/ABAC/ReBAC, User Enumeration & Timing Attacks
- **Chapter 09 (Video 009):** Boundary Defense, Fail-Fast Principle, Syntactic/Semantic/Type Validation, and Data Normalization
- **Chapter 10 (Video 010):** Layered Architecture (Controllers vs Services vs Repositories), Middleware Pipeline Order, and Request Context
- **Chapter 11 (Video 011):** Roy Fielding's 6 REST Constraints, URI Modeling, Offset vs Cursor/Keyset Pagination, and Standardized Envelopes

### Module 3: Persistence, Caching & Search Engine Architecture
- **Chapter 12 (Video 012):** PostgreSQL Architecture, Flat File Limitations, Data Types (`TEXT` vs `VARCHAR`, `NUMERIC` vs `FLOAT`, `TIMESTAMPTZ`, UUIDs, `JSON` vs `JSONB`), Constraints, Migrations, Soft Deletes, and B-Tree Indexing (`EXPLAIN ANALYZE`)
- **Chapter 13 (Video 013):** Memory Hierarchy, Caching Layers, Cache-Aside vs Write-Through vs Write-Back, Eviction (LRU/LFU/TTL), Cache Stampede/Thundering Herd (Mutexes, XFetch), and Cache Penetration (Bloom Filters)
- **Chapter 14 (Video 015):** Why SQL `ILIKE` Fails, Inverted Index Internals, Analysis Pipelines (Tokenizers, Stemming, Stop Words), `text` vs `keyword`, and BM25 Relevance Scoring

### Module 4: Asynchronous Processing, Real-Time & Event-Driven Systems
- **Chapter 15 (Video 014):** Synchronous Latency Traps, Task Queue Architecture (Producers, Brokers, Consumers), Priority Queues, DAG Workflows, Exponential Backoff with Jitter, Dead Letter Queues (DLQ), and Worker Idempotency
- **Chapter 16 (Video 026):** Polling vs SSE vs WebSockets, Handshake Protocol (`101 Switching Protocols`), Linux File Descriptors (`ulimit -n`), and Cross-Instance Scaling with Redis Pub/Sub
- **Chapter 17 (Video 030):** Webhooks as Reverse APIs, HMAC-SHA256 Signatures, Raw Body Verification, Constant-Time Comparison, Replay Defenses, and Provider SSRF Safeguards

### Module 5: Scalable Object Storage & Unstructured Data
- **Chapter 18 (Video 024):** Object Storage Flat Namespace, Availability vs 11 9s Durability, and Direct Pre-signed `PUT` URLs
- **Chapter 19 (Video 025):** Multipart Upload Protocol (Initiation → Parallel 5–10MB Chunk Uploads → Complete Assembly), Lifecycle Auto-Abort Rules, Pre-signed `GET` URLs, and CDN Edge Delivery

### Module 6: Resilience, Configuration & Observability
- **Chapter 20 (Video 016):** Error Taxonomy (Programmer vs Operational vs Client), Fail-Fast Boot, Centralized Error Middleware, Information Disclosure Sanitization, Timeouts, and Circuit Breakers
- **Chapter 21 (Video 017):** 12-Factor Config (Factor III), `.env` vs `.env.example`, Cloud Secrets Managers, and Boot Schema Validation
- **Chapter 22 (Video 018):** Logs vs Metrics vs Traces, Structured JSON Logging, Log Levels, PII Masking, Latency Percentiles (p50, p95, p99), and OpenTelemetry
- **Chapter 23 (Video 019):** Catastrophic Abrupt Kills vs Graceful Shutdown, POSIX Signals (`SIGINT`, `SIGTERM`, `SIGKILL`), In-Flight Request Draining, Connection Pool Teardowns, and Timeout Safeguards

### Module 7: Security Engineering & High-Performance Scaling
- **Chapter 24 (Video 020):** Defense in Depth, SQL Injection, Slow Password Hashing (Argon2id/bcrypt with Salt & Cost Factors), BOLA/IDOR Tenant Scoping, XSS, CSRF, and Security Headers
- **Chapter 25 (Video 021):** Latency vs Throughput, CPU Flame Graphs, Profiling before Optimizing, Missing Indexes, N+1 Query Batching, and Connection Pool Sizing
- **Chapter 26 (Video 022):** Vertical vs Horizontal Scaling, L4 vs L7 Load Balancers, Read Replicas, WAL Streaming Replication, and Read-Your-Own-Writes Consistency
- **Chapter 27 (Video 023):** Concurrency vs Parallelism, I/O-Bound vs CPU-Bound Profiles, OS Threads vs Event Loop vs Goroutines (2 KB Stack & M:N Scheduler), Race Conditions, Mutexes, and Deadlocks

### Module 8: Quality Engineering, Cloud-Native Standards & DevOps
- **Chapter 28 (Video 027):** Testing Pyramid, Test Doubles (Dummies, Stubs, Spies, Mocks, Fakes), Testcontainers for Real DBs, TDD (Red-Green-Refactor), Flaky Test Quarantine, and Cyclomatic Complexity (≤ 10)
- **Chapter 29 (Video 028):** Exhaustive Breakdown of All Twelve Factors in the 12-Factor App Methodology
- **Chapter 30 (Video 029):** OpenAPI 3.x Specifications, Design-First Workflows, Mock Servers (Prism), and Automated SDK Generation
- **Chapter 31 (Video 031):** DevOps for Backends, CI/CD, Linux Namespaces & Cgroups, Multi-Stage Distroless Dockerfiles, Kubernetes Primitives (Pods, Deployments, Services), Zero-Downtime Deployments, and Blameless Post-Mortems

---

## 🛠️ Tooling: Playlist Transcript Downloader

The included script [`get_playlist_transcripts.py`](get_playlist_transcripts.py) downloads and processes transcripts from any YouTube playlist.

### Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage
```bash
# Run with default playlist ("Backend from first principles")
python get_playlist_transcripts.py

# Or pass a custom playlist URL
python get_playlist_transcripts.py --playlist-url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

Transcripts are extracted video-by-video with timestamps and merged into `transcripts/<Playlist_Name>/000_ALL_TRANSCRIPTS_COMBINED.txt`.
