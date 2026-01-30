# ========================================
# VSCode 확장 알림 비활성화 자동 설정 (Windows)
# ========================================

Write-Host "🔧 VSCode 설정을 초기화합니다..." -ForegroundColor Cyan

# .vscode 디렉토리 생성
if (-not (Test-Path ".vscode")) {
    New-Item -ItemType Directory -Path ".vscode" | Out-Null
    Write-Host "✅ .vscode 디렉토리 생성 완료" -ForegroundColor Green
} else {
    Write-Host "ℹ️  .vscode 디렉토리가 이미 존재합니다" -ForegroundColor Yellow
}

# settings.json 생성
$settingsJson = @"
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
"@

$settingsJson | Out-File -FilePath ".vscode\settings.json" -Encoding UTF8
Write-Host "✅ .vscode\settings.json 생성 완료" -ForegroundColor Green

# extensions.json 생성
$extensionsJson = @"
{
  "recommendations": [
    "ms-azuretools.vscode-docker",
    "eamodio.gitlens",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
"@

$extensionsJson | Out-File -FilePath ".vscode\extensions.json" -Encoding UTF8
Write-Host "✅ .vscode\extensions.json 생성 완료" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 설정 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 다음 단계:" -ForegroundColor Cyan
Write-Host "1. VSCode를 재시작하세요"
Write-Host "2. 더 이상 확장 프로그램 추천 알림이 뜨지 않습니다"
Write-Host ""
Write-Host "💡 팁: Git에 커밋하려면 다음 명령을 실행하세요:" -ForegroundColor Yellow
Write-Host "   git add .vscode/"
Write-Host "   git commit -m 'Add VSCode settings'"
Write-Host ""
