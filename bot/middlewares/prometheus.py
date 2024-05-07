from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Coroutine

import prometheus_client
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_middlewares import middleware

if TYPE_CHECKING:
    from aiohttp.web_request import Request
    from aiohttp.web_response import Response

METRICS_PREFIX = "tgbot"


def prometheus_middleware_factory(
    metrics_prefix: str = METRICS_PREFIX, registry: prometheus_client.CollectorRegistry | None = None
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Coroutine[Any, Any, Response]]:
    used_registry = registry or prometheus_client.REGISTRY

    requests_metrics = prometheus_client.Counter(
        name=f"{metrics_prefix}_requests",
        documentation="Total requests by method, scheme, remote and path template.",
        labelnames=["method", "scheme", "remote", "path_template"],
        registry=used_registry,
    )

    responses_metrics = prometheus_client.Counter(
        name=f"{metrics_prefix}_responses",
        documentation="Total responses by method, scheme, remote, path template and status code.",
        labelnames=["method", "scheme", "remote", "path_template", "status_code"],
        registry=used_registry,
    )

    requests_processing_time_metrics = prometheus_client.Histogram(
        name=f"{metrics_prefix}_request_duration",
        documentation="Histogram of requests processing time by method, "
        "scheme, remote, path template and status code (in seconds)",
        labelnames=["method", "scheme", "remote", "path_template", "status_code"],
        unit="seconds",
        registry=used_registry,
    )

    requests_in_progress_metrics = prometheus_client.Gauge(
        name=f"{metrics_prefix}_requests_in_progress",
        documentation="Gauge of requests by method, scheme, remote and path template currently being processed.",
        labelnames=["method", "scheme", "remote", "path_template"],
        registry=used_registry,
    )

    exceptions_metrics = prometheus_client.Counter(
        name=f"{metrics_prefix}_exceptions",
        documentation="Total exceptions raised by path, scheme, remote, path template and exception type.",
        labelnames=["method", "scheme", "remote", "path_template", "exception_type"],
        registry=used_registry,
    )

    @middleware
    async def prometheus_middleware(request: Request, handler: Callable[[Request], Awaitable[Response]]) -> Response:
        loop = asyncio.get_running_loop() or asyncio.get_event_loop()

        try:
            path_template = request.match_info.route.resource.canonical
        except AttributeError:
            path_template = "__not_matched__"

        requests_metrics.labels(
            method=request.method,
            scheme=request.scheme,
            remote=request.remote,
            path_template=path_template,
        ).inc()
        requests_in_progress_metrics.labels(
            method=request.method,
            scheme=request.scheme,
            remote=request.remote,
            path_template=path_template,
        ).inc()

        request_start_time = loop.time()
        try:
            response = await handler(request)
            request_end_time = loop.time()

        except Exception as e:  # noqa: BLE001
            request_end_time = loop.time()
            status = e.status if isinstance(e, HTTPException) else 500

            responses_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
                status_code=status,
            ).inc()
            exceptions_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
                exception_type=type(e).__name__,
            ).inc()
            requests_processing_time_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
                status_code=status,
            ).observe(request_end_time - request_start_time)
            raise e from None
        else:
            responses_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
                status_code=response.status,
            ).inc()
            requests_processing_time_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
                status_code=response.status,
            ).observe(request_end_time - request_start_time)
        finally:
            requests_in_progress_metrics.labels(
                method=request.method,
                scheme=request.scheme,
                remote=request.remote,
                path_template=path_template,
            ).dec()
        return response

    return prometheus_middleware
