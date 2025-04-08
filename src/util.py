from datetime import datetime, timedelta


def diff_minutes(start: str, end: str) -> int:
    """
    HHMM 형식의 문자열 2개의 분 차이를 반환

    Args:
        start(str)  : 시작 시간
        end(str)    : 끝 시간

    Returns:
        int:    분 차이

    Raises:
        ValueError: 둘 중 하나라도 HHMM이 아닌 경우.
    """
    fmt = "%H%M"
    dt1 = datetime.strptime(start, fmt)
    dt2 = datetime.strptime(end, fmt)
    if dt2 < dt1:
        dt2 += timedelta(days=1)
    return int((dt2 - dt1).total_seconds() // 60)
