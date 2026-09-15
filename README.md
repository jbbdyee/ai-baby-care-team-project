![베베온 배너](assets/ai-baby-care-banner.png)

# 베베온 (AI Baby Care Assistant)

> **Single Agent + MCP + RAG 기반 맞춤형 육아 지원 서비스**

0~36개월 영유아 보호자가 육아 기록을 관리하고, 아기의 정보와 최근 기록을 기반으로 맞춤형 육아 정보를 제공받을 수 있도록 개발한 **4인 팀 프로젝트**입니다.

단순한 LLM 챗봇이 아니라 **Single Agent가 사용자의 요청을 판단하고 필요한 MCP Tool을 선택하여 실행하는 구조**로 구현했습니다.

> ### 📌 Repository Notice
>
> 본 저장소는 AI 멀티 에이전트 개발자 과정에서 진행한 팀 프로젝트를 기반으로, **개인 포트폴리오 및 추가 학습·개선을 위해 재구성한 저장소**입니다.
>
> 팀 프로젝트의 전체 구조와 기능은 유지하면서, 제가 담당한 **Baby Care MCP Server** 구현 영역과 프로젝트 종료 후 개인적으로 개선하는 내용을 구분하여 기록합니다.
>
> **Original Team Repository**  
> https://github.com/jyeyeyej/team3_AI_Baby_Care_Assistant

---

## 📌 Project Overview

| 항목 | 내용 |
| --- | --- |
| 프로젝트 | AI Baby Care Assistant |
| 팀명 | 응애이전트 |
| 인원 | 4명 |
| 개발 기간 | 2026.09.08 ~ 2026.09.10 |
| 프로젝트 형태 | AI Agent 팀 프로젝트 |
| 담당 영역 | Baby Care MCP Server |
| 주요 기술 | Python, FastAPI, Streamlit, OpenAI Responses API, MCP, RAG, PostgreSQL, Redis |

### 프로젝트 목표

- 수유·수면·배변·성장 등 육아 기록 관리
- 아기 정보와 최근 기록을 활용한 맞춤형 AI 답변
- Agent가 사용자 요청에 맞는 MCP Tool을 판단하여 호출
- RAG를 활용한 육아 정보 검색
- 음성 및 이미지 기반 멀티모달 입력
- 지역 기반 병·의원 및 응급의료기관 검색

---

## 🤖 System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
AI Agent
 │
 ├───────────────────────────┐
 │                           │
 ▼                           ▼
Baby Care MCP Server     Baby Info MCP Server
 │                           │
 ├─ 육아 기록 저장           ├─ 육아 정보 RAG
 ├─ 육아 기록 조회           └─ 병원 검색
 ├─ 생활 패턴 조회
 └─ 기저귀 이미지 분석
 │                           │
 ▼                           ▼
PostgreSQL / Vision       pgvector / External API
```

사용자의 자연어 요청이 들어오면 Single Agent가 요청을 분석하고, 필요한 기능에 따라 적절한 MCP Tool을 선택하여 실행합니다.

예를 들어 사용자가 “오늘 마지막으로 수유한 시간이 언제야?”라고 질문하면 다음 흐름으로 처리됩니다.

```text
User → AI Agent → 육아 기록 조회 필요성 판단
     → get_care_records → Baby Care MCP Server
     → 육아 기록 조회 → AI Agent → 사용자 응답
```

---

## ✨ Team Project Features

### 🍼 육아 기록 관리

- 수유·수면·배변·성장 기록 관리
- 최근 및 기간별 육아 기록 조회
- 수유 간격 및 생활 패턴 확인
- 육아 기록을 활용한 AI 답변

### 🤖 AI 육아 도우미

- 자연어 기반 육아 질문
- 아기 정보와 최근 육아 기록을 반영한 맞춤 답변
- RAG 기반 육아 정보 검색
- 요청에 필요한 MCP Tool 자동 선택 및 호출

### 🎙 음성 기반 기록

```text
음성 입력 → STT → 인식 결과 확인 → 사용자 승인 → 기록 저장
```

음성으로 인식된 기록은 바로 저장하지 않고, 사용자가 내용을 확인하고 승인한 경우에만 저장하도록 구성했습니다.

### 📷 기저귀 이미지 분석

- 사진 업로드 및 카메라 촬영
- 이미지 품질 확인
- Vision 모델 기반 특징 관찰
- 규칙 기반 위험 신호 분류
- RAG를 활용한 관련 정보 제공
- 사진만으로 질환을 단정하지 않도록 제한

### 🏥 병원 검색

- 지역 기반 병·의원 검색
- 응급의료기관 검색
- 공공데이터 API 활용

---

## 🧑‍💻 My Contribution — Baby Care MCP Server

팀 프로젝트에서 저는 육아 기록과 생활 패턴을 AI Agent와 연결하는 **Baby Care MCP Server**를 담당했습니다.

```text
baby_care_server
 ├─ record_care_event
 │    └─ 육아 기록 저장
 ├─ get_care_records
 │    └─ 육아 기록 및 생활 패턴 조회
 └─ analyze_infant_stool
      └─ 기저귀 이미지 분석
