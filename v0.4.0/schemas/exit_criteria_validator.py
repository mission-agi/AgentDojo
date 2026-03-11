#!/usr/bin/env python3
"""
TaskPilot Exit Criteria Validator v0.4.0

[BUG-006 FIX] Validates that all skill exit criteria are binary, measurable,
and verifiable. Rejects vague criteria at registration time.

Rules:
1. Each criterion must contain a measurable assertion verb
2. Each criterion must not contain vague/ambiguous words
3. Each criterion must be expressible as binary pass/fail
"""

import yaml
import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple, Set
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CriterionVerdict(str, Enum):
    VALID = "valid"
    VAGUE = "vague"
    NO_ASSERTION = "no_assertion"
    MISSING = "missing"


# Verbs/patterns that indicate a measurable, binary assertion
MEASURABLE_PATTERNS = [
    r'\b(zero|no|none)\b',  # Negation as assertion ("Zero X", "No Y")
    r'\b(all|every|each|100%)\b',
    r'\b(at least|minimum|>=|≥)\b',
    r'\b(covers?|includes?|contains?|addresses?)\b',
    r'\b(exists?|present|available|produced|documented|defined|listed)\b',
    r'\b(verified|validated|confirmed|tested|checked|audited|reviewed)\b',
    r'\b(passes?|compiles?|succeeds?|builds?|runs?)\b',
    r'\b(accepted|approved|signed.off|sign.off)\b',
    r'\b(categorized|classified|prioritized|tagged|mapped|traced)\b',
    r'\b(<=|<|>=|>|==|≤|≥)\b',
    r'\b(\d+%|\d+\s*(or more|or fewer|minimum|maximum))\b',
    r'\b(per.module|per.feature|per.endpoint|per.stage)\b',
    r'\b(step.by.step|end.to.end)\b',
    r'\b(indexed|searchable|formatted)\b',
    r'\b(completed|established|calculated|measured|profiling|executed)\b',
    r'\b(identified|assessed|proposed|provided|updated|recorded)\b',
    r'\b(configured|building|parameterized|uploaded)\b',
    r'\b(consistent|compliant|explicit)\b',
]

# Words that indicate vague, non-binary criteria
VAGUE_PATTERNS = [
    r'\b(sufficient|adequate|appropriate|reasonable|good)\b',
    r'\b(quality bar|meets? quality|high quality|acceptable)\b',
    r'\b(should consider|might want|could improve)\b',
    r'\b(as needed|where possible|if applicable|when feasible)\b',
    r'\b(try to|attempt to|aim for)\b',
    r'\b(various|several|some|many|multiple)\b(?!.*\b(at least|minimum|>=)\b)',
]

# Compiled patterns
MEASURABLE_RE = [re.compile(p, re.IGNORECASE) for p in MEASURABLE_PATTERNS]
VAGUE_RE = [re.compile(p, re.IGNORECASE) for p in VAGUE_PATTERNS]


@dataclass
class CriterionValidation:
    """Validation result for a single exit criterion."""
    criterion_text: str
    verdict: CriterionVerdict
    has_measurable_verb: bool
    has_vague_words: bool
    matched_measurable: List[str] = field(default_factory=list)
    matched_vague: List[str] = field(default_factory=list)
    suggestion: str = ""


@dataclass
class SkillValidation:
    """Validation result for all exit criteria of a skill."""
    skill_id: str
    role: str
    total_criteria: int
    valid_count: int
    vague_count: int
    no_assertion_count: int
    missing_count: int
    criteria_validations: List[CriterionValidation] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.vague_count == 0 and self.no_assertion_count == 0 and self.missing_count == 0


