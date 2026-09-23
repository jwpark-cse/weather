# API로 날씨 정보 가져오기
import requests
from datetime import datetime, timedelta
import json
from typing import Optional

# 한국 주요 도시 좌표
KOREA_CITIES = {
    '서울': {'lat': 37.5665, 'lon': 126.9780},
    '부산': {'lat': 35.1796, 'lon': 129.0756},
    '인천': {'lat': 37.4563, 'lon': 126.7052},
    '대구': {'lat': 35.8714, 'lon': 128.6014},
    '대전': {'lat': 36.3504, 'lon': 127.3845},
    '광주': {'lat': 35.1595, 'lon': 126.8526},
    '수원': {'lat': 37.2636, 'lon': 127.0286},
    '울산': {'lat': 35.5384, 'lon': 129.3114},
    '창원': {'lat': 35.2281, 'lon': 128.6811},
    '고양': {'lat': 37.6564, 'lon': 126.8350},
    '용인': {'lat': 37.2410, 'lon': 127.1776},
    '성남': {'lat': 37.4386, 'lon': 127.1378},
    '부천': {'lat': 37.4989, 'lon': 126.7831},
    '청주': {'lat': 36.6424, 'lon': 127.4890},
    '전주': {'lat': 35.8242, 'lon': 127.1480},
    '안산': {'lat': 37.3219, 'lon': 126.8309},
    '천안': {'lat': 36.8151, 'lon': 127.1139},
    '김해': {'lat': 35.2285, 'lon': 128.8809},
    '제주': {'lat': 33.4996, 'lon': 126.5312},
    '강릉': {'lat': 37.7519, 'lon': 128.8760},
    '춘천': {'lat': 37.8813, 'lon': 127.7298},
    '원주': {'lat': 37.3422, 'lon': 127.9202},
    '목포': {'lat': 34.8118, 'lon': 126.3922},
    '여수': {'lat': 34.7604, 'lon': 127.6622},
    '순천': {'lat': 34.9506, 'lon': 127.4922},
    '포항': {'lat': 36.0190, 'lon': 129.3435},
    '경주': {'lat': 35.8562, 'lon': 129.2247},
    '안동': {'lat': 36.5684, 'lon': 128.7294},
    '구미': {'lat': 36.1196, 'lon': 128.3394},
    '김천': {'lat': 36.1395, 'lon': 128.1147},
    '상주': {'lat': 36.4091, 'lon': 128.1574},
    '문경': {'lat': 36.5874, 'lon': 128.1874},
    '영주': {'lat': 36.8062, 'lon': 128.6229},
    '영천': {'lat': 35.9754, 'lon': 128.9380},
    '경산': {'lat': 35.8254, 'lon': 128.7429},
    '군위': {'lat': 36.2062, 'lon': 128.4929},
    '의성': {'lat': 36.3629, 'lon': 128.6929},
    '청송': {'lat': 36.3929, 'lon': 129.0429},
    '영양': {'lat': 36.6029, 'lon': 129.1429},
    '봉화': {'lat': 36.8229, 'lon': 128.7329},
    '울진': {'lat': 36.9929, 'lon': 129.4029},
    '영덕': {'lat': 36.4129, 'lon': 129.1229},
    '칠곡': {'lat': 35.9929, 'lon': 128.3929},
    '성주': {'lat': 35.9829, 'lon': 128.2629},
    '고령': {'lat': 35.7429, 'lon': 128.2629},
    '창녕': {'lat': 35.5429, 'lon': 128.4029},
    '함안': {'lat': 35.2729, 'lon': 128.4029},
    '의령': {'lat': 35.2929, 'lon': 128.2629},
    '합천': {'lat': 35.5629, 'lon': 128.1729},
    '거창': {'lat': 35.7029, 'lon': 127.9029},
    '무주': {'lat': 35.9929, 'lon': 127.7429},
    '진안': {'lat': 35.7829, 'lon': 127.7129},
    '장수': {'lat': 35.6929, 'lon': 127.8229},
    '임실': {'lat': 35.6329, 'lon': 127.6129},
    '남원': {'lat': 35.4129, 'lon': 127.6029},
    '순창': {'lat': 35.3829, 'lon': 127.3329},
    '고창': {'lat': 35.4329, 'lon': 126.7029},
    '부안': {'lat': 35.7329, 'lon': 126.7329},
    '김제': {'lat': 35.8029, 'lon': 126.8829},
    '익산': {'lat': 35.9429, 'lon': 126.9629},
    '군산': {'lat': 35.9829, 'lon': 126.7129},
    '보령': {'lat': 36.3329, 'lon': 126.6129},
    '서천': {'lat': 36.0929, 'lon': 126.6629},
    '홍성': {'lat': 36.6029, 'lon': 126.6729},
    '예산': {'lat': 36.6829, 'lon': 126.8429},
    '서산': {'lat': 36.7829, 'lon': 126.4529},
    '태안': {'lat': 36.7429, 'lon': 126.2829},
    '당진': {'lat': 36.8929, 'lon': 126.6329},
    '아산': {'lat': 36.7829, 'lon': 127.0029},
    '논산': {'lat': 36.2029, 'lon': 127.0829},
    '계룡': {'lat': 36.2629, 'lon': 127.2629},
    '공주': {'lat': 36.4529, 'lon': 127.1229},
    '부여': {'lat': 36.2829, 'lon': 126.9029},
    '금산': {'lat': 36.1129, 'lon': 127.4729},
    '옥천': {'lat': 36.3029, 'lon': 127.6829},
    '영동': {'lat': 36.1729, 'lon': 127.7829},
    '증평': {'lat': 36.7829, 'lon': 127.5629},
    '진천': {'lat': 36.8629, 'lon': 127.4329},
    '음성': {'lat': 36.9629, 'lon': 127.6929},
    '괴산': {'lat': 36.8429, 'lon': 127.8629},
    '단양': {'lat': 36.9829, 'lon': 128.3629},
    '제천': {'lat': 37.1329, 'lon': 128.1929},
    '영월': {'lat': 37.1829, 'lon': 128.4629},
    '평창': {'lat': 37.3729, 'lon': 128.3929},
    '정선': {'lat': 37.4029, 'lon': 128.6729},
    '태백': {'lat': 37.1629, 'lon': 128.9829},
    '삼척': {'lat': 37.4429, 'lon': 129.1629},
    '동해': {'lat': 37.5229, 'lon': 129.1129},
    '속초': {'lat': 38.2029, 'lon': 128.5929},
    '고성': {'lat': 38.3829, 'lon': 128.4629},
    '양양': {'lat': 38.0829, 'lon': 128.6229},
    '인제': {'lat': 38.0629, 'lon': 128.1729},
    '양구': {'lat': 38.1029, 'lon': 127.9929},
    '화천': {'lat': 38.1029, 'lon': 127.7229},
    '철원': {'lat': 38.1429, 'lon': 127.3229},
    '연천': {'lat': 38.0829, 'lon': 127.0729},
    '포천': {'lat': 37.8929, 'lon': 127.2029},
    '동두천': {'lat': 37.9229, 'lon': 127.0529},
    '의정부': {'lat': 37.7329, 'lon': 127.0329},
    '양주': {'lat': 37.7829, 'lon': 127.0429},
    '남양주': {'lat': 37.6329, 'lon': 127.2129},
    '구리': {'lat': 37.5929, 'lon': 127.1329},
    '하남': {'lat': 37.5329, 'lon': 127.2129},
    '광주': {'lat': 37.4129, 'lon': 127.2529},
    '이천': {'lat': 37.2729, 'lon': 127.4429},
    '여주': {'lat': 37.2929, 'lon': 127.6329},
    '양평': {'lat': 37.4929, 'lon': 127.4929},
    '가평': {'lat': 37.8329, 'lon': 127.5129},
    '파주': {'lat': 37.7529, 'lon': 126.7829},
    '김포': {'lat': 37.6129, 'lon': 126.7129},
    '시흥': {'lat': 37.3829, 'lon': 126.8129},
    '군포': {'lat': 37.3629, 'lon': 126.9329},
    '의왕': {'lat': 37.3429, 'lon': 126.9629},
    '과천': {'lat': 37.4329, 'lon': 126.9929},
    '광명': {'lat': 37.4829, 'lon': 126.8629},
    '오산': {'lat': 37.1529, 'lon': 127.0729},
    '평택': {'lat': 36.9929, 'lon': 127.1129},
    '안성': {'lat': 37.0129, 'lon': 127.2829},
    '화성': {'lat': 37.2029, 'lon': 126.8129},
}


