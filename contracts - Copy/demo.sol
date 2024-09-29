// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MusicNFT is ERC721, Ownable {
    uint256 public nextTokenId;
    mapping(uint256 => string) private _tokenURIs;

    constructor(
    ) ERC721("MusicNFT", "MNFT") {}

    // Function to mint a new music NFT
           event MintAttempt(address indexed sender, string tokenURI);
    function mint(string memory tokenURI) public onlyOwner {
        emit MintAttempt(msg.sender, tokenURI);
        uint256 tokenId = nextTokenId;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
        nextTokenId++;
    }
    function exists(uint256 tokenId) public view returns (bool) {
    return _exists(tokenId);
    }

    // Internal function to set the token URI
    function _setTokenURI(uint256 tokenId, string memory tokenURI) internal {
        _tokenURIs[tokenId] = tokenURI;
    }

    // Function to retrieve the token URI
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "Query for nonexistent token");
        return _tokenURIs[tokenId];
    }
    event TokenMinted(uint256 tokenId, string tokenURI);

    // Function to withdraw Ether from the contract
    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}

