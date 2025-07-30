# Samsung AI Experience Group Dashboard

Samsung AI Experience Group을 위한 실시간 대시보드입니다. Cursor Admin API를 통해 팀의 사용량, 멤버 활동, 지출 현황을 실시간으로 모니터링할 수 있습니다.

## 🚀 주요 기능

### 📊 Overview 섹션
- **실시간 통계 카드**: 전체 멤버, 활성 멤버, 비활성 멤버 수
- **활동 차트**: 일별 활동 추이 시각화
- **활동 리스트**: 멤버별 상세 활동 정보
- **기간 필터링**: 1일, 7일, 30일 또는 사용자 정의 기간

### 👥 Members 섹션
- **전체 멤버 목록**: 팀의 모든 멤버 정보 표시
- **실시간 데이터**: Premium Requests, 지출, 역할 정보
- **검색 기능**: 이름 또는 이메일로 멤버 검색
- **정렬 기능**: 각 컬럼별 정렬 지원

### 📈 Usage 섹션
- **사용량 카드**: Total Users, Lines of Agent Edits, Tabs Accepted, Chats
- **사용자별 누적 정보**: 선택된 기간의 상세 사용 통계
- **All Raw Events**: 모든 활동 이벤트 로그 (페이지네이션 지원)
- **기간별 필터링**: 1일, 7일, 30일 또는 사용자 정의 기간

### ⚙️ Settings 섹션
- **활성 기간 설정**: 자동 비활성 전환 설정
- **Email Report**: 자동 리포트 발송 설정
- **Export Documents**: 데이터 내보내기 설정

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/jeongmin-na/dashboard.git
cd dashboard
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
`proxy_server.py` 파일에서 API 키를 설정하세요:
```python
self.api_key = "your_cursor_admin_api_key_here"
```

### 4. 프록시 서버 실행
```bash
python proxy_server.py
```

### 5. 대시보드 접속
브라우저에서 `http://localhost:8000/dash.html`로 접속하세요.

## 📁 파일 구조

```
dashboard/
├── dash.html                 # 메인 대시보드 HTML 파일
├── proxy_server.py           # Cursor API 프록시 서버
├── cursor_teams_api.py       # Cursor Teams API 클라이언트
├── requirements.txt          # Python 의존성 목록
└── README.md                # 이 파일
```

## 🔧 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.8+
- **API**: Cursor Admin API
- **서버**: Python HTTP Server (프록시)

## 📊 API 엔드포인트

이 대시보드는 다음 Cursor Admin API 엔드포인트를 사용합니다:

- `GET /teams/members` - 팀 멤버 목록
- `POST /teams/spend` - 지출 데이터
- `POST /teams/daily-usage-data` - 일별 사용량 데이터
- `POST /teams/filtered-usage-events` - 필터링된 사용 이벤트

## 🎯 주요 특징

### ✅ 실시간 데이터
- 모든 데이터는 Cursor Admin API에서 실시간으로 가져옴
- 자동 새로고침 기능으로 최신 정보 유지

### ✅ 반응형 디자인
- 다크 테마로 개발자 친화적 UI
- 모든 화면 크기에서 최적화된 레이아웃

### ✅ 성능 최적화
- Progressive Loading으로 빠른 초기 로딩
- 캐싱 시스템으로 API 호출 최소화
- 비동기 데이터 로딩으로 UI 블로킹 방지

### ✅ 사용자 경험
- 직관적인 네비게이션
- 실시간 로딩 상태 표시
- 오류 처리 및 사용자 피드백

## 🔍 사용법

### Overview 섹션
1. 통계 카드 클릭으로 해당 타입의 활동 리스트 필터링
2. 기간 필터 버튼 (1d, 7d, 30d) 클릭으로 데이터 업데이트
3. 사용자 정의 날짜 범위 설정 가능

### Members 섹션
1. 검색창에 이름 또는 이메일 입력으로 멤버 검색
2. 컬럼 헤더 클릭으로 정렬
3. 자동으로 전체 멤버 데이터 로드

### Usage 섹션
1. 기간 필터로 사용량 데이터 조회
2. 사용자별 누적 정보에서 상세 통계 확인
3. All Raw Events에서 페이지네이션으로 이벤트 탐색

## 🐛 문제 해결

### 프록시 서버 연결 오류
```bash
# 포트가 이미 사용 중인 경우
python proxy_server.py --port 8001
```

### API 키 오류
- Cursor Admin API 키가 올바른지 확인
- API 키에 Admin 권한이 있는지 확인

### 데이터가 표시되지 않는 경우
- 프록시 서버가 실행 중인지 확인
- 브라우저 개발자 도구에서 네트워크 오류 확인
- API 키 설정 확인

## 📈 성능 모니터링

대시보드는 다음 성능 지표를 제공합니다:
- 페이지 로드 시간
- API 응답 시간
- 캐시 히트율
- 데이터 처리 시간

## 🔒 보안

- API 키는 프록시 서버에서만 사용
- CORS 설정으로 안전한 API 호출
- 클라이언트 측에서는 민감한 정보 노출 없음

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트나 기능 요청은 GitHub Issues를 통해 제출해주세요.

## 📞 지원

기술적 문제나 질문이 있으시면 이슈를 등록해주세요.

---

**Samsung AI Experience Group Dashboard** - 실시간 팀 모니터링 솔루션 