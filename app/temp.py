# requirements.txt
# fastapi==0.104.1
# uvicorn==0.23.2
# opentelemetry-api==1.20.0
# opentelemetry-sdk==1.20.0
# opentelemetry-instrumentation-fastapi==0.41b0
# opentelemetry-exporter-otlp-proto-http==1.20.0
# opentelemetry-instrumentation-logging==0.41b0
# requests>=2.0.0

import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Dict, List
import uvicorn
import time
import random

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Set up basic console logging with a simpler format initially
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="FastAPI Dynatrace Demo")


def setup_telemetry():
    # Set resource attributes for service identity
    resource = Resource.create({
        "service.name": "fastapi-demo-service",
        "service.version": "1.0.0",
        "deployment.environment": "development"
    })

    # Configure the OTLP exporter
    # Replace with your Dynatrace environment ID
    dynatrace_endpoint = "https://fmd14971.live.dynatrace.com/api/v2/otlp"

    # Add API token header
    headers = {
        "Authorization": "Api-Token dt0c01.UCVAHNVEJYOUDGT4Y2DH6V4P.HWKYO2ZKOKINATR4HHCGKFYGO6ZO7YXXDPYHVYFBP4TLKSFMXXYWKCPQCEO6KWGB"
    }

    # Log configuration details (without sensitive info)
    logger.info(f"Initializing OpenTelemetry with endpoint: {dynatrace_endpoint}")

    # 1. Set up traces
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=f"{dynatrace_endpoint}/v1/traces",
        headers=headers
    )
    span_processor = BatchSpanProcessor(otlp_trace_exporter)
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)

    # 2. Set up metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint=f"{dynatrace_endpoint}/v1/metrics",
            headers=headers
        )
    )
    metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(metrics_provider)

    # 3. Set up logs using logging instrumentation only
    # The LoggingInstrumentor will add trace context to standard logs
    LoggingInstrumentor().instrument(set_logging_format=True)

    # Create a custom formatter that includes the trace context
    class TraceContextFormatter(logging.Formatter):
        def format(self, record):
            # Add trace context to the log message itself
            trace_id = getattr(record, "otelTraceID", "0")
            span_id = getattr(record, "otelSpanID", "0")
            trace_flags = getattr(record, "otelTraceFlags", "0")

            # Ensure we have the basic message formatted
            formatted_message = super().format(record)

            # For Dynatrace, add special metadata as JSON
            dynatrace_metadata = {
                "trace.id": trace_id if trace_id != "0" else None,
                "span.id": span_id if span_id != "0" else None,
                "severity": record.levelname,
                "service.name": "fastapi-demo-service"
            }

            # Only include non-None values
            dynatrace_metadata = {k: v for k, v in dynatrace_metadata.items() if v is not None}

            # Add Dynatrace-compatible format
            if trace_id != "0":
                import json
                return f"{formatted_message} | dt.trace.data={json.dumps(dynatrace_metadata)}"
            else:
                return formatted_message

    # Set up a handler that will push logs to Dynatrace via HTTP
    class DynatraceLogHandler(logging.Handler):
        def __init__(self, endpoint, api_token):
            super().__init__()
            self.endpoint = endpoint
            self.headers = {
                "Authorization": f"Api-Token {api_token}",
                "Content-Type": "application/json"
            }
            self.formatter = TraceContextFormatter("%(asctime)s [%(levelname)s] %(message)s")

        def emit(self, record):
            try:
                import requests
                import json
                from datetime import datetime
                import time

                # Format the log message with trace context
                log_entry = self.formatter.format(record)

                # Create the payload for Dynatrace Logs Ingest API
                # This uses the simpler Logs Ingest API rather than OTLP

                # Create a proper ISO 8601 timestamp with Z suffix for UTC
                # Convert timestamp to UTC and format correctly for Dynatrace
                utc_time = time.gmtime(record.created)
                timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', utc_time)

                payload = {
                    "content": log_entry,
                    "status": record.levelname,
                    "timestamp": timestamp,  # Use UTC timestamp with Z suffix
                    "log.source": record.pathname,
                    "service.name": "fastapi-demo-service"
                }

                # Add trace context if available
                trace_id = getattr(record, "otelTraceID", "0")
                if trace_id != "0":
                    payload["trace.id"] = trace_id

                span_id = getattr(record, "otelSpanID", "0")
                if span_id != "0":
                    payload["span.id"] = span_id

                # Try to add any extra attributes
                if hasattr(record, "args") and isinstance(record.args, dict):
                    for key, value in record.args.items():
                        payload[key] = value

                # Send to Dynatrace Logs Ingest API (not OTLP)
                logs_ingest_endpoint = f"https://fmd14971.live.dynatrace.com/api/v2/logs/ingest"
                response = requests.post(
                    logs_ingest_endpoint,
                    headers=self.headers,
                    data=json.dumps([payload])  # API accepts an array of log entries
                )

                if response.status_code >= 400:
                    print(f"Failed to send log to Dynatrace: {response.status_code} {response.text}")

            except Exception as e:
                # Don't let logging exceptions stop the application
                print(f"Error sending log to Dynatrace: {str(e)}")

    # Get API token from headers (remove the "Api-Token " prefix)
    api_token = headers["Authorization"].replace("Api-Token ", "")

    # Add our custom Dynatrace log handler to the root logger
    root_logger = logging.getLogger()
    dynatrace_handler = DynatraceLogHandler(dynatrace_endpoint, api_token)
    dynatrace_handler.setLevel(logging.INFO)
    root_logger.addHandler(dynatrace_handler)

    # Update console handler formatter for better trace visibility
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, DynatraceLogHandler):
            handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s"
            ))

    # Get tracer and meter
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)

    # Create metrics
    request_counter = meter.create_counter(
        name="app.request.count",
        description="Counts the number of requests"
    )

    logger.info("OpenTelemetry initialization complete with log forwarding enabled")

    return tracer, request_counter


