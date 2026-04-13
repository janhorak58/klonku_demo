from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request as urllib_request

from flask import current_app, session


class ApiError(Exception):
    def __init__(self, status_code: int, payload: dict[str, Any] | None = None):
        self.status_code = status_code
        self.payload = payload or {}
        super().__init__(self.payload.get("error") or f"API request failed with {status_code}")


@dataclass
class ApiResponse:
    status_code: int
    payload: dict[str, Any] | None


class BackendApi:
    def __init__(self) -> None:
        self.base_url = current_app.config["BACKEND_URL"].rstrip("/")
        self.test_client = current_app.config.get("BACKEND_TEST_CLIENT")

    def _headers(self, auth: bool, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if extra:
            headers.update(extra)
        if auth and session.get("access_token"):
            headers["Authorization"] = f"Bearer {session['access_token']}"
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        auth: bool = True,
        json_body: dict[str, Any] | None = None,
    ) -> ApiResponse:
        if self.test_client is not None:
            response = self.test_client.open(path, method=method, json=json_body, headers=self._headers(auth, {"Content-Type": "application/json"}))
            payload = response.get_json(silent=True)
            if response.status_code >= 400:
                raise ApiError(response.status_code, payload)
            return ApiResponse(response.status_code, payload)

        headers = self._headers(auth)
        data = None
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib_request.Request(f"{self.base_url}{path}", method=method, headers=headers, data=data)
        try:
            with urllib_request.urlopen(req) as response:
                raw = response.read().decode("utf-8")
                payload = json.loads(raw) if raw else None
                return ApiResponse(response.status, payload)
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            payload = json.loads(raw) if raw else None
            raise ApiError(exc.code, payload) from exc

    def get(self, path: str, *, auth: bool = True) -> dict[str, Any] | None:
        return self.request("GET", path, auth=auth).payload

    def post(self, path: str, *, auth: bool = True, json_body: dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self.request("POST", path, auth=auth, json_body=json_body).payload

    def put(self, path: str, *, auth: bool = True, json_body: dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self.request("PUT", path, auth=auth, json_body=json_body).payload

    def patch(self, path: str, *, auth: bool = True, json_body: dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self.request("PATCH", path, auth=auth, json_body=json_body).payload

    def delete(self, path: str, *, auth: bool = True) -> None:
        self.request("DELETE", path, auth=auth)


def backend_api() -> BackendApi:
    return BackendApi()
