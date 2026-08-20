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

## 6) Memory Sync

After a backtesting framework is designed, a strategy is validated, or a backtest report is generated, you **MUST** trigger the local memory capture. 

1. Save the final backtest report, strategy validation, or framework design as a Markdown file in the project directory.
2. Invoke the capture script: 
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that backtesting results, strategy validations, and framework designs are automatically routed to the correct storage (OKF or ChromaDB).

