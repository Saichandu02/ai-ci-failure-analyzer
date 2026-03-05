"""Failure patterns for CI log analysis."""

from __future__ import annotations

import re

from ai_ci_analyzer.models import FailureCategory

FAILURE_PATTERNS: list[dict] = [
    {
        "pattern": re.compile(r"ModuleNotFoundError: No module named", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "Python module not found",
        "suggested_fix": "Run `pip install <package>` or add the package to requirements.txt",
    },
    {
        "pattern": re.compile(r"No module named '([^']+)'", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "Missing Python module",
        "suggested_fix": "Install the missing module with pip or add it to your requirements file",
    },
    {
        "pattern": re.compile(r"Could not find a version that satisfies the requirement", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "pip could not find a matching package version",
        "suggested_fix": "Check the package name and version constraints in requirements.txt",
    },
    {
        "pattern": re.compile(r"pip\._internal", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "pip internal error",
        "suggested_fix": "Upgrade pip with `pip install --upgrade pip` and retry",
    },
    {
        "pattern": re.compile(r"ERROR: pip's dependency resolver", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "pip dependency resolution conflict",
        "suggested_fix": "Resolve conflicting package versions in requirements.txt",
    },
    {
        "pattern": re.compile(r"npm (ERR!|error)", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "npm install error",
        "suggested_fix": "Check package.json for dependency issues and run `npm install` locally",
    },
    {
        "pattern": re.compile(r"npm WARN", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "npm install warning",
        "suggested_fix": "Review npm warnings and update package.json accordingly",
    },
    {
        "pattern": re.compile(r"Cannot find module '([^']+)'", re.IGNORECASE),
        "category": FailureCategory.DEPENDENCY,
        "description": "Node.js module not found",
        "suggested_fix": "Run `npm install` or add the missing module to package.json",
    },
    {
        "pattern": re.compile(r"FAILED .+ - ", re.IGNORECASE),
        "category": FailureCategory.TEST,
        "description": "pytest test failure",
        "suggested_fix": "Review failing test output and fix the underlying code or test",
    },
    {
        "pattern": re.compile(r"AssertionError", re.IGNORECASE),
        "category": FailureCategory.TEST,
        "description": "Test assertion failed",
        "suggested_fix": "Check the assertion logic in the failing test",
    },
    {
        "pattern": re.compile(r"pytest.*error", re.IGNORECASE),
        "category": FailureCategory.TEST,
        "description": "pytest error",
        "suggested_fix": "Review pytest output for error details",
    },
    {
        "pattern": re.compile(r"^\s*(E\s+assert|E\s+AssertionError)", re.MULTILINE),
        "category": FailureCategory.TEST,
        "description": "pytest assertion output",
        "suggested_fix": "Fix the failing assertion in the test",
    },
    {
        "pattern": re.compile(r"tests? (failed|error)", re.IGNORECASE),
        "category": FailureCategory.TEST,
        "description": "Test suite failure",
        "suggested_fix": "Review test output and fix failing tests",
    },
    {
        "pattern": re.compile(r"SyntaxError:", re.IGNORECASE),
        "category": FailureCategory.SYNTAX,
        "description": "Python syntax error",
        "suggested_fix": "Fix the syntax error in the indicated file and line number",
    },
    {
        "pattern": re.compile(r"IndentationError:", re.IGNORECASE),
        "category": FailureCategory.SYNTAX,
        "description": "Python indentation error",
        "suggested_fix": "Fix the indentation in the indicated file",
    },
    {
        "pattern": re.compile(r"unexpected (token|EOF|indent)", re.IGNORECASE),
        "category": FailureCategory.SYNTAX,
        "description": "Unexpected token or structure in code",
        "suggested_fix": "Check and fix the syntax at the indicated location",
    },
    {
        "pattern": re.compile(r"timed? out", re.IGNORECASE),
        "category": FailureCategory.TIMEOUT,
        "description": "Operation timed out",
        "suggested_fix": "Increase timeout limits or optimize the slow operation",
    },
    {
        "pattern": re.compile(r"ETIMEDOUT", re.IGNORECASE),
        "category": FailureCategory.TIMEOUT,
        "description": "Network connection timed out",
        "suggested_fix": "Check network connectivity or increase timeout settings",
    },
    {
        "pattern": re.compile(r"deadline exceeded", re.IGNORECASE),
        "category": FailureCategory.TIMEOUT,
        "description": "Deadline exceeded",
        "suggested_fix": "Increase job timeout in CI configuration",
    },
    {
        "pattern": re.compile(r"##\[error\].*timeout", re.IGNORECASE),
        "category": FailureCategory.TIMEOUT,
        "description": "GitHub Actions job timeout",
        "suggested_fix": "Increase `timeout-minutes` in the workflow YAML",
    },
    {
        "pattern": re.compile(r"Connection refused", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "Network connection refused",
        "suggested_fix": "Ensure the target service is running and accessible",
    },
    {
        "pattern": re.compile(r"Network unreachable", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "Network is unreachable",
        "suggested_fix": "Check network configuration and connectivity in CI environment",
    },
    {
        "pattern": re.compile(r"Name or service not known", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "DNS resolution failed",
        "suggested_fix": "Verify the hostname is correct and DNS is configured properly",
    },
    {
        "pattern": re.compile(r"ECONNREFUSED", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "Connection refused (Node.js/npm)",
        "suggested_fix": "Check that the target server is running and the port is correct",
    },
    {
        "pattern": re.compile(r"curl:.+failed", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "curl command failed",
        "suggested_fix": "Check the URL and network connectivity",
    },
    {
        "pattern": re.compile(r"SSL.*error", re.IGNORECASE),
        "category": FailureCategory.NETWORK,
        "description": "SSL/TLS error",
        "suggested_fix": "Check SSL certificates and TLS configuration",
    },
    {
        "pattern": re.compile(r"Permission denied", re.IGNORECASE),
        "category": FailureCategory.PERMISSION,
        "description": "File or directory permission denied",
        "suggested_fix": "Check file permissions and ensure the CI user has appropriate access",
    },
    {
        "pattern": re.compile(r"EACCES", re.IGNORECASE),
        "category": FailureCategory.PERMISSION,
        "description": "EACCES permission error (Node.js)",
        "suggested_fix": "Fix file permissions or run with appropriate privileges",
    },
    {
        "pattern": re.compile(r"Access denied", re.IGNORECASE),
        "category": FailureCategory.PERMISSION,
        "description": "Access denied",
        "suggested_fix": "Check IAM roles, credentials, or file permissions",
    },
    {
        "pattern": re.compile(r"docker build (failed|error)", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "Docker build failed",
        "suggested_fix": "Review the Dockerfile and the build context for errors",
    },
    {
        "pattern": re.compile(r"Dockerfile.*error", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "Dockerfile error",
        "suggested_fix": "Fix the error in the Dockerfile",
    },
    {
        "pattern": re.compile(r"error building image", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "Container image build error",
        "suggested_fix": "Check Dockerfile instructions and base image availability",
    },
    {
        "pattern": re.compile(r"make.*error", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "Make build error",
        "suggested_fix": "Review Makefile and build output for the specific error",
    },
    {
        "pattern": re.compile(r"yaml.*error|invalid yaml", re.IGNORECASE),
        "category": FailureCategory.CONFIGURATION,
        "description": "YAML syntax or structure error",
        "suggested_fix": "Validate the YAML file using a linter or online validator",
    },
    {
        "pattern": re.compile(r"mapping values are not allowed", re.IGNORECASE),
        "category": FailureCategory.CONFIGURATION,
        "description": "YAML mapping error",
        "suggested_fix": "Fix the indentation or key-value structure in the YAML file",
    },
    {
        "pattern": re.compile(r"environment variable.+not set", re.IGNORECASE),
        "category": FailureCategory.CONFIGURATION,
        "description": "Required environment variable not set",
        "suggested_fix": "Set the required environment variable in CI secrets or environment settings",
    },
    {
        "pattern": re.compile(r"KeyError: '[A-Z_]+'", re.IGNORECASE),
        "category": FailureCategory.CONFIGURATION,
        "description": "Missing environment variable (KeyError)",
        "suggested_fix": "Set the missing environment variable in CI configuration or secrets",
    },
    {
        "pattern": re.compile(r"MemoryError", re.IGNORECASE),
        "category": FailureCategory.RESOURCE,
        "description": "Python MemoryError",
        "suggested_fix": "Reduce memory usage or increase runner memory allocation",
    },
    {
        "pattern": re.compile(r"Out of memory", re.IGNORECASE),
        "category": FailureCategory.RESOURCE,
        "description": "Out of memory error",
        "suggested_fix": "Use a larger CI runner or optimize memory usage",
    },
    {
        "pattern": re.compile(r"Killed\s*$", re.MULTILINE),
        "category": FailureCategory.RESOURCE,
        "description": "Process killed (likely OOM)",
        "suggested_fix": "Increase runner memory or optimize resource-intensive operations",
    },
    {
        "pattern": re.compile(r"no space left on device", re.IGNORECASE),
        "category": FailureCategory.RESOURCE,
        "description": "Disk space exhausted",
        "suggested_fix": "Free disk space or use a runner with more storage",
    },
    {
        "pattern": re.compile(r"##\[error\]", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "GitHub Actions error annotation",
        "suggested_fix": "Review the GitHub Actions step that produced this error",
    },
    {
        "pattern": re.compile(r"Process completed with exit code [1-9]", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "GitHub Actions step exited with non-zero code",
        "suggested_fix": "Check the step output for the root cause of the non-zero exit",
    },
    {
        "pattern": re.compile(r"Error: The process .+ failed with exit code", re.IGNORECASE),
        "category": FailureCategory.BUILD,
        "description": "GitHub Actions process failure",
        "suggested_fix": "Review the failing step logs for details",
    },
]
