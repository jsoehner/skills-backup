---
name: backtesting-frameworks
description: Build robust backtesting systems for trading strategies with proper handling of look-ahead bias, survivorship bias, and transaction costs. Use when developing trading algorithms, validating strategies, or building backtesting infrastructure.
---

# Backtesting Frameworks

Build robust, production-grade backtesting systems that avoid common pitfalls and produce reliable strategy performance estimates.

## Use this skill when

- Developing trading strategy backtests
- Building backtesting infrastructure
- Validating strategy performance and robustness
- Avoiding common backtesting biases
- Implementing walk-forward analysis

## Do not use this skill when

- You need live trading execution or investment advice
- Historical data quality is unknown or incomplete
- The task is only a quick performance summary

## Instructions

- Define hypothesis, universe, timeframe, and evaluation criteria.
- Build point-in-time data pipelines and realistic cost models.
- Implement event-driven simulation and execution logic.
- Use train/validation/test splits and walk-forward testing.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Safety

- Do not present backtests as guarantees of future performance.
- Avoid providing financial or investment advice.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER compute indicators using data from the future (look-ahead bias).
- NEVER present backtest results without deducting transaction costs, slippage, and fees.

## Knowledge Capture Requirement
When completing a task that involves a significant architectural decision, a complex bug fix, or a new infrastructure pattern, you MUST:
1. Synthesize the decision/fix into a concise summary (3-5 sentences).
2. Classify it as either **OKF** (High-level policy, architectural rule, or cross-cutting standard) or **CHROMA** (Technical context, implementation detail, or specific bug fix).
3. Execute `capture_knowledge.py` with the appropriate `--type` flag.
4. Ensure the captured knowledge is deduplicated and properly chunked using the `smart_chunk` logic.
