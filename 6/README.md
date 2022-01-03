```
TIP: 5
Name: Oracle
Type: Standard
Status: raw
Editor: Alberto Granzotto @vrde
```

# Oracle

This document is governed by [TIP-0](../0).

## 1 Abstract

Contributors that work on the DAO must be rewarded. The Oracle main activity is to tokenize the work that has been done by contributors. To achieve that, the Oracle weekly queries Odoo to get information about who did what, and it mints and assign tokens.

## 2 Motivation

The work of the company is managed and organized in Odoo. Odoo is the "single source of truth" about employees, assets, projects, timesheets, and much more. Another important piece of the infrastructure is the [Time tracking app](../2) (TTA). TTA allows contributors to track the time they spend on the different tasks of the company. All those time entries are stored in Odoo as well. Once a task is done, it is reviewed and eventually approved by the *controller*. At this point a new *timesheet record* is created in Odoo. The *timesheet record* represents value added to the company. In order to

The role of the Oracle is to periodically query for new *timesheet records*, mint new [Teledisko Taler](../5) (TT) and assign them to contributors.

## 3 Specification

### 3.1 Overview

The oracle is an idempotent process. Every time it's run, it performs the following steps:

- Preconditions: 
  - Given `$PERIOD` as `day`, `week`, or `month`.
  - Given `$ENDPOINT` as an HTTP endpoint to an Ethereum node.
- Check the current 

### 3.2 Minimize the cost

When and how often should the oracle mint new tokens? Ideally, as soon as a task has been approved. The sooner contributors are paid, the better they feel. Given the current state of the Ethereum main network, transacting often will easily drain your wallet.

### 3.2.1 Payment scheduling

The cost of an Ethereum transaction depends on the complexity of the transaction itself, and on the gas price. Minting new tokens is around `70,000 gas units` ([ref](https://etherscan.io/tx/0xf8fe44718f03169719e47249c2e16cce6068f8f02e872340e3ef6c92b609e978)). On a good day the cost is around $1, on a normal day $10 (to do the math with the current gas market price, use the [transaction calculator](https://ethgasstation.info/calculatorTxV.php)). Paying contributors for each task that has been approved is going to be quite expensive.

To mitigate the impact of the gas fees, payments can be executed once a week or once a month. Let's consider a small organization with 10 active contributors.

- If payments are scheduled once a week, in one month the organization will spend $400 in fees.
- If payments are scheduled once a month, in one month the organization will spend $100 in fees.

### 3.2.2 xDAI network

Lowering the frequency of payments will obviously result in lower fees. Another scenario is to consider using another Ethereum network like xDAI. I didn't do the math, but the cost of minting new tokens in the xDAI network should be around `$0.00007`, that is ridiculously low. In that case tokens will reside in another network, and contributors would need to use the xDAI to Mainnet bridge to move their tokens.

### 3.2.3 No one-size-fit-all solution

We don't need to make a decision now. Both *scheduling* and *network* are variables that can be configured when running the oracle.

In order to minimize the fees, the oracle:

- Should group transactions...

The Oracle every hour takes the following steps:


### 3.3 Security

The oracle can be hacked and private key exposed. Even with the oracle private key, an attacker MUST not be able to generate tokens.

In order to mitigate this:

- (Simple but expensive on Mainnet) Multisig scheme: the oracle submits a "mint request" that should be signed by the DAO members, or a trusted subset of them.
- (Complex but cheaper?) Use the Boneh-Lynn-Shacham signature scheme (BLS) to aggregate signatures offline, then make a single transaction. [Intro to BLS](https://medium.com/cryptoadvance/bls-signatures-better-than-schnorr-5a7fe30ea716), [implementation](https://gist.github.com/BjornvdLaan/ca6dd4e3993e1ef392f363ec27fe74c4), [more info](https://gist.github.com/hermanjunge/3308fbd3627033fc8d8ca0dd50809844).

## 4 Rationale

Minting tokens is a tricky business. Many things can go wrong, errors, bugs, cheating, and hacking can lead to mint and assign the wrong amount of tokens to the wrong contributors.

This can be mitigated by having contributors to vote before minting and assigning tokens.

## 5 Implementation

TBD

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
