from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings


@dataclass(frozen=True)
class ProjectBClient:
    base_url: str
    username: str
    password: str

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_access_token(self) -> str:
        resp = requests.post(
            self._url("/api/auth/token/"),
            json={"username": self.username, "password": self.password},
            timeout=10,
        )
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()
        return data["access"]

    def create_conversation(
        self,
        *,
        access_token: str,
        external_ref: int,
        patient_external_id: int,
        doctor_external_id: int,
    ) -> dict[str, Any]:
        resp = requests.post(
            self._url("/api/telemed/conversations/"),
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "external_ref": external_ref,
                "patient_external_id": patient_external_id,
                "doctor_external_id": doctor_external_id,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


def get_projectb_client() -> ProjectBClient:
    return ProjectBClient(
        base_url=settings.PROJECTB_BASE_URL,
        username=settings.PROJECTB_SERVICE_USERNAME,
        password=settings.PROJECTB_SERVICE_PASSWORD,
    )