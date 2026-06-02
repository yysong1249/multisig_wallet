import sys, os
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DST = r'C:\Users\용선유\Downloads\multisig_발표자료_v2.pptx'

D = os.path.expanduser('~') + r'\Desktop'
IMGS = {
    'home':     os.path.join(D, 'KakaoTalk_20260601_212226137.png'),
    'modal':    os.path.join(D, 'KakaoTalk_20260601_213558037.png'),
    'pending':  os.path.join(D, 'KakaoTalk_20260601_213929249.png'),
    'executed': os.path.join(D, 'KakaoTalk_20260601_214519735.png'),
}

# ── 색상 (웹 UI 동일) ───────────────────────────────────────────
C_DARK  = RGBColor(0x23, 0x15, 0x09)
C_CARD  = RGBColor(0x2D, 0x1C, 0x0A)
C_CARD2 = RGBColor(0x38, 0x26, 0x12)
C_GOLD  = RGBColor(0xC8, 0xA8, 0x4B)
C_GOLDL = RGBColor(0xE8, 0xC8, 0x78)
C_GOLDD = RGBColor(0xA0, 0x80, 0x30)
C_BG    = RGBColor(0xF5, 0xED, 0xE0)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TEXT  = RGBColor(0x2A, 0x1A, 0x08)
C_MUTED = RGBColor(0x8A, 0x70, 0x60)
C_BODY  = RGBColor(0xD0, 0xC0, 0xA8)
C_GREEN = RGBColor(0x22, 0xA6, 0x5A)
C_RED   = RGBColor(0xD0, 0x50, 0x40)
C_PLHLD = RGBColor(0xEC, 0xE4, 0xD4)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── 공통 헬퍼 ──────────────────────────────────────────────────

def S(bg=C_BG):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s

def R(s, l, t, w, h, fill=None, lc=None, lp=1.0):
    sh = s.shapes.add_shape(1, l, t, w, h)
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if lc:
        sh.line.color.rgb = lc; sh.line.width = Pt(lp)
    else:
        sh.line.fill.background()
    return sh

def T(s, text, l, t, w, h, sz=13, bold=False, c=None,
      al=PP_ALIGN.LEFT, wrap=True):
    bx = s.shapes.add_textbox(l, t, w, h)
    tf = bx.text_frame; tf.word_wrap = wrap
    pg = tf.paragraphs[0]; pg.alignment = al
    rn = pg.add_run(); rn.text = text
    rn.font.size = Pt(sz); rn.font.bold = bold
    if c: rn.font.color.rgb = c
    return bx

def HDR(s, title, tag=None):
    R(s, 0, 0, Inches(13.33), Inches(0.72), fill=C_DARK)
    R(s, 0, 0, Inches(0.08),  Inches(0.72), fill=C_GOLD)
    T(s, title, Inches(0.22), Inches(0.11), Inches(10.5), Inches(0.55),
      sz=24, bold=True, c=C_GOLD)
    if tag:
        T(s, tag, Inches(10.3), Inches(0.2), Inches(2.9), Inches(0.38),
          sz=10, c=C_BODY, al=PP_ALIGN.RIGHT)

def FTR(s):
    T(s, 'Ethereum Multi-Signature Wallet  |  Sepolia: 0x09fBa7c6c534882dF15a920671Fc9dbB3864c005',
      Inches(0.3), Inches(7.22), Inches(13), Inches(0.28), sz=10, c=C_BODY)

def PH(s, l, t, w, h, label='스크린샷 공란', img_key=None):
    img_path = IMGS.get(img_key) if img_key else None
    if img_path and os.path.exists(img_path):
        s.shapes.add_picture(img_path, l, t, w, h)
        print(f'  [이미지] {img_key}')
    else:
        R(s, l, t, w, h, fill=C_PLHLD, lc=C_GOLDD, lp=1.5)
        T(s, label, l, t + h//2 - Inches(0.22), w, Inches(0.44),
          sz=11, c=C_MUTED, al=PP_ALIGN.CENTER)

I = Inches  # shorthand

