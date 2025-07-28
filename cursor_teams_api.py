import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import base64
import os
import csv

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
    
    def get_user_usage_summary(self, start_date: int, end_date: int) -> Optional[Dict]:
        """
        특정 날짜 범위 내 사용자별 사용 횟수를 집계합니다.
        
        Args:
            start_date (int): 시작 날짜 (epoch milliseconds)
            end_date (int): 종료 날짜 (epoch milliseconds)
            
        Returns:
            Dict: 사용자별 사용 횟수 집계 정보
        """
        try:
            endpoint = "/teams/daily-usage-data"
            
            # 요청 데이터
            request_data = {
                "startDate": start_date,
                "endDate": end_date
            }
            
            print(f"엔드포인트 시도: {endpoint}")
            print(f"요청 데이터: {request_data}")
            
            # urllib.request를 사용한 HTTP 요청
            req = urllib.request.Request(
                f"{self.base_url}{endpoint}",
                data=json.dumps(request_data).encode('utf-8'),
                headers=self.headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    print(f"응답 데이터: {data[:200]}...")
                    
                    response_data = json.loads(data)
                    print(f"✅ 성공한 엔드포인트: {endpoint}")
                    
                    return response_data
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
    
    def get_filtered_usage_events(self, start_date: int = None, end_date: int = None, email: str = None, page: int = 1, page_size: int = 100) -> Optional[Dict]:
        """
        필터링된 사용 이벤트 데이터를 가져옵니다.
        
        Args:
            start_date (int): 시작 날짜 (epoch milliseconds)
            end_date (int): 종료 날짜 (epoch milliseconds)
            email (str): 특정 사용자 이메일
            page (int): 페이지 번호 (1부터 시작)
            page_size (int): 페이지당 결과 수
            
        Returns:
            Dict: 필터링된 사용 이벤트 데이터
        """
        try:
            endpoint = "/teams/filtered-usage-events"
            
            # 요청 데이터
            request_data = {
                "page": page,
                "pageSize": page_size
            }
            
            if start_date:
                request_data["startDate"] = start_date
            if end_date:
                request_data["endDate"] = end_date
            if email:
                request_data["email"] = email
            
            print(f"엔드포인트 시도: {endpoint}")
            print(f"요청 데이터: {request_data}")
            
            # urllib.request를 사용한 HTTP 요청
            req = urllib.request.Request(
                f"{self.base_url}{endpoint}",
                data=json.dumps(request_data).encode('utf-8'),
                headers=self.headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    print(f"응답 데이터: {data[:500]}...")
                    
                    response_data = json.loads(data)
                    print(f"✅ 성공한 엔드포인트: {endpoint}")
                    
                    return response_data
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

def display_user_usage_summary(usage_data: Dict) -> None:
    """
    사용자별 사용 횟수 집계 데이터를 표시합니다.
    
    Args:
        usage_data (Dict): API에서 받은 사용량 데이터
    """
    try:
        if not usage_data or 'dailyUsageData' not in usage_data:
            print("❌ 사용량 데이터가 없습니다.")
            return
        
        daily_data = usage_data['dailyUsageData']
        
        if not daily_data:
            print("❌ 해당 기간에 사용량 데이터가 없습니다.")
            return
        
        # 사용자별 사용 횟수 집계
        user_usage = {}
        
        for day_data in daily_data:
            if 'usageData' in day_data:
                for usage in day_data['usageData']:
                    user_email = usage.get('userEmail', 'Unknown')
                    cost = usage.get('cost', 0)
                    
                    if user_email not in user_usage:
                        user_usage[user_email] = {
                            'total_requests': 0,
                            'total_cost': 0,
                            'usage_count': 0
                        }
                    
                    user_usage[user_email]['total_requests'] += cost
                    user_usage[user_email]['usage_count'] += 1
                    # cost는 이미 요청 수를 나타내므로 total_cost는 별도 계산
        
        if not user_usage:
            print("❌ 사용자별 사용량 데이터가 없습니다.")
            return
        
        # 사용 횟수별로 정렬
        sorted_users = sorted(user_usage.items(), 
                            key=lambda x: x[1]['total_requests'], 
                            reverse=True)
        
        print(f"\n📊 사용자별 사용 횟수 집계")
        print("=" * 60)
        print(f"{'사용자 이메일':<35} {'총 요청 수':<10} {'사용 횟수':<10}")
        print("=" * 60)
        
        total_team_requests = 0
        total_team_usage_count = 0
        
        for user_email, usage_info in sorted_users:
            requests = usage_info['total_requests']
            usage_count = usage_info['usage_count']
            
            print(f"{user_email:<35} {requests:<10} {usage_count:<10}")
            
            total_team_requests += requests
            total_team_usage_count += usage_count
        
        print("=" * 60)
        print(f"{'팀 전체':<35} {total_team_requests:<10} {total_team_usage_count:<10}")
        print("=" * 60)
        
        # 상세 정보
        print(f"\n📈 상세 정보:")
        print(f"• 총 사용자 수: {len(user_usage)}명")
        print(f"• 총 요청 수: {total_team_requests:,}회")
        print(f"• 총 사용 횟수: {total_team_usage_count:,}회")
        
        if user_usage:
            most_active_user = max(user_usage.items(), key=lambda x: x[1]['total_requests'])
            print(f"• 가장 활발한 사용자: {most_active_user[0]} ({most_active_user[1]['total_requests']}회)")
        
    except Exception as e:
        print(f"❌ 사용량 데이터 표시 중 오류 발생: {e}")

def display_user_detailed_activity(usage_data: Dict, target_user: str = None) -> None:
    """
    사용자별 상세 활동 정보를 출력합니다.
    
    Args:
        usage_data (Dict): API에서 받은 사용량 데이터
        target_user (str): 특정 사용자 이메일 (None이면 전체 사용자)
    """
    try:
        if not usage_data or 'dailyUsageData' not in usage_data:
            print("❌ 사용량 데이터가 없습니다.")
            return
        
        daily_data = usage_data['dailyUsageData']
        
        if not daily_data:
            print("❌ 해당 기간에 사용량 데이터가 없습니다.")
            return
        
        # 사용자별 상세 활동 정보 수집
        user_activities = {}
        
        for day_data in daily_data:
            if 'usageData' in day_data:
                for usage in day_data['usageData']:
                    user_email = usage.get('userEmail', 'Unknown')
                    
                    # 특정 사용자만 필터링
                    if target_user and user_email != target_user:
                        continue
                    
                    if user_email not in user_activities:
                        user_activities[user_email] = []
                    
                    # 활동 정보 추가
                    activity = {
                        'date': day_data.get('date', 0),
                        'cost': usage.get('cost', 0),
                        'kind': usage.get('kind', 'Unknown'),
                        'maxMode': usage.get('maxMode', 'No'),
                        'model': usage.get('model', 'Unknown'),
                        'tokens': usage.get('tokens', 0),
                        'cost_requests': usage.get('cost', 0)
                    }
                    
                    user_activities[user_email].append(activity)
        
        if not user_activities:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 활동 데이터가 없습니다.")
            else:
                print("❌ 사용자별 활동 데이터가 없습니다.")
            return
        
        # 각 사용자별 상세 정보 출력
        for user_email, activities in user_activities.items():
            print(f"\n{'='*80}")
            print(f"👤 사용자: {user_email}")
            print(f"📊 총 활동 횟수: {len(activities)}회")
            print(f"{'='*80}")
            
            # 활동별 통계
            total_requests = sum(act['cost_requests'] for act in activities)
            total_tokens = sum(act['tokens'] for act in activities)
            models_used = set(act['model'] for act in activities)
            kinds_used = set(act['kind'] for act in activities)
            
            print(f"📈 활동 통계:")
            print(f"   • 총 요청 수: {total_requests}회")
            print(f"   • 총 토큰 수: {total_tokens:,}개")
            print(f"   • 사용한 모델: {', '.join(models_used)}")
            print(f"   • 활동 유형: {', '.join(kinds_used)}")
            print()
            
            # 날짜별로 그룹화
            activities_by_date = {}
            for activity in activities:
                date = activity['date']
                if date not in activities_by_date:
                    activities_by_date[date] = []
                activities_by_date[date].append(activity)
            
            # 날짜순으로 정렬하여 출력
            for date in sorted(activities_by_date.keys()):
                date_str = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')
                day_activities = activities_by_date[date]
                
                print(f"📅 날짜: {date_str}")
                print(f"   활동 횟수: {len(day_activities)}회")
                print()
                
                for idx, activity in enumerate(day_activities, 1):
                    print(f"   {idx}. 활동 상세:")
                    print(f"      • 유형: {activity['kind']}")
                    print(f"      • 모델: {activity['model']}")
                    print(f"      • 요청 수: {activity['cost_requests']}")
                    print(f"      • 토큰 수: {activity['tokens']:,}")
                    print(f"      • Max Mode: {activity['maxMode']}")
                    print()
            
            # 모델별 사용 통계
            model_stats = {}
            for activity in activities:
                model = activity['model']
                if model not in model_stats:
                    model_stats[model] = {'count': 0, 'tokens': 0, 'requests': 0}
                model_stats[model]['count'] += 1
                model_stats[model]['tokens'] += activity['tokens']
                model_stats[model]['requests'] += activity['cost_requests']
            
            print(f"🔍 모델별 사용 통계:")
            for model, stats in model_stats.items():
                print(f"   • {model}: {stats['count']}회, {stats['tokens']:,}토큰, {stats['requests']}요청")
            print()
            
            # 활동 유형별 통계
            kind_stats = {}
            for activity in activities:
                kind = activity['kind']
                if kind not in kind_stats:
                    kind_stats[kind] = {'count': 0, 'requests': 0}
                kind_stats[kind]['count'] += 1
                kind_stats[kind]['requests'] += activity['cost_requests']
            
            print(f"📋 활동 유형별 통계:")
            for kind, stats in kind_stats.items():
                print(f"   • {kind}: {stats['count']}회, {stats['requests']}요청")
            print()
        
        # 전체 요약 (여러 사용자가 있는 경우)
        if len(user_activities) > 1:
            print(f"\n{'='*80}")
            print(f"📊 전체 요약")
            print(f"{'='*80}")
            
            total_users = len(user_activities)
            total_activities = sum(len(acts) for acts in user_activities.values())
            total_requests = sum(sum(act['cost_requests'] for act in acts) for acts in user_activities.values())
            total_tokens = sum(sum(act['tokens'] for act in acts) for acts in user_activities.values())
            
            print(f"• 총 사용자 수: {total_users}명")
            print(f"• 총 활동 횟수: {total_activities}회")
            print(f"• 총 요청 수: {total_requests}회")
            print(f"• 총 토큰 수: {total_tokens:,}개")
            
            # 가장 활발한 사용자
            most_active_user = max(user_activities.items(), 
                                 key=lambda x: len(x[1]))
            print(f"• 가장 활발한 사용자: {most_active_user[0]} ({len(most_active_user[1])}회)")
        
    except Exception as e:
        print(f"❌ 상세 활동 데이터 표시 중 오류 발생: {e}")

def display_filtered_usage_events(usage_data: Dict, target_user: str = None) -> None:
    """
    필터링된 사용 이벤트 데이터를 출력합니다.
    
    Args:
        usage_data (Dict): API에서 받은 사용 이벤트 데이터
        target_user (str): 특정 사용자 이메일 (None이면 전체 사용자)
    """
    try:
        if not usage_data or 'usageEvents' not in usage_data:
            print("❌ 사용 이벤트 데이터가 없습니다.")
            return
        
        usage_events = usage_data['usageEvents']
        total_count = usage_data.get('totalUsageEventsCount', 0)
        pagination = usage_data.get('pagination', {})
        
        if not usage_events:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 사용 이벤트 데이터가 없습니다.")
            else:
                print("❌ 사용 이벤트 데이터가 없습니다.")
            return
        
        print(f"\n📊 사용 이벤트 데이터 (총 {total_count}개)")
        if pagination:
            print(f"페이지: {pagination.get('currentPage', 1)}/{pagination.get('numPages', 1)}")
        print("=" * 80)
        
        # 사용자별 상세 정보 출력
        user_events = {}
        
        for event in usage_events:
            user_email = event.get('userEmail', 'Unknown')
            
            # 특정 사용자만 필터링
            if target_user and user_email != target_user:
                continue
            
            if user_email not in user_events:
                user_events[user_email] = []
            
            user_events[user_email].append(event)
        
        if not user_events:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 사용 이벤트 데이터가 없습니다.")
            else:
                print("❌ 사용자별 사용 이벤트 데이터가 없습니다.")
            return
        
        # 각 사용자별 상세 정보 출력
        for user_email, events in user_events.items():
            print(f"\n{'='*80}")
            print(f"👤 사용자: {user_email}")
            print(f"📊 총 이벤트 수: {len(events)}개")
            print(f"{'='*80}")
            
            # 이벤트별 통계
            total_requests = sum(event.get('requestsCosts', 0) for event in events)
            total_tokens = sum(
                event.get('tokenUsage', {}).get('inputTokens', 0) + 
                event.get('tokenUsage', {}).get('outputTokens', 0) 
                for event in events if event.get('isTokenBasedCall', False)
            )
            models_used = set(event.get('model', 'Unknown') for event in events)
            kinds_used = set(event.get('kindLabel', 'Unknown') for event in events)
            
            print(f"📈 이벤트 통계:")
            print(f"   • 총 요청 비용: {total_requests}")
            print(f"   • 총 토큰 수: {total_tokens:,}개")
            print(f"   • 사용한 모델: {', '.join(models_used)}")
            print(f"   • 활동 유형: {', '.join(kinds_used)}")
            print()
            
            # 시간순으로 정렬하여 출력
            sorted_events = sorted(events, key=lambda x: int(x.get('timestamp', 0)))
            
            for idx, event in enumerate(sorted_events, 1):
                timestamp = int(event.get('timestamp', 0))
                date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"   {idx}. 이벤트 상세:")
                print(f"      • 시간: {date_str}")
                print(f"      • 유형: {event.get('kindLabel', 'Unknown')}")
                print(f"      • 모델: {event.get('model', 'Unknown')}")
                print(f"      • 요청 비용: {event.get('requestsCosts', 0)}")
                print(f"      • Max Mode: {event.get('maxMode', False)}")
                
                if event.get('isTokenBasedCall', False):
                    token_usage = event.get('tokenUsage', {})
                    print(f"      • 입력 토큰: {token_usage.get('inputTokens', 0):,}")
                    print(f"      • 출력 토큰: {token_usage.get('outputTokens', 0):,}")
                    print(f"      • 총 비용: ${token_usage.get('totalCents', 0) / 100:.4f}")
                
                print(f"      • Free Bugbot: {event.get('isFreeBugbot', False)}")
                print()
            
            # 모델별 사용 통계
            model_stats = {}
            for event in events:
                model = event.get('model', 'Unknown')
                if model not in model_stats:
                    model_stats[model] = {'count': 0, 'requests': 0, 'tokens': 0}
                model_stats[model]['count'] += 1
                model_stats[model]['requests'] += event.get('requestsCosts', 0)
                
                if event.get('isTokenBasedCall', False):
                    token_usage = event.get('tokenUsage', {})
                    model_stats[model]['tokens'] += (
                        token_usage.get('inputTokens', 0) + 
                        token_usage.get('outputTokens', 0)
                    )
            
            print(f"🔍 모델별 사용 통계:")
            for model, stats in model_stats.items():
                print(f"   • {model}: {stats['count']}회, {stats['requests']}요청, {stats['tokens']:,}토큰")
            print()
            
            # 활동 유형별 통계
            kind_stats = {}
            for event in events:
                kind = event.get('kindLabel', 'Unknown')
                if kind not in kind_stats:
                    kind_stats[kind] = {'count': 0, 'requests': 0}
                kind_stats[kind]['count'] += 1
                kind_stats[kind]['requests'] += event.get('requestsCosts', 0)
            
            print(f"📋 활동 유형별 통계:")
            for kind, stats in kind_stats.items():
                print(f"   • {kind}: {stats['count']}회, {stats['requests']}요청")
            print()
        
        # 전체 요약 (여러 사용자가 있는 경우)
        if len(user_events) > 1:
            print(f"\n{'='*80}")
            print(f"📊 전체 요약")
            print(f"{'='*80}")
            
            total_users = len(user_events)
            total_events = sum(len(events) for events in user_events.values())
            total_requests = sum(
                sum(event.get('requestsCosts', 0) for event in events) 
                for events in user_events.values()
            )
            
            print(f"• 총 사용자 수: {total_users}명")
            print(f"• 총 이벤트 수: {total_events}개")
            print(f"• 총 요청 비용: {total_requests}")
            
            # 가장 활발한 사용자
            most_active_user = max(user_events.items(), 
                                 key=lambda x: len(x[1]))
            print(f"• 가장 활발한 사용자: {most_active_user[0]} ({len(most_active_user[1])}개)")
        
    except Exception as e:
        print(f"❌ 사용 이벤트 데이터 표시 중 오류 발생: {e}")

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

def save_user_activity_to_csv(usage_data: Dict, target_user: str = None, filename: str = "user_activity.csv") -> None:
    """
    사용자별 상세 활동 정보를 CSV 파일로 저장합니다.
    
    Args:
        usage_data (Dict): API에서 받은 사용량 데이터
        target_user (str): 특정 사용자 이메일 (None이면 전체 사용자)
        filename (str): 저장할 파일명
    """
    try:
        if not usage_data or 'dailyUsageData' not in usage_data:
            print("❌ 사용량 데이터가 없습니다.")
            return
        
        daily_data = usage_data['dailyUsageData']
        
        if not daily_data:
            print("❌ 해당 기간에 사용량 데이터가 없습니다.")
            return
        
        # CSV 파일에 저장할 데이터 준비
        csv_data = []
        
        for day_data in daily_data:
            if 'usageData' in day_data:
                for usage in day_data['usageData']:
                    user_email = usage.get('userEmail', 'Unknown')
                    
                    # 특정 사용자만 필터링
                    if target_user and user_email != target_user:
                        continue
                    
                    # 활동 정보 추가
                    activity_row = {
                        '사용자 이메일': user_email,
                        '날짜': datetime.fromtimestamp(day_data.get('date', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                        '활동 유형': usage.get('kind', 'Unknown'),
                        '모델': usage.get('model', 'Unknown'),
                        '요청 수': usage.get('cost', 0),
                        '토큰 수': usage.get('tokens', 0),
                        'Max Mode': usage.get('maxMode', 'No'),
                        '타임스탬프': day_data.get('date', 0)
                    }
                    
                    csv_data.append(activity_row)
        
        if not csv_data:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 활동 데이터가 없습니다.")
            else:
                print("❌ 사용자별 활동 데이터가 없습니다.")
            return
        
        # CSV 파일로 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['사용자 이메일', '날짜', '활동 유형', '모델', '요청 수', '토큰 수', 'Max Mode', '타임스탬프']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 헤더 작성
            writer.writeheader()
            
            # 데이터 작성 (날짜순으로 정렬)
            sorted_data = sorted(csv_data, key=lambda x: x['타임스탬프'])
            for row in sorted_data:
                writer.writerow(row)
        
        print(f"✅ 총 {len(csv_data)}개의 활동 기록이 저장되었습니다.")
        
        # 요약 통계도 별도 시트로 저장
        save_summary_statistics_to_csv(csv_data, filename.replace('.csv', '_summary.csv'))
        
    except Exception as e:
        print(f"❌ CSV 파일 저장 중 오류 발생: {e}")

def save_summary_statistics_to_csv(csv_data: List[Dict], filename: str) -> None:
    """
    요약 통계를 별도 CSV 파일로 저장합니다.
    
    Args:
        csv_data (List[Dict]): 활동 데이터 리스트
        filename (str): 저장할 파일명
    """
    try:
        if not csv_data:
            return
        
        # 사용자별 통계 계산
        user_stats = {}
        
        for row in csv_data:
            user = row['사용자 이메일']
            if user not in user_stats:
                user_stats[user] = {
                    '총 활동 횟수': 0,
                    '총 요청 수': 0,
                    '총 토큰 수': 0,
                    '사용한 모델': set(),
                    '활동 유형': set()
                }
            
            user_stats[user]['총 활동 횟수'] += 1
            user_stats[user]['총 요청 수'] += row['요청 수']
            user_stats[user]['총 토큰 수'] += row['토큰 수']
            user_stats[user]['사용한 모델'].add(row['모델'])
            user_stats[user]['활동 유형'].add(row['활동 유형'])
        
        # 요약 통계 데이터 준비
        summary_data = []
        
        for user, stats in user_stats.items():
            summary_row = {
                '사용자 이메일': user,
                '총 활동 횟수': stats['총 활동 횟수'],
                '총 요청 수': stats['총 요청 수'],
                '총 토큰 수': stats['총 토큰 수'],
                '사용한 모델': ', '.join(stats['사용한 모델']),
                '활동 유형': ', '.join(stats['활동 유형'])
            }
            summary_data.append(summary_row)
        
        # 모델별 통계
        model_stats = {}
        for row in csv_data:
            model = row['모델']
            if model not in model_stats:
                model_stats[model] = {'사용 횟수': 0, '총 요청 수': 0, '총 토큰 수': 0}
            model_stats[model]['사용 횟수'] += 1
            model_stats[model]['총 요청 수'] += row['요청 수']
            model_stats[model]['총 토큰 수'] += row['토큰 수']
        
        # 활동 유형별 통계
        kind_stats = {}
        for row in csv_data:
            kind = row['활동 유형']
            if kind not in kind_stats:
                kind_stats[kind] = {'사용 횟수': 0, '총 요청 수': 0}
            kind_stats[kind]['사용 횟수'] += 1
            kind_stats[kind]['총 요청 수'] += row['요청 수']
        
        # 요약 통계 CSV 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 사용자별 요약
            writer = csv.writer(csvfile)
            writer.writerow(['=== 사용자별 요약 통계 ==='])
            writer.writerow(['사용자 이메일', '총 활동 횟수', '총 요청 수', '총 토큰 수', '사용한 모델', '활동 유형'])
            
            for summary in sorted(summary_data, key=lambda x: x['총 활동 횟수'], reverse=True):
                writer.writerow([
                    summary['사용자 이메일'],
                    summary['총 활동 횟수'],
                    summary['총 요청 수'],
                    summary['총 토큰 수'],
                    summary['사용한 모델'],
                    summary['활동 유형']
                ])
            
            writer.writerow([])  # 빈 줄
            
            # 모델별 통계
            writer.writerow(['=== 모델별 사용 통계 ==='])
            writer.writerow(['모델', '사용 횟수', '총 요청 수', '총 토큰 수'])
            
            for model, stats in sorted(model_stats.items(), key=lambda x: x[1]['사용 횟수'], reverse=True):
                writer.writerow([model, stats['사용 횟수'], stats['총 요청 수'], stats['총 토큰 수']])
            
            writer.writerow([])  # 빈 줄
            
            # 활동 유형별 통계
            writer.writerow(['=== 활동 유형별 통계 ==='])
            writer.writerow(['활동 유형', '사용 횟수', '총 요청 수'])
            
            for kind, stats in sorted(kind_stats.items(), key=lambda x: x[1]['사용 횟수'], reverse=True):
                writer.writerow([kind, stats['사용 횟수'], stats['총 요청 수']])
            
            writer.writerow([])  # 빈 줄
            
            # 전체 요약
            writer.writerow(['=== 전체 요약 ==='])
            writer.writerow(['항목', '값'])
            writer.writerow(['총 사용자 수', len(user_stats)])
            writer.writerow(['총 활동 횟수', len(csv_data)])
            writer.writerow(['총 요청 수', sum(row['요청 수'] for row in csv_data)])
            writer.writerow(['총 토큰 수', sum(row['토큰 수'] for row in csv_data)])
            
            if summary_data:
                most_active = max(summary_data, key=lambda x: x['총 활동 횟수'])
                writer.writerow(['가장 활발한 사용자', f"{most_active['사용자 이메일']} ({most_active['총 활동 횟수']}회)"])
        
        print(f"✅ 요약 통계가 '{filename}' 파일로 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ 요약 통계 CSV 저장 중 오류 발생: {e}")

def display_user_activity_as_csv(usage_data: Dict, target_user: str = None) -> None:
    """
    사용자별 상세 활동 정보를 CSV 형태로 출력합니다.
    
    Args:
        usage_data (Dict): API에서 받은 사용량 데이터
        target_user (str): 특정 사용자 이메일 (None이면 전체 사용자)
    """
    try:
        if not usage_data or 'dailyUsageData' not in usage_data:
            print("❌ 사용량 데이터가 없습니다.")
            return
        
        daily_data = usage_data['dailyUsageData']
        
        if not daily_data:
            print("❌ 해당 기간에 사용량 데이터가 없습니다.")
            return
        
        # CSV 형태로 출력할 데이터 준비
        csv_data = []
        
        for day_data in daily_data:
            if 'usageData' in day_data:
                for usage in day_data['usageData']:
                    user_email = usage.get('userEmail', 'Unknown')
                    
                    # 특정 사용자만 필터링
                    if target_user and user_email != target_user:
                        continue
                    
                    # 활동 정보 추가
                    activity_row = {
                        '사용자 이메일': user_email,
                        '날짜': datetime.fromtimestamp(day_data.get('date', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                        '활동 유형': usage.get('kind', 'Unknown'),
                        '모델': usage.get('model', 'Unknown'),
                        '요청 수': usage.get('cost', 0),
                        '토큰 수': usage.get('tokens', 0),
                        'Max Mode': usage.get('maxMode', 'No')
                    }
                    
                    csv_data.append(activity_row)
        
        if not csv_data:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 활동 데이터가 없습니다.")
            else:
                print("❌ 사용자별 활동 데이터가 없습니다.")
            return
        
        # CSV 헤더 출력
        fieldnames = ['사용자 이메일', '날짜', '활동 유형', '모델', '요청 수', '토큰 수', 'Max Mode']
        print(','.join(fieldnames))
        
        # 데이터 출력 (날짜순으로 정렬)
        sorted_data = sorted(csv_data, key=lambda x: datetime.strptime(x['날짜'], '%Y-%m-%d %H:%M:%S'))
        for row in sorted_data:
            csv_line = ','.join([
                f'"{row["사용자 이메일"]}"',
                f'"{row["날짜"]}"',
                f'"{row["활동 유형"]}"',
                f'"{row["모델"]}"',
                str(row['요청 수']),
                str(row['토큰 수']),
                f'"{row["Max Mode"]}"'
            ])
            print(csv_line)
        
        print(f"\n📊 총 {len(csv_data)}개의 활동 기록이 출력되었습니다.")
        
        # 요약 통계도 출력
        print("\n" + "="*80)
        print("📈 요약 통계")
        print("="*80)
        display_summary_statistics_as_text(csv_data)
        
    except Exception as e:
        print(f"❌ CSV 형태 출력 중 오류 발생: {e}")

def display_summary_statistics_as_text(csv_data: List[Dict]) -> None:
    """
    요약 통계를 텍스트 형태로 출력합니다.
    
    Args:
        csv_data (List[Dict]): 활동 데이터 리스트
    """
    try:
        if not csv_data:
            return
        
        # 사용자별 통계 계산
        user_stats = {}
        
        for row in csv_data:
            user = row['사용자 이메일']
            if user not in user_stats:
                user_stats[user] = {
                    '총 활동 횟수': 0,
                    '총 요청 수': 0,
                    '총 토큰 수': 0,
                    '사용한 모델': set(),
                    '활동 유형': set()
                }
            
            user_stats[user]['총 활동 횟수'] += 1
            user_stats[user]['총 요청 수'] += row['요청 수']
            user_stats[user]['총 토큰 수'] += row['토큰 수']
            user_stats[user]['사용한 모델'].add(row['모델'])
            user_stats[user]['활동 유형'].add(row['활동 유형'])
        
        # 사용자별 요약 출력
        print("👥 사용자별 요약 통계:")
        print("-" * 60)
        print(f"{'사용자 이메일':<30} {'활동 횟수':<10} {'요청 수':<10} {'토큰 수':<15}")
        print("-" * 60)
        
        for user, stats in sorted(user_stats.items(), key=lambda x: x[1]['총 활동 횟수'], reverse=True):
            print(f"{user:<30} {stats['총 활동 횟수']:<10} {stats['총 요청 수']:<10} {stats['총 토큰 수']:<15}")
        
        print("-" * 60)
        
        # 모델별 통계
        model_stats = {}
        for row in csv_data:
            model = row['모델']
            if model not in model_stats:
                model_stats[model] = {'사용 횟수': 0, '총 요청 수': 0, '총 토큰 수': 0}
            model_stats[model]['사용 횟수'] += 1
            model_stats[model]['총 요청 수'] += row['요청 수']
            model_stats[model]['총 토큰 수'] += row['토큰 수']
        
        print("\n🤖 모델별 사용 통계:")
        print("-" * 50)
        print(f"{'모델':<25} {'사용 횟수':<10} {'요청 수':<10} {'토큰 수':<15}")
        print("-" * 50)
        
        for model, stats in sorted(model_stats.items(), key=lambda x: x[1]['사용 횟수'], reverse=True):
            print(f"{model:<25} {stats['사용 횟수']:<10} {stats['총 요청 수']:<10} {stats['총 토큰 수']:<15}")
        
        print("-" * 50)
        
        # 활동 유형별 통계
        kind_stats = {}
        for row in csv_data:
            kind = row['활동 유형']
            if kind not in kind_stats:
                kind_stats[kind] = {'사용 횟수': 0, '총 요청 수': 0}
            kind_stats[kind]['사용 횟수'] += 1
            kind_stats[kind]['총 요청 수'] += row['요청 수']
        
        print("\n📋 활동 유형별 통계:")
        print("-" * 50)
        print(f"{'활동 유형':<25} {'사용 횟수':<10} {'요청 수':<10}")
        print("-" * 50)
        
        for kind, stats in sorted(kind_stats.items(), key=lambda x: x[1]['사용 횟수'], reverse=True):
            print(f"{kind:<25} {stats['사용 횟수']:<10} {stats['총 요청 수']:<10}")
        
        print("-" * 50)
        
        # 전체 요약
        print("\n📊 전체 요약:")
        print(f"• 총 사용자 수: {len(user_stats)}명")
        print(f"• 총 활동 횟수: {len(csv_data)}회")
        print(f"• 총 요청 수: {sum(row['요청 수'] for row in csv_data)}회")
        print(f"• 총 토큰 수: {sum(row['토큰 수'] for row in csv_data):,}개")
        
        if user_stats:
            most_active = max(user_stats.items(), key=lambda x: x[1]['총 활동 횟수'])
            print(f"• 가장 활발한 사용자: {most_active[0]} ({most_active[1]['총 활동 횟수']}회)")
        
    except Exception as e:
        print(f"❌ 요약 통계 출력 중 오류 발생: {e}")

def display_detailed_usage_events(usage_data: Dict, target_user: str = None, date_str: str = "") -> None:
    """
    특정 날짜의 사용자별 상세 활동 내역을 표 형태로 출력합니다.
    
    Args:
        usage_data (Dict): filtered-usage-events API에서 받은 데이터
        target_user (str): 특정 사용자 이메일 (None이면 전체 사용자)
        date_str (str): 조회한 날짜 문자열
    """
    try:
        if not usage_data or 'usageEvents' not in usage_data:
            print("❌ 활동 데이터가 없습니다.")
            return
        
        usage_events = usage_data['usageEvents']
        total_count = usage_data.get('totalUsageEventsCount', 0)
        
        if not usage_events:
            print(f"❌ {date_str} 날짜에 활동 데이터가 없습니다.")
            return
        
        # 사용자별로 이벤트 그룹화
        user_events = {}
        for event in usage_events:
            user_email = event.get('userEmail', 'Unknown')
            
            # 특정 사용자만 필터링
            if target_user and user_email != target_user:
                continue
            
            if user_email not in user_events:
                user_events[user_email] = []
            
            user_events[user_email].append(event)
        
        if not user_events:
            if target_user:
                print(f"❌ '{target_user}' 사용자의 {date_str} 날짜 활동 데이터가 없습니다.")
            else:
                print(f"❌ {date_str} 날짜에 활동 데이터가 없습니다.")
            return
        
        # 헤더 출력
        print(f"\n{'='*100}")
        if target_user:
            print(f"📊 {target_user} 사용자의 {date_str} 활동 내역")
        else:
            print(f"📊 {date_str} 전체 사용자 활동 내역 (총 {len(user_events)}명)")
        print(f"{'='*100}")
        
        # 표 헤더
        print(f"{'날짜/시간':<20} {'사용자':<25} {'종류':<15} {'모델':<20} {'MAX':<5} {'요청수':<8} {'토큰수':<10}")
        print("-" * 100)
        
        # 전체 통계를 위한 변수
        total_events = 0
        total_requests = 0
        total_tokens = 0
        
        # 사용자별 데이터 출력
        for user_email, events in sorted(user_events.items()):
            # 시간순으로 정렬
            sorted_events = sorted(events, key=lambda x: int(x.get('timestamp', 0)))
            
            user_total_events = len(events)
            user_total_requests = sum(event.get('requestsCosts', 0) for event in events)
            user_total_tokens = sum(
                (event.get('tokenUsage', {}).get('inputTokens', 0) + 
                 event.get('tokenUsage', {}).get('outputTokens', 0))
                if event.get('isTokenBasedCall', False) else 0
                for event in events
            )
            
            # 각 이벤트 출력
            for idx, event in enumerate(sorted_events):
                timestamp = int(event.get('timestamp', 0))
                time_str = datetime.fromtimestamp(timestamp / 1000).strftime('%m-%d %H:%M:%S')
                
                kind_label = event.get('kindLabel', 'Unknown')
                model = event.get('model', 'Unknown')
                max_mode = "Yes" if event.get('maxMode', False) else "No"
                requests = event.get('requestsCosts', 0)
                
                # 토큰 정보
                if event.get('isTokenBasedCall', False):
                    token_usage = event.get('tokenUsage', {})
                    tokens = token_usage.get('inputTokens', 0) + token_usage.get('outputTokens', 0)
                else:
                    tokens = 0
                
                # 첫 번째 행에는 사용자 이메일 표시, 나머지는 공백
                user_display = user_email if idx == 0 else ""
                
                print(f"{time_str:<20} {user_display:<25} {kind_label:<15} {model:<20} {max_mode:<5} {requests:<8.1f} {tokens:<10,}")
            
            # 사용자별 소계 출력
            if len(events) > 1:
                print("-" * 100)
                print(f"{'소계':<20} {user_email:<25} {'총 ' + str(user_total_events) + '건':<15} {'':<20} {'':<5} {user_total_requests:<8.1f} {user_total_tokens:<10,}")
                print("-" * 100)
            
            total_events += user_total_events
            total_requests += user_total_requests
            total_tokens += user_total_tokens
        
        # 전체 합계 출력 (여러 사용자인 경우)
        if len(user_events) > 1:
            print("=" * 100)
            total_users_text = f"{len(user_events)}명 참여"
            total_events_text = f"총 {total_events}건"
            print(f"{'전체 합계':<20} {total_users_text:<25} {total_events_text:<15} {'':<20} {'':<5} {total_requests:<8.1f} {total_tokens:<10,}")
            print("=" * 100)
        
        # 상세 통계 출력
        print(f"\n📈 상세 통계:")
        print(f"• 조회 날짜: {date_str}")
        print(f"• 참여 사용자 수: {len(user_events)}명")
        print(f"• 총 활동 건수: {total_events}건")
        print(f"• 총 요청 비용: {total_requests:.1f}")
        print(f"• 총 토큰 사용량: {total_tokens:,}개")
        
        # 모델별 사용 통계
        model_stats = {}
        kind_stats = {}
        
        for events in user_events.values():
            for event in events:
                # 모델별 통계
                model = event.get('model', 'Unknown')
                if model not in model_stats:
                    model_stats[model] = {'count': 0, 'requests': 0, 'tokens': 0}
                model_stats[model]['count'] += 1
                model_stats[model]['requests'] += event.get('requestsCosts', 0)
                
                if event.get('isTokenBasedCall', False):
                    token_usage = event.get('tokenUsage', {})
                    model_stats[model]['tokens'] += (
                        token_usage.get('inputTokens', 0) + 
                        token_usage.get('outputTokens', 0)
                    )
                
                # 종류별 통계
                kind = event.get('kindLabel', 'Unknown')
                if kind not in kind_stats:
                    kind_stats[kind] = {'count': 0, 'requests': 0}
                kind_stats[kind]['count'] += 1
                kind_stats[kind]['requests'] += event.get('requestsCosts', 0)
        
        # 모델별 통계 출력
        if model_stats:
            print(f"\n🤖 모델별 사용 통계:")
            for model, stats in sorted(model_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                print(f"   • {model}: {stats['count']}회, 요청 {stats['requests']:.1f}, 토큰 {stats['tokens']:,}개")
        
        # 종류별 통계 출력
        if kind_stats:
            print(f"\n📋 활동 종류별 통계:")
            for kind, stats in sorted(kind_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                print(f"   • {kind}: {stats['count']}회, 요청 {stats['requests']:.1f}")
        
        # 가장 활발한 사용자
        if len(user_events) > 1:
            most_active_user = max(user_events.items(), key=lambda x: len(x[1]))
            print(f"\n🏆 가장 활발한 사용자: {most_active_user[0]} ({len(most_active_user[1])}건)")
        
    except Exception as e:
        print(f"❌ 활동 내역 출력 중 오류 발생: {e}")

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
            print("9. 사용자별 사용 횟수 확인")
            print("10. 사용자별 상세 활동 확인")
            print("11. 특정 날짜 활동 내역 조회")
            print("0. 종료")
            
            choice = input("\n선택하세요 (0-11): ").strip()
            
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
                    
            elif choice == '9':
                print("\n=== 사용자별 사용 횟수 확인 ===")
                print("날짜 형식: YYYY-MM-DD (예: 2024-07-01)")
                print("날짜를 입력하지 않으면 이번 달 1일부터 오늘까지 조회됩니다.")
                
                start_date_str = input("시작 날짜 (선택사항): ").strip() or None
                end_date_str = input("종료 날짜 (선택사항): ").strip() or None
                
                start_ms, end_ms = get_date_range(start_date_str, end_date_str)
                
                if start_ms and end_ms:
                    print(f"\n🔄 {datetime.fromtimestamp(start_ms/1000).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(end_ms/1000).strftime('%Y-%m-%d')} 사용자별 사용 횟수를 가져오는 중...")
                    usage_data = api.get_user_usage_summary(start_ms, end_ms)
                    if usage_data:
                        print("\n=== 출력 옵션 ===")
                        print("1. 요약 정보만 보기")
                        print("2. 상세 활동 정보 보기")
                        
                        output_choice = input("선택하세요 (1-2): ").strip()
                        
                        if output_choice == '1':
                            display_user_usage_summary(usage_data)
                        elif output_choice == '2':
                            user_email = input("특정 사용자 이메일을 입력하세요 (선택사항): ").strip() or None
                            if user_email:
                                print(f"\n📋 '{user_email}' 사용자의 상세 활동 정보:")
                            else:
                                print(f"\n📋 전체 사용자의 상세 활동 정보:")
                            display_user_detailed_activity(usage_data, user_email)
                        else:
                            print("❌ 잘못된 선택입니다.")
                    else:
                        print("❌ 사용자별 사용 횟수 데이터를 가져오는데 실패했습니다.")
                else:
                    print("❌ 날짜 형식이 잘못되었습니다.")
                    
            elif choice == '10':
                print("\n=== 사용자별 상세 활동 확인 ===")
                print("날짜 형식: YYYY-MM-DD (예: 2024-07-01)")
                print("날짜를 입력하지 않으면 이번 달 1일부터 오늘까지 조회됩니다.")
                
                start_date_str = input("시작 날짜 (선택사항): ").strip() or None
                end_date_str = input("종료 날짜 (선택사항): ").strip() or None
                
                start_ms, end_ms = get_date_range(start_date_str, end_date_str)
                
                if start_ms and end_ms:
                    print(f"\n🔄 {datetime.fromtimestamp(start_ms/1000).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(end_ms/1000).strftime('%Y-%m-%d')} 사용자별 상세 활동을 가져오는 중...")
                    user_email = input("특정 사용자 이메일을 입력하세요 (선택사항): ").strip() or None
                    if user_email:
                        display_user_detailed_activity(api.get_user_usage_summary(start_ms, end_ms), user_email)
                    else:
                        display_user_detailed_activity(api.get_user_usage_summary(start_ms, end_ms))
                else:
                    print("❌ 날짜 형식이 잘못되었습니다.")
                    
            elif choice == '11':
                print("\n=== 사용자별 상세 활동 내역 확인 ===")
                print("날짜 형식: YYYY-MM-DD (예: 2024-07-28)")
                print("특정 날짜의 사용자 활동 내역을 상세하게 확인할 수 있습니다.")
                
                start_date_str = input("날짜를 입력하세요: ").strip()
                if not start_date_str:
                    # 오늘 날짜로 기본 설정
                    start_date_str = datetime.now().strftime('%Y-%m-%d')
                    print(f"날짜가 입력되지 않아 오늘 날짜({start_date_str})로 설정합니다.")
                
                try:
                    # 입력된 날짜를 파싱
                    target_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    start_ms = int(target_date.timestamp() * 1000)
                    end_ms = int((target_date + timedelta(days=1)).timestamp() * 1000)
                    
                    print(f"\n🔄 {start_date_str} 날짜의 사용자별 활동 내역을 가져오는 중...")
                    
                    # filtered-usage-events 엔드포인트 사용
                    usage_data = api.get_filtered_usage_events(
                        start_date=start_ms,
                        end_date=end_ms,
                        page_size=1000  # 더 많은 결과를 가져오기 위해
                    )
                    
                    if usage_data and usage_data.get('usageEvents'):
                        user_email = input("특정 사용자 이메일을 입력하세요 (선택사항, 전체 보려면 엔터): ").strip() or None
                        display_detailed_usage_events(usage_data, user_email, start_date_str)
                    else:
                        print(f"❌ {start_date_str} 날짜에 활동 데이터가 없습니다.")
                        
                except ValueError:
                    print("❌ 날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")
                except Exception as e:
                    print(f"❌ 데이터를 가져오는 중 오류 발생: {e}")
            else:
                print("❌ 잘못된 선택입니다.")
        
        print("\n프로그램을 종료합니다.")
        
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main() 