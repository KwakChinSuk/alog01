#!/bin/bash
# /home/ec2-user/alog/alog-bori/ga/cleanup.sh
set -u
shopt -s nullglob
shopt -s nocaseglob

export TZ=Asia/Seoul

echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"

#TARGET_DIR="/home/ec2-user/alog/alog-bori/ga"

TARGET_DIR="${1:-/home/ec2-user/alog/alog-bori/ga}"
RETENTION_DAYS=3         # 오늘 기준 3일 이상 지난 파일 삭제
DRY_RUN=0                # 1=미삭제 테스트, 0=실삭제

# 오늘 자정(epoch)
NOW_EPOCH=$(date -d "today 00:00" +%s)

deleted=0; skipped=0; errors=0

# 하위 디렉토리 포함해서 모든 csv 찾기
find "$TARGET_DIR" -type f -name "*.csv" | while read -r file; do
  filename=$(basename "$file")

  # 파일명에서 YYYY-MM-DD 추출
  if [[ "$filename" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})_ ]]; then
    filedate="${BASH_REMATCH[1]}"
  else
    echo "[SKIP] 날짜 패턴 아님: $filename"
    ((skipped++)); continue
  fi

  file_epoch=$(date -d "$filedate 00:00" +%s 2>/dev/null) || {
    echo "[ERR ] 날짜 파싱 실패: $filename"
    ((errors++)); continue
  }

  if (( file_epoch > NOW_EPOCH )); then
    echo "[SKIP] 미래 날짜: $filename"
    ((skipped++)); continue
  fi

  diff_days=$(( (NOW_EPOCH - file_epoch) / 86400 ))

  if (( diff_days >= RETENTION_DAYS )); then
    if (( DRY_RUN == 1 )); then
      echo "[DRY ] 삭제 대상: $file (기준일 $filedate, ${diff_days}일 경과)"
    else
      if rm -f -- "$file"; then
        echo "[DEL ] $file (기준일 $filedate, ${diff_days}일 경과)"
        ((deleted++))
      else
        echo "[ERR ] 삭제 실패: $file"
        ((errors++))
      fi
    fi
  else
    echo "[KEEP] $file (기준일 $filedate, ${diff_days}일 경과 < ${RETENTION_DAYS})"
    ((skipped++))
  fi
done

echo "[DONE] 삭제:${deleted} 보존:${skipped} 오류:${errors}"

echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"