# ════════════════════════════════════════════════════════════════
# S1 — 표지
# ════════════════════════════════════════════════════════════════
s1 = S(bg=C_DARK)
R(s1, 0, 0, I(13.33), I(0.07), fill=C_GOLD)

# 로고 박스
R(s1, I(5.92), I(1.1), I(1.5), I(1.5), fill=C_CARD)
T(s1, 'MSW', I(5.92), I(1.42), I(1.5), I(0.65),
  sz=24, bold=True, c=C_GOLD, al=PP_ALIGN.CENTER)

T(s1, '이더리움 기반 다중 서명 지갑',
  I(1.5), I(2.9), I(10.33), I(0.9),
  sz=34, bold=True, c=C_WHITE, al=PP_ALIGN.CENTER)
T(s1, 'Ethereum Multi-Signature Wallet',
  I(1.5), I(3.88), I(10.33), I(0.52),
  sz=16, c=C_GOLD, al=PP_ALIGN.CENTER)

R(s1, I(4.5), I(4.55), I(4.33), I(0.04), fill=C_GOLDD)

T(s1, 'Owner 제어  ·  트랜잭션별 N-of-M 서명  ·  유연한 서명자 지정',
  I(1.5), I(4.72), I(10.33), I(0.45),
  sz=12, c=C_BODY, al=PP_ALIGN.CENTER)

R(s1, 0, I(6.82), I(13.33), I(0.68), fill=C_CARD)
T(s1, 'Solidity 0.8.24  ·  Hardhat  ·  Ethers.js v6  ·  Sepolia Testnet',
  I(0.5), I(6.9), I(9), I(0.45), sz=10, c=C_BODY)
T(s1, '2026', I(11.5), I(6.9), I(1.7), I(0.45),
  sz=13, bold=True, c=C_GOLD, al=PP_ALIGN.RIGHT)

print('S1 완료')

# ════════════════════════════════════════════════════════════════
# S2 — 목차
# ════════════════════════════════════════════════════════════════
s2 = S()
R(s2, 0, 0, I(2.5), I(7.5), fill=C_DARK)
R(s2, 0, 0, I(0.08), I(7.5), fill=C_GOLD)
T(s2, '목  차', I(0.18), I(0.3), I(2.2), I(0.52),
  sz=18, bold=True, c=C_GOLD)
T(s2, 'Contents', I(0.18), I(0.88), I(2.2), I(0.35),
  sz=10, c=C_BODY)

items = [
    ('01', '프로젝트 개요'),
    ('02', '컨트랙트 구조'),
    ('03', '핵심 함수 구현'),
    ('04', '보안 · 권한 설계'),
    ('05', '트랜잭션 시나리오'),
    ('06', '프론트엔드 시연'),
    ('07', '테스트 결과'),
    ('08', '결론'),
]
for i, (num, name) in enumerate(items):
    y = I(0.85 + i * 0.77)
    R(s2, I(2.8), y, I(10.2), I(0.62),
      fill=C_CARD if i % 2 == 0 else C_CARD2)
    T(s2, num, I(2.98), y + I(0.12), I(0.65), I(0.4),
      sz=14, bold=True, c=C_GOLD)
    T(s2, name, I(3.78), y + I(0.14), I(8.9), I(0.38),
      sz=13, c=C_WHITE)

FTR(s2)
print('S2 완료')

# ════════════════════════════════════════════════════════════════
# S3 — 프로젝트 개요
# ════════════════════════════════════════════════════════════════
s3 = S()
HDR(s3, '01  프로젝트 개요', 'Project Overview')

# 왼쪽 — 기존 한계
R(s3, I(0.3), I(0.85), I(5.95), I(5.0), fill=C_CARD)
T(s3, '단순 구현 기반 Multisig의 한계', I(0.5), I(0.97),
  I(5.6), I(0.42), sz=14, bold=True, c=C_GOLDD)

left_items = [
    ('❌  배포 시 서명자 목록 전역 고정', C_BODY),
    ('❌  모든 트랜잭션에 동일 서명자 적용', C_BODY),
    ('❌  서명자 변경 시 재배포 필요', C_BODY),
    ('❌  트랜잭션 개별 취소 불가', C_BODY),
    ('❌  역할 기반 버튼 UI 부재', C_BODY),
]
for j, (item, col) in enumerate(left_items):
    T(s3, item, I(0.5), I(1.52 + j * 0.82), I(5.6), I(0.68),
      sz=12, c=col)

