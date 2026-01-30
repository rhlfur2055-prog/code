#!/bin/bash

# ========================================
# VSCode 확장 알림 비활성화 자동 설정
# ========================================

echo "🔧 VSCode 설정을 초기화합니다..."

# .vscode 디렉토리 생성
if [ ! -d ".vscode" ]; then
    mkdir -p .vscode
    echo "✅ .vscode 디렉토리 생성 완료"
else
    echo "ℹ️  .vscode 디렉토리가 이미 존재합니다"
fi

# settings.json 생성
cat > .vscode/settings.json << 'EOF'
{
  "extensions.ignoreRecommendations": true,
  "extensions.autoCheckUpdates": false,
  "extensions.autoUpdate": false,
  "extensions.ignoredRecommendations": [
    "ms-azuretools.vscode-docker",
    "ms-python.python",
    "redhat.java",
    "vscjava.vscode-java-pack"
  ],
  "workbench.enableExperiments": false,
  "workbench.startupEditor": "none",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "editor.formatOnSave": true,
  "files.associations": {
    "docker-compose*.yml": "dockercompose",
    "Dockerfile*": "dockerfile"
  }
}
EOF
echo "✅ .vscode/settings.json 생성 완료"

# extensions.json 생성
cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "ms-azuretools.vscode-docker",
    "eamodio.gitlens",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
EOF
echo "✅ .vscode/extensions.json 생성 완료"

echo ""
echo "🎉 설정 완료!"
echo ""
echo "📌 다음 단계:"
echo "1. VSCode를 재시작하세요"
echo "2. 더 이상 확장 프로그램 추천 알림이 뜨지 않습니다"
echo ""
echo "💡 팁: Git에 커밋하려면 다음 명령을 실행하세요:"
echo "   git add .vscode/"
echo "   git commit -m 'Add VSCode settings'"
echo ""
