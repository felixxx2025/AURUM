"""Service layer exposing high level operations for the copilot feature."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from adapters.repo_client import RepoClient, RepoClientError
from adapters.ci_client import CIClient, CIClientError


class CopilotService:
    """High level operations for creating blueprints and managing PRs."""

    def __init__(self, repo_client: RepoClient, ci_client: CIClient) -> None:
        self.repo_client = repo_client
        self.ci_client = ci_client
        self.template_dir = Path("templates/starters")

    def create_blueprint(
        self,
        template_name: str,
        output_path: str | Path,
        context: Optional[Dict[str, Any]] = None,
    ) -> Path:
        """Generate a blueprint file from a starter template.

        Parameters
        ----------
        template_name:
            Name of the template file located in ``templates/starters`` without
            the extension.
        output_path:
            Destination path where the generated file will be written.
        context:
            Optional mapping used to render the template.
        """
        if not template_name:
            raise ValueError("template_name is required")

        template_file = self.template_dir / f"{template_name}.py.tpl"
        if not template_file.exists():
            raise FileNotFoundError(f"Template '{template_file}' not found")

        output = Path(output_path)
        try:
            raw = template_file.read_text()
            rendered = raw.format(**(context or {}))
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered)
        except OSError as exc:
            raise RuntimeError(f"Failed to generate blueprint: {exc}") from exc

        return output

    def open_pr(self, branch: str, title: str, body: str) -> str:
        """Open a pull request using the repository client."""
        if not branch or not title:
            raise ValueError("branch and title are required")
        try:
            return self.repo_client.open_pull_request(branch, title, body)
        except RepoClientError as exc:
            raise RuntimeError(f"Failed to open pull request: {exc}") from exc

    def apply_changes(self, patch_content: str) -> None:
        """Apply a patch to the repository using the repository client."""
        if not patch_content:
            raise ValueError("patch_content is required")
        try:
            self.repo_client.apply_patch(patch_content)
        except RepoClientError as exc:
            raise RuntimeError(f"Failed to apply changes: {exc}") from exc

    def status(self, pr_id: str) -> str:
        """Return the CI status for the given pull request."""
        if not pr_id:
            raise ValueError("pr_id is required")
        try:
            return self.ci_client.get_status(pr_id)
        except CIClientError as exc:
            raise RuntimeError(f"Failed to obtain status: {exc}") from exc