# 오른쪽 — 해결 방법
R(s3, I(6.55), I(0.85), I(6.45), I(5.0), fill=C_CARD)
T(s3, '이 프로젝트의 설계', I(6.75), I(0.97),
  I(6.1), I(0.42), sz=14, bold=True, c=C_GOLD)

right_items = [
    ('✅  Owner 목록 배포 시 등록 (제출 제어)', C_GOLD),
    ('✅  트랜잭션마다 서명자 직접 지정', C_GOLD),
    ('✅  Owner 외 주소도 서명자로 참여 가능', C_GOLDL),
    ('✅  제출자 전용 트랜잭션 취소 기능', C_GOLDL),
    ('✅  역할별 버튼 자동 표시/숨김', C_GOLDL),
]
for j, (item, col) in enumerate(right_items):
    T(s3, item, I(6.75), I(1.52 + j * 0.82), I(5.9), I(0.68),
      sz=11.5, c=col)

# 실생활 활용 예시
R(s3, I(0.3), I(5.97), I(12.7), I(0.68), fill=RGBColor(0x1A, 0x10, 0x04))
R(s3, I(0.3), I(5.97), I(0.07), I(0.68), fill=C_GOLD)
T(s3, '실생활 활용', I(0.52), I(6.01), I(1.75), I(0.28),
  sz=11, bold=True, c=C_GOLD)

use_cases = [
    ('기업 자금 승인', 'CFO · CEO · 이사 2명 이상 서명 후 법인 자금 집행'),
    ('DAO 금고 관리', '커뮤니티 운영진 5명 중 3명 서명 시 프로토콜 자금 사용'),
    ('공동 투자 출금', '공동 투자자 전원 동의 없이 자금 인출 불가'),
]
for k, (title, desc) in enumerate(use_cases):
    x = I(2.4 + k * 3.45)
    T(s3, title, x, I(5.99), I(3.3), I(0.28),
      sz=11, bold=True, c=C_GOLDL)
    T(s3, desc, x, I(6.28), I(3.3), I(0.32),
      sz=10, c=C_BODY)

# 기술 스택
R(s3, I(0.3), I(6.73), I(12.7), I(0.44), fill=C_CARD2)
T(s3, 'Solidity 0.8.24  ·  Hardhat 2.x  ·  Ethers.js v6  ·  MetaMask  ·  Sepolia Testnet',
  I(0.5), I(6.79), I(12.3), I(0.35),
  sz=10.5, c=C_BODY, al=PP_ALIGN.CENTER)

FTR(s3)
print('S3 완료')

# ════════════════════════════════════════════════════════════════
# S4 — 컨트랙트 구조
# ════════════════════════════════════════════════════════════════
s4 = S()
HDR(s4, '02  컨트랙트 구조', 'Contract Architecture')

# 왼쪽 — Transaction 구조체
R(s4, I(0.3), I(0.85), I(5.95), I(6.0), fill=C_CARD)
T(s4, 'Transaction  구조체', I(0.5), I(0.95),
  I(5.6), I(0.42), sz=14, bold=True, c=C_GOLD)
R(s4, I(0.5), I(1.43), I(5.55), I(0.03), fill=C_GOLDD)

fields = [
    ('address    to',             '수신 주소'),
    ('uint       value',          'ETH 금액 (wei)'),
    ('bool       executed',       '실행 여부'),
    ('bool       cancelled',      '취소 여부'),
    ('uint       confirmCount',   '현재 서명 수'),
    ('uint       required',       '최소 서명 수'),
    ('address[]  allowedSigners', '허용 서명자 목록'),
    ('address    submitter',      '트랜잭션 제출자'),
]
for j, (field, desc) in enumerate(fields):
    y = I(1.52 + j * 0.56)
    T(s4, field, I(0.5), y, I(3.3), I(0.42),
      sz=11, bold=True, c=C_GOLDL)
    T(s4, desc,  I(3.85), y, I(2.1), I(0.42),
      sz=10.5, c=C_BODY)

