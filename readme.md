# 이게뭐죠
파편화된 Misskey용 redis 데이터베이스의 데이터를 병합하는 도구

## 사용법
1. `redis1/` 과 `redis2/` 에  각각 `dump.rdb` 를 저장합니다.
   1. 이 때에, dump1 쪽이 마지막으로 사용된(가장 최근에 사용된) 데이터베이스라고 가정합니다
2. docker compose up
