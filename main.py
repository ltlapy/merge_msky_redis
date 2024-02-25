#!/usr/bin/env python3
import redis

log = print

# Redis 서버에 연결
log("Redis 서버에 연결합니다...")
r1 = redis.Redis(host='redis1', port=6379, db=0)
r2 = redis.Redis(host='redis2', port=6379, db=0)

# 모든 키 검색
log("키 목록을 가져옵니다...")
r1_keys = set(key for key in r1.scan_iter("*"))
r2_keys = set(key for key in r2.scan_iter("*"))

# String 타입의 경우 최신 것으로 덮어쓰되,
# k.lapy.link:latestReadNotification: 은 전자로 덮어쓰고,
# k.lapy.link:kvcache:* 는 모두 날린다

# kvcache:* (string)
#   여러 개 있는 데 모두 날린다
# list:
#   userTimelineWithReplies:*
#   homeTimeline:*
#   userTimelineWithFiles:*
#   userTimeline:*
#   homeTimelineWithFiles:*
# latestReadNotification:* (string)
# notificationTimeline:* (stream)
# antennaTimeline:*  (?)
# queue:*:* (hash)
# hashtagUsers:*:* (?)
# fetchInstanceMetadata:*:* (?)

# * kvcache 는 모두 날린다
log("kvcache를 삭제합니다...")
kvcache1 = set(key for key in r1_keys if b':kvcache:' in key)
r1.delete(*kvcache1)

# * latestReadNotification은 가장 최신 것으로 한다
log("latestReadNotification을 최신으로 갱신합니다...")
lastnoti1 = set(key for key in r1_keys if b':latestReadNotification:' in key)
lastnoti2 = set(key for key in r2_keys if b':latestReadNotification:' in key)

for key in lastnoti1 & lastnoti2:
    log(key)
    a = r1.get(key)
    b = r2.get(key)
    r1.set(key, max(a, b))

# 둘 중 하나에만 있는 거는 일단 넣고 본다
for key in lnoti2 - lastnoti1:
    log(key)
    val = r2.get(key)
    r1.set(key, max(a, b))

# * list는 병합하고 내림차순으로 정렬한다
# duplicated_list = list_key1 & list_key2
# unique_list = list_key2 - list_key1
log("list를 병합하고 내림차순으로 정렬합니다...")

# List 타입의 모든 키 검색
list_key1 = set(key for key in r1_keys if r.type(key) == b'list')
list_key2 = set(key for key in r1_keys if r.type(key) == b'list')

for key in list_key1 & list_key2:
    log(key)
    a = set(r1.lrange(key, 0, -1))
    b = set(r2.lrange(key, 0, -1))
    sorted_values = sorted(a + b, reverse=True)

    r1.delete(key)
    r1.rpush(*sorted_values)

# 둘 중 하나에만 있는 거는 일단 넣고 본다
for key in list_key2 - list_key1:
    log(key)
    b = set(r2.lrange(key, 0, -1))
    r1.rpush(*sorted_values)

log("완료되었습니다. redis1의 자료를 확인하시고 적용하십시오...")