# 오른쪽 — 상태 변수
R(s4, I(6.55), I(0.85), I(6.45), I(2.55), fill=C_CARD)
T(s4, '상태 변수', I(6.75), I(0.95), I(6.1), I(0.42),
  sz=14, bold=True, c=C_GOLD)
R(s4, I(6.75), I(1.43), I(6.05), I(0.03), fill=C_GOLDD)

svars = [
    ('mapping(address => bool)  isOwner', C_GOLDL),
    ('address[]  owners', C_GOLDL),
    ('Transaction[]  transactions', C_GOLDL),
    ('mapping(uint => mapping(address => bool))', C_GOLDL),
    ('    isAllowedSigner  // 허용 서명자', C_BODY),
    ('mapping(uint => mapping(address => bool))', C_GOLDL),
    ('    isConfirmed      // 서명 여부', C_BODY),
]
for j, (sv, col) in enumerate(svars):
    T(s4, sv, I(6.75), I(1.52 + j * 0.3), I(6.1), I(0.3),
      sz=10, c=col)

# 오른쪽 아래 — 핵심 원칙
R(s4, I(6.55), I(3.55), I(6.45), I(3.3), fill=RGBColor(0x1A, 0x10, 0x04))
R(s4, I(6.55), I(3.55), I(0.07), I(3.3), fill=C_GOLD)
T(s4, '핵심 설계 원칙', I(6.75), I(3.65), I(6.1), I(0.42),
  sz=14, bold=True, c=C_GOLD)

principles = [
    '①  Owner 목록은 생성자에서 등록',
    '②  전역 서명자(global owners) 없음',
    '③  트랜잭션 제출 시 서명자 직접 지정',
    '④  Owner ≠ 서명자 (누구든 서명자 가능)',
    '⑤  취소 권한은 submitter에게만',
]
for j, pr in enumerate(principles):
    T(s4, pr, I(6.75), I(4.2 + j * 0.48), I(6.1), I(0.44),
      sz=10.5, c=C_WHITE)

FTR(s4)
print('S4 완료')

# ════════════════════════════════════════════════════════════════
# S5 — 핵심 함수 구현
# ════════════════════════════════════════════════════════════════
s5 = S()
HDR(s5, '03  핵심 함수 구현', 'Core Functions')

funcs = [
    {
        'name': 'submitTransaction()',
        'badge': 'onlyOwner',
        'bc': C_GOLD,
        'btc': C_DARK,
        'lines': [
            'Owner만 호출 가능',
            'to, value, signers[], required 입력',
            '허용 서명자 isAllowedSigner에 저장',
            'submitter 주소 기록',
            'TransactionSubmitted 이벤트 발생',
        ],
    },
    {
        'name': 'confirmTransaction()',
        'badge': 'onlyAllowedSigner',
        'bc': C_GOLDD,
        'btc': C_WHITE,
        'lines': [
            '허용 서명자만 호출 가능',
            'notConfirmed / notExecuted / notCancelled',
            'confirmCount++ 증가',
            'isConfirmed[txId][msg.sender] = true',
            'required 충족 시 executeTransaction() 자동 호출',
        ],
    },
    {
        'name': 'cancelTransaction()',
        'badge': 'submitter only',
        'bc': C_RED,
        'btc': C_WHITE,
        'lines': [
            '제출자(submitter)만 호출 가능',
            'notExecuted / notCancelled 상태에서만',
            'cancelled = true 설정',
            '취소 후 서명 · 실행 모두 차단',
            'TransactionCancelled 이벤트 발생',
        ],
    },
    {
        'name': 'executeTransaction()',
        'badge': 'public',
        'bc': C_GREEN,
        'btc': C_WHITE,
        'lines': [
            '누구나 호출 가능',
            'confirmCount >= required 검증',
            'ETH 전송 실행 (.call{value})',
            'executed = true 설정',
            'TransactionExecuted 이벤트 발생',
        ],
    },
]

positions = [
    (I(0.3),  I(0.85)),
    (I(6.85), I(0.85)),
    (I(0.3),  I(4.1)),
    (I(6.85), I(4.1)),
]

