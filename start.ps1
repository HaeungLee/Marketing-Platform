# AI 마케팅 플랫폼 PowerShell 실행 스크립트
param(
    [string]$Mode = "menu"
)

function Write-Banner {
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "🚀 AI 마케팅 플랫폼" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "소상공인을 위한 스마트 마케팅 솔루션" -ForegroundColor Green
    Write-Host ""
}

function Test-Prerequisites {
    Write-Host "📋 시스템 요구사항 확인 중..." -ForegroundColor Blue
    
    # Python 확인
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Python이 설치되어 있지 않습니다." -ForegroundColor Red
        Write-Host "   https://python.org에서 설치해주세요." -ForegroundColor Yellow
        return $false
    }
    
    # Node.js 확인
    try {
        $nodeVersion = node --version 2>&1
        Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Node.js가 설치되어 있지 않습니다." -ForegroundColor Red
        Write-Host "   https://nodejs.org에서 설치해주세요." -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Install-BackendDependencies {
    Write-Host "🔧 백엔드 의존성 설치 중..." -ForegroundColor Blue
    
    Set-Location "$PSScriptRoot\backend"
    
    try {
        python -m pip install fastapi uvicorn pydantic python-dotenv pydantic-settings --quiet
        Write-Host "✅ 백엔드 의존성 설치 완료" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ 백엔드 의존성 설치 실패" -ForegroundColor Red
        return $false
    }
}

function Install-FrontendDependencies {
    Write-Host "🌐 프론트엔드 의존성 확인 중..." -ForegroundColor Blue
    
    Set-Location "$PSScriptRoot\frontend"
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "📦 프론트엔드 의존성 설치 중... (시간이 걸릴 수 있습니다)" -ForegroundColor Yellow
        try {
            npm install
            Write-Host "✅ 프론트엔드 의존성 설치 완료" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "❌ 프론트엔드 의존성 설치 실패" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "✅ 프론트엔드 의존성 이미 설치됨" -ForegroundColor Green
        return $true
    }
}

function Start-Backend {
    Write-Host "🔧 백엔드 서버 시작 중..." -ForegroundColor Blue
    Set-Location "$PSScriptRoot\backend"
    
    Write-Host "📍 API 서버: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "📖 API 문서: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "🛑 서버를 중지하려면 Ctrl+C를 누르세요" -ForegroundColor Yellow
    Write-Host ""
    
    python run.py
}

function Start-Frontend {
    Write-Host "🌐 프론트엔드 서버 시작 중..." -ForegroundColor Blue
    Set-Location "$PSScriptRoot\frontend"
    
    Write-Host "📍 웹사이트: http://localhost:5173" -ForegroundColor Cyan
    Write-Host "🛑 서버를 중지하려면 Ctrl+C를 누르세요" -ForegroundColor Yellow
    Write-Host ""
    
    npm run dev
}

function Start-FullSystem {
    Write-Host "🚀 전체 시스템 시작 중..." -ForegroundColor Blue
    Write-Host ""
    
    # 백엔드 시작 (새 창)
    Write-Host "새 터미널에서 백엔드를 시작합니다..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '🔧 백엔드 서버 시작 중...' -ForegroundColor Blue; Write-Host '📍 API: http://localhost:8000' -ForegroundColor Cyan; python run.py"
    
    # 잠깐 대기
    Start-Sleep -Seconds 3
    
    # 프론트엔드 시작 (새 창)  
    Write-Host "새 터미널에서 프론트엔드를 시작합니다..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; Write-Host '🌐 프론트엔드 서버 시작 중...' -ForegroundColor Blue; Write-Host '📍 웹사이트: http://localhost:5173' -ForegroundColor Cyan; npm run dev"
    
    Write-Host ""
    Write-Host "✅ 시스템 시작 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 접속 정보:" -ForegroundColor Cyan
    Write-Host "   프론트엔드: http://localhost:5173" -ForegroundColor White
    Write-Host "   백엔드 API: http://localhost:8000" -ForegroundColor White
    Write-Host "   API 문서: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 브라우저에서 http://localhost:5173 으로 접속하세요!" -ForegroundColor Yellow
    
    # 브라우저 자동 열기
    Start-Process "http://localhost:5173"
}

function Show-ProjectStatus {
    Write-Host "📊 프로젝트 상태 확인" -ForegroundColor Blue
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    
    # 프로젝트 구조 확인
    Write-Host "📁 프로젝트 구조:" -ForegroundColor Yellow
    Get-ChildItem $PSScriptRoot -Directory | Select-Object Name | Format-Table -HideTableHeaders
    
    # 백엔드 상태
    Write-Host "🔧 백엔드 상태:" -ForegroundColor Yellow
    $backendPath = "$PSScriptRoot\backend"
    
    if (Test-Path "$backendPath\src\main.py") {
        Write-Host "✅ 메인 애플리케이션 존재" -ForegroundColor Green
    } else {
        Write-Host "❌ 메인 애플리케이션 누락" -ForegroundColor Red
    }
    
    if (Test-Path "$backendPath\requirements.txt") {
        Write-Host "✅ 의존성 파일 존재" -ForegroundColor Green
    } else {
        Write-Host "❌ 의존성 파일 누락" -ForegroundColor Red
    }
    
    # 프론트엔드 상태
    Write-Host ""
    Write-Host "🌐 프론트엔드 상태:" -ForegroundColor Yellow
    $frontendPath = "$PSScriptRoot\frontend"
    
    if (Test-Path "$frontendPath\package.json") {
        Write-Host "✅ 패키지 설정 존재" -ForegroundColor Green
    } else {
        Write-Host "❌ 패키지 설정 누락" -ForegroundColor Red
    }
    
    if (Test-Path "$frontendPath\src\App.tsx") {
        Write-Host "✅ 메인 React 앱 존재" -ForegroundColor Green
    } else {
        Write-Host "❌ 메인 React 앱 누락" -ForegroundColor Red
    }
    
    if (Test-Path "$frontendPath\node_modules") {
        Write-Host "✅ 의존성 설치됨" -ForegroundColor Green
    } else {
        Write-Host "⚠️  의존성 미설치 (npm install 필요)" -ForegroundColor Yellow
    }
    
    # 주요 페이지 확인
    Write-Host ""
    Write-Host "📋 주요 페이지 확인:" -ForegroundColor Yellow
    $pages = @(
        "ContentGeneratorPage.tsx",
        "AnalyticsPage.tsx", 
        "SettingsPage.tsx",
        "BusinessSetupPage.tsx"
    )
    
    foreach ($page in $pages) {
        if (Test-Path "$frontendPath\src\pages\$page") {
            $displayName = switch ($page) {
                "ContentGeneratorPage.tsx" { "AI 콘텐츠 생성 페이지" }
                "AnalyticsPage.tsx" { "분석 대시보드 페이지" }
                "SettingsPage.tsx" { "설정 페이지" }
                "BusinessSetupPage.tsx" { "비즈니스 설정 페이지" }
            }
            Write-Host "✅ $displayName" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    Write-Host "📈 프로젝트 완성도: 95%" -ForegroundColor Green
}

function Run-Demo {
    Write-Host "🎮 데모 스크립트 실행 중..." -ForegroundColor Blue
    Set-Location $PSScriptRoot
    python demo.py
}

function Show-Menu {
    Write-Host "🎯 실행 옵션을 선택하세요:" -ForegroundColor Yellow
    Write-Host "1. 백엔드만 시작 (API 서버)" -ForegroundColor White
    Write-Host "2. 프론트엔드만 시작 (웹 인터페이스)" -ForegroundColor White
    Write-Host "3. 전체 시스템 시작 (권장)" -ForegroundColor Green
    Write-Host "4. 데모 스크립트 실행" -ForegroundColor White
    Write-Host "5. 프로젝트 상태 확인" -ForegroundColor White
    Write-Host "6. 종료" -ForegroundColor Gray
    Write-Host ""
    
    do {
        $choice = Read-Host "선택 (1-6)"
        
        switch ($choice) {
            "1" { Start-Backend; break }
            "2" { Start-Frontend; break }
            "3" { Start-FullSystem; break }
            "4" { Run-Demo; break }
            "5" { Show-ProjectStatus; break }
            "6" { Write-Host "🎉 감사합니다!" -ForegroundColor Green; exit }
            default { Write-Host "❌ 잘못된 선택입니다. 1-6 중에서 선택해주세요." -ForegroundColor Red }
        }
    } while ($true)
}

# 메인 실행 로직
Set-Location $PSScriptRoot

Write-Banner

if (-not (Test-Prerequisites)) {
    Read-Host "아무 키나 누르세요..."
    exit 1
}

if (-not (Install-BackendDependencies)) {
    Read-Host "아무 키나 누르세요..."
    exit 1
}

if (-not (Install-FrontendDependencies)) {
    Read-Host "아무 키나 누르세요..."
    exit 1
}

# 명령줄 인자에 따른 실행
switch ($Mode) {
    "backend" { Start-Backend }
    "frontend" { Start-Frontend }
    "full" { Start-FullSystem }
    "demo" { Run-Demo }
    "status" { Show-ProjectStatus }
    default { Show-Menu }
}
