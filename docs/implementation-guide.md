# Implementation Guide

## 1. Define approved AI tools
Assign an owner to each service and document which data classifications it may process.

## 2. Define simple data classes
Start with a small vocabulary such as `public`, `internal`, `customer`, and `confidential`. Align it with your existing information-classification standard.

## 3. Put a check before AI access
Run tool approval, sensitive-data scanning, classification policy, and human-review rules before a request crosses the AI-provider boundary.

## 4. Keep humans in high-impact workflows
Require explicit approval for sensitive data and actions such as send, delete, publish, financial changes, or permission changes.

## 5. Log minimally and improve
Capture enough metadata to investigate policy decisions without creating a second sensitive-data store. Review false positives/negatives and update policy/tests.