```

### 1. `record_care_event`

수유·수면·배변·성장 데이터를 기록하기 위한 MCP Tool입니다.

- 수유 기록 처리
- 수면 시작·종료 기록 처리
- 배변 및 성장 데이터 기록
- 입력값 검증
- 중복 요청 방지를 위한 멱등성 처리
- STT 입력 시 사용자 승인 여부 확인

LLM이 생성한 값을 바로 저장하지 않고 Tool 내부에서 데이터 검증과 저장 규칙을 적용하도록 역할을 분리했습니다.

### 2. `get_care_records`

저장된 육아 기록을 조회하고 생활 패턴을 확인하기 위한 MCP Tool입니다.

- 오늘 및 기간별 육아 기록 조회
- 최근 수유 기록 조회
- 최근 N일 생활 패턴 조회
- 수유량 및 수유 간격 확인
- 수면 시간 및 배변 기록 확인

Agent가 사용자의 질문에 필요한 실제 육아 기록을 조회하여 답변에 활용할 수 있도록 구성했습니다.

### 3. `analyze_infant_stool`

기저귀 이미지를 분석하기 위한 MCP Tool이며, 단일 LLM 호출이 아닌 단계별 Workflow로 구성했습니다.

```text
이미지 입력 → 이미지 검증 → 이미지 품질 확인 → Vision 분석
           → Rule 기반 위험도 판단 → Stool RAG 검색 → 결과 반환
```

- 이미지 형식 및 크기 검증
- 이미지 품질 확인
- OpenAI Vision 기반 특징 관찰
- 규칙 기반 위험 신호 판단
- RAG 기반 관련 육아 정보 검색
- 분석 완료 후 임시 이미지 정리

LLM의 판단만으로 결과를 생성하지 않고 **Vision + Rule + RAG**를 각각 다른 역할로 분리한 Workflow를 경험했습니다.

### 🔗 My MCP Server Flow

```text
                  AI Agent
                      │
                MCP Tool Call
                      │
                      ▼
             Baby Care MCP Server
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
 record_care_event get_care_records analyze_infant_stool
       │              │              │
       ▼              ▼              ▼
  기록 저장        기록 조회      Vision / Rule / RAG
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              External Resources
```

이 과정에서 **LLM → Agent → Tool → MCP Server → 실제 데이터·AI 기능**으로 이어지는 구조를 직접 구현하고 연결했습니다.

---

## 🛠 Tech Stack

| 영역 | 기술 |
| --- | --- |
| Backend | Python, FastAPI |
| AI & Agent | OpenAI Responses API, Tool Calling, MCP, RAG, Vision, STT |
| Database | PostgreSQL, pgvector, Redis |
| Frontend | Streamlit, HTML/CSS |

---

## 📂 Project Structure

```text
ai-baby-care-team-project/
├── frontend/                     # Streamlit UI
├── backend/                      # FastAPI Backend
├── mcp_servers/
│   ├── baby_care_server/         # My Contribution
│   │   ├── database/
│   │   ├── prompts/
│   │   ├── repositories/
│   │   ├── rules/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tools/
│   │   └── server.py
│   └── baby_info_server/         # RAG / 병원 검색
└── documents/                    # 프로젝트 설계 및 기획 문서
```

---

## 👥 Team Roles

| 팀원 | 담당 |
| --- | --- |
| 정예진 | 팀장 / Streamlit Frontend |
| 신유빈 | FastAPI Backend / DB / Redis |
| 한다영 | Baby Care MCP Server |
| 한태경 | Baby Info MCP Server / RAG / 병원 검색 |

프로젝트 전체 기능은 팀원들과 역할을 분담하여 개발했으며, 이 README의 **My Contribution** 섹션에서 제가 담당한 영역을 별도로 구분했습니다.

---

## 💡 What I Learned

이번 프로젝트에서 가장 중요하게 경험한 부분은 LLM 자체와 실제 기능을 수행하는 Tool의 역할을 분리하는 것이었습니다.

```text
사용자 요청 → LLM / Agent → 필요한 기능 판단 → MCP Tool
           → Business Logic → Database / Vision / RAG
