"""
AFRB.py — Asymmetric Fairness Regulation Boundary (v2)

Goal:
- Decide the appropriate stance under asymmetry without moralizing.
- Separate: (A) Fair+Legal, (B) Unfair+Legal, (C) Unfair+Legal-Greyzone, (D) Unfair+Illegal.
- Encode the “Greyzone justification” filters we discussed:
  1) Transparency / ex-ante defensibility
  2) Ultima ratio (B exhausted; continued B implies severe damage)
  3) No new blackmail surface / reversibility control

IMPORTANT:
- This module does NOT provide operational guidance on illegal acts.
- Field D is classified and blocked (always "do not proceed"), except for narrowly defined
  emergency defenses which must be assessed by qualified legal counsel.

Input model:
- Facts and constraints only (no mind-reading).
- Outputs: recommended field/strategy + reasons + risk flags.

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


# ----------------------------- Core Enums ---------------------------------


class Tri(Enum):
    YES = auto()
    PARTIAL = auto()
    NO = auto()


class CostLevel(Enum):
    LOW = auto()
    MODERATE = auto()
    HIGH = auto()


class Severity(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    EXISTENTIAL = auto()


class Field(Enum):
    A_FAIR_LEGAL = auto()
    B_UNFAIR_LEGAL = auto()
    C_UNFAIR_GREYZONE = auto()
    D_UNFAIR_ILLEGAL = auto()


class Strategy(Enum):
    # Field A/B/C produce strategies; Field D is blocked.
    COOPERATIVE_FAIRNESS = auto()
    STRATEGIC_FAIRNESS = auto()
    SELF_PROTECTIVE_UNFAIRNESS = auto()
    TARGETED_ESCALATION = auto()
    GREYZONE_CAUTION = auto()
    GREYZONE_ALLOWED = auto()
    ILLEGAL_BLOCKED = auto()


class RiskFlag(Enum):
    # Signals for auditing, not “advice”
    HARD_ASYMMETRY = auto()
    ENFORCEMENT_GAP = auto()
    SANCTION_GAP = auto()
    HIGH_SELF_COST = auto()
    SYSTEMATIC_ABUSE = auto()
    EXISTENTIAL_THREAT = auto()
    GREYZONE_FAIL_TRANSPARENCY = auto()
    GREYZONE_FAIL_ULTIMA_RATIO = auto()
    GREYZONE_FAIL_BLACKMAIL_SURFACE = auto()
    GREYZONE_FAIL_DISPROPORTIONATE = auto()
    ILLEGAL_METHOD = auto()


# ----------------------------- Context Models ------------------------------


@dataclass(frozen=True)
class GreyzoneFilters:
    """
    Filters for whether entering Field C (greyzone) is defensible as a last resort.

    transparency_test:
        Could you defend the action ex ante to a neutral third party if it becomes public,
        without relying on secrecy as the argument?

    ultima_ratio:
        Have you exhausted Field B measures AND does remaining in B foreseeably lead to
        severe/existential harm?

    no_blackmail_surface:
        Does the action avoid creating new leverage against you (blackmailability),
        and avoid irreversible reputational/legal exposure?

    proportionality:
        Is the contemplated step proportionate relative to the threatened harm,
        and not a “downward escalation” (i.e., it remains close to legality)?

    Note: These do NOT legalize anything. They only gate *greyzone classification*.
    """
    transparency_test: bool
    ultima_ratio: bool
    no_blackmail_surface: bool
    proportionality: bool


@dataclass(frozen=True)
class Context:
    """
    R (reciprocity):  other side acts rule-bound when you do?
    S (sanction):     their rule-breaking has real consequences?
    D (enforcement):  is there an effective enforcement instance?

    K (cost_to_self): cost you bear by staying fair/transparent/cooperative.

    threat_severity: expected harm if you remain in A/B (not speculative, but best estimate).
    systematic_abuse: is your fairness being instrumentally exploited?

    contemplated_method_illegal:
        True if the contemplated step would require an illegal act.
        AFRB will then classify as Field D and block.

    greyzone:
        Optional filters if you are considering a “greyzone” move.
    """
    R: Tri
    S: Tri
    D: Tri
    cost_to_self: CostLevel

    threat_severity: Severity = Severity.LOW
    systematic_abuse: bool = False

    contemplated_method_illegal: bool = False
    greyzone: Optional[GreyzoneFilters] = None


# ----------------------------- Output Model --------------------------------


@dataclass(frozen=True)
class Decision:
    field: Field
    strategy: Strategy
    reasons: List[str]
    risk_flags: List[RiskFlag]


# ----------------------------- AFRB Engine ---------------------------------


def _is_hard_asymmetry(ctx: Context) -> bool:
    return (
        ctx.R == Tri.NO
        and ctx.cost_to_self == CostLevel.HIGH
        and (ctx.S == Tri.NO or ctx.D == Tri.NO)
    )


def _severity_score(sev: Severity) -> int:
    return {
        Severity.LOW: 0,
        Severity.MEDIUM: 1,
        Severity.HIGH: 2,
        Severity.EXISTENTIAL: 3,
    }[sev]


def _greyzone_passes(filters: GreyzoneFilters) -> (bool, List[RiskFlag], List[str]):
    flags: List[RiskFlag] = []
    reasons: List[str] = []

    if not filters.transparency_test:
        flags.append(RiskFlag.GREYZONE_FAIL_TRANSPARENCY)
        reasons.append("Greyzone fails transparency/ex-ante defensibility test.")

    if not filters.ultima_ratio:
        flags.append(RiskFlag.GREYZONE_FAIL_ULTIMA_RATIO)
        reasons.append("Greyzone fails ultima-ratio condition (B not exhausted / not severe enough).")

    if not filters.no_blackmail_surface:
        flags.append(RiskFlag.GREYZONE_FAIL_BLACKMAIL_SURFACE)
        reasons.append("Greyzone creates new blackmail/attack surface (unacceptable exposure).")

    if not filters.proportionality:
        flags.append(RiskFlag.GREYZONE_FAIL_DISPROPORTIONATE)
        reasons.append("Greyzone is disproportionate relative to the harm / too close to illegal escalation.")

    ok = len(flags) == 0
    if ok:
        reasons.append("Greyzone passes all four filters (still risk-bearing, but defensibility improved).")

    return ok, flags, reasons


def decide(ctx: Context) -> Decision:
    reasons: List[str] = []
    risk_flags: List[RiskFlag] = []

    # --- Illegal methods are always blocked in this model ---
    if ctx.contemplated_method_illegal:
        risk_flags.append(RiskFlag.ILLEGAL_METHOD)
        reasons.append("Contemplated method is illegal. AFRB classifies this as Field D and blocks it.")
        reasons.append("Rationale: high personal exposure + possible evidence handling issues + risk inversion.")
        return Decision(
            field=Field.D_UNFAIR_ILLEGAL,
            strategy=Strategy.ILLEGAL_BLOCKED,
            reasons=reasons,
            risk_flags=risk_flags,
        )

    # --- Compute asymmetry / gaps ---
    hard_asym = _is_hard_asymmetry(ctx)
    if hard_asym:
        risk_flags.append(RiskFlag.HARD_ASYMMETRY)
        reasons.append("Hard asymmetry detected: R=NO, cost_to_self=HIGH, and (S=NO or D=NO).")

    if ctx.D != Tri.YES:
        risk_flags.append(RiskFlag.ENFORCEMENT_GAP)
        reasons.append("Enforcement gap: D != YES (effective rule enforcement uncertain/absent).")

    if ctx.S != Tri.YES:
        risk_flags.append(RiskFlag.SANCTION_GAP)
        reasons.append("Sanction gap: S != YES (rule-breaking consequences uncertain/absent).")

    if ctx.cost_to_self == CostLevel.HIGH:
        risk_flags.append(RiskFlag.HIGH_SELF_COST)
        reasons.append("High self-cost if staying fair/transparent/cooperative (K=HIGH).")

    if ctx.systematic_abuse:
        risk_flags.append(RiskFlag.SYSTEMATIC_ABUSE)
        reasons.append("Systematic abuse present: your fairness is being instrumentally exploited.")

    if ctx.threat_severity == Severity.EXISTENTIAL:
        risk_flags.append(RiskFlag.EXISTENTIAL_THREAT)
        reasons.append("Threat severity is existential (continuation implies severe damage).")

    # --- Field C (Greyzone) handling: only if user provides filters ---
    if ctx.greyzone is not None:
        ok, flags, greasons = _greyzone_passes(ctx.greyzone)
        risk_flags.extend(flags)
        reasons.extend(greasons)

        if ok:
            # If greyzone passes, choose Field C with caution; escalation depends on severity/asymmetry.
            reasons.append("Entering Field C is permitted by filters (not 'safe', but gated).")

            # If existential/hard asymmetry/systematic abuse => allow 'targeted escalation' within legal edge.
            if hard_asym and (_severity_score(ctx.threat_severity) >= _severity_score(Severity.HIGH) or ctx.systematic_abuse):
                reasons.append("Given hard asymmetry + high severity/abuse: recommend controlled escalation within legal edge.")
                return Decision(
                    field=Field.C_UNFAIR_GREYZONE,
                    strategy=Strategy.GREYZONE_ALLOWED,
                    reasons=reasons,
                    risk_flags=risk_flags,
                )

            return Decision(
                field=Field.C_UNFAIR_GREYZONE,
                strategy=Strategy.GREYZONE_CAUTION,
                reasons=reasons,
                risk_flags=risk_flags,
            )

        # Greyzone fails => fall back to Field B (unfair + legal)
        reasons.append("Greyzone entry rejected by filters; fall back to Field B (unfair but legal self-protection).")
        return Decision(
            field=Field.B_UNFAIR_LEGAL,
            strategy=Strategy.SELF_PROTECTIVE_UNFAIRNESS,
            reasons=reasons,
            risk_flags=risk_flags,
        )

    # --- Default routing across A/B using reciprocity, enforceability, and cost ---
    # Field A: cooperative fairness only when reciprocity exists and costs are not high and at least one backstop exists.
    if ctx.R == Tri.YES and ctx.cost_to_self != CostLevel.HIGH and (ctx.S == Tri.YES or ctx.D == Tri.YES):
        reasons.append("Conditions for Field A met: reciprocity YES, costs manageable, and sanction/enforcement exists.")
        return Decision(
            field=Field.A_FAIR_LEGAL,
            strategy=Strategy.COOPERATIVE_FAIRNESS,
            reasons=reasons,
            risk_flags=risk_flags,
        )

    # Field B: strategic or self-protective unfairness when reciprocity is partial/absent or costs/gaps exist.
    if ctx.R in (Tri.YES, Tri.PARTIAL) and ctx.cost_to_self != CostLevel.HIGH:
        reasons.append("Partial/limited reciprocity or missing backstops => Field B (strategic fairness).")
        return Decision(
            field=Field.B_UNFAIR_LEGAL,
            strategy=Strategy.STRATEGIC_FAIRNESS,
            reasons=reasons,
            risk_flags=risk_flags,
        )

    # If hard asymmetry + high severity or abuse, recommend escalation (still legal).
    if hard_asym and (_severity_score(ctx.threat_severity) >= _severity_score(Severity.HIGH) or ctx.systematic_abuse):
        reasons.append("Hard asymmetry + high severity/abuse => Field B with targeted escalation (still legal).")
        return Decision(
            field=Field.B_UNFAIR_LEGAL,
            strategy=Strategy.TARGETED_ESCALATION,
            reasons=reasons,
            risk_flags=risk_flags,
        )

    # Otherwise: self-protective unfairness (legal).
    reasons.append("Default: Field B self-protective unfairness (legal boundary; minimize exposure).")
    return Decision(
        field=Field.B_UNFAIR_LEGAL,
        strategy=Strategy.SELF_PROTECTIVE_UNFAIRNESS,
        reasons=reasons,
        risk_flags=risk_flags,
    )


# ----------------------------- Example Usage -------------------------------

if __name__ == "__main__":
    # Example 1: cooperative environment
    ctx1 = Context(R=Tri.YES, S=Tri.YES, D=Tri.YES, cost_to_self=CostLevel.LOW)
    print(decide(ctx1))

    # Example 2: hard asymmetry, high cost, missing enforcement -> self-protective + escalation (legal)
    ctx2 = Context(
        R=Tri.NO, S=Tri.NO, D=Tri.NO, cost_to_self=CostLevel.HIGH,
        threat_severity=Severity.HIGH, systematic_abuse=True
    )
    print(decide(ctx2))

    # Example 3: considering greyzone, passes filters
    ctx3 = Context(
        R=Tri.NO, S=Tri.NO, D=Tri.PARTIAL, cost_to_self=CostLevel.HIGH,
        threat_severity=Severity.EXISTENTIAL,
        greyzone=GreyzoneFilters(
            transparency_test=True,
            ultima_ratio=True,
            no_blackmail_surface=True,
            proportionality=True,
        )
    )
    print(decide(ctx3))

    # Example 4: illegal method contemplated -> blocked
    ctx4 = Context(
        R=Tri.NO, S=Tri.NO, D=Tri.NO, cost_to_self=CostLevel.HIGH,
        contemplated_method_illegal=True
    )
    print(decide(ctx4))
