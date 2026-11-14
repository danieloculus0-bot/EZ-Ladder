"""Deterministic, simulation-only ladder Boolean scan interpreter."""
import json
from pathlib import Path

class ProgramError(ValueError):
    pass

def validate(program):
    if not isinstance(program, dict) or program.get("version") != 1:
        raise ProgramError("expected version 1 program")
    rungs = program.get("rungs")
    if not isinstance(rungs, list) or not rungs:
        raise ProgramError("nonempty rungs required")
    outputs = set()
    for rung in rungs:
        if not isinstance(rung, dict) or set(rung) != {"coil", "expr"}:
            raise ProgramError("rung requires coil and expr")
        coil = rung["coil"]
        if not isinstance(coil, str) or not coil.isidentifier() or coil in outputs:
            raise ProgramError("invalid or duplicate coil")
        outputs.add(coil)
        _validate_expr(rung["expr"])
    return outputs

def _validate_expr(expr):
    if not isinstance(expr, dict) or len(expr) != 1:
        raise ProgramError("expression must have one operator")
    op, value = next(iter(expr.items()))
    if op == "contact":
        if not isinstance(value, str) or not value.isidentifier():
            raise ProgramError("invalid contact")
    elif op == "not":
        _validate_expr(value)
    elif op in ("all", "any"):
        if not isinstance(value, list) or not value:
            raise ProgramError("nonempty operands required")
        for item in value:
            _validate_expr(item)
    else:
        raise ProgramError("unsupported operator: " + str(op))

def _eval(expr, inputs):
    op, value = next(iter(expr.items()))
    if op == "contact":
        if value not in inputs:
            raise ProgramError("missing input: " + value)
        if type(inputs[value]) is not bool:
            raise ProgramError("nonboolean input: " + value)
        return inputs[value]
    if op == "not":
        return not _eval(value, inputs)
    # Evaluate every branch to validate all contacts, even after short-circuit.
    results = [_eval(item, inputs) for item in value]
    return all(results) if op == "all" else any(results)

def scan(program, inputs):
    outputs = validate(program)
    if not isinstance(inputs, dict) or outputs.intersection(inputs):
        raise ProgramError("inputs must not shadow output coils")
    decisions = []
    for index, rung in enumerate(program["rungs"]):
        energized = _eval(rung["expr"], inputs)
        decisions.append({"rung": index, "coil": rung["coil"], "energized": energized})
    return {"version": 1, "inputs": dict(sorted(inputs.items())),
            "outputs": {r["coil"]: r["energized"] for r in decisions},
            "trace": decisions}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Offline ladder scan simulator")
    parser.add_argument("program", type=Path)
    parser.add_argument("inputs", help='JSON object of boolean input values')
    args = parser.parse_args()
    print(json.dumps(scan(json.loads(args.program.read_text()), json.loads(args.inputs)), sort_keys=True))

if __name__ == "__main__":
    main()
