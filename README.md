> **Lifecycle: successful conceptual prototype archive, superseded (owner disposition, November 14, 2026).** This repository completed its exploratory purpose of specifying a proposed deterministic ladder-logic workflow and documenting its intended boundary with BEAN/Axiom. It is preserved as a historical design idea, not an active product-delivery backlog. **No ladder editor, interpreter, PLC interface, executable simulation or tested controller was implemented in this repository.** Future implementation, if desired, belongs in a newly scoped successor initiative rather than being assumed complete here. GitHub's repository-level Archived flag is separate from this documented lifecycle status.

# EZ-Ladder

**Ladder logic made approachable, testable, and reusable.**

EZ-Ladder is an early-stage, standalone project exploring a visual ladder-logic editor and deterministic execution engine. The goal is to make control logic easy to *see*, easy to *test*, and easy to *explain*, without turning a language model into a real-time controller.

**Status: design foundation only (November 1, 2026).** No ladder engine, editor, PLC hardware interface, or production-certified controller has been implemented or tested here yet.

## The idea

- **Draw or describe the logic.** Contacts, branches, coils, timers, counters, and interlocks should be understandable in one view.
- **Execute deterministically.** A defined scan evaluates inputs against a versioned program and returns traceable outputs. Identical inputs and state must produce identical results.
- **See what happened.** A live preview should illuminate the current path through each rung; a compact execution receipt should record inputs, decisions, outputs, and failures without a chatbot narrating every step.
- **Use language as an interface, not a control loop.** A local model such as Qwen could *propose* ladder logic from natural language, describe a rung, or help locate a fault. The deterministic engine validates and executes the approved logic.
- **Recognize familiar patterns.** The optional BEAN connection may compare abstract patterns across software modules: “Where have I seen this combination of conditions, constraints, and outcomes before?” It must cite actual records instead of inventing similarities.

## Project boundaries

**EZ-Ladder owns** the ladder program format, validator, interpreter/simulator, visualization, and test fixtures.

**BEAN Core owns** cognition, durable evidence, abstractions, and cross-module reasoning. EZ-Ladder may emit versioned, privacy-safe execution receipts for BEAN or other consumers, but does not require BEAN or duplicate its memory system.

**Axiom** may eventually use the same logic representation for observable process dependencies and workflow gates. That is a possible adapter, not a claimed current integration.

Industrial PLC compatibility and export are **future research** requiring vendor-specific validation. EZ-Ladder is not a safety PLC, failsafe control system, or authorized means of driving real machinery. Emergency stops and personnel-protection functions must remain with independently engineered, safety-rated systems.

## First useful demonstration

A **fictional conveyor permissive**: an operator request and two readiness conditions must be true before a *simulated* output turns on. Show the rung highlight, change one input, show the output change, and save a compact receipt. All example signals are invented; no real employer or shop data.

## Where the work starts

- [Architecture and event contract](docs/ARCHITECTURE.md)
- [Incremental development roadmap](docs/ROADMAP.md)
- [Synthetic sample program](examples/conveyor_permissive.json)

**Design rule:** one source of truth for each ladder program; many ways to view, inspect, and propose changes to it. No invented live connections, no unnecessary chatbot interface, and no duplicated BEAN Core.