```

- Agent가 Tool을 선택하여 외부 기능을 사용하는 흐름
- MCP Server를 통한 AI Agent와 기능 간 연결
- LLM과 실제 데이터 처리 로직의 역할 분리
- 데이터 저장 전 입력값 검증의 필요성
- 반복 요청에 대한 중복 처리 방지
- Vision 결과와 규칙 기반 판단의 역할 분리
- RAG를 활용하여 외부 지식을 답변에 연결하는 방식

---

## 🚀 Personal Development

> 이 섹션부터는 **팀 프로젝트 종료 후 개인적으로 추가한 개선 사항**입니다.
> 팀 프로젝트 결과물은 Git 태그 `v1.0-team-project`에서 확인할 수 있으며, 원본 팀 저장소와
> 당시 README는 상단의 Repository Notice 및 Documents 섹션에 별도로 보존했습니다.

팀 프로젝트의 기능과 팀원별 담당 영역은 유지하면서, 실행 환경의 재현성과 향후 배포 가능성을
높이는 작업을 개인 개발 범위로 진행했습니다.

### 개인 개선 완료 항목

- [x] 루트 공용 환경설정을 Frontend와 Backend의 `.env`로 분리
- [x] 실제 비밀값을 제외한 서비스별 `.env.example` 제공
- [x] Backend·Frontend Dockerfile 구성
- [x] PostgreSQL·Redis·Ollama·두 MCP 서버·Backend·Frontend 통합 Compose 구성
- [x] 컨테이너 간 서비스 이름 기반 통신과 시작 순서·상태 확인 설정
- [x] Backend와 Baby Care MCP의 이미지 분석용 임시 파일 volume 공유
- [x] pgvector 및 RAG 테이블 초기화 연결
- [x] Registry 이미지 실행용 `compose.release.yml` 구성
- [x] GitHub Actions를 통한 Backend·Frontend 이미지 자동 빌드 및 GHCR 배포 구성

### 향후 개인 개선 계획

- [ ] Baby Care MCP Server 구조 리팩터링
- [ ] MCP Tool 테스트 보강
- [ ] 예외 처리 및 Logging 개선
- [ ] RAG 검색 품질 평가
- [ ] Agent Workflow 개선
- [ ] LangGraph 기반 Agent Workflow 적용 검토

### Docker로 전체 실행

실제 API Key가 필요하면 `backend/.env`에 입력합니다. 저장소를 새로 받은 경우에는
각 예제 파일을 복사해 설정 파일을 만듭니다.

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
docker compose -f compose.yml config --quiet
docker compose -f compose.yml up --build -d
docker compose -f compose.yml ps
```

첫 실행에서는 Ollama의 `nomic-embed-text` 모델을 내려받기 때문에 시간이 걸릴 수 있습니다.

| 확인 대상 | 주소 |
| --- | --- |
| Streamlit | `http://127.0.0.1:8501` |
| FastAPI 문서 | `http://127.0.0.1:8000/docs` |
| Backend 상태 | `http://127.0.0.1:8000/health` |

전체 서비스를 종료합니다.

```powershell
docker compose -f compose.yml down
```

데이터를 유지하려면 `down -v`를 사용하지 마세요. `-v`를 붙이면 PostgreSQL, Redis,
Ollama 데이터가 들어 있는 Docker volume도 삭제됩니다.

### 배포 이미지 만들기

`main` 브랜치에 반영된 코드는 GitHub Actions가 Backend와 Frontend 이미지를 빌드해
GitHub Container Registry(GHCR)에 저장합니다. Pull Request에서는 빌드만 검사하고
이미지는 올리지 않습니다.

```text
ghcr.io/jbbdyee/ai-baby-care-backend:latest
ghcr.io/jbbdyee/ai-baby-care-frontend:latest
```

`v1.0.0`과 같은 Git 태그를 푸시하면 `1.0.0`, `1.0`, 커밋 SHA 태그도 함께 생성됩니다.

```powershell
git tag v1.0.0
git push origin v1.0.0
```

Registry 이미지를 사용하는 PC에서는 소스를 다시 빌드하지 않고 배포용 Compose를
실행할 수 있습니다.

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
docker compose -f compose.release.yml pull
docker compose -f compose.release.yml up -d
docker compose -f compose.release.yml ps
```

GHCR 패키지가 비공개라면 먼저 `docker login ghcr.io`가 필요합니다. 포트폴리오에서
다른 사람이 바로 실행하게 하려면 GitHub 패키지 설정에서 두 이미지를 공개로 전환합니다.
실제 API Key가 들어 있는 `.env` 파일은 이미지나 저장소에 포함하지 않습니다.

향후 실제 개선이 완료되면 해당 항목을 체크하고 관련 Issue·PR·구현 내용을 함께 기록할 예정입니다.

---

## 📚 Documents

- [Original Team Project README](documents/original-team-readme.md)
- [전체 기획서](documents/overall_plan.md)
- [프론트엔드 기획서](documents/frontend_plan.md)
- [백엔드 계획서](documents/backend_plan.md)
- [API 계약서](documents/frontend_api_contract.md)
- [육아 기록·패턴 MCP 서버 계획서](documents/baby_care_server_plan.md)
- [육아 정보 RAG·병원 검색 MCP 서버 계획서](documents/baby%20info%20server_plan.md)
- [에이전트 아키텍처 설계서](documents/deliverable_1_agent_architecture.md)
- [상세 에이전트 아키텍처 설계서](documents/agent-architecture-design.md)

---

## 📎 Project History

이 프로젝트는 4인 팀으로 진행한 AI Baby Care Assistant 프로젝트에서 시작되었습니다.

현재 저장소는 팀 프로젝트 결과물을 보존하면서, 제가 담당한 MCP Server 구현 경험과 이후의 개인적인 학습·개선 과정을 포트폴리오로 기록하기 위해 운영하고 있습니다.

**Original Team Repository**  
https://github.com/jyeyeyej/team3_AI_Baby_Care_Assistant
