// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract MultiSigWallet {
    // ─── 이벤트 ───────────────────────────────────────────────────────────────
    event Deposit(address indexed sender, uint amount, uint balance);
    event TransactionSubmitted(
        uint indexed txId,
        address indexed submitter,
        address indexed to,
        uint value
    );
    event TransactionConfirmed(uint indexed txId, address indexed signer);
    event ConfirmationRevoked(uint indexed txId, address indexed signer);
    event TransactionExecuted(uint indexed txId);
    event TransactionCancelled(uint indexed txId, address indexed submitter);

    // ─── 상태 변수 ────────────────────────────────────────────────────────────
    mapping(address => bool) public isOwner;
    address[] public owners;

    struct Transaction {
        address to;
        uint value;
        bool executed;
        bool cancelled;
        uint confirmCount;
        uint required;
        address[] allowedSigners;
        address submitter;
    }

    Transaction[] public transactions;
    mapping(uint => mapping(address => bool)) public isAllowedSigner;
    mapping(uint => mapping(address => bool)) public isConfirmed;

    // ─── 생성자 ───────────────────────────────────────────────────────────────
    constructor(address[] memory _owners) {
        require(_owners.length > 0, "Owners required");
        for (uint i = 0; i < _owners.length; i++) {
            address o = _owners[i];
            require(o != address(0), "Invalid owner address");
            require(!isOwner[o], "Duplicate owner");
            isOwner[o] = true;
            owners.push(o);
        }
    }

    // ─── Modifier ─────────────────────────────────────────────────────────────
    modifier onlyOwner() {
        require(isOwner[msg.sender], "Not an owner");
        _;
    }

    modifier txExists(uint _txId) {
        require(_txId < transactions.length, "Transaction does not exist");
        _;
    }

    modifier notConfirmed(uint _txId) {
        require(!isConfirmed[_txId][msg.sender], "Already confirmed");
        _;
    }

    modifier notExecuted(uint _txId) {
        require(!transactions[_txId].executed, "Already executed");
        _;
    }

    modifier notCancelled(uint _txId) {
        require(!transactions[_txId].cancelled, "Already cancelled");
        _;
    }

    modifier onlyAllowedSigner(uint _txId) {
        require(isAllowedSigner[_txId][msg.sender], "Not an allowed signer");
        _;
    }

    // ─── ETH 입금 ─────────────────────────────────────────────────────────────
    receive() external payable {
        emit Deposit(msg.sender, msg.value, address(this).balance);
    }

    // ─── 트랜잭션 제출 (서명자 직접 지정) ────────────────────────────────────
    function submitTransaction(
        address _to,
        uint _value,
        address[] memory _allowedSigners,
        uint _required
    ) public onlyOwner returns (uint txId) {
        require(_to != address(0), "Invalid recipient address");
        require(_allowedSigners.length > 0, "Signers required");
        require(
            _required > 0 && _required <= _allowedSigners.length,
            "Invalid required number"
        );

        txId = transactions.length;
        transactions.push();
        Transaction storage newTx = transactions[txId];
        newTx.to = _to;
        newTx.value = _value;
        newTx.executed = false;
        newTx.cancelled = false;
        newTx.confirmCount = 0;
        newTx.required = _required;
        newTx.submitter = msg.sender;

        for (uint i = 0; i < _allowedSigners.length; i++) {
            address signer = _allowedSigners[i];
            require(signer != address(0), "Invalid signer address");
            require(!isAllowedSigner[txId][signer], "Duplicate signer");
            isAllowedSigner[txId][signer] = true;
            newTx.allowedSigners.push(signer);
        }

        emit TransactionSubmitted(txId, msg.sender, _to, _value);
    }

    // ─── 트랜잭션 서명 ────────────────────────────────────────────────────────
    function confirmTransaction(uint _txId)
        public
        txExists(_txId)
        notConfirmed(_txId)
        notExecuted(_txId)
        notCancelled(_txId)
        onlyAllowedSigner(_txId)
    {
        Transaction storage transaction = transactions[_txId];
        transaction.confirmCount++;
        isConfirmed[_txId][msg.sender] = true;
        emit TransactionConfirmed(_txId, msg.sender);

        if (transaction.confirmCount >= transaction.required) {
            executeTransaction(_txId);
        }
    }

    // ─── 서명 취소 ────────────────────────────────────────────────────────────
    function revokeConfirmation(uint _txId)
        public
        txExists(_txId)
        notExecuted(_txId)
        notCancelled(_txId)
        onlyAllowedSigner(_txId)
    {
        require(isConfirmed[_txId][msg.sender], "Not confirmed");
        Transaction storage transaction = transactions[_txId];
        transaction.confirmCount--;
        isConfirmed[_txId][msg.sender] = false;
        emit ConfirmationRevoked(_txId, msg.sender);
    }

    // ─── 트랜잭션 실행 ────────────────────────────────────────────────────────
    function cancelTransaction(uint _txId)
        public
        txExists(_txId)
        notExecuted(_txId)
        notCancelled(_txId)
    {
        require(transactions[_txId].submitter == msg.sender, "Not the submitter");
        transactions[_txId].cancelled = true;
        emit TransactionCancelled(_txId, msg.sender);
    }

    function executeTransaction(uint _txId)
        public
        txExists(_txId)
        notExecuted(_txId)
        notCancelled(_txId)
    {
        Transaction storage transaction = transactions[_txId];
        require(transaction.confirmCount >= transaction.required, "Not enough confirmations");
        transaction.executed = true;
        (bool success, ) = transaction.to.call{value: transaction.value}("");
        require(success, "Transaction failed");
        emit TransactionExecuted(_txId);
    }

    // ─── 조회 함수 ────────────────────────────────────────────────────────────
    function getOwners() public view returns (address[] memory) {
        return owners;
    }

    function getTransactionCount() public view returns (uint) {
        return transactions.length;
    }

    function getTransaction(uint _txId)
        public
        view
        txExists(_txId)
        returns (
            address to,
            uint value,
            bool executed,
            bool cancelled,
            uint confirmCount,
            uint required,
            address[] memory allowedSigners,
            address submitter
        )
    {
        Transaction storage t = transactions[_txId];
        return (t.to, t.value, t.executed, t.cancelled, t.confirmCount, t.required, t.allowedSigners, t.submitter);
    }

    function getConfirmations(uint _txId)
        public
        view
        txExists(_txId)
        returns (address[] memory)
    {
        Transaction storage t = transactions[_txId];
        address[] memory temp = new address[](t.allowedSigners.length);
        uint count = 0;
        for (uint i = 0; i < t.allowedSigners.length; i++) {
            if (isConfirmed[_txId][t.allowedSigners[i]]) {
                temp[count] = t.allowedSigners[i];
                count++;
            }
        }
        address[] memory result = new address[](count);
        for (uint i = 0; i < count; i++) {
            result[i] = temp[i];
        }
        return result;
    }
}
