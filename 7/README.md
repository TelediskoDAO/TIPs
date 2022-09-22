# Register TelediskoToken as a Cosmos Coin

## 1 Abstract

Make TelediskoToken available as a Cosmos coin so our holders will be able to access all services and DEX available in the Cosmos network.

## 2 Motivation

TelediskoToken is an ERC-20 token deployed in the EVMOS blockchain. While it's freely transferrable across EVMOS addresses, the token is not compatible with the Cosmos Network. This means that TelediskoToken holders cannot transfer tokens to other chains in the Cosmos ecosystem. But fear not, EVMOS allows to register an ERC-20 token as a Cosmos coin through a governance proposal.

To avoid confusion between EVMOS tokens and Cosmos tokens, we will use this nomenclature from now on:

- **token**: an ERC-20 fungible asset that lives in EVMOS.
- **coin**: a native Cosmos fungible asset that can be transferred to different chains using IBC.

EVMOS allows on-chain bidirectional internal conversion of tokens between Evmos EVM and Cosmos runtimes. Coins can be registered as tokens, and tokens can be registered as coins (more info in the EVMOS [docs](erc20)).

While registering a Cosmos coin as an ERC-20 token is fairly simple, registering an ERC-20 token as a Cosmos coin requires more attention and effort. The ERC-20 standard is an interface that defines a set of method signatures (name, arguments and output) without defining its methods' internal logic. Therefore it is possible for developers to deploy contracts that contain hidden malicious behaviour within those methods. For instance, the ERC20 `transfer` method, which is responsible for sending an `amount` of tokens to a given `recipient` could include code to siphon some amount of tokens intended for the recipient into a different predefined account, which is owned by the malicious contract deployer.

As EVMOS allows any arbitrary ERC-20 contract to be registered through governance, it is essential that the proposer and the voters manually verify during voting phase that the proposed contract uses the default ERC20.sol implementation. EVMOS recommends voters to follow this review process:

- Contract solidity code should be verified and accessable (e.g. using an explorer).
- Contract should be audited by a reputable auditor.
- Inherited contracts need to be verified for correctness.

The more complex the ERC-20 contract is, the more effort is required for voters to review and eventually approve the proposal. Our ERC-20 token is fairly complex as it implements the logic described in the SHA and AOA. Even if this logic is used only for contributors and investors' addresses (or KYC'd addresses), it still need to be reviewed. Moreover our token implements an upgradeable proxy, making it susceptible to arbitrary code changes.

How can we simplify our token implementation to have a smoother registration process?

We propose to deploy a new, minimal ERC-20 token contract called `WrappedTelediskoToken (WTT)` (the name is not finalized yet) that wraps `TelediskoToken (TT)`. If the proposal is accepted, then:

- Only KYC'd addresses can hold `TT`.
- Contributors (KYC) earn `TT` by contributing to the DAO.
- Investors (KYC) get `TT` by investing capital in the DAO.
- `TT` holders can transfer their tokens to `WTT` to wrap them.
- `WTT` can transfer their tokens to `TT` to unwrap them.
- (Not sure this is useful, the more I think about this the less I'm convinced it's a good idea) The `TT` total supply is always equal to `WTT` total supply.

## 3 Specification

<!-- The technical specification should describe the syntax and semantics of
any new feature. The specification must address the exact issues described in
the solution breakdown and should describe how it addresses them. The
specification should be detailed enough to allow competing, interoperable
implementations. It MAY describe the impact on data models, API endpoints,
security, performance, end users, deployment, documentation, and testing.-->

## 4 Rationale

<!-- The rationale fleshes out the specification by describing what motivated
the design and why particular design decisions were made. It should describe
alternate designs that were considered and related work, e.g. how the feature
is supported in other languages. The rationale may also provide evidence of
consensus within the community, and should discuss important objections or
concerns raised during discussion.-->

## 5 Implementation

<!--The implementations must be completed before any TIP is given status
"stable", but it need not be completed before the TIP is accepted. While there
is merit to the approach of reaching consensus on the TIP and rationale before
writing code, the principle of "rough consensus and running code" is still
useful when it comes to resolving many discussions of API details.-->

## 6 Copyright

<!--All TIPs MUST be released to the public domain.-->

Copyright and related rights waived via
[CC0](https://creativecommons.org/publicdomain/zero/1.0/)


[erc20]: https://github.com/evmos/evmos/tree/1ff151a527551126ac126824bddd7c71bc45ceb1/x/erc20/spec
[registerproposal]: https://github.com/evmos/evmos/blob/1ff151a527551126ac126824bddd7c71bc45ceb1/x/erc20/spec/04_transactions.md#registererc20proposal
[maliciouscontracts]: https://github.com/evmos/evmos/blob/1ff151a527551126ac126824bddd7c71bc45ceb1/x/erc20/spec/01_concepts.md#malicious-contracts