def validate_criterion(text) -> CriterionValidation:
    """Validate a single exit criterion for binary, measurable assertion."""
    # Handle YAML parsing dicts from "Key: value" strings
    if isinstance(text, dict):
        text = " ".join(f"{k}: {v}" for k, v in text.items())
    text = str(text).strip()
    if not text:
        return CriterionValidation(
            criterion_text=text,
            verdict=CriterionVerdict.MISSING,
            has_measurable_verb=False,
            has_vague_words=False,
            suggestion="Criterion is empty"
        )

    # Check for measurable patterns
    matched_measurable = []
    for pattern in MEASURABLE_RE:
        match = pattern.search(text)
        if match:
            matched_measurable.append(match.group())

    # Check for vague patterns
    matched_vague = []
    for pattern in VAGUE_RE:
        match = pattern.search(text)
        if match:
            matched_vague.append(match.group())

    has_measurable = len(matched_measurable) > 0
    has_vague = len(matched_vague) > 0

    if has_vague:
        verdict = CriterionVerdict.VAGUE
        suggestion = f"Remove vague words ({', '.join(matched_vague)}). Replace with specific measurable conditions."
    elif not has_measurable:
        verdict = CriterionVerdict.NO_ASSERTION
        suggestion = "Add a measurable assertion (e.g., 'All X documented', 'Zero Y remaining', '>= N%')."
    else:
        verdict = CriterionVerdict.VALID
        suggestion = ""

    return CriterionValidation(
        criterion_text=text,
        verdict=verdict,
        has_measurable_verb=has_measurable,
        has_vague_words=has_vague,
        matched_measurable=matched_measurable,
        matched_vague=matched_vague,
        suggestion=suggestion,
    )


def validate_skill(skill: Dict) -> SkillValidation:
    """Validate all exit criteria for a single skill."""
    skill_id = skill.get("skill_id", "UNKNOWN")
    role = skill.get("role", "UNKNOWN")
    exit_criteria = skill.get("exit_criteria", [])

    if not exit_criteria:
        return SkillValidation(
            skill_id=skill_id, role=role,
            total_criteria=0, valid_count=0, vague_count=0,
            no_assertion_count=0, missing_count=1,
            criteria_validations=[CriterionValidation(
                criterion_text="", verdict=CriterionVerdict.MISSING,
                has_measurable_verb=False, has_vague_words=False,
                suggestion="Skill has no exit criteria defined"
            )]
        )

    validations = [validate_criterion(c) for c in exit_criteria]

    return SkillValidation(
        skill_id=skill_id,
        role=role,
        total_criteria=len(exit_criteria),
        valid_count=sum(1 for v in validations if v.verdict == CriterionVerdict.VALID),
        vague_count=sum(1 for v in validations if v.verdict == CriterionVerdict.VAGUE),
        no_assertion_count=sum(1 for v in validations if v.verdict == CriterionVerdict.NO_ASSERTION),
        missing_count=sum(1 for v in validations if v.verdict == CriterionVerdict.MISSING),
        criteria_validations=validations,
    )


def validate_all_skills(skills_dir: Path) -> Tuple[List[SkillValidation], float]:
    """Validate all skills in a directory. Returns validations and pass rate."""
    all_validations = []

    for yaml_file in sorted(skills_dir.glob("*.yaml")):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        skill_lists = []
        if isinstance(data, dict):
            if "skills" in data:
                skill_lists.append(data["skills"])
            for key in ["security_skills", "release_skills", "documentation_skills"]:
                if key in data:
                    skill_lists.append(data[key])

        for skills in skill_lists:
            if isinstance(skills, list):
                for skill in skills:
                    validation = validate_skill(skill)
                    all_validations.append(validation)

    total = len(all_validations)
    valid = sum(1 for v in all_validations if v.is_valid)
    pass_rate = valid / total if total > 0 else 0.0

    return all_validations, pass_rate


def print_report(validations: List[SkillValidation], pass_rate: float):
    """Print a validation report."""
    print(f"\n=== Exit Criteria Validation Report ===")
    print(f"Total skills: {len(validations)}")
    print(f"Valid: {sum(1 for v in validations if v.is_valid)}")
    print(f"Invalid: {sum(1 for v in validations if not v.is_valid)}")
    print(f"Pass rate: {pass_rate:.2%}")
    print()

    for v in validations:
        if not v.is_valid:
            print(f"  FAIL: {v.skill_id} ({v.role})")
            for cv in v.criteria_validations:
                if cv.verdict != CriterionVerdict.VALID:
                    print(f"    [{cv.verdict.value}] {cv.criterion_text[:80]}...")
                    if cv.suggestion:
                        print(f"      Suggestion: {cv.suggestion}")
            print()


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent
    skills_dir = base_dir / "skills"

    if not skills_dir.exists():
        logger.error(f"Skills directory not found: {skills_dir}")
        return

    validations, pass_rate = validate_all_skills(skills_dir)
    print_report(validations, pass_rate)


if __name__ == "__main__":
    main()
