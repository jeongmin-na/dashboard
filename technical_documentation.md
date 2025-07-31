# Samsung AI Experience Group Dashboard - 기술 문서

## 목차
1. [시스템 아키텍처](#1-시스템-아키텍처)
2. [API 구조](#2-api-구조)
3. [프론트엔드 컴포넌트](#3-프론트엔드-컴포넌트)
4. [데이터 플로우](#4-데이터-플로우)
5. [성능 최적화](#5-성능-최적화)
6. [보안 고려사항](#6-보안-고려사항)
7. [개발 가이드](#7-개발-가이드)

## 1. 시스템 아키텍처

### 1.1 전체 구조

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Proxy Server   │    │  Cursor Admin   │
│                 │◄──►│  (localhost:8000)│◄──►│      API       │
│   Dashboard     │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 기술 스택

**프론트엔드**
- HTML5 + CSS3 + Vanilla JavaScript
- 다크 테마 UI/UX
- 반응형 디자인
- Canvas API (차트 렌더링)

**백엔드 통신**
- Fetch API (RESTful)
- Basic Authentication
- JSON 데이터 형식

**데이터 처리**
- 클라이언트 사이드 필터링
- 페이지네이션
- 실시간 검색

### 1.3 파일 구조

```
0728/
├── dash.html              # 메인 대시보드 파일
├── proxy_server.py        # 프록시 서버
├── cursor_teams_api.py    # API 클라이언트
├── requirements.txt       # Python 의존성
├── user_manual_doc.md    # 사용자 매뉴얼
├── technical_documentation.md # 기술 문서
└── README.md             # 프로젝트 개요
```

## 2. API 구조

### 2.1 API 엔드포인트

**기본 설정**
```javascript
const API_CONFIG = {
    baseUrl: 'http://localhost:8000',
    apiKey: 'key_e46368ce482125bbd568b7d55090c657e30e4b73c824f522cbc9ef9b1bf3f0d3',
    headers: {
        'Content-Type': 'application/json'
    }
};
```

**주요 엔드포인트**

| 엔드포인트 | 메서드 | 설명 | 응답 형식 |
|-----------|--------|------|-----------|
| `/teams/members` | GET | 팀 멤버 목록 조회 | `{teamMembers: [...]}` |
| `/teams/spend` | POST | 팀 지출 데이터 조회 | `{teamMemberSpend: [...]}` |
| `/teams/daily-usage-data` | POST | 일별 사용량 데이터 | `{data: [...]}` |
| `/teams/filtered-usage-events` | POST | 필터링된 이벤트 조회 | `{usageEvents: [...]}` |

### 2.2 인증 방식

**Basic Authentication**
```javascript
const credentials = `${API_CONFIG.apiKey}:`;
const encodedCredentials = btoa(credentials);
const authHeader = `Basic ${encodedCredentials}`;
```

### 2.3 데이터 모델

**팀 멤버 (Team Member)**
```javascript
{
    name: string,           // 멤버 이름
    email: string,          // 이메일 주소
    role: string           // 역할 (owner/member)
}
```

**지출 데이터 (Spend Data)**
```javascript
{
    email: string,                    // 이메일
    fastPremiumRequests: number,      // 프리미엄 요청 수
    spendCents: number,              // 지출 (센트)
    hardLimitOverrideDollars: number // 하드 리미트 오버라이드
}
```

**사용량 이벤트 (Usage Event)**
```javascript
{
    timestamp: string,        // 타임스탬프
    userEmail: string,       // 사용자 이메일
    kindLabel: string,       // 이벤트 유형
    requestsCosts: number,   // 요청 비용
    model: string,          // 사용 모델
    maxMode: boolean        // 최대 모드 사용 여부
}
```

## 3. 프론트엔드 컴포넌트

### 3.1 메인 레이아웃

**HTML 구조**
```html
<div class="dashboard-container">
    <nav class="sidebar">          <!-- 좌측 네비게이션 -->
    <main class="main-content">    <!-- 메인 콘텐츠 영역 -->
        <header class="header">    <!-- 상단 헤더 -->
        <div class="content-area"> <!-- 콘텐츠 영역 -->
```

**CSS Grid 시스템**
```css
.dashboard-container {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    flex-shrink: 0;
}

.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}
```

### 3.2 섹션별 컴포넌트

#### 3.2.1 Overview 섹션

**통계 카드 (Statistics Cards)**
```javascript
// 카드 데이터 구조
const statCards = [
    { type: 'total', number: 20, label: '전체 멤버', description: '모든 멤버의 활동 기록' },
    { type: 'active', number: 13, label: '활성 멤버', description: '활성 멤버의 활동 기록' },
    { type: 'inactive', number: 7, label: '비활성 멤버', description: '비활성 멤버의 활동 기록' }
];
```

**활동 차트 (Activity Chart)**
```javascript
// Canvas 기반 차트 렌더링
function createOverviewChart() {
    const canvas = document.getElementById('overviewChart');
    const ctx = canvas.getContext('2d');
    
    // 그리드 그리기
    // 데이터 포인트 계산
    // 선 그래프 렌더링
    // 데이터 포인트 원 그리기
}
```

#### 3.2.2 Usage 섹션

**연동 검색 시스템**
```javascript
function filterUsageMembers(searchTerm) {
    // 1. 사용자별 누적 사용량 정보 테이블 필터링
    const matchedEmails = new Set();
    
    // 2. All Raw Events 테이블 연동 필터링
    if (matchedEmails.size > 0) {
        const filteredEvents = currentRawEventsData.filter(event => {
            // 이메일 매칭 로직
        });
        
        renderFilteredRawEventsTable(filteredEvents, container);
    }
}
```

**페이지네이션 시스템**
```javascript
function renderRawEventsTableWithPagination() {
    const totalEvents = currentRawEventsData.length;
    const totalPages = Math.ceil(totalEvents / currentRawEventsPageSize);
    const startIndex = (currentRawEventsPage - 1) * currentRawEventsPageSize;
    const endIndex = Math.min(startIndex + currentRawEventsPageSize, totalEvents);
    const pageEvents = currentRawEventsData.slice(startIndex, endIndex);
}
```

### 3.3 상태 관리

**전역 변수**
```javascript
let currentFilterType = 'total';           // 현재 필터 타입
let currentActivities = [];               // 현재 활동 데이터
let currentMembers = [];                  // 현재 멤버 데이터
let currentDateRange = null;              // 현재 날짜 범위 (Overview)
let currentUsageDateRange = null;         // 현재 날짜 범위 (Usage)
let currentRawEventsData = [];            // 현재 Raw Events 전체 데이터
let currentRawEventsPage = 1;             // 현재 Raw Events 페이지
let currentRawEventsPageSize = 10;        // 현재 Raw Events 페이지 크기
```

## 4. 데이터 플로우

### 4.1 초기 로드 플로우

```mermaid
graph TD
    A[페이지 로드] --> B[스켈레톤 UI 표시]
    B --> C[기본 UI 초기화]
    C --> D[백그라운드 데이터 로드 시작]
    D --> E[API 호출: 팀 멤버]
    D --> F[API 호출: 지출 데이터]
    D --> G[API 호출: 사용량 이벤트]
    E --> H[데이터 처리 및 UI 업데이트]
    F --> H
    G --> H
    H --> I[차트 렌더링]
    I --> J[초기화 완료]
```

### 4.2 검색 플로우

```mermaid
graph TD
    A[사용자 검색 입력] --> B[디바운스 처리]
    B --> C[검색어 분석]
    C --> D[사용자별 누적 정보 테이블 필터링]
    D --> E[매칭된 이메일 수집]
    E --> F[전체 Raw Events 데이터에서 필터링]
    F --> G{매칭된 이벤트가 있는가?}
    G -->|Yes| H[필터링된 테이블 렌더링]
    G -->|No| I[빈 테이블 메시지 표시]
    H --> J[검색 완료]
    I --> J
```

### 4.3 필터링 플로우

```mermaid
graph TD
    A[필터 버튼 클릭] --> B[날짜 범위 계산]
    B --> C[API 호출: 필터링된 이벤트]
    C --> D[데이터 처리]
    D --> E[UI 업데이트]
    E --> F[차트 업데이트]
    F --> G[활동 리스트 업데이트]
```

## 5. 성능 최적화

### 5.1 프로그레시브 로딩

**스켈레톤 UI**
```javascript
function showSkeletonUI() {
    // 로딩 중임을 나타내는 스켈레톤 UI 표시
    // 실제 데이터 로드 전에 사용자에게 피드백 제공
}
```

**백그라운드 데이터 로드**
```javascript
// 메인 UI 렌더링과 병렬로 데이터 로드
setTimeout(async () => {
    await refreshAllRealData();
}, 100);
```

### 5.2 캐싱 시스템

**데이터 캐시**
```javascript
const DataCache = {
    members: null,
    events: null,
    spending: null,
    
    isValid: function(key) {
        // 캐시 유효성 검사
    },
    
    clear: function() {
        // 캐시 초기화
    }
};
```

### 5.3 디바운스 검색

```javascript
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
```

### 5.4 메모리 최적화

**이벤트 리스너 관리**
```javascript
// 이벤트 위임 사용
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('chart-btn')) {
        // 차트 버튼 클릭 처리
    }
});
```

**DOM 조작 최적화**
```javascript
// DocumentFragment 사용으로 DOM 조작 최소화
function updateActivityList(activities) {
    const fragment = document.createDocumentFragment();
    // 여러 요소를 fragment에 추가
    container.appendChild(fragment);
}
```

## 6. 보안 고려사항

### 6.1 API 인증

**Basic Authentication**
- API 키를 Base64로 인코딩하여 전송
- HTTPS 사용 권장 (프로덕션 환경)

### 6.2 데이터 검증

**입력 검증**
```javascript
function validateSearchInput(searchTerm) {
    // XSS 방지를 위한 입력 검증
    return searchTerm.replace(/[<>]/g, '');
}
```

**출력 이스케이핑**
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### 6.3 CORS 설정

**프록시 서버 설정**
```python
# proxy_server.py에서 CORS 헤더 설정
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
```

## 7. 개발 가이드

### 7.1 개발 환경 설정

**필요한 도구**
- Python 3.7+
- 웹 브라우저 (Chrome 권장)
- 텍스트 에디터 (VS Code 권장)

**설치 및 실행**
```bash
# 의존성 설치
pip install -r requirements.txt

# 프록시 서버 실행
python proxy_server.py

# 브라우저에서 대시보드 접속
# http://localhost:8000/dash.html
```

### 7.2 코드 구조

**모듈화된 함수들**
```javascript
// API 호출 함수들
async function getTeamMembers() { ... }
async function getTeamSpendingData() { ... }
async function getFilteredEvents() { ... }

// UI 업데이트 함수들
function updateStatsCards() { ... }
function updateActivityList() { ... }
function renderRawEventsTable() { ... }

// 유틸리티 함수들
function getDateRange() { ... }
function debounce() { ... }
function escapeHtml() { ... }
```

### 7.3 디버깅

**콘솔 로깅**
```javascript
console.log('=== API 호출 시작 ===');
console.log('📊 데이터 처리 결과:', data);
console.error('❌ 오류 발생:', error);
```

**성능 모니터링**
```javascript
const PerformanceMonitor = {
    start: function(label) {
        console.time(label);
    },
    end: function(label) {
        console.timeEnd(label);
    }
};
```

### 7.4 테스트

**기능 테스트**
1. 각 섹션별 데이터 로드 확인
2. 검색 기능 동작 확인
3. 필터링 기능 동작 확인
4. 페이지네이션 동작 확인

**성능 테스트**
1. 대용량 데이터 로드 테스트
2. 검색 성능 테스트
3. 메모리 사용량 모니터링

### 7.5 배포

**정적 파일 배포**
- `dash.html`을 웹 서버에 업로드
- 프록시 서버 설정
- SSL 인증서 설정 (프로덕션)

**환경 변수 설정**
```bash
# API 키 설정
export CURSOR_API_KEY="your_api_key_here"

# 서버 포트 설정
export PROXY_PORT=8000
```

## 8. 향후 개선 사항

### 8.1 기능 개선

**예정된 기능**
- 실시간 데이터 업데이트 (WebSocket)
- 고급 차트 라이브러리 도입 (Chart.js)
- 데이터 내보내기 기능 강화
- 다국어 지원

### 8.2 성능 개선

**최적화 계획**
- 가상 스크롤링 도입
- 서버 사이드 페이지네이션
- 이미지 최적화
- 코드 스플리팅

### 8.3 보안 강화

**보안 개선**
- JWT 토큰 인증
- API 요청 제한
- 입력 검증 강화
- HTTPS 강제 적용

이 기술 문서를 통해 Samsung AI Experience Group Dashboard의 기술적 구조와 개발 방법을 이해하시기 바랍니다. 