for fn, (fl, ft) in zip(funcs, positions):
    fw, fh = I(6.15), I(3.05)
    R(s5, fl, ft, fw, fh, fill=C_CARD)
    T(s5, fn['name'], fl + I(0.2), ft + I(0.12), I(3.8), I(0.4),
      sz=14, bold=True, c=C_GOLDL)
    R(s5, fl + I(4.25), ft + I(0.13), I(1.65), I(0.37), fill=fn['bc'])
    T(s5, fn['badge'], fl + I(4.25), ft + I(0.15), I(1.65), I(0.34),
      sz=10, bold=True, c=fn['btc'], al=PP_ALIGN.CENTER)
    R(s5, fl + I(0.2), ft + I(0.6), fw - I(0.4), I(0.02), fill=C_GOLDD)
    for k, line in enumerate(fn['lines']):
        T(s5, '·  ' + line, fl + I(0.2), ft + I(0.7 + k * 0.44),
          fw - I(0.3), I(0.4), sz=10.5, c=C_BODY)

FTR(s5)
print('S5 완료')

# ════════════════════════════════════════════════════════════════
# S6 — 보안 · 권한 설계
# ════════════════════════════════════════════════════════════════
s6 = S()
HDR(s6, '04  보안 · 권한 설계', 'Security & Access Control')

# 테이블 헤더
R(s6, I(0.3), I(0.85), I(12.7), I(0.52), fill=C_CARD)
cols = [
    ('기능',       I(0.5),  I(3.9)),
    ('Owner',     I(4.55), I(1.55)),
    ('허용 서명자', I(6.2),  I(1.8)),
    ('제출자',     I(8.1),  I(1.55)),
    ('누구나',     I(9.75), I(3.0)),
]
for hdr_txt, cx, cw in cols:
    T(s6, hdr_txt, cx, I(0.92), cw, I(0.38),
      sz=10, bold=True, c=C_GOLD, al=PP_ALIGN.CENTER)

rows = [
    ('submitTransaction()',     '✅', '—', '—', '—'),
    ('confirmTransaction()',    '—', '✅', '—', '—'),
    ('revokeConfirmation()',    '—', '✅', '—', '—'),
    ('executeTransaction()',    '—', '—', '—', '✅'),
    ('cancelTransaction()',     '—', '—', '✅', '—'),
    ('getTransaction() 조회',   '—', '—', '—', '✅'),
    ('ETH 입금 (receive)',      '—', '—', '—', '✅'),
]

for r_i, (fname, *cells) in enumerate(rows):
    y = I(1.43 + r_i * 0.59)
    R(s6, I(0.3), y, I(12.7), I(0.55),
      fill=C_CARD if r_i % 2 == 0 else C_CARD2)
    T(s6, fname, I(0.5), y + I(0.09), I(3.9), I(0.4), sz=10.5, c=C_GOLDL)
    for cell, (_, cx, cw) in zip(cells, cols[1:]):
        cc = C_GREEN if cell == '✅' else C_MUTED
        T(s6, cell, cx, y + I(0.09), cw, I(0.4),
          sz=12, bold=(cell == '✅'), c=cc, al=PP_ALIGN.CENTER)

# 보안 노트
R(s6, I(0.3), I(5.63), I(12.7), I(1.1), fill=RGBColor(0x1A, 0x10, 0x04))
R(s6, I(0.3), I(5.63), I(0.07), I(1.1), fill=C_GOLD)
notes = [
    ('보안 포인트', C_GOLD, True, 10.5),
    ('isAllowedSigner[txId][msg.sender]  —  비허용 주소의 서명 함수 호출 차단', C_BODY, False, 10.5),
    ('transactions[txId].submitter == msg.sender  —  제출자 외 취소 차단', C_BODY, False, 10.5),
    ('notExecuted / notCancelled modifier  —  완료·취소 TX에 모든 상태 변경 차단', C_BODY, False, 10.5),
]
for j, (note, col, bld, sz) in enumerate(notes):
    T(s6, note, I(0.52), I(5.7 + j * 0.25), I(12.3), I(0.26),
      sz=sz, bold=bld, c=col)

