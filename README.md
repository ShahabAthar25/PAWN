# PAWN

A small, experimental programming language for quantitative analysis and interpreter-driven computation.

PAWN is a work-in-progress language project built in Python with a lexer, parser, AST, and runtime interpreter. The goal is to explore how a compact expression language can support arithmetic, variables, conditionals, loops, and eventual domain-oriented tooling for data and numeric workflows.

## Why PAWN?

PAWN is designed as a learning-first and research-first language project:

- Lightweight and interpreter-based
- Built around a clear tokenizer/parser pipeline
- Focused on numeric computation and expression evaluation
- Designed to grow toward domain-specific analytical workflows
- Easy to extend with new language features and runtime semantics

## Current capabilities

PAWN currently includes the foundations of a custom language runtime:

- Lexical analysis with regex-based tokenization
- Parsing of arithmetic and comparison expressions
- Variable assignment and mutation
- Boolean logic (`and`, `or`, `not`)
- Conditional branching
- While loops and iteration primitives
- Runtime error reporting with source-aware diagnostics

## Example

```text
>>> let a = 5
>>> a / 5
1

>>> (5 + 3) * (2 - 1)
8

>>> 2 ^ 3 % 7
1
```

## Project structure

```text
PAWN/
├── main.py
├── pawn.grammar
├── pyproject.toml
├── src/
│   └── pawn/
│       ├── __init__.py
│       ├── context.py
│       ├── interpreter.py
│       ├── nodes.py
│       ├── parserPawn.py
│       ├── lexer/
│       │   ├── __init__.py
│       │   ├── lexer.py
│       │   ├── position.py
│       │   └── tokens.py
│       ├── errors/
│       │   ├── error.py
│       │   ├── runtime.py
│       │   ├── string_with_arrows.py
│       │   └── syntax.py
│       ├── error_handlers/
│       │   ├── RTResult.py
│       │   ├── parseResult.py
│       │   └── __init__.py
│       ├── data_types/
│       │   ├── __init__.py
│       │   └── number.py
│       ├── symbol_table/
│       │   ├── __init__.py
│       │   ├── setGlobalSymbolTable.py
│       │   └── symbolTable.py
│       └── main.py
├── .python-version
├── .gitignore
├── uv.lock
└── README.md
```

## Architecture

PAWN follows a conventional interpreter pipeline:

1. Lexer scans source text into tokens
2. Parser transforms tokens into an AST
3. Interpreter evaluates the AST in a runtime context
4. Symbol table tracks variables and scope
5. Error handlers produce contextual runtime and syntax diagnostics

This architecture keeps the implementation easy to understand and extend while exposing a clean path for future language features.

## Getting started

### Prerequisites

- Python 3.12+
- Optional: `uv` for dependency and project management

### Clone the repository

```bash
git clone https://github.com/ShahabAthar25/PAWN.git
cd PAWN
```

### Run the REPL

```bash
python src/pawn/main.py
```

You should then see a PAWN prompt similar to:

```text
PAWN 0.0.1 (main, ALPHA) ...
Type 'help()' for help
>>> 
```

### Example usage

```text
>>> let a = 10
>>> let b = 3
>>> a + b * 2
16
```

## Language design goals

The project is intentionally designed as a compact, numerically expressive language with a roadmap toward quantitative and analytical workloads.

Planned directions include:

- richer data types
- function definitions
- structured control flow
- standard library utilities for math and statistics
- better tooling and diagnostics
- optional transpilation or code generation

## Roadmap

### Near-term

- stabilize parser semantics
- improve expression and loop correctness
- expand runtime vocabulary
- add richer examples and tests

### Medium-term

- introduce functions and user-defined abstractions
- build a standard library for numeric tasks
- improve error messages and REPL usability

### Long-term

- add a more formal grammar and execution model
- support domain-specific quantitative workflows
- explore performance and optimization techniques

## Contributing

Contributions are welcome.

If you want to help build PAWN:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Open a pull request with a clear description

Suggested areas for contribution:

- parser fixes
- runtime improvements
- new language constructs
- tests and examples
- documentation and language design notes

## Status

PAWN is currently in an early alpha stage. The project is actively evolving and should be treated as a research and educational interpreter rather than a production-ready language runtime.

## License

This repository does not currently declare an explicit license. If you plan to use or extend the project commercially or publicly, it is recommended to confirm licensing status before distribution or publication.

## Acknowledgements

This project is a hands-on exploration of language implementation concepts, inspired by classic interpreter design patterns and the challenges of building a custom numeric language from the ground up.
