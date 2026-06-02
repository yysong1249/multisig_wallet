import sys
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

SRC = r'C:\Users\용선유\Downloads\multisig_wallet_presentation_final.pptx'
DST = r'C:\Users\용선유\Downloads\multisig_wallet_presentation_final.pptx'

D = r'C:\Users\용선유\Desktop'

# ── 선별된 핵심 4장 ──────────────────────────────────────────
# ① 홈 화면 초기 — 진입점
# ② 새 트랜잭션 모달 — 핵심 차별점: 트랜잭션별 서명자 지정
# ③ 트랜잭션 목록 Owner1 시점 — 역할별 버튼 (서명·취소·실행·트랜잭션취소)
# ④ TX 실행 완료 — 최종 결과
IMGS = {
    'home':      D + r'\KakaoTalk_20260601_212150492.png',
    'new_tx':    D + r'\KakaoTalk_20260601_212403206.png',
    'tx_owner1': D + r'\KakaoTalk_20260601_213833634.png',
    'executed':  D + r'\KakaoTalk_20260601_214519735.png',
}

p = Presentation(SRC)
blank = p.slide_layouts[6]

C_TITLE  = RGBColor(0x2A, 0x1A, 0x08)
C_CAP    = RGBColor(0x8A, 0x70, 0x60)
C_ACCENT = RGBColor(0xC8, 0xA8, 0x4B)
BG       = RGBColor(0xF5, 0xED, 0xE0)


def new_slide(title):
    s = p.slides.add_slide(blank)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = BG

    tb = s.shapes.add_textbox(Inches(0.35), Inches(0.13), Inches(11.3), Inches(0.5))
    r = tb.text_frame.paragraphs[0].add_run()
    r.text = title
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = C_TITLE

    foot = s.shapes.add_textbox(Inches(0.35), Inches(6.48), Inches(11.0), Inches(0.22))
    fr = foot.text_frame.paragraphs[0].add_run()
    fr.text = '이더리움 기반 다중 서명 지갑  |  Ethereum Multi-Signature Wallet'
    fr.font.size = Pt(8)
    fr.font.color.rgb = C_CAP
    return s


def add_img(slide, path, l, t, w, h):
    import os
    if not os.path.exists(path):
        print(f'  [없음] {path}')
        return
    slide.shapes.add_picture(path, l, t, w, h)


def add_caption(slide, text, l, t, w, accent_line=None):
    """캡션: accent_line이 있으면 강조 텍스트를 금색으로 첫 줄에 추가."""
    tb = slide.shapes.add_textbox(l, t, w, Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True

    if accent_line:
        pa0 = tf.paragraphs[0]
        pa0.alignment = PP_ALIGN.CENTER
        r0 = pa0.add_run()
        r0.text = accent_line
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = C_ACCENT

        pa1 = tf.add_paragraph()
        pa1.alignment = PP_ALIGN.CENTER
        r1 = pa1.add_run()
        r1.text = text
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_CAP
    else:
        pa = tf.paragraphs[0]
        pa.alignment = PP_ALIGN.CENTER
        r = pa.add_run()
        r.text = text
        r.font.size = Pt(10)
        r.font.color.rgb = C_CAP


# ── 공통 좌표 ────────────────────────────────────────────────
TOP   = Inches(0.68)
H     = Inches(5.1)
W_L   = Inches(5.6)    # 왼쪽 이미지 너비 (약간 넓게)
W_R   = Inches(5.6)
X_L   = Inches(0.2)
X_R   = Inches(6.2)
Y_CAP = Inches(5.85)


# ════════════════════════════════════════════════════════════
# 슬라이드 A: 접속 → 트랜잭션 제출
# 메시지: "누구나 접속해서 원하는 서명자를 직접 지정할 수 있다"
# ════════════════════════════════════════════════════════════
sA = new_slide('프론트엔드 시연 ①  —  접속 및 트랜잭션 제출')

add_img(sA, IMGS['home'], X_L, TOP, W_L, H)
add_caption(sA,
    '컨트랙트 주소만 입력하면 바로 접속',
    X_L, Y_CAP, W_L,
    accent_line='홈 화면')

add_img(sA, IMGS['new_tx'], X_R, TOP, W_R, H)
add_caption(sA,
    '수신 주소 · 금액 · 서명자 목록 · 최소 서명 수를\n'
    '트랜잭션마다 자유롭게 지정',
    X_R, Y_CAP, W_R,
    accent_line='새 트랜잭션 제출 — 서명자 직접 지정')

print('슬라이드 A 완료')


# ════════════════════════════════════════════════════════════
# 슬라이드 B: 서명 → 실행 완료
# 메시지: "권한에 따라 보이는 버튼이 다르고, 요건 충족 시 자동 실행"
# ════════════════════════════════════════════════════════════
sB = new_slide('프론트엔드 시연 ②  —  서명 및 자동 실행')

add_img(sB, IMGS['tx_owner1'], X_L, TOP, W_L, H)
add_caption(sB,
    '서명·서명취소·실행 + 제출자에게만 "트랜잭션 취소" 버튼 노출\n'
    '서명 현황 바로 확인 가능 (1 / 2)',
    X_L, Y_CAP, W_L,
    accent_line='대기 중 — Owner1(제출자) 시점')

add_img(sB, IMGS['executed'], X_R, TOP, W_R, H)
add_caption(sB,
    '2명 서명 완료 → required 충족 → 자동 실행\n'
    '서명 바 초록색 전환, 버튼 사라짐',
    X_R, Y_CAP, W_R,
    accent_line='실행 완료 — TX #0 ✅')

print('슬라이드 B 완료')


# 저장
p.save(DST)
print(f'\n저장 완료: {DST}  (총 {len(p.slides)}슬라이드)')