# Set up telemetry
tracer, request_counter = setup_telemetry()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)


# Middleware to log requests and manage spans
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = random.randint(1000, 9999)
    start_time = time.time()

    # Start a new span for this request
    with tracer.start_as_current_span("http_request", attributes={
        "http.method": request.method,
        "http.url": str(request.url),
        "request.id": str(request_id)
    }) as span:
        # Log the request - this log will include trace context
        logger.info(f"Request {request_id}: {request.method} {request.url}")

        # Increment request counter
        request_counter.add(1, {"http.method": request.method, "http.path": request.url.path})

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log the response - this log will include trace context
            logger.info(f"Response {request_id}: Status {response.status_code}, Duration: {duration:.4f}s")

            # Add response information to span
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("response.duration_seconds", duration)

            return response
        except Exception as e:
            # Log the error - this log will include trace context
            logger.error(f"Error processing request {request_id}: {str(e)}")

            # Record error in span
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))

            raise


# Sample endpoints
@app.get("/", response_model=Dict)
async def root():
    with tracer.start_as_current_span("calculate_response") as span:
        # This log is automatically associated with the current span
        logger.info("Processing root endpoint request")
        span.set_attribute("processing.type", "simple")

        time.sleep(0.1)
        return {"message": "Hello from FastAPI with Dynatrace integration!"}


@app.get("/items/{item_id}", response_model=Dict)
async def get_item(item_id: int):
    with tracer.start_as_current_span("get_item") as span:
        span.set_attribute("item.id", item_id)
        logger.info(f"Getting item with ID: {item_id}")

        time.sleep(0.2)

        if random.random() < 0.1:  # 10% chance of failure
            error_msg = f"Could not find item with ID: {item_id}"
            logger.error(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)

        return {"item_id": item_id, "name": f"Test Item {item_id}", "price": 10.99 * item_id}


@app.get("/slow", response_model=Dict)
async def slow_endpoint():
    with tracer.start_as_current_span("slow_operation") as span:
        logger.info("Processing slow endpoint request")

        delay = random.uniform(0.5, 2.0)
        span.set_attribute("operation.delay_seconds", delay)
        logger.info(f"Operation will take {delay:.2f} seconds")
        time.sleep(delay)

        return {"message": "Slow operation completed", "delay_seconds": delay}


@app.get("/log-test", response_model=Dict)
async def log_test():
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")

    return {"message": "Logs generated at all levels"}

# Save as main.py and run with: uvicorn main:app --reload