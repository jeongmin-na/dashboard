import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import base64
import os

class CursorTeamAPI:
    """Cursor Teams Admin API 클라이언트"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key (str): Cursor Admin API 키 (형식: key_xxxxxxx...)
        """
        self.api_key = api_key
        self.base_url = "https://api.cursor.com"
        
        # Basic Auth 설정
        # API 키를 username으로 사용하고 password는 빈 문자열
        credentials = f"{api_key}:"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    def get_team_members(self) -> Optional[List[Dict]]:
        """
        팀의 모든 멤버 정보를 가져옵니다.
        
        Returns:
            List[Dict]: 팀원 정보 리스트
                - name: 사용자 이름
                - email: 이메일 주소
                - role: 역할 (owner, member, free-owner)
        """
        try:
            # API 문서에 따른 올바른 엔드포인트
            endpoint = "/teams/members"
            
            print(f"엔드포인트 시도: {endpoint}")
            
            # urllib.request를 사용한 HTTP 요청
            req = urllib.request.Request(
                f"{self.base_url}{endpoint}",
                headers=self.headers
            )
            
            with urllib.request.urlopen(req) as response:
                # 응답 상태 확인
                if response.status == 200:
                    # JSON 응답 파싱
                    data = response.read().decode('utf-8')
                    print(f"응답 데이터: {data[:200]}...")  # 처음 200자만 출력
                    
                    response_data = json.loads(data)
                    print(f"✅ 성공한 엔드포인트: {endpoint}")
                    print(f"응답 타입: {type(response_data)}")
                    
                    # API 문서에 따른 응답 구조 처리
                    if isinstance(response_data, dict) and 'teamMembers' in response_data:
                        members = response_data['teamMembers']
                        print(f"팀원 수: {len(members)}")
                        return members
                    else:
                        print(f"❌ 예상하지 못한 응답 구조: {response_data}")
                        return None
                else:
                    print(f"엔드포인트 {endpoint} 실패: {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            print(f"HTTP 에러 발생: {e}")
            print(f"응답 코드: {e.code}")
            print(f"응답 내용: {e.read().decode()}")
            return None
        except urllib.error.URLError as e:
            print(f"URL 에러 발생: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {e}")
            return None
        except Exception as e:
            print(f"요청 에러 발생: {e}")
            return None
    
    def get_team_spending(self, search_term: str = None, start_date: int = None, end_date: int = None) -> Optional[Dict]:
        """
        팀의 사용량 및 청구액 정보를 가져옵니다.
        
        Args:
            search_term (str): 특정 사용자 검색 (이메일 또는 이름)
            start_date (int): 시작 날짜 (epoch milliseconds)
            end_date (int): 종료 날짜 (epoch milliseconds)
            
        Returns:
            Dict: 사용량 및 청구액 정보
        """
        try:
            endpoint = "/teams/spend"
            
            # 요청 본문 구성
            request_body = {}
            
            if search_term:
                request_body['searchTerm'] = search_term
            
            if start_date:
                request_body['startDate'] = start_date
                
            if end_date:
                request_body['endDate'] = end_date
            
            # POST 요청 생성
            data = json.dumps(request_body).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.base_url}{endpoint}",
                data=data,
                headers=self.headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    print(f"✅ 사용량 데이터 가져오기 성공")
                    return json.loads(data)
                else:
                    print(f"❌ 사용량 데이터 가져오기 실패: {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            print(f"HTTP 에러 발생: {e}")
            return None
        except Exception as e:
            print(f"요청 에러 발생: {e}")
            return None
    
    def get_daily_usage_data(self, start_date: int, end_date: int) -> Optional[Dict]:
        """
        일별 사용량 데이터를 가져옵니다.
        
        Args:
            start_date (int): 시작 날짜 (epoch milliseconds)
            end_date (int): 종료 날짜 (epoch milliseconds)
            
        Returns:
            Dict: 일별 사용량 데이터
        """
        try:
            endpoint = "/teams/daily-usage-data"
            
            # 요청 본문 구성
            request_body = {
                "startDate": start_date,
                "endDate": end_date
            }
            
            # POST 요청 생성
            data = json.dumps(request_body).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.base_url}{endpoint}",
                data=data,
                headers=self.headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    print(f"✅ 일별 사용량 데이터 가져오기 성공")
                    return json.loads(data)
                else:
                    print(f"❌ 일별 사용량 데이터 가져오기 실패: {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            print(f"HTTP 에러 발생: {e}")
            return None
        except Exception as e:
            print(f"요청 에러 발생: {e}")
            return None
    
    def display_team_members(self, members: List[Dict]) -> None:
        """
        팀원 정보를 보기 좋게 출력합니다.
        
        Args:
            members: 팀원 정보 리스트
        """
        if not members:
            print("팀원이 없습니다.")
            return
        
        print(f"\n=== Cursor 팀원 정보 ({len(members)}명) ===\n")
        
        for idx, member in enumerate(members, 1):
            print(f"{idx}. {member.get('name', 'N/A')}")
            print(f"   - 이메일: {member.get('email', 'N/A')}")
            print(f"   - 역할: {member.get('role', 'N/A')}")
            
            # 역할에 따른 설명 추가
            role = member.get('role', '')
            if role == 'owner':
                print(f"   - 설명: 팀 소유자")
            elif role == 'member':
                print(f"   - 설명: 일반 멤버")
            elif role == 'free-owner':
                print(f"   - 설명: 무료 팀 소유자")
            
            print()  # 줄바꿈

# 필터링 기능
def filter_by_role(members: List[Dict], role: str) -> List[Dict]:
    """특정 역할의 팀원만 필터링"""
    return [m for m in members if m.get('role', '').lower() == role.lower()]

def filter_owners(members: List[Dict]) -> List[Dict]:
    """소유자만 필터링"""
    return [m for m in members if m.get('role', '').lower() in ['owner', 'free-owner']]

def filter_members(members: List[Dict]) -> List[Dict]:
    """일반 멤버만 필터링"""
    return [m for m in members if m.get('role', '').lower() == 'member']

def get_team_statistics(members: List[Dict]) -> Dict:
    """팀 통계 정보 생성"""
    total = len(members)
    owners = sum(1 for m in members if m.get('role', '').lower() in ['owner', 'free-owner'])
    members_count = sum(1 for m in members if m.get('role', '').lower() == 'member')
    
    return {
        'total': total,
        'owners': owners,
        'members': members_count,
        'owner_rate': (owners / total * 100) if total > 0 else 0,
        'member_rate': (members_count / total * 100) if total > 0 else 0
    }

def display_statistics(stats: Dict) -> None:
    """통계 정보를 보기 좋게 출력"""
    print("\n=== 팀 통계 정보 ===")
    print(f"총 팀원 수: {stats['total']}명")
    print(f"소유자: {stats['owners']}명 ({stats['owner_rate']:.1f}%)")
    print(f"일반 멤버: {stats['members']}명 ({stats['member_rate']:.1f}%)")

def save_member_report(members: List[Dict], filename: str = "team_report.json"):
    """팀원 정보와 통계를 리포트로 저장"""
    stats = get_team_statistics(members)
    owners = filter_owners(members)
    members_only = filter_members(members)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'statistics': stats,
        'all_members': members,
        'owners': owners,
        'members': members_only
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 리포트가 '{filename}' 파일로 저장되었습니다.")

def display_spending_data(spending_data: Dict) -> None:
    """사용량 및 청구액 정보를 보기 좋게 출력"""
    if not spending_data or 'teamMemberSpend' not in spending_data:
        print("❌ 사용량 데이터가 없습니다.")
        return
    
    members = spending_data['teamMemberSpend']
    total_members = spending_data.get('totalMembers', len(members))
    
    print(f"\n=== 사용량 및 청구액 정보 ({len(members)}명) ===")
    
    # 총액 계산
    total_spend_cents = sum(m.get('spendCents', 0) for m in members)
    total_spend_dollars = total_spend_cents / 100
    
    print(f"총 청구액: ${total_spend_dollars:.2f}")
    print(f"총 팀원 수: {total_members}명")
    print()
    
    for idx, member in enumerate(members, 1):
        name = member.get('name', 'N/A')
        email = member.get('email', 'N/A')
        role = member.get('role', 'N/A')
        spend_cents = member.get('spendCents', 0)
        spend_dollars = spend_cents / 100
        fast_premium_requests = member.get('fastPremiumRequests', 0)
        hard_limit = member.get('hardLimitOverrideDollars', 0)
        
        print(f"{idx}. {name}")
        print(f"   - 이메일: {email}")
        print(f"   - 역할: {role}")
        print(f"   - 청구액: ${spend_dollars:.2f}")
        print(f"   - Fast Premium 요청: {fast_premium_requests}회")
        if hard_limit > 0:
            print(f"   - 사용자 정의 한도: ${hard_limit:.2f}")
        print()

def display_daily_usage_data(usage_data: Dict) -> None:
    """일별 사용량 데이터를 보기 좋게 출력"""
    if not usage_data or 'data' not in usage_data:
        print("❌ 일별 사용량 데이터가 없습니다.")
        return
    
    data = usage_data['data']
    period = usage_data.get('period', {})
    
    print(f"\n=== 일별 사용량 데이터 ({len(data)}일) ===")
    
    if period:
        start_date = datetime.fromtimestamp(period.get('startDate', 0) / 1000)
        end_date = datetime.fromtimestamp(period.get('endDate', 0) / 1000)
        print(f"기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
        print()
    
    for day_data in data:
        date = datetime.fromtimestamp(day_data.get('date', 0) / 1000)
        is_active = day_data.get('isActive', False)
        email = day_data.get('email', 'N/A')
        
        print(f"📅 {date.strftime('%Y-%m-%d')} - {email}")
        print(f"   - 활성 상태: {'활성' if is_active else '비활성'}")
        
        if is_active:
            total_added = day_data.get('totalLinesAdded', 0)
            total_deleted = day_data.get('totalLinesDeleted', 0)
            accepted_added = day_data.get('acceptedLinesAdded', 0)
            accepted_deleted = day_data.get('acceptedLinesDeleted', 0)
            
            print(f"   - 총 추가된 라인: {total_added}")
            print(f"   - 총 삭제된 라인: {total_deleted}")
            print(f"   - AI 제안 수락으로 추가: {accepted_added}")
            print(f"   - AI 제안 수락으로 삭제: {accepted_deleted}")
            
            total_applies = day_data.get('totalApplies', 0)
            total_accepts = day_data.get('totalAccepts', 0)
            total_rejects = day_data.get('totalRejects', 0)
            
            print(f"   - Apply 작업: {total_applies}회")
            print(f"   - 수락: {total_accepts}회")
            print(f"   - 거부: {total_rejects}회")
            
            composer_requests = day_data.get('composerRequests', 0)
            chat_requests = day_data.get('chatRequests', 0)
            agent_requests = day_data.get('agentRequests', 0)
            
            print(f"   - Composer 요청: {composer_requests}회")
            print(f"   - Chat 요청: {chat_requests}회")
            print(f"   - Agent 요청: {agent_requests}회")
            
            most_used_model = day_data.get('mostUsedModel', 'N/A')
            print(f"   - 가장 많이 사용한 모델: {most_used_model}")
        
        print()

def get_date_range(start_date_str: str = None, end_date_str: str = None) -> tuple:
    """날짜 범위를 epoch milliseconds로 변환"""
    if not start_date_str:
        # 이번 달 1일부터 오늘까지
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)
    else:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            print("❌ 시작 날짜 형식이 잘못되었습니다. (YYYY-MM-DD)")
            return None, None
    
    if not end_date_str:
        # 오늘까지
        end_date = datetime.now()
    else:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            print("❌ 종료 날짜 형식이 잘못되었습니다. (YYYY-MM-DD)")
            return None, None
    
    # epoch milliseconds로 변환
    start_ms = int(start_date.timestamp() * 1000)
    end_ms = int(end_date.timestamp() * 1000)
    
    return start_ms, end_ms

# 환경 변수에서 API 키를 읽어오는 안전한 방법
def get_api_key_from_env():
    """환경 변수에서 API 키를 가져옵니다."""
    api_key = os.environ.get('CURSOR_API_KEY')
    if not api_key:
        raise ValueError("환경 변수 CURSOR_API_KEY가 설정되지 않았습니다.")
    return api_key

def main():
    """메인 실행 함수"""
    try:
        # API 키 설정
        API_KEY = "key_e46368ce482125bbd568b7d55090c657e30e4b73c824f522cbc9ef9b1bf3f0d3"
        
        # API 클라이언트 생성
        api = CursorTeamAPI(API_KEY)
        
        # 팀원 정보 가져오기
        print("\n🔄 팀원 정보를 가져오는 중...")
        members = api.get_team_members()
        
        if members is None:
            print("❌ 팀원 정보를 가져오는데 실패했습니다.")
            return
        
        print(f"✅ {len(members)}명의 팀원 정보를 가져왔습니다.")
        
        while True:
            print("\n=== 메뉴 ===")
            print("1. 전체 팀원 보기")
            print("2. 소유자만 보기")
            print("3. 일반 멤버만 보기")
            print("4. 역할별 필터링")
            print("5. 팀 통계 보기")
            print("6. 전체 리포트 저장")
            print("7. 사용량 및 청구액 확인")
            print("8. 일별 사용량 확인")
            print("0. 종료")
            
            choice = input("\n선택하세요 (0-8): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                api.display_team_members(members)
            elif choice == '2':
                owners = filter_owners(members)
                print(f"\n소유자 ({len(owners)}명):")
                api.display_team_members(owners)
            elif choice == '3':
                members_only = filter_members(members)
                print(f"\n일반 멤버 ({len(members_only)}명):")
                api.display_team_members(members_only)
            elif choice == '4':
                role = input("역할을 입력하세요 (owner/member/free-owner): ").strip().lower()
                filtered = filter_by_role(members, role)
                print(f"\n{role} 역할 ({len(filtered)}명):")
                api.display_team_members(filtered)
            elif choice == '5':
                stats = get_team_statistics(members)
                display_statistics(stats)
            elif choice == '6':
                save_member_report(members)
            elif choice == '7':
                print("\n=== 사용량 및 청구액 확인 ===")
                print("1. 전체 멤버 사용량")
                print("2. 특정 사용자 사용량")
                
                sub_choice = input("선택하세요 (1-2): ").strip()
                
                if sub_choice == '1':
                    print("\n🔄 전체 멤버 사용량을 가져오는 중...")
                    spending_data = api.get_team_spending()
                    if spending_data:
                        display_spending_data(spending_data)
                    else:
                        print("❌ 사용량 데이터를 가져오는데 실패했습니다.")
                        
                elif sub_choice == '2':
                    search_term = input("사용자 이메일 또는 이름을 입력하세요: ").strip()
                    if search_term:
                        print(f"\n🔄 '{search_term}' 사용량을 가져오는 중...")
                        spending_data = api.get_team_spending(search_term=search_term)
                        if spending_data:
                            display_spending_data(spending_data)
                        else:
                            print("❌ 사용량 데이터를 가져오는데 실패했습니다.")
                    else:
                        print("❌ 검색어를 입력해주세요.")
                        
            elif choice == '8':
                print("\n=== 일별 사용량 확인 ===")
                print("날짜 형식: YYYY-MM-DD (예: 2024-07-01)")
                print("날짜를 입력하지 않으면 이번 달 1일부터 오늘까지 조회됩니다.")
                
                start_date_str = input("시작 날짜 (선택사항): ").strip() or None
                end_date_str = input("종료 날짜 (선택사항): ").strip() or None
                
                start_ms, end_ms = get_date_range(start_date_str, end_date_str)
                
                if start_ms and end_ms:
                    print(f"\n🔄 {datetime.fromtimestamp(start_ms/1000).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(end_ms/1000).strftime('%Y-%m-%d')} 일별 사용량을 가져오는 중...")
                    usage_data = api.get_daily_usage_data(start_ms, end_ms)
                    if usage_data:
                        display_daily_usage_data(usage_data)
                    else:
                        print("❌ 일별 사용량 데이터를 가져오는데 실패했습니다.")
                else:
                    print("❌ 날짜 형식이 잘못되었습니다.")
                    
            else:
                print("❌ 잘못된 선택입니다.")
        
        print("\n프로그램을 종료합니다.")
        
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main() 