#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ec2-user/alog"
cd "$REPO_DIR"

# git이 아니면 종료
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# 추적 제외할 파일은 .gitignore에 관리하세요

# 변경 여부 확인
if [[ -z "$(git status --porcelain)" ]]; then
  echo "[$(date '+%F %T %Z')] no changes"
  exit 0
fi

# 변경된 파일 중 .json, .csv, cfg.py 제외
git add -A ':!*/.json' ':!*.json' ':!*/.csv' ':!*/.log' 
MSG="auto: $(date '+%F %T %Z')"
git commit -m "$MSG" || exit 0

# SSH 키를 특정해야 하면 아래 행처럼 지정 가능 (키 경로 조정)
# export GIT_SSH_COMMAND="ssh -i /home/ec2-user/.ssh/id_rsa -o StrictHostKeyChecking=accept-new"

# 원격이 있으면 푸시 (없으면 건너뜀)
if git remote get-url origin >/dev/null 2>&1; then
  git push origin HEAD
fi

echo "[$(date '+%F %T %Z')] committed and pushed"
