# Ethereum Multi-Signature Wallet

이더리움 스마트 컨트랙트 기반 다중 서명(Multi-Signature) 지갑입니다.  
트랜잭션을 제출할 때 서명자와 최소 서명 수를 직접 지정합니다. 전역 서명자 목록 없이 트랜잭션마다 독립적인 N-of-M 서명 정책을 설정할 수 있습니다.

---

## 컨트랙트 구조

```
MultiSigWallet.sol
├── 상태 변수
│   ├── Transaction[] transactions              — 트랜잭션 목록
│   ├── mapping isAllowedSigner                 — 서명 허용 여부 (txId → address → bool)
│   └── mapping isConfirmed                     — 서명 여부     (txId → address → bool)
│
├── Transaction 구조체
│   ├── address to                              — 수신 주소
│   ├── uint value                              — 전송 금액 (wei)
│   ├── bool executed                           — 실행 여부
│   ├── bool cancelled                          — 취소 여부
│   ├── uint confirmCount                       — 현재 서명 수
│   ├── uint required                           — 최소 서명 수
│   ├── address[] allowedSigners                — 허용된 서명자 목록
│   └── address submitter                       — 트랜잭션 제출자
│
├── 이벤트
│   ├── Deposit(sender, amount, balance)         — ETH 입금
│   ├── TransactionSubmitted(txId, submitter, to, value) — 트랜잭션 제출
│   ├── TransactionConfirmed(txId, signer)       — 서명
│   ├── ConfirmationRevoked(txId, signer)        — 서명 취소
│   ├── TransactionExecuted(txId)                — 트랜잭션 실행
│   └── TransactionCancelled(txId, submitter)    — 트랜잭션 취소
│
└── 주요 함수
    ├── submitTransaction(to, value, signers[], required) — 트랜잭션 제출 (서명자 직접 지정)
    ├── confirmTransaction(txId)                 — 서명
    ├── revokeConfirmation(txId)                 — 서명 취소
    ├── executeTransaction(txId)                 — 트랜잭션 실행
    ├── cancelTransaction(txId)                  — 트랜잭션 취소 (제출자 전용)
    ├── getTransaction(txId)                     — 트랜잭션 정보 조회 (8개 반환값)
    ├── getTransactionCount()                    — 트랜잭션 수 조회
    └── getConfirmations(txId)                   — 실제 서명한 주소 목록 조회
```

---

## 설치 및 실행

### 1. 의존성 설치

```bash
cd multisig-wallet
npm install
```

### 2. 컴파일

```bash
npx hardhat compile
```

### 3. 테스트

```bash
npx hardhat test
```

---

## 배포 방법

### 공통: 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 값을 입력합니다.

```bash
cp .env.example .env
```

| 변수명 | 설명 |
|--------|------|
| `DEPLOYER_PRIVATE_KEY` | 배포 계정 개인키 (가스 납부) |
| `SEPOLIA_RPC_URL` | Sepolia RPC 엔드포인트 (Alchemy 등) |
| `GANACHE_URL` | Ganache 주소 (기본값: `http://127.0.0.1:7545`) |
| `GANACHE_CHAIN_ID` | Ganache 체인 ID (기본값: `1337`) |

> 컨트랙트에 전역 서명자가 없으므로 `OWNER*` 관련 변수는 불필요합니다.

---

### Ganache 로컬 배포

1. Ganache GUI 또는 CLI 실행 (기본 포트 7545)
2. `.env`에 `DEPLOYER_PRIVATE_KEY` 입력
3. 배포:

```bash
npx hardhat run scripts/deploy.js --network ganache
```

---

### Sepolia 테스트넷 배포

1. `.env`에 `SEPOLIA_RPC_URL`과 `DEPLOYER_PRIVATE_KEY` 입력
2. [Google Cloud Web3 Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)에서 테스트 ETH 충전
3. 배포:

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**현재 배포된 컨트랙트 주소 (Sepolia):** `0x09fBa7c6c534882dF15a920671Fc9dbB3864c005`

---

## 프론트엔드 사용법

`frontend/index.html`을 브라우저에서 열거나 로컬 서버로 실행합니다.

### 홈 화면
1. **MetaMask 연결** — 계정 선택 팝업이 뜹니다.
2. **컨트랙트 주소 입력** 후 **대시보드 열기** 클릭.

### 대시보드
| 기능 | 설명 |
|------|------|
| 입금 | 컨트랙트에 ETH를 전송합니다. |
| 새 트랜잭션 | 수신 주소, 금액, 서명자 목록, 최소 서명 수를 지정해 트랜잭션을 제출합니다. |
| ✅ 서명 | 허용된 서명자만 표시됩니다. |
| ↩ 서명취소 | 서명을 철회합니다 (트랜잭션은 유지). |
| ▶ 실행 | 서명 수 충족 시 누구나 실행할 수 있습니다. |
| 🚫 트랜잭션 취소 | **제출자만** 표시됩니다. 트랜잭션을 완전히 무효화합니다. |

---

## 시연 시나리오

```
1. 컨트랙트 배포 (생성자 인자 없음)
2. 컨트랙트에 ETH 입금
3. Alice가 submitTransaction(to=Bob, value=0.1 ETH, signers=[Alice,Carol], required=2) 제출
4. Alice가 confirmTransaction → confirmCount = 1
5. Carol이 confirmTransaction → confirmCount = 2 (자동 실행)
6. TransactionExecuted 이벤트 확인

[취소 시나리오]
7. Alice가 새 트랜잭션 제출
8. Alice가 cancelTransaction → 트랜잭션 무효화
9. Carol이 confirmTransaction 시도 → revert ("Already cancelled")

[예외 시나리오]
10. 비허용 서명자가 confirmTransaction 시도 → revert ("Not an allowed signer")
11. 서명 수 미달 상태에서 executeTransaction 시도 → revert ("Not enough confirmations")
```

---

## 예외 처리 목록

| 조건 | 에러 메시지 |
|------|------------|
| 허용되지 않은 서명자 접근 | `Not an allowed signer` |
| 중복 서명 | `Already confirmed` |
| 서명 수 미달 실행 | `Not enough confirmations` |
| 재실행 시도 | `Already executed` |
| 이미 취소된 트랜잭션 | `Already cancelled` |
| 잘못된 txId | `Transaction does not exist` |
| 미서명 상태에서 서명 취소 | `Not confirmed` |
| 제출자가 아닌 취소 시도 | `Not the submitter` |
| 잘못된 수신자 주소 | `Invalid recipient address` |
| 서명자 배열 비어있음 | `Signers required` |
| 잘못된 최소 서명 수 | `Invalid required number` |
| 중복 서명자 등록 | `Duplicate signer` |
| ETH 전송 실패 | `Transaction failed` |
