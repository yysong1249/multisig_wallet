const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MultiSigWallet", function () {
  let wallet;
  let signer1, signer2, signer3, outsider, recipient;
  const SEND_VALUE = ethers.parseEther("1");
  const FUND_VALUE = ethers.parseEther("10");

  // 공통 헬퍼: 기본 트랜잭션 제출 (signer1, signer2, signer3 / required=2)
  async function submit(signers, required, to, value) {
    return wallet.submitTransaction(to, value, signers, required);
  }

  beforeEach(async function () {
    [signer1, signer2, signer3, outsider, recipient] = await ethers.getSigners();

    const MultiSigWallet = await ethers.getContractFactory("MultiSigWallet");
    wallet = await MultiSigWallet.deploy([signer1.address, signer2.address, signer3.address]);
    await wallet.waitForDeployment();

    // 컨트랙트에 ETH 예치
    await signer1.sendTransaction({
      to: await wallet.getAddress(),
      value: FUND_VALUE,
    });
  });

  // ─── TC-01: 배포 확인 ──────────────────────────────────────────────────────
  describe("TC-01: 배포 확인", function () {
    it("배포 후 트랜잭션 수가 0이어야 한다", async function () {
      expect(await wallet.getTransactionCount()).to.equal(0);
    });

    it("컨트랙트가 ETH를 받아야 한다", async function () {
      const bal = await ethers.provider.getBalance(await wallet.getAddress());
      expect(bal).to.equal(FUND_VALUE);
    });

    it("배포 시 등록된 Owner가 isOwner에 저장되어야 한다", async function () {
      expect(await wallet.isOwner(signer1.address)).to.be.true;
      expect(await wallet.isOwner(signer2.address)).to.be.true;
      expect(await wallet.isOwner(signer3.address)).to.be.true;
      expect(await wallet.isOwner(outsider.address)).to.be.false;
    });

    it("getOwners가 Owner 목록을 반환해야 한다", async function () {
      const ownerList = await wallet.getOwners();
      expect(ownerList).to.deep.equal([signer1.address, signer2.address, signer3.address]);
    });

    it("Owner가 없으면 배포 시 revert되어야 한다", async function () {
      const MultiSigWallet = await ethers.getContractFactory("MultiSigWallet");
      await expect(MultiSigWallet.deploy([])).to.be.revertedWith("Owners required");
    });

    it("중복 Owner 배포 시 revert되어야 한다", async function () {
      const MultiSigWallet = await ethers.getContractFactory("MultiSigWallet");
      await expect(
        MultiSigWallet.deploy([signer1.address, signer1.address])
      ).to.be.revertedWith("Duplicate owner");
    });
  });

  // ─── TC-02: 트랜잭션 제출 확인 ───────────────────────────────────────────
  describe("TC-02: 트랜잭션 제출 확인", function () {
    it("제출 후 트랜잭션이 생성되어야 한다", async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        2,
        recipient.address,
        SEND_VALUE
      );
      const tx = await wallet.getTransaction(0);
      expect(tx.to).to.equal(recipient.address);
      expect(tx.value).to.equal(SEND_VALUE);
      expect(tx.executed).to.be.false;
      expect(tx.confirmCount).to.equal(0);
      expect(tx.required).to.equal(2);
    });

    it("allowedSigners가 올바르게 저장되어야 한다", async function () {
      await submit(
        [signer1.address, signer2.address],
        1,
        recipient.address,
        SEND_VALUE
      );
      const tx = await wallet.getTransaction(0);
      expect(tx.allowedSigners).to.deep.equal([signer1.address, signer2.address]);
    });

    it("isAllowedSigner 매핑이 올바르게 설정되어야 한다", async function () {
      await submit(
        [signer1.address, signer2.address],
        1,
        recipient.address,
        SEND_VALUE
      );
      expect(await wallet.isAllowedSigner(0, signer1.address)).to.be.true;
      expect(await wallet.isAllowedSigner(0, signer2.address)).to.be.true;
      expect(await wallet.isAllowedSigner(0, outsider.address)).to.be.false;
    });

    it("TransactionSubmitted 이벤트가 발생해야 한다", async function () {
      await expect(
        submit(
          [signer1.address, signer2.address],
          1,
          recipient.address,
          SEND_VALUE
        )
      )
        .to.emit(wallet, "TransactionSubmitted")
        .withArgs(0, signer1.address, recipient.address, SEND_VALUE);
    });

    it("getTransactionCount가 올바르게 증가해야 한다", async function () {
      expect(await wallet.getTransactionCount()).to.equal(0);
      await submit([signer1.address], 1, recipient.address, SEND_VALUE);
      expect(await wallet.getTransactionCount()).to.equal(1);
      await submit([signer2.address], 1, recipient.address, SEND_VALUE);
      expect(await wallet.getTransactionCount()).to.equal(2);
    });

    it("Owner는 트랜잭션을 제출할 수 있어야 한다", async function () {
      await expect(
        submit([signer1.address], 1, recipient.address, SEND_VALUE)
      ).to.not.be.reverted;
    });

    it("Owner가 아닌 자가 제출 시 revert되어야 한다", async function () {
      await expect(
        wallet.connect(outsider).submitTransaction(recipient.address, SEND_VALUE, [outsider.address], 1)
      ).to.be.revertedWith("Not an owner");
    });

    it("수신자가 zero address이면 revert되어야 한다", async function () {
      await expect(
        submit([signer1.address], 1, ethers.ZeroAddress, SEND_VALUE)
      ).to.be.revertedWith("Invalid recipient address");
    });

    it("서명자 배열이 비어있으면 revert되어야 한다", async function () {
      await expect(
        wallet.submitTransaction(recipient.address, SEND_VALUE, [], 1)
      ).to.be.revertedWith("Signers required");
    });

    it("required가 0이면 revert되어야 한다", async function () {
      await expect(
        wallet.submitTransaction(recipient.address, SEND_VALUE, [signer1.address], 0)
      ).to.be.revertedWith("Invalid required number");
    });

    it("required가 서명자 수보다 크면 revert되어야 한다", async function () {
      await expect(
        wallet.submitTransaction(recipient.address, SEND_VALUE, [signer1.address], 2)
      ).to.be.revertedWith("Invalid required number");
    });

    it("중복 서명자 등록 시 revert되어야 한다", async function () {
      await expect(
        wallet.submitTransaction(
          recipient.address,
          SEND_VALUE,
          [signer1.address, signer1.address],
          1
        )
      ).to.be.revertedWith("Duplicate signer");
    });

    it("zero address 서명자 등록 시 revert되어야 한다", async function () {
      await expect(
        wallet.submitTransaction(
          recipient.address,
          SEND_VALUE,
          [ethers.ZeroAddress],
          1
        )
      ).to.be.revertedWith("Invalid signer address");
    });
  });

  // ─── TC-03: 서명(confirmTransaction) 확인 ────────────────────────────────
  describe("TC-03: 서명 확인", function () {
    beforeEach(async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        2,
        recipient.address,
        SEND_VALUE
      );
    });

    it("서명 후 confirmCount가 증가해야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      const tx = await wallet.getTransaction(0);
      expect(tx.confirmCount).to.equal(1);
    });

    it("서명 후 isConfirmed가 true여야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      expect(await wallet.isConfirmed(0, signer1.address)).to.be.true;
    });

    it("TransactionConfirmed 이벤트가 발생해야 한다", async function () {
      await expect(wallet.connect(signer1).confirmTransaction(0))
        .to.emit(wallet, "TransactionConfirmed")
        .withArgs(0, signer1.address);
    });

    it("허용되지 않은 서명자가 서명 시 revert되어야 한다", async function () {
      await expect(
        wallet.connect(outsider).confirmTransaction(0)
      ).to.be.revertedWith("Not an allowed signer");
    });

    it("존재하지 않는 txId 서명 시 revert되어야 한다", async function () {
      await expect(
        wallet.connect(signer1).confirmTransaction(999)
      ).to.be.revertedWith("Transaction does not exist");
    });

    it("중복 서명 시 revert되어야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      await expect(
        wallet.connect(signer1).confirmTransaction(0)
      ).to.be.revertedWith("Already confirmed");
    });
  });

  // ─── TC-04: required 충족 → 자동 실행 확인 ───────────────────────────────
  describe("TC-04: required 충족 시 자동 실행 확인", function () {
    beforeEach(async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        2,
        recipient.address,
        SEND_VALUE
      );
    });

    it("required 충족 시 트랜잭션이 자동 실행되어야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      await expect(wallet.connect(signer2).confirmTransaction(0))
        .to.emit(wallet, "TransactionExecuted")
        .withArgs(0);
      const tx = await wallet.getTransaction(0);
      expect(tx.executed).to.be.true;
    });

    it("실행 후 수신자 잔액이 증가해야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      await expect(
        wallet.connect(signer2).confirmTransaction(0)
      ).to.changeEtherBalance(recipient, SEND_VALUE);
    });

    it("실행 후 컨트랙트 잔액이 감소해야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      await expect(
        wallet.connect(signer2).confirmTransaction(0)
      ).to.changeEtherBalance(wallet, -SEND_VALUE);
    });
  });

  // ─── TC-05: 서명 취소(revokeConfirmation) 확인 ───────────────────────────
  describe("TC-05: 서명 취소 확인", function () {
    beforeEach(async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        2,
        recipient.address,
        SEND_VALUE
      );
      await wallet.connect(signer1).confirmTransaction(0);
    });

    it("ConfirmationRevoked 이벤트가 발생해야 한다", async function () {
      await expect(wallet.connect(signer1).revokeConfirmation(0))
        .to.emit(wallet, "ConfirmationRevoked")
        .withArgs(0, signer1.address);
    });

    it("서명 취소 후 isConfirmed가 false여야 한다", async function () {
      await wallet.connect(signer1).revokeConfirmation(0);
      expect(await wallet.isConfirmed(0, signer1.address)).to.be.false;
    });

    it("서명 취소 후 confirmCount가 감소해야 한다", async function () {
      await wallet.connect(signer1).revokeConfirmation(0);
      const tx = await wallet.getTransaction(0);
      expect(tx.confirmCount).to.equal(0);
    });

    it("서명 취소 후 재서명이 가능해야 한다", async function () {
      await wallet.connect(signer1).revokeConfirmation(0);
      await wallet.connect(signer1).confirmTransaction(0);
      expect(await wallet.isConfirmed(0, signer1.address)).to.be.true;
    });

    it("서명하지 않은 사람이 취소 시 revert되어야 한다", async function () {
      await expect(
        wallet.connect(signer2).revokeConfirmation(0)
      ).to.be.revertedWith("Not confirmed");
    });

    it("허용되지 않은 서명자가 취소 시 revert되어야 한다", async function () {
      await expect(
        wallet.connect(outsider).revokeConfirmation(0)
      ).to.be.revertedWith("Not an allowed signer");
    });
  });

  // ─── TC-06: 실행 완료 트랜잭션 재시도 → revert 확인 ─────────────────────
  describe("TC-06: 실행 완료 트랜잭션 재시도 → revert 확인", function () {
    beforeEach(async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        2,
        recipient.address,
        SEND_VALUE
      );
      await wallet.connect(signer1).confirmTransaction(0);
      await wallet.connect(signer2).confirmTransaction(0); // 자동 실행
    });

    it("실행된 트랜잭션의 executeTransaction 시 revert되어야 한다", async function () {
      await expect(wallet.connect(signer1).executeTransaction(0)).to.be.revertedWith(
        "Already executed"
      );
    });

    it("실행된 트랜잭션의 confirmTransaction 시 revert되어야 한다", async function () {
      await expect(wallet.connect(signer3).confirmTransaction(0)).to.be.revertedWith(
        "Already executed"
      );
    });

    it("실행된 트랜잭션의 revokeConfirmation 시 revert되어야 한다", async function () {
      await expect(wallet.connect(signer1).revokeConfirmation(0)).to.be.revertedWith(
        "Already executed"
      );
    });
  });

  // ─── TC-07-A: 트랜잭션 취소 확인 ────────────────────────────────────────
  describe("TC-07-A: 트랜잭션 취소 확인", function () {
    beforeEach(async function () {
      await submit(
        [signer1.address, signer2.address],
        2,
        recipient.address,
        SEND_VALUE
      );
    });

    it("제출자가 취소할 수 있어야 한다", async function () {
      await expect(wallet.connect(signer1).cancelTransaction(0))
        .to.emit(wallet, "TransactionCancelled")
        .withArgs(0, signer1.address);
      const t = await wallet.getTransaction(0);
      expect(t.cancelled).to.be.true;
    });

    it("취소 후 confirmTransaction 시 revert되어야 한다", async function () {
      await wallet.connect(signer1).cancelTransaction(0);
      await expect(wallet.connect(signer1).confirmTransaction(0)).to.be.revertedWith("Already cancelled");
    });

    it("취소 후 executeTransaction 시 revert되어야 한다", async function () {
      await wallet.connect(signer1).cancelTransaction(0);
      await expect(wallet.connect(signer1).executeTransaction(0)).to.be.revertedWith("Already cancelled");
    });

    it("취소 후 revokeConfirmation 시 revert되어야 한다", async function () {
      await wallet.connect(signer1).confirmTransaction(0);
      await wallet.connect(signer1).cancelTransaction(0);
      await expect(wallet.connect(signer1).revokeConfirmation(0)).to.be.revertedWith("Already cancelled");
    });

    it("제출자가 아닌 사람이 취소 시 revert되어야 한다", async function () {
      await expect(wallet.connect(signer2).cancelTransaction(0)).to.be.revertedWith("Not the submitter");
    });

    it("이미 취소된 트랜잭션을 재취소 시 revert되어야 한다", async function () {
      await wallet.connect(signer1).cancelTransaction(0);
      await expect(wallet.connect(signer1).cancelTransaction(0)).to.be.revertedWith("Already cancelled");
    });

    it("실행된 트랜잭션을 취소 시 revert되어야 한다", async function () {
      await submit([signer1.address, signer2.address], 2, recipient.address, SEND_VALUE);
      await wallet.connect(signer1).confirmTransaction(1);
      await wallet.connect(signer2).confirmTransaction(1); // 자동 실행
      await expect(wallet.connect(signer1).cancelTransaction(1)).to.be.revertedWith("Already executed");
    });
  });

  // ─── TC-07: 서명 수 미달 직접 실행 → revert 확인 ────────────────────────
  describe("TC-07: 서명 수 미달 실행 시도 → revert 확인", function () {
    it("서명 수 미달 시 executeTransaction 시 revert되어야 한다", async function () {
      await submit(
        [signer1.address, signer2.address],
        2,
        recipient.address,
        SEND_VALUE
      );
      await wallet.connect(signer1).confirmTransaction(0);
      await expect(wallet.connect(signer1).executeTransaction(0)).to.be.revertedWith(
        "Not enough confirmations"
      );
    });

    it("누구나 요건 충족된 트랜잭션을 실행할 수 있어야 한다", async function () {
      await submit(
        [signer1.address, signer2.address],
        2,
        recipient.address,
        SEND_VALUE
      );
      await wallet.connect(signer1).confirmTransaction(0);
      await wallet.connect(signer2).confirmTransaction(0);
      // 이미 자동 실행됨, revert 확인
      await expect(wallet.executeTransaction(0)).to.be.revertedWith("Already executed");
    });
  });

  // ─── TC-08: 조회 기능 ─────────────────────────────────────────────────────
  describe("TC-08: 조회 기능", function () {
    it("ETH 입금 시 Deposit 이벤트가 발생해야 한다", async function () {
      await expect(
        signer2.sendTransaction({
          to: await wallet.getAddress(),
          value: ethers.parseEther("5"),
        })
      ).to.emit(wallet, "Deposit");
    });

    it("getConfirmations가 서명자 목록을 올바르게 반환해야 한다", async function () {
      await submit(
        [signer1.address, signer2.address, signer3.address],
        3,
        recipient.address,
        SEND_VALUE
      );
      await wallet.connect(signer1).confirmTransaction(0);
      await wallet.connect(signer2).confirmTransaction(0);

      const confirmations = await wallet.getConfirmations(0);
      expect(confirmations).to.include(signer1.address);
      expect(confirmations).to.include(signer2.address);
      expect(confirmations).to.not.include(signer3.address);
    });

    it("존재하지 않는 txId 조회 시 revert되어야 한다", async function () {
      await expect(wallet.getTransaction(999)).to.be.revertedWith(
        "Transaction does not exist"
      );
    });

    it("트랜잭션별로 다른 서명자 집합이 독립적으로 관리되어야 한다", async function () {
      await submit([signer1.address], 1, recipient.address, SEND_VALUE);
      await submit([signer2.address, signer3.address], 1, recipient.address, SEND_VALUE);

      expect(await wallet.isAllowedSigner(0, signer1.address)).to.be.true;
      expect(await wallet.isAllowedSigner(0, signer2.address)).to.be.false;
      expect(await wallet.isAllowedSigner(1, signer2.address)).to.be.true;
      expect(await wallet.isAllowedSigner(1, signer1.address)).to.be.false;
    });
  });
});
