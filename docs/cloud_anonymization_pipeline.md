# Cloud-Based DICOM Anonymization Pipeline

A cloud-based anonymization pipeline receives DICOM studies from healthcare partners, removes or masks all patient identifiable information, and delivers compliant artifacts for downstream analytics. The following sections describe a reference design that can be adapted to HIPAA, GDPR, or other regional privacy requirements.

## Architectural Overview

1. **Secure Ingestion Layer**
   - Supports DICOMweb `STOW-RS`, VPN file drops, or secure upload portals.
   - Performs checksum validation and schema inspection as soon as a study arrives.
   - Stores inbound objects in an isolated quarantine bucket (e.g., Amazon S3 with bucket policies or Azure Blob Storage with SAS tokens).
   - Emits queue messages (SQS, Pub/Sub, or Event Grid) so downstream services can process studies asynchronously.

2. **Metadata De-identification Service**
   - Applies DICOM PS3.15 Appendix E or locally customised rule sets.
   - Removes or pseudonymises fields such as `PatientName`, `PatientID`, `AccessionNumber`, `PatientBirthDate`, and institutional identifiers.
   - Generates synthetic identifiers (GUIDs or salted hashes) and optionally maintains a re-identification key vault when legally permitted.
   - Supports date shifting with deterministic offsets to preserve clinical timelines while protecting privacy.

3. **Pixel Sanitisation Module**
   - Detects burned-in text using OCR and computer-vision models tailored for radiology modalities.
   - Applies masking, inpainting, or overpainting for detected regions.
   - Stores detection masks to enable audit and to improve model retraining.

4. **Validation and Audit Trail**
   - Runs automated validation against unit tests derived from the DICOM standard.
   - Emits compliance reports (JSON/CSV/PDF) summarising which tags were altered, removed, or retained with justification.
   - Maintains append-only audit logs (e.g., CloudTrail, Azure Monitor) and optional mapping tables in encrypted databases for authorised re-identification workflows.

5. **Distribution and Storage**
   - Writes anonymised objects to dedicated cloud storage (S3, Azure Blob, Google Cloud Storage) with lifecycle policies.
   - Exposes APIs or event-driven notifications for downstream consumers such as research data lakes, PACS viewers, or AI training pipelines.
   - Integrates with data catalogues and IAM policies to control access by project, dataset, or user role.

## Typical End-to-End Workflow

1. **Upload**: Healthcare facilities push DICOM studies using secure transport. The pipeline stages the studies in a quarantine bucket and records metadata in an ingestion queue.
2. **De-identification**: Worker nodes pull studies from the queue, apply tag-removal and pseudonymisation rules, and log every transformation for compliance.
3. **Pixel Anonymisation**: Images pass through OCR/ML services that mask burned-in identifiers. Manual review workflows can be triggered if confidence thresholds are not met.
4. **Validation & Audit**: The pipeline validates the resulting DICOM objects, produces compliance certificates, and updates mapping tables when permitted.
5. **Output**: Clean DICOM files are stored in secure cloud storage and made accessible through APIs, message queues, or direct download links for approved consumers.

## Security and Compliance Considerations

- Enforce end-to-end encryption (TLS in transit, AES-256 at rest) and use customer-managed keys for regulated environments.
- Implement fine-grained IAM policies and multi-factor authentication for administrative users.
- Maintain monitoring and alerting to detect anomalous access patterns.
- Periodically review de-identification rules to align with updated regulations and institutional policies.
- Provide disaster recovery by replicating anonymised datasets across regions.

## Extensibility

- Modularise the metadata and pixel processing stages so that new modality-specific rules or OCR models can be introduced without downtime.
- Offer configuration-as-code (YAML/JSON) for rule sets, making it easier to version control compliance policies.
- Integrate with data science platforms to trigger downstream jobs (model training, federated learning) once anonymised datasets are available.

## Deliverables

- A reproducible workflow that ingests, de-identifies, validates, and distributes DICOM studies.
- Compliance artefacts and audit logs required for HIPAA, GDPR, or local regulations.
- Secure storage endpoints and APIs for downstream research, AI development, and multi-site collaborations.

## Building the First Layer: Secure Ingestion

The ingestion layer is the security and reliability anchor for the remainder of the pipeline. A minimal cloud-native implementation can be assembled with the following building blocks:

1. **Network Entry Points**
   - Deploy a DICOMweb gateway (e.g., Orthanc with the DICOMweb plugin or a managed PACS router) behind an HTTPS load balancer.
   - Terminate TLS with certificates issued by a private CA, and enforce mutual TLS or signed URLs when collaborating with external sites.
   - Provide a fallback secure file transfer method (SFTP/Aspera) when legacy modalities cannot push over DICOMweb.

2. **Landing Zone Storage**
   - Create a dedicated object store bucket or container with bucket policies that only allow writes from the gateway service account.
   - Enable object-lock or immutable retention windows to prevent tampering with inbound artefacts.
   - Configure server-side encryption with customer-managed keys and enforce TLS-only access policies.

3. **Integrity and Schema Validation**
   - Attach a serverless function or lightweight microservice that is invoked on every object creation event.
   - Validate DICOM metadata using libraries such as `pydicom`, checking transfer syntax, modality type, and mandatory tags.
   - Generate checksum manifests (MD5/SHA-256) and compare them with hashes provided by the sender when available.

4. **Event Propagation**
   - Publish a message to a durable queue (Amazon SQS, Google Pub/Sub, Azure Service Bus) containing the object location and minimal routing metadata (study UID, modality, facility ID).
   - Use dead-letter queues for malformed studies so operators can triage without blocking the happy-path flow.

5. **Operational Guardrails**
   - Instrument the gateway and validation services with structured logging, metrics, and distributed tracing.
   - Configure alerting on failed uploads, repeated schema violations, or ingestion rate anomalies.
   - Record partner-specific metadata (facility, contract ID, data use agreement) in a configuration database to drive policy-aware processing downstream.

By standing up this first layer, the pipeline achieves secure hand-off from the external producers to the internal anonymisation services. Downstream de-identification and pixel-sanitisation components can safely consume studies from the queue knowing that every object has been validated, logged, and stored with the necessary compliance controls in place.
