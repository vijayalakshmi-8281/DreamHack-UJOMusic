const MusicNFT = artifacts.require("MusicNFT");

module.exports = function (deployer) {
  // Deploy the MusicNFT contract
  deployer.deploy(MusicNFT);
}