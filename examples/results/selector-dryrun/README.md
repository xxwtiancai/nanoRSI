# Selector-study dry-run: the protocol toolchain, exercised end to end (2026-10-17)

The first instantiation of the [selector-study protocol](../../../docs/SELECTOR_STUDY_PROTOCOL.md)
— deliberately offline and deterministic: a program-mode fixture (scripted proposer always
proposes the same one-line fix; the **stock** program evaluator exact-matches) runs through
the [multi-seed orchestrator](../../multiseed/run.py) under two arms, and every workspace is
double-scored ([double_scoring](../../double_scoring/run.py)) against the control gate.

| Arm | Seeds | Decisions | Final candidate | false-blocks |
| --- | --- | --- | ---: | ---: |
| Control (strict gate) | 0/1/2 | accepted ×1 each | 1.000 (all seeds) | 0 |
| Noise-band 1.5 | 0/1/2 | rejected ×3 each | 0.000 (all seeds) | **3 per seed (9 total)** |

Reading: the +1.0 fix is blocked by the band, the parent never advances, the scripted
proposer re-proposes, and each rejection is a false block against the control — the
protocol's accounting quantifies exactly what a selector costs on a deterministic fixture.
On this fixture all seeds agree by construction; **this validates machinery and accounting,
not effect sizes**. The live three-seed × three-budget study (real panels, measured noise
band, offline double-scoring) is the protocol's next step and now has a working template.

Command: `python examples/selector_dryrun/run.py ./out --seeds 0,1,2 --band 1.5`.
Validated in `tests/test_selector_dryrun.py`; the run also exposed and fixed a real
multi-seed bug (a patched seed left the tree dirty for baseline on committed templates).