FTR(s6)
print('S6 완료')

# ════════════════════════════════════════════════════════════════
# S7 — 시나리오
# ════════════════════════════════════════════════════════════════
s7 = S()
HDR(s7, '05  트랜잭션 시나리오', 'Transaction Scenario')

steps = [
    ('①', '컨트랙트 배포',
     'constructor([Alice, Bob, Carol])  →  3명 Owner 등록'),
    ('②', 'ETH 입금',
     'Dave  →  Contract: 5 ETH  →  Deposit 이벤트'),
    ('③', '트랜잭션 제출 (Alice)',
     'submitTransaction(Eve, 1ETH, [Alice,Bob], required=2)  →  txId=0'),
    ('④', 'Alice 서명',
     'confirmTransaction(0)  →  confirmCount = 1 / 2  (미충족)'),
    ('⑤', 'Bob 서명 → 자동 실행',
     'confirmTransaction(0)  →  count=2=required  →  executeTransaction()  →  Eve +1ETH'),
]

for j, (num, title, detail) in enumerate(steps):
    y = I(0.85 + j * 1.1)
    num_c = C_GREEN if j == 4 else C_GOLD
    R(s7, I(0.3), y, I(0.7), I(0.95), fill=num_c)
    T(s7, num, I(0.3), y + I(0.22), I(0.7), I(0.52),
      sz=16, bold=True, c=C_DARK, al=PP_ALIGN.CENTER)
    R(s7, I(1.08), y, I(5.85), I(0.95), fill=C_CARD)
    T(s7, title, I(1.22), y + I(0.06), I(5.55), I(0.38),
      sz=11, bold=True, c=num_c)
    T(s7, detail, I(1.22), y + I(0.5), I(5.55), I(0.38),
      sz=10.5, c=C_BODY)

# 취소 시나리오 노트
R(s7, I(0.3), I(6.45), I(6.65), I(0.7), fill=C_CARD2)
T(s7, '[취소 시나리오]', I(0.5), I(6.5), I(6.3), I(0.28),
  sz=10, bold=True, c=C_RED)
T(s7, 'Alice.cancelTransaction(0)  →  cancelled=true  →  Carol 서명 시 revert "Already cancelled"',
  I(0.5), I(6.73), I(6.3), I(0.35), sz=10, c=C_BODY)

# 오른쪽 — 스크린샷
PH(s7, I(7.35), I(0.85), I(5.65), I(6.3), '시나리오 결과 화면', img_key='pending')

FTR(s7)
print('S7 완료')

# ════════════════════════════════════════════════════════════════
# S8 — 프론트엔드 시연 ①
# ════════════════════════════════════════════════════════════════
s8 = S()
HDR(s8, '06  프론트엔드 시연 ①  —  접속 및 트랜잭션 제출', 'Frontend Demo ①')

PH(s8, I(0.3),  I(0.85), I(6.15), I(5.42), '홈 화면', img_key='home')
PH(s8, I(6.85), I(0.85), I(6.15), I(5.42), '새 트랜잭션 제출 모달', img_key='modal')

R(s8, I(0.3),  I(6.32), I(6.15), I(0.85), fill=C_CARD)
T(s8, '홈 화면', I(0.5), I(6.38), I(5.8), I(0.38),
  sz=11, bold=True, c=C_GOLD)
T(s8, 'MetaMask 연결  →  컨트랙트 주소 입력  →  대시보드 열기',
  I(0.5), I(6.7), I(5.8), I(0.35), sz=10.5, c=C_BODY)

R(s8, I(6.85), I(6.32), I(6.15), I(0.85), fill=C_CARD)
T(s8, '새 트랜잭션 제출 — 서명자 직접 지정', I(7.05), I(6.38),
  I(5.8), I(0.38), sz=11, bold=True, c=C_GOLD)
T(s8, '수신 주소 · 금액 · 서명자 목록 · 최소 서명 수를 트랜잭션마다 자유롭게 지정',
  I(7.05), I(6.7), I(5.8), I(0.35), sz=10.5, c=C_BODY)

FTR(s8)
print('S8 완료')

