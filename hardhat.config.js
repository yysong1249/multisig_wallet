require("@nomicfoundation/hardhat-toolbox");

try {
  require("dotenv").config();
} catch {}

function getAccounts() {
  const keys = [
    process.env.DEPLOYER_PRIVATE_KEY,
    process.env.OWNER2_PRIVATE_KEY,
    process.env.OWNER3_PRIVATE_KEY,
  ].filter(Boolean);
  return keys.map((k) => (k.startsWith("0x") ? k : `0x${k}`));
}

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24",
  networks: {
    ganache: {
      url: process.env.GANACHE_URL || "http://127.0.0.1:7545",
      chainId: parseInt(process.env.GANACHE_CHAIN_ID || "1337"),
      accounts: getAccounts().length > 0 ? getAccounts() : undefined,
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: getAccounts(),
      chainId: 11155111,
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY || "",
  },
  mocha: {
    timeout: 60000,
    exit: true,
  },
};
