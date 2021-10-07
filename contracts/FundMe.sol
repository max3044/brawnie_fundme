// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // as well as we're using 0.6.0 version we need to specify safe math
    using SafeMathChainlink for uint256;

    // set array for funders
    address[] public funders;

    // set mapping
    mapping(address => uint256) public addressToAmountFunded;

    // set owner of the contract
    address public owner;

    // set var for priceFeed addresses
    AggregatorV3Interface public priceFeed;

    // set constructor
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);

        // first sender will be an owner
        owner = msg.sender;
    }

    // func to fund contract
    function fund() public payable {
        // min amount of eth
        uint256 minimumUSD = 50 * 10**18;

        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;

        funders.push(msg.sender);
    }

    // get version of AggregatorV3Interface
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    // get current price eth to usd in wei (with 18 decimals)
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        // answer is 8-decimals number
        // since we using wei (18 decimals), we need to multiply it by 10 ** 10

        return uint256(answer * (10**10));
    }

    // convert eth to usd (get max eth by usd)
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();

        uint256 ethAmountInUSD = (ethPrice * ethAmount) / (10**18);

        return ethAmountInUSD;
    }

    // get entrance fee - minimum amount of eth that person should pay

    function getEntranceFee() public view returns (uint256) {
        // minimal usd
        uint256 minimumUSD = 50 * 10**18;

        uint256 price = getPrice();

        uint256 precision = 1 * 10**18;

        return (minimumUSD * precision) / price;
    }

    // modifier that checks that sender is owner
    modifier onlyOwner() {
        require(msg.sender == owner, "You aren't the owner of the contract!");

        _;
    }

    // to withdraw all funds to owner and clear array of funders and funder's mapping
    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];

            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}
