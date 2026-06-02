const hre = require("hardhat");
const { ethers } = hre;

async function main() {
  const signers = await ethers.getSigners();
  const deployer = signers[0];

  console.log("========================================");
  console.log("MultiSigWallet 배포 시작");
  console.log("========================================");
  console.log("네트워크      :", hre.network.name);
  console.log("배포 계정     :", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("배포 계정 잔액:", ethers.formatEther(balance), "ETH");

  const ownerAddresses = process.env.OWNER_ADDRESSES
    ? process.env.OWNER_ADDRESSES.split(",").map(a => a.trim())
    : signers.map(s => s.address);   // .env의 모든 PRIVATE_KEY 계정을 Owner로 등록

  console.log("\nOwner 목록:");
  ownerAddresses.forEach((a, i) => console.log(`  [${i}]`, a));
  console.log("\n컨트랙트 배포 중...");
  const MultiSigWallet = await ethers.getContractFactory("MultiSigWallet");
  const wallet = await MultiSigWallet.deploy(ownerAddresses);
  await wallet.waitForDeployment();

  const contractAddress = await wallet.getAddress();
  const deployTx = wallet.deploymentTransaction();

  console.log("\n========================================");
  console.log("배포 완료");
  console.log("========================================");
  console.log("컨트랙트 주소 :", contractAddress);
  console.log("트랜잭션 해시  :", deployTx?.hash || "N/A");

  if (hre.network.name === "sepolia") {
    console.log(
      "\nEtherscan 확인:",
      `https://sepolia.etherscan.io/address/${contractAddress}`
    );
  }
}

main().catch((error) => {
  console.error("\n[배포 실패]", error.message);
  process.exit(1);
});
