import sys
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
import copy

SRC = r'C:\Users\용선유\Downloads\multisig_wallet_presentation.pptx'
DST = r'C:\Users\용선유\Downloads\multisig_wallet_presentation_final.pptx'

p = Presentation(SRC)


def find_shape(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
    return None


def set_text(slide, name, new_text):
    """텍스트박스 전체 텍스트를 교체 (첫 번째 단락/런의 서식 유지)."""
    s = find_shape(slide, name)
    if s is None or not s.has_text_frame:
        print(f'  [경고] 슬라이드에서 {name} 미발견')
        return
    tf = s.text_frame
    # 기존 단락/런 구조 유지하면서 텍스트만 교체
    lines = new_text.split('\n')
    # 첫 단락 처리
    for para_idx, para in enumerate(tf.paragraphs):
        if para_idx < len(lines):
            if para.runs:
                para.runs[0].text = lines[para_idx]
                for run in para.runs[1:]:
                    run.text = ''
            else:
                para.text = lines[para_idx]
        else:
            for run in para.runs:
                run.text = ''
    # 남은 lines는 무시 (슬라이드 구조 변경 없이 텍스트만 교체)


# ════════════════════════════════════════════════════════
# 슬라이드 7 (index 6) — Solidity 핵심 구조
# ════════════════════════════════════════════════════════
slide7 = p.slides[6]

# 상태 변수 — 구버전 3줄 → 신버전으로 교체
set_text(slide7, 'TextBox 8',  'Transaction[] public transactions;')
set_text(slide7, 'TextBox 9',  'mapping(uint => mapping(address => bool))')
set_text(slide7, 'TextBox 10', '  public isAllowedSigner;  // 트랜잭션별 허용 서명자')
set_text(slide7, 'TextBox 11', 'mapping(uint => mapping(address => bool))')
set_text(slide7, 'TextBox 12', '  public isConfirmed;      // 실제 서명 여부')
set_text(slide7, 'TextBox 13', '// 전역 owners 없음 — 트랜잭션별 지정')

# Modifier — onlyOwner → onlyAllowedSigner
set_text(slide7, 'TextBox 18', 'onlyAllowedSigner(txId)')
set_text(slide7, 'TextBox 19', '트랜잭션별 허용 서명자만 접근')
set_text(slide7, 'TextBox 24', 'notCancelled')
set_text(slide7, 'TextBox 25', '취소되지 않은 트랜잭션 확인')

# 비교표 — onlyOwner → onlyAllowedSigner
set_text(slide7, 'TextBox 49', 'onlyOwner modifier')
set_text(slide7, 'TextBox 51', 'onlyAllowedSigner(txId)')

print('슬라이드 7 업데이트 완료')


# ════════════════════════════════════════════════════════
# 슬라이드 8 (index 7) — 핵심 함수 구현
# ════════════════════════════════════════════════════════
slide8 = p.slides[7]

# submitTransaction
set_text(slide8, 'TextBox 8',  '· 누구나 호출 가능 (권한 제한 없음)')
set_text(slide8, 'TextBox 9',  '· to, value, signers[], required 입력')
set_text(slide8, 'TextBox 10', '· 트랜잭션 ID 자동 부여')
set_text(slide8, 'TextBox 11', '· 제출자(submitter) 주소 저장')
set_text(slide8, 'TextBox 12', '· TransactionSubmitted 이벤트 발생')

# confirmTransaction
set_text(slide8, 'TextBox 17', '· onlyAllowedSigner(txId) 검증')
set_text(slide8, 'TextBox 18', '· txExists / notConfirmed / notExecuted / notCancelled')
set_text(slide8, 'TextBox 19', '· confirmCount++ 증가')
set_text(slide8, 'TextBox 20', '· isConfirmed[txId][msg.sender] = true')
set_text(slide8, 'TextBox 21', '· required 충족 시 자동 executeTransaction()')

# executeTransaction
set_text(slide8, 'TextBox 26', '· confirmCount >= required 조건 검증')
set_text(slide8, 'TextBox 27', '· notCancelled 검증 추가')
set_text(slide8, 'TextBox 28', '· ETH 전송 실행 (.call{value})')
set_text(slide8, 'TextBox 29', '· executed = true 상태 변경')
set_text(slide8, 'TextBox 30', '· 누구나 호출 가능 (서명자 제한 없음)')

# revokeConfirmation → cancelTransaction 으로 교체
set_text(slide8, 'TextBox 33', 'cancelTransaction()')
set_text(slide8, 'TextBox 34', '트랜잭션 취소')
set_text(slide8, 'TextBox 35', '· 제출자(submitter)만 호출 가능')
set_text(slide8, 'TextBox 36', '· 미실행(notExecuted) · 미취소(notCancelled) 상태에서만 가능')
set_text(slide8, 'TextBox 37', '· cancelled = true 상태 변경')
set_text(slide8, 'TextBox 38', '· 취소 후 서명 · 실행 모두 차단')
set_text(slide8, 'TextBox 39', '· TransactionCancelled 이벤트 발생')

print('슬라이드 8 업데이트 완료')


# ════════════════════════════════════════════════════════
# 슬라이드 9 (index 8) — 트랜잭션 시나리오
# ════════════════════════════════════════════════════════
slide9 = p.slides[8]

# 제목 부제 수정
set_text(slide9, 'TextBox 3', '서명자 직접 지정 → 3명 중 2명 서명 → 자동 실행 흐름')

# STEP 1: 배포 (인자 없음)
set_text(slide9, 'TextBox 10',
         '인자 없이 배포\n'
         '→ 전역 서명자 없음\n'
         '→ 트랜잭션별 서명자 지정')

# STEP 2: ETH 입금 (그대로 유지)
# STEP 3: 트랜잭션 제출 (새 시그니처)
set_text(slide9, 'TextBox 26',
         'Alice.submitTransaction(\n'
         '  Dave, 3 ETH,\n'
         '  [Alice, Bob, Carol], required=2\n'
         ')\n→ txId=0, submitter=Alice')

# STEP 4: Alice 서명
set_text(slide9, 'TextBox 33', '서명 (1)')
set_text(slide9, 'TextBox 34',
         'Alice.confirmTransaction(0)\n'
         '→ confirmCount = 1\n'
         '→ required(2) 미충족')

# STEP 5: Bob 서명 → 자동 실행
set_text(slide9, 'TextBox 40', '서명 (2) → 자동 실행')
set_text(slide9, 'TextBox 41', '서명 (2) · 자동 실행')
set_text(slide9, 'TextBox 42',
         'Bob.confirmTransaction(0)\n'
         '→ confirmCount = 2 = required\n'
         '→ executeTransaction() 자동 호출\n'
         '→ Dave에게 3 ETH 전송')

# 하단 결과 요약
set_text(slide9, 'TextBox 44',
         'Dave에게 3 ETH 전송 완료  |  '
         '이벤트 로그 온체인 영구 기록  |  '
         'executed = true  |  Carol은 서명 불필요')

print('슬라이드 9 업데이트 완료')


# ════════════════════════════════════════════════════════
# 슬라이드 10 (index 9) — 보안 강화 요소
# ════════════════════════════════════════════════════════
slide10 = p.slides[9]

# 비허용 서명자 접근 차단
set_text(slide10, 'TextBox 10',
         'require(isAllowedSigner[txId]\n'
         '  [msg.sender],\n'
         '  "Not an allowed signer");')
set_text(slide10, 'TextBox 11',
         '트랜잭션별 허용 서명자 외\n'
         '모든 함수 호출 차단')

# "배포 시 검증" → "제출 시 검증" (submitTransaction 내부로 이동)
set_text(slide10, 'TextBox 47', '🔒')
set_text(slide10, 'TextBox 48', '트랜잭션 취소 보호')
set_text(slide10, 'TextBox 50',
         'require(tx.submitter\n'
         '  == msg.sender,\n'
         '  "Not the submitter");')
set_text(slide10, 'TextBox 51',
         '제출자만 취소 가능\n취소 후 재취소·실행 불가')

print('슬라이드 10 업데이트 완료')


# ════════════════════════════════════════════════════════
# 슬라이드 11 (index 10) — 테스트
# ════════════════════════════════════════════════════════
slide11 = p.slides[10]

# 제목 업데이트 (계획 → 결과)
set_text(slide11, 'TextBox 2', '09  테스트 결과')
set_text(slide11, 'TextBox 3', 'Hardhat · Chai · Ethers.js 기반 유닛 테스트  —  45 passing ✅')

# "예상 결과" → "결과" (헤더)
set_text(slide11, 'TextBox 7', '결과')

# TC-01
set_text(slide11, 'TextBox 12', '배포 확인')
set_text(slide11, 'TextBox 13', '✅ 통과')
set_text(slide11, 'TextBox 14', '인자 없이 배포, 트랜잭션 수 0 확인')

# TC-02
set_text(slide11, 'TextBox 19', '트랜잭션 제출')
set_text(slide11, 'TextBox 20', '✅ 통과')
set_text(slide11, 'TextBox 21', 'signers[], required 포함 제출, allowedSigners 저장 확인')

# TC-03
set_text(slide11, 'TextBox 27', '✅ 통과')
set_text(slide11, 'TextBox 28', '서명자 2명 서명 후 required 충족 → 자동 실행 확인')

# TC-04
set_text(slide11, 'TextBox 34', '✅ 통과')
set_text(slide11, 'TextBox 35', "재서명 시 revert 'Already confirmed' 확인")

# TC-05
set_text(slide11, 'TextBox 40', '비허용 서명자 차단')
set_text(slide11, 'TextBox 41', '✅ 통과')
set_text(slide11, 'TextBox 42', "미등록 주소 호출 시 revert 'Not an allowed signer' 확인")

# TC-06
set_text(slide11, 'TextBox 48', '✅ 통과')
set_text(slide11, 'TextBox 49', '서명 취소 → confirmCount 감소 → 재서명 가능 확인')

# TC-07 → TC-07-A: 트랜잭션 취소
set_text(slide11, 'TextBox 53', 'TC-07-A')
set_text(slide11, 'TextBox 54', '트랜잭션 취소')
set_text(slide11, 'TextBox 55', '✅ 통과')
set_text(slide11, 'TextBox 56', '제출자만 취소 가능, 취소 후 서명·실행 revert 확인')
set_text(slide11, 'TextBox 58', '신규')

# TC-08 → TC-08: 서명 수 미달
set_text(slide11, 'TextBox 60', 'TC-08')
set_text(slide11, 'TextBox 61', '서명 수 미달 실행')
set_text(slide11, 'TextBox 62', '✅ 통과')
set_text(slide11, 'TextBox 63', "confirmCount 미달 시 revert 'Not enough confirmations' 확인")
set_text(slide11, 'TextBox 65', '예외')

print('슬라이드 11 업데이트 완료')


# 저장
p.save(DST)
print(f'\n완료: {DST}')
