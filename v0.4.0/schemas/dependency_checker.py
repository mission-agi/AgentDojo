#!/usr/bin/env python3
"""
TaskPilot Dependency Checker v0.4.0

[P4] Runtime dependency enforcement. Validates that all skills' `depends_on`
prerequisites have been completed (artifacts exist) before a skill is dispatched.

Integrates with the orchestration graph as a pre-execution check during
the DEPENDENCY_VALIDATION state.
"""

import yaml
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class DependencyViolation:
    """A dependency that is not satisfied."""
    skill_id: str
    depends_on: str
    violation_type: str  # "missing_skill", "missing_artifact", "circular"
    detail: str


@dataclass
class DependencyReport:
    """Full dependency validation report."""
    total_skills: int
    total_dependencies: int
    violations: List[DependencyViolation] = field(default_factory=list)
    circular_chains: List[List[str]] = field(default_factory=list)
    orphan_skills: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.violations) == 0 and len(self.circular_chains) == 0


class DependencyChecker:
    """Validates skill dependency chains before execution."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skill_catalog: Dict[str, Dict] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self._load_skills()

    def _load_skills(self):
        """Load all skill definitions and build dependency graph."""
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return

        for yaml_file in sorted(self.skills_dir.glob("*.yaml")):
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
                        skill_id = skill.get("skill_id", "")
                        if skill_id:
                            self.skill_catalog[skill_id] = skill
                            deps = skill.get("depends_on", [])
                            self.dependency_graph[skill_id] = set(deps) if deps else set()

        logger.info(f"Loaded {len(self.skill_catalog)} skills, "
                     f"{sum(len(d) for d in self.dependency_graph.values())} dependencies")

    def validate(self) -> DependencyReport:
        """Run full dependency validation."""
        report = DependencyReport(
            total_skills=len(self.skill_catalog),
            total_dependencies=sum(len(d) for d in self.dependency_graph.values()),
        )

        # Check 1: Missing dependency references
        all_skill_ids = set(self.skill_catalog.keys())
        for skill_id, deps in self.dependency_graph.items():
            for dep in deps:
                if dep not in all_skill_ids:
                    report.violations.append(DependencyViolation(
                        skill_id=skill_id,
                        depends_on=dep,
                        violation_type="missing_skill",
                        detail=f"{skill_id} depends on {dep}, but {dep} is not in the skill catalog"
                    ))

        # Check 2: Circular dependencies
        report.circular_chains = self._detect_cycles()
        for chain in report.circular_chains:
            report.violations.append(DependencyViolation(
                skill_id=chain[0],
                depends_on=chain[-1],
                violation_type="circular",
                detail=f"Circular dependency: {' → '.join(chain)}"
            ))

        # Check 3: Orphan skills (no depends_on and no one depends on them)
        dependents = set()
        for deps in self.dependency_graph.values():
            dependents.update(deps)
        for skill_id in all_skill_ids:
            if not self.dependency_graph.get(skill_id) and skill_id not in dependents:
                report.orphan_skills.append(skill_id)

        return report

    def validate_execution_order(self, execution_order: List[str]) -> List[DependencyViolation]:
        """Validate that a proposed execution order satisfies all dependencies."""
        violations = []
        completed = set()

        for skill_id in execution_order:
            deps = self.dependency_graph.get(skill_id, set())
            for dep in deps:
                if dep not in completed:
                    violations.append(DependencyViolation(
                        skill_id=skill_id,
                        depends_on=dep,
                        violation_type="missing_artifact",
                        detail=f"{skill_id} requires {dep} but it has not been executed yet"
                    ))
            completed.add(skill_id)

        return violations

    def get_execution_order(self) -> List[str]:
        """Compute a valid topological execution order."""
        visited = set()
        order = []
        visiting = set()

        def visit(node: str):
            if node in visiting:
                return  # Skip cycles (already reported)
            if node in visited:
                return
            visiting.add(node)
            for dep in self.dependency_graph.get(node, set()):
                if dep in self.skill_catalog:
                    visit(dep)
            visiting.discard(node)
            visited.add(node)
            order.append(node)

        for skill_id in sorted(self.skill_catalog.keys()):
            visit(skill_id)

        return order

    def _detect_cycles(self) -> List[List[str]]:
        """Detect circular dependency chains using DFS."""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep in self.dependency_graph.get(node, set()):
                if dep not in visited:
                    dfs(dep, path)
                elif dep in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    cycles.append(cycle)

            path.pop()
            rec_stack.discard(node)

        for skill_id in self.skill_catalog:
            if skill_id not in visited:
                dfs(skill_id, [])

        return cycles


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent
    skills_dir = base_dir / "skills"

    checker = DependencyChecker(skills_dir)
    report = checker.validate()

    print(f"\n=== Dependency Validation Report ===")
    print(f"Total skills: {report.total_skills}")
    print(f"Total dependencies: {report.total_dependencies}")
    print(f"Valid: {report.is_valid}")
    print(f"Violations: {len(report.violations)}")
    print(f"Circular chains: {len(report.circular_chains)}")
    print(f"Orphan skills: {len(report.orphan_skills)}")

    if report.violations:
        print(f"\nViolations:")
        for v in report.violations:
            print(f"  [{v.violation_type}] {v.detail}")

    if report.orphan_skills:
        print(f"\nOrphan skills (no dependencies in or out):")
        for s in report.orphan_skills:
            print(f"  - {s}")

    # Print valid execution order
    order = checker.get_execution_order()
    print(f"\nValid execution order ({len(order)} skills):")
    for i, skill_id in enumerate(order):
        deps = checker.dependency_graph.get(skill_id, set())
        dep_str = f" (depends: {', '.join(deps)})" if deps else ""
        print(f"  {i+1}. {skill_id}{dep_str}")


if __name__ == "__main__":
    main()
