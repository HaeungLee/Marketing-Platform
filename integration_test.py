#!/usr/bin/env python3
"""
🧪 AI 마케팅 플랫폼 통합 테스트
모든 주요 컴포넌트가 정상 작동하는지 확인
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class PlatformIntegrationTest:
    """플랫폼 통합 테스트 클래스"""
    
    def __init__(self):
        self.project_root = Path("d:/FinalProjects/Marketing-Platform")
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        self.test_results = []
        
    def log_test(self, name: str, status: bool, details: str = ""):
        """테스트 결과 로깅"""
        self.test_results.append({
            "name": name,
            "status": "✅ PASS" if status else "❌ FAIL", 
            "details": details
        })
        print(f"{self.test_results[-1]['status']} {name}")
        if details:
            print(f"   {details}")
    
    def test_project_structure(self):
        """프로젝트 구조 테스트"""
        print("\n🏗️  프로젝트 구조 테스트")
        print("-" * 40)
        
        # 필수 디렉토리 확인
        required_dirs = [
            "backend/src",
            "backend/tests", 
            "frontend/src",
            "frontend/src/pages",
            "frontend/src/components"
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            self.log_test(
                f"디렉토리 존재: {dir_path}",
                full_path.exists(),
                f"경로: {full_path}"
            )
        
        # 필수 파일 확인
        required_files = [
            "backend/src/main.py",
            "backend/run.py",
            "backend/requirements.txt",
            "frontend/package.json",
            "frontend/src/App.tsx",
            "README.md"
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            self.log_test(
                f"파일 존재: {file_path}",
                full_path.exists(),
                f"크기: {full_path.stat().st_size if full_path.exists() else 0} bytes"
            )
    
    def test_backend_components(self):
        """백엔드 컴포넌트 테스트"""
        print("\n🔧 백엔드 컴포넌트 테스트")
        print("-" * 40)
        
        # Python 경로 설정
        sys.path.insert(0, str(self.backend_path / "src"))
        
        try:
            # 설정 모듈 테스트
            from config.settings import Settings
            settings = Settings()
            self.log_test(
                "설정 모듈 import",
                True,
                f"앱 이름: {settings.app_name}"
            )
        except Exception as e:
            self.log_test("설정 모듈 import", False, str(e))
        
        try:
            # 도메인 엔티티 테스트
            from domain.entities.user import User
            from domain.entities.business import Business
            self.log_test("도메인 엔티티 import", True, "User, Business 클래스")
        except Exception as e:
            self.log_test("도메인 엔티티 import", False, str(e))
        
        try:
            # 값 객체 테스트
            from domain.value_objects.email import Email
            from domain.value_objects.coordinates import Coordinates
            self.log_test("값 객체 import", True, "Email, Coordinates 클래스")
        except Exception as e:
            self.log_test("값 객체 import", False, str(e))
        
        try:
            # FastAPI 앱 생성 테스트
            from main import create_app
            app = create_app()
            self.log_test(
                "FastAPI 앱 생성",
                app is not None,
                f"앱 타입: {type(app).__name__}"
            )
        except Exception as e:
            self.log_test("FastAPI 앱 생성", False, str(e))
    
    def test_frontend_components(self):
        """프론트엔드 컴포넌트 테스트"""
        print("\n🌐 프론트엔드 컴포넌트 테스트")
        print("-" * 40)
        
        # package.json 확인
        package_json_path = self.frontend_path / "package.json"
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            self.log_test(
                "package.json 파싱",
                True,
                f"프로젝트: {package_data.get('name', 'Unknown')}"
            )
            
            # 주요 의존성 확인
            deps = package_data.get('dependencies', {})
            required_deps = ['react', '@chakra-ui/react', 'recharts']
            
            for dep in required_deps:
                self.log_test(
                    f"의존성: {dep}",
                    dep in deps,
                    f"버전: {deps.get(dep, 'Missing')}"
                )
                
        except Exception as e:
            self.log_test("package.json 파싱", False, str(e))
        
        # 주요 페이지 파일 확인
        pages = [
            "HomePage.tsx",
            "DashboardPage.tsx", 
            "BusinessSetupPage.tsx",
            "ContentGeneratorPage.tsx",
            "AnalyticsPage.tsx",
            "SettingsPage.tsx"
        ]
        
        for page in pages:
            page_path = self.frontend_path / "src" / "pages" / page
            file_size = page_path.stat().st_size if page_path.exists() else 0
            self.log_test(
                f"페이지: {page}",
                page_path.exists() and file_size > 1000,  # 최소 1KB
                f"크기: {file_size} bytes"
            )
        
        # 컴포넌트 파일 확인
        components = ["Layout.tsx", "Header.tsx", "Sidebar.tsx"]
        
        for component in components:
            comp_path = self.frontend_path / "src" / "components" / component
            file_size = comp_path.stat().st_size if comp_path.exists() else 0
            self.log_test(
                f"컴포넌트: {component}",
                comp_path.exists() and file_size > 500,  # 최소 500B
                f"크기: {file_size} bytes"
            )
    
    def test_build_processes(self):
        """빌드 프로세스 테스트"""
        print("\n🔨 빌드 프로세스 테스트")
        print("-" * 40)
        
        # 백엔드 Python 문법 체크
        try:
            result = subprocess.run([
                sys.executable, "-m", "py_compile", 
                str(self.backend_path / "src" / "main.py")
            ], capture_output=True, text=True, cwd=self.backend_path)
            
            self.log_test(
                "백엔드 Python 문법",
                result.returncode == 0,
                "main.py 컴파일 성공" if result.returncode == 0 else result.stderr[:100]
            )
        except Exception as e:
            self.log_test("백엔드 Python 문법", False, str(e))
        
        # 프론트엔드 TypeScript 빌드 테스트
        try:
            # node_modules 존재 여부 확인
            node_modules_path = self.frontend_path / "node_modules"
            if node_modules_path.exists():
                result = subprocess.run([
                    "npm", "run", "build"
                ], capture_output=True, text=True, cwd=self.frontend_path, timeout=120)
                
                self.log_test(
                    "프론트엔드 빌드",
                    result.returncode == 0,
                    "빌드 성공" if result.returncode == 0 else "빌드 실패"
                )
            else:
                self.log_test(
                    "프론트엔드 빌드",
                    False,
                    "node_modules 없음 - npm install 필요"
                )
        except subprocess.TimeoutExpired:
            self.log_test("프론트엔드 빌드", False, "빌드 시간 초과 (120초)")
        except Exception as e:
            self.log_test("프론트엔드 빌드", False, str(e))
    
    def test_documentation(self):
        """문서화 테스트"""
        print("\n📚 문서화 테스트")
        print("-" * 40)
        
        docs = {
            "README.md": 5000,  # 최소 5KB
            "PROJECT_COMPLETION_REPORT.md": 3000,  # 최소 3KB
            "QUICK_START.md": 2000,  # 최소 2KB
        }
        
        for doc_name, min_size in docs.items():
            doc_path = self.project_root / doc_name
            if doc_path.exists():
                file_size = doc_path.stat().st_size
                self.log_test(
                    f"문서: {doc_name}",
                    file_size >= min_size,
                    f"크기: {file_size} bytes (최소: {min_size})"
                )
            else:
                self.log_test(f"문서: {doc_name}", False, "파일 없음")
    
    def generate_report(self):
        """테스트 결과 리포트 생성"""
        print("\n" + "=" * 60)
        print("📊 통합 테스트 결과 리포트")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if "✅ PASS" in t["status"]])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 테스트 통계:")
        print(f"   전체 테스트: {total_tests}")
        print(f"   성공: {passed_tests} ✅")
        print(f"   실패: {failed_tests} ❌")
        print(f"   성공률: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ 실패한 테스트:")
            for test in self.test_results:
                if "❌ FAIL" in test["status"]:
                    print(f"   - {test['name']}: {test['details']}")
        
        print(f"\n🎯 플랫폼 준비도: {'✅ 배포 준비 완료' if failed_tests == 0 else '⚠️ 일부 수정 필요'}")
        
        # 성공률에 따른 권장사항
        success_rate = passed_tests / total_tests * 100
        
        if success_rate >= 95:
            print("\n🚀 우수: 플랫폼이 완벽하게 구성되었습니다!")
            print("   - 즉시 데모 가능")
            print("   - 프로덕션 배포 준비 완료")
        elif success_rate >= 85:
            print("\n👍 양호: 플랫폼이 잘 구성되었습니다.")
            print("   - 대부분 기능 정상 작동")
            print("   - 몇 가지 개선사항 있음")
        elif success_rate >= 70:
            print("\n⚠️ 보통: 추가 작업이 필요합니다.")
            print("   - 핵심 기능은 작동")
            print("   - 일부 컴포넌트 수정 필요")
        else:
            print("\n🔧 개선 필요: 상당한 수정 작업이 필요합니다.")
            print("   - 기본 설정 확인")
            print("   - 의존성 설치 확인")
    
    def run_full_test(self):
        """전체 테스트 실행"""
        print("🧪 AI 마케팅 플랫폼 통합 테스트 시작")
        print("=" * 60)
        
        start_time = time.time()
        
        self.test_project_structure()
        self.test_backend_components()
        self.test_frontend_components()
        self.test_build_processes()
        self.test_documentation()
        
        end_time = time.time()
        test_duration = end_time - start_time
        
        self.generate_report()
        
        print(f"\n⏱️ 테스트 실행 시간: {test_duration:.2f}초")
        print("\n🎉 통합 테스트 완료!")

if __name__ == "__main__":
    tester = PlatformIntegrationTest()
    tester.run_full_test()