# ════════════════════════════════════════════════════════════════
# S9 — 프론트엔드 시연 ②
# ════════════════════════════════════════════════════════════════
s9 = S()
HDR(s9, '06  프론트엔드 시연 ②  —  서명 및 실행 완료', 'Frontend Demo ②')

PH(s9, I(0.3),  I(0.85), I(6.15), I(5.42), 'TX 목록 — Owner1(제출자) 시점', img_key='pending')
PH(s9, I(6.85), I(0.85), I(6.15), I(5.42), 'TX 실행 완료', img_key='executed')

R(s9, I(0.3),  I(6.32), I(6.15), I(0.85), fill=C_CARD)
T(s9, '대기 중 — Owner1(제출자) 시점', I(0.5), I(6.38),
  I(5.8), I(0.38), sz=11, bold=True, c=C_GOLD)
T(s9, '서명 · 서명취소 · 실행 버튼 + 제출자에게만 "트랜잭션 취소" 버튼 노출',
  I(0.5), I(6.7), I(5.8), I(0.35), sz=10.5, c=C_BODY)

R(s9, I(6.85), I(6.32), I(6.15), I(0.85), fill=C_CARD)
T(s9, '실행 완료', I(7.05), I(6.38), I(5.8), I(0.38),
  sz=11, bold=True, c=C_GREEN)
T(s9, '2명 서명 완료  →  required 충족  →  자동 실행 / 진행 바 초록 전환',
  I(7.05), I(6.7), I(5.8), I(0.35), sz=10.5, c=C_BODY)

FTR(s9)
print('S9 완료')

# ════════════════════════════════════════════════════════════════
# S10 — 테스트 결과
# ════════════════════════════════════════════════════════════════
s10 = S()
HDR(s10, '07  테스트 결과', 'Test Results — Hardhat · Chai · Ethers.js v6')

# 큰 숫자
R(s10, I(0.3), I(0.85), I(3.5), I(2.85), fill=C_CARD)
T(s10, '50', I(0.3), I(1.0), I(3.5), I(1.5),
  sz=80, bold=True, c=C_GOLD, al=PP_ALIGN.CENTER)
T(s10, 'passing', I(0.3), I(2.55), I(3.5), I(0.45),
  sz=16, bold=True, c=C_GREEN, al=PP_ALIGN.CENTER)
R(s10, I(0.3), I(3.8), I(3.5), I(0.52), fill=C_CARD2)
T(s10, '✅  전 케이스 통과', I(0.3), I(3.87), I(3.5), I(0.38),
  sz=11, c=C_GREEN, al=PP_ALIGN.CENTER)

# 테스트 케이스 테이블
R(s10, I(4.1), I(0.85), I(8.9), I(0.52), fill=C_CARD)
for hdr_txt, hx, hw in [
    ('ID',     I(4.25), I(1.1)),
    ('테스트 내용', I(5.45), I(4.6)),
    ('수',     I(10.15), I(0.7)),
    ('결과',   I(10.95), I(1.9)),
]:
    T(s10, hdr_txt, hx, I(0.92), hw, I(0.38),
      sz=10, bold=True, c=C_GOLD)

tc_rows = [
    ('TC-01',   '배포 확인 (Owner 등록·조회)',          '6',  '✅ 통과'),
    ('TC-02',   '트랜잭션 제출 / Owner 권한',           '9',  '✅ 통과'),
    ('TC-03',   '서명 확인 (confirmTransaction)',       '6',  '✅ 통과'),
    ('TC-04',   'required 충족 → 자동 실행',       '3',  '✅ 통과'),
    ('TC-05',   '서명 취소 (revokeConfirmation)',       '6',  '✅ 통과'),
    ('TC-06',   '실행 완료 트랜잭션 재시도',              '3',  '✅ 통과'),
    ('TC-07-A', '트랜잭션 취소 (신규)',                  '7',  '✅ 통과'),
    ('TC-07',   '서명 수 미달 직접 실행',                '2',  '✅ 통과'),
    ('TC-08',   '조회 기능',                            '4',  '✅ 통과'),
]
for r_i, (tc_id, tc_nm, tc_n, tc_r) in enumerate(tc_rows):
    y = I(1.43 + r_i * 0.59)
    R(s10, I(4.1), y, I(8.9), I(0.55),
      fill=C_CARD if r_i % 2 == 0 else C_CARD2)
    T(s10, tc_id, I(4.25), y + I(0.09), I(1.1), I(0.4),
      sz=10.5, c=C_GOLD)
    T(s10, tc_nm, I(5.45), y + I(0.09), I(4.6), I(0.4),
      sz=10, c=C_WHITE)
    T(s10, tc_n, I(10.15), y + I(0.09), I(0.7), I(0.4),
      sz=10, c=C_BODY, al=PP_ALIGN.CENTER)
    T(s10, tc_r, I(10.95), y + I(0.09), I(1.9), I(0.4),
      sz=10.5, c=C_GREEN, al=PP_ALIGN.CENTER)