def get_coordinates(location: str) -> dict:
    """
    지역명으로 좌표 찾기
    
    Args:
        location: 지역명
    
    Returns:
        {'lat': float, 'lon': float, 'name': str}
    """
    location = location.strip()
    
    # 알려진 도시인지 확인
    if location in KOREA_CITIES:
        coords = KOREA_CITIES[location]
        return {'lat': coords['lat'], 'lon': coords['lon'], 'name': location}
    
    # 좌표 직접 입력 처리 (예: "37.5665,126.9780")
    if ',' in location:
        try:
            parts = location.split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return {'lat': lat, 'lon': lon, 'name': f"{lat:.2f}, {lon:.2f}"}
        except:
            pass
    
    # 기본값: 서울
    print(f"⚠️  '{location}' 지역의 좌표를 찾을 수 없습니다. 서울 좌표를 사용합니다.")
    return {'lat': 37.5665, 'lon': 126.9780, 'name': '서울'}


def get_weather_data(lat: float, lon: float) -> Optional[dict]:
    """
    Open-Meteo API 에서 날씨 데이터 가져오기
    
    Args:
        lat: 위도
        lon: 경도
    
    Returns:
        날씨 데이터 딕셔너리
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # 파라미터 수동으로 구성 (인코딩 문제 방지)
    params = (
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,weathercode,windspeed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&timezone=Asia/Seoul"
        f"&forecast_days=3"
    )
    
    url = f"{base_url}?{params}"
    
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Python-Weather-App',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: 날씨 정보를 가져오는데 실패했습니다: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def parse_weather_code(code: int) -> str:
    """
    WMO 날씨 코드를 한글로 변환
    
    Args:
        code: WMO 날씨 코드
    
    Returns:
        날씨 상태 문자열
    """
    weather_codes = {
        0: '맑음',
        1: '주로 맑음',
        2: '구름많음',
        3: '흐림',
        45: '안개',
        48: '안개 (서리)',
        51: '이슬비 (약함)',
        53: '이슬비 (보통)',
        55: '이슬비 (강함)',
        56: '얼어붙는 이슬비 (약함)',
        57: '얼어붙는 이슬비 (강함)',
        61: '비 (약함)',
        63: '비 (보통)',
        65: '비 (강함)',
        66: '얼어붙는 비 (약함)',
        67: '얼어붙는 비 (강함)',
        71: '눈 (약함)',
        73: '눈 (보통)',
        75: '눈 (강함)',
        77: '눈알',
        80: '소나기 (약함)',
        81: '소나기 (보통)',
        82: '소나기 (강함)',
        85: '눈소나기 (약함)',
        86: '눈소나기 (강함)',
        95: '뇌우',
        96: '뇌우 + 우박',
        99: '뇌우 + 강한 우박',
    }
    
    return weather_codes.get(code, '정보없음')

def extract_hourly_data(hourly_data: dict, target_hour: int, day_offset: int) -> dict:
    """
    시간별 데이터에서 특정 시간의 데이터 추출
    
    Args:
        hourly_data: Open-Meteo 의 hourly 데이터
        target_hour: 목표 시간 (6 또는 15)
        day_offset: 일 오프셋 (0=오늘, 1=내일, 2=모레)
    
    Returns:
        날씨 데이터 딕셔너리
    """
    result = {
        'condition': '정보없음',
        'temp': 'N/A',
        'precip': 'N/A',
        'humidity': 'N/A',
        'wind': 'N/A'
    }
    
    if not hourly_data:
        return result
    
    times = hourly_data.get('time', [])
    temps = hourly_data.get('temperature_2m', [])
    humidity = hourly_data.get('relativehumidity_2m', [])
    precip = hourly_data.get('precipitation_probability', [])
    weather = hourly_data.get('weathercode', [])
    wind = hourly_data.get('windspeed_10m', [])
    
    # 현재 시간부터 3 일 후까지의 인덱스 계산
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    target_date = today_start + timedelta(days=day_offset)
    
    # API 가 반환하는 시간은 현지 시간 (Asia/Seoul) 이므로 직접 비교
    for i, time_str in enumerate(times):
        try:
            # ISO 형식 파싱 (예: "2026-09-22T06:00")
            data_time = datetime.fromisoformat(time_str)
            
            if (data_time.date() == target_date.date() and 
                data_time.hour == target_hour):
                
                # 데이터 추출
                if i < len(temps) and temps[i] is not None:
                    result['temp'] = f"{round(temps[i])} °C"
                
                if i < len(precip) and precip[i] is not None:
                    result['precip'] = f"{precip[i]}%"
                
                if i < len(humidity) and humidity[i] is not None:
                    result['humidity'] = f"{humidity[i]}%"
                
                if i < len(weather) and weather[i] is not None:
                    result['condition'] = parse_weather_code(weather[i])
                
                if i < len(wind) and wind[i] is not None:
                    result['wind'] = f"{round(wind[i])} m/s"
                
                break
        except Exception as e:
            continue
    
    return result


def extract_daily_data(daily_data: dict, day_offset: int) -> dict:
    """
    일일 데이터에서 최저/최고 기온 추출
    
    Args:
        daily_data: Open-Meteo 의 daily 데이터
        day_offset: 일 오프셋 (0=오늘, 1=내일, 2=모레)
    
    Returns:
        {'min_temp': str, 'max_temp': str}
    """
    result = {'min_temp': 'N/A', 'max_temp': 'N/A'}
    
    if not daily_data:
        return result
    
    min_temps = daily_data.get('temperature_2m_min', [])
    max_temps = daily_data.get('temperature_2m_max', [])
    
    if day_offset < len(min_temps) and min_temps[day_offset] is not None:
        result['min_temp'] = f"{round(min_temps[day_offset])} °C"
    
    if day_offset < len(max_temps) and max_temps[day_offset] is not None:
        result['max_temp'] = f"{round(max_temps[day_offset])} °C"
    
    return result


def get_weather(location: str = "서울") -> dict:
    """
    날씨 정보 가져오기
    
    Args:
        location: 지역명
    
    Returns:
        날씨 정보 딕셔너리
    """
    # 좌표 찾기
    coords = get_coordinates(location)
    
    print(f"📍 {coords['name']} (위도: {coords['lat']}, 경도: {coords['lon']}) 의 날씨 정보를 가져옵니다...")
    
    # API 호출
    weather_data = get_weather_data(coords['lat'], coords['lon'])
    
    if not weather_data:
        return {
            'location': location,
            'forecast': []
        }
    
    # 데이터 파싱
    hourly = weather_data.get('hourly', {})
    daily = weather_data.get('daily', {})
    
    forecast = []
    today = datetime.now()
    
    for day_offset in range(3):
        date = today + timedelta(days=day_offset)
        day_name = ['오늘', '내일', '모레'][day_offset]
        
        # 오전 6 시 데이터
        morning_data = extract_hourly_data(hourly, 6, day_offset)
        
        # 오후 3 시 데이터
        afternoon_data = extract_hourly_data(hourly, 15, day_offset)
        
        # 일일 데이터
        daily_temp = extract_daily_data(daily, day_offset)
        
        day_info = {
            'date': date.strftime("%m.%d."),
            'day_name': day_name,
            'morning': {
                'time': '06:00',
                'condition': morning_data['condition'],
                'temp': morning_data['temp'],
                'precip': morning_data['precip'],
                'humidity': morning_data['humidity'],
                'wind': morning_data['wind']
            },
            'afternoon': {
                'time': '15:00',
                'condition': afternoon_data['condition'],
                'temp': afternoon_data['temp'],
                'precip': afternoon_data['precip'],
                'humidity': afternoon_data['humidity'],
                'wind': afternoon_data['wind']
            },
            'min_temp': daily_temp['min_temp'],
            'max_temp': daily_temp['max_temp']
        }
        
        forecast.append(day_info)
    
    return {
        'location': coords['name'],
        'forecast': forecast
    }


def display_weather(weather_data: dict):
    """
    날씨 정보를 화면에 표시
    """
    if not weather_data or not weather_data.get('forecast'):
        print("날씨 정보를 가져올 수 없습니다.")
        return
    
    print("\n" + "="*70)
    print(f"🌤️  {weather_data['location']} 날씨 예보 (오전 6 시 / 오후 3 시 기준)")
    print("="*70 + "\n")
    
    for day in weather_data['forecast']:
        print(f"📅 {day['day_name']} ({day['date']})")
        print("-" * 60)
        
        # 오전 6 시
        morning = day['morning']
        print(f"  🌅 오전 {morning['time']}")
        print(f"     날씨: {morning['condition']}")
        print(f"     기온: {morning['temp']}")
        print(f"     강수확률: {morning['precip']}")
        if morning['humidity'] != 'N/A':
            print(f"     습도: {morning['humidity']}")
        if morning['wind'] != 'N/A':
            print(f"     풍속: {morning['wind']}")
        
        print()
        
        # 오후 3 시
        afternoon = day['afternoon']
        print(f"  🌇 오후 {afternoon['time']}")
        print(f"     날씨: {afternoon['condition']}")
        print(f"     기온: {afternoon['temp']}")
        print(f"     강수확률: {afternoon['precip']}")
        if afternoon['humidity'] != 'N/A':
            print(f"     습도: {afternoon['humidity']}")
        if afternoon['wind'] != 'N/A':
            print(f"     풍속: {afternoon['wind']}")
        
        print()
        
        # 최저/최고 기온
        if day['min_temp'] != 'N/A' or day['max_temp'] != 'N/A':
            print(f"  🌡️  일일 기온: 최저 {day['min_temp']} / 최고 {day['max_temp']}")
        
        print("\n" + "="*70 + "\n")


def save_to_json(weather_data: dict, filename: str = None):
    """
    날씨 정보를 JSON 파일로 저장
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_{weather_data['location']}_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 날씨 정보가 '{filename}' 파일로 저장되었습니다.")
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {e}")

def main():
    """
    메인 함수
    """
    print("🌤️  날씨 예보 프로그램 (Open-Meteo API)")
    print("-" * 50)
    print("오전 6 시, 오후 3 시 기준으로 3 일간 날씨를 제공합니다.")
    print("-" * 50)
    
    # 사용자에게 지역 입력 받기
    location = input("\n날씨를 확인할 지역을 입력하세요 (기본값: 서울): ").strip()
    
    # 입력이 없으면 기본값 사용
    if not location:
        location = "서울"
    
    print()
    
    # 날씨 정보 가져오기
    weather_data = get_weather(location)
    
    # 결과 표시
    display_weather(weather_data)
    
    # JSON 저장 여부 확인
    if weather_data and weather_data.get('forecast'):
        save = input("\n날씨 정보를 JSON 파일로 저장하시겠습니까? (y/n): ").strip().lower()
        if save == 'y':
            save_to_json(weather_data)


if __name__ == "__main__":
    main()