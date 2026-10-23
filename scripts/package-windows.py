"""Build the portable Windows package using only the Python standard library."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import subprocess

root = Path(__file__).resolve().parents[1]
subprocess.run(['node', 'scripts/standalone.js'], cwd=root, check=True)
launcher = r'''@echo off
setlocal
set "APP=%~dp0setup-note.html"
if not exist "%APP%" goto missing
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
  start "" "%LocalAppData%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
echo Chrome was not found in standard locations.
echo Opening Setup Note in your default browser.
start "" "%APP%"
exit /b 0
:missing
echo setup-note.html is missing.
echo Extract ALL files from the ZIP before running this launcher.
pause
exit /b 1
'''
readme = '''셋업 노트 — Windows 포터블 버전
=================================

Windows 10 / 11에서 Chrome으로 사용할 수 있는 HTML 웹앱입니다.
별도 설치, Node.js, 서버, 관리자 권한, 인터넷 연결이 필요 없습니다.
네이티브 EXE가 아니라 로컬 HTML 앱과 CMD 실행 도우미로 구성됩니다.

시작하기
1. ZIP 파일을 마우스 오른쪽 클릭 → 모두 압축 풀기.
2. 압축을 푼 폴더를 문서 등 계속 사용할 위치에 보관합니다.
3. 실행.cmd를 더블클릭합니다. Chrome이 열리고 앱이 표시됩니다.
   Chrome을 찾지 못하면 기본 브라우저로 엽니다.
   실행.cmd가 차단되면 setup-note.html을 오른쪽 클릭하여
   연결 프로그램 → Google Chrome으로 열 수도 있습니다.
   조직의 보안 정책이 로컬 HTML 실행을 금지한다면 관리자에게 문의하세요.
   보안 설정이나 검증을 해제할 필요는 없습니다.

사용 순서
1. 체크리스트 설정: 샘플 항목, 배점, 필수 조건과 등급 기준을 수정하고 저장.
2. 진입 전 평가: 종목, 매수/매도, 매매법을 정하고 조건을 체크한 뒤 평가 저장.
3. 평가 기록: R 결과를 입력하고 결과 저장. 거래하지 않았다면 미진입 선택.
4. 성과 분석: 등급별 완료 거래 수, 승률, 평균 R 확인.
5. 내보내기로 JSON 백업. 가져오기는 현재 데이터를 교체하므로 먼저 백업.

판정
배점은 100점으로 환산합니다. 필수 조건 미충족이면 점수와 관계없이 PASS.
기본 기준은 A+ 90점 / A 80점 / B 70점이며 수정 가능합니다.
등급은 조건 충족도이며 승률 예측이 아닙니다. 초기 항목은 샘플입니다.
R은 본인이 계획한 리스크 대비 실제 손익입니다. 예: -1R, +2.5R.
통계는 거래 완료만 포함하며 결과 대기·미진입은 제외합니다.
0R은 완료 거래이지만 승리로 계산하지 않습니다.

데이터 보관
기록은 같은 Chrome 프로필의 브라우저 저장 공간에 보관됩니다.
시크릿 모드에서는 사용하지 마세요.
HTML 파일 위치/이름이나 브라우저 프로필이 바뀌면 기록이 보이지 않을 수 있습니다.
폴더 이동·업데이트·PC 변경 전에 JSON으로 내보내고 새 위치에서 가져오세요.
브라우저 데이터 삭제로 기록이 지워질 수 있습니다. 정기적으로 백업하세요.
저장하지 않은 평가 입력은 창을 닫거나 새로고침하면 초기화됩니다.

삭제
필요한 기록을 JSON으로 백업한 뒤 이 폴더를 삭제하면 됩니다.
브라우저에 저장된 기록까지 지우려면 해당 브라우저의 사이트 데이터 관리를 사용하세요.
'''
out = root / 'windows'
out.mkdir(exist_ok=True)
(out / '실행.cmd').write_bytes(launcher.replace('\n', '\r\n').encode('ascii'))
(out / '사용방법.txt').write_bytes(readme.replace('\n', '\r\n').encode('utf-8-sig'))
(root / 'windows' / 'setup-note.html').write_bytes((root / 'setup-note.html').read_bytes())
archive = root / 'SetupNote-Windows.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for name in ('setup-note.html', '실행.cmd', '사용방법.txt'):
        z.write(out / name, f'SetupNote/{name}')
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == 3
    assert b'http://' not in z.read('SetupNote/setup-note.html')
    assert b'https://' not in z.read('SetupNote/setup-note.html')
print(f'Created {archive.name}: {archive.stat().st_size:,} bytes; 3 files; ZIP integrity verified.')