FTR(s10)
print('S10 완료')

# ════════════════════════════════════════════════════════════════
# S11 — 결론
# ════════════════════════════════════════════════════════════════
s11 = S(bg=C_DARK)
R(s11, 0, 0, I(13.33), I(0.07), fill=C_GOLD)

T(s11, '결  론', I(1.5), I(0.75), I(10.33), I(0.72),
  sz=32, bold=True, c=C_GOLD, al=PP_ALIGN.CENTER)
T(s11, 'Conclusion', I(1.5), I(1.52), I(10.33), I(0.4),
  sz=13, c=C_BODY, al=PP_ALIGN.CENTER)

R(s11, I(4.5), I(2.05), I(4.33), I(0.04), fill=C_GOLDD)

conclusions = [
    ('Owner 기반 제출 제어',
     'Owner만 트랜잭션 제출 가능\n스팸 방지 · 책임 추적 명확화'),
    ('트랜잭션별 서명자 지정',
     '외부인도 서명자로 참여 가능\n실무 다목적 지갑 구현'),
    ('완전한 트랜잭션 취소',
     '제출자 전용 cancelTransaction\n서명·실행 모두 차단'),
    ('50개 유닛 테스트',
     'Hardhat + Chai + Ethers.js v6\n전 케이스 통과'),
]

box_positions = [
    (I(1.0), I(2.25)),
    (I(7.2), I(2.25)),
    (I(1.0), I(3.95)),
    (I(7.2), I(3.95)),
]

for (title, desc), (bx, by) in zip(conclusions, box_positions):
    bw, bh = I(5.0), I(1.5)
    R(s11, bx, by, bw, bh, fill=C_CARD)
    R(s11, bx, by, I(0.07), bh, fill=C_GOLD)
    T(s11, title, bx + I(0.22), by + I(0.15), bw - I(0.35), I(0.42),
      sz=13, bold=True, c=C_GOLD)
    for k, line in enumerate(desc.split('\n')):
        T(s11, line, bx + I(0.22), by + I(0.6 + k * 0.35),
          bw - I(0.35), I(0.36), sz=11.5, c=C_BODY)

# 바이브 코딩 노하우
R(s11, I(1.0), I(5.6), I(11.33), I(0.65), fill=C_CARD2)
R(s11, I(1.0), I(5.6), I(0.07), I(0.65), fill=C_GOLD)
T(s11, '바이브 코딩 노하우', I(1.22), I(5.65), I(2.8), I(0.38),
  sz=11, bold=True, c=C_GOLD)
T(s11, '① 기능 단위로 요청 세분화  ·  ② 테스트로 AI 결과 직접 검증  ·  ③ 에러 메시지 그대로 공유',
  I(4.2), I(5.68), I(7.8), I(0.38), sz=11, c=C_BODY)

# 배포 주소
R(s11, I(2.5), I(6.38), I(8.33), I(0.48), fill=C_CARD)
T(s11, 'Sepolia: 0x09fBa7c6c534882dF15a920671Fc9dbB3864c005',
  I(2.7), I(6.44), I(8.0), I(0.38),
  sz=10.5, c=C_BODY, al=PP_ALIGN.CENTER)

print('S11 완료')

# ── 저장 ─────────────────────────────────────────────────────
prs.save(DST)
print(f'\n저장 완료: {DST}  (총 {len(prs.slides)} 슬라이드)')
