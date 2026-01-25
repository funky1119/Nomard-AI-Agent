```markdown
# Interview Prep: Exactpi – Core Developer

## Job Overview
Position: Core Developer  
Location: Amsterdam or Zwolle (Hybrid; 2 days on-site/week)  
Type: 12-month Contract (strong potential for extension)  
Compensation: Up to €7.000 gross/month (40h)  
Key Responsibilities:
- Architect, build and maintain distributed Golang microservices  
- Implement encryption for data-at-rest and in-transit  
- Design and optimize CI/CD pipelines in Azure DevOps  
- Automate cloud infrastructure with Terraform  
- Collaborate in an agile, cross-functional squad, owning code reviews and best practices  

## Why This Job Is a Fit
- You thrive on **distributed systems** design: at TechSolutions you built 5+ microservices serving 10k+ users.  
- Strong **DevOps pedigree**: Docker, GitHub Actions CI/CD → ready to ramp into Azure DevOps.  
- Security focus: you’ve implemented JWT/OAuth2 encryption; Exactpi’s “Security First” culture aligns with your values.  
- Rapid learner: you’re actively expanding into Golang (currently 3+ yrs in Node/Python) and eager to take full ownership of core services.  
- Collaborative mindset: experienced in code reviews, pair programming, and Agile rituals—perfect for Exactpi’s team-oriented pods.

## Resume Highlights for This Role
1. **Golang & Distributed Systems**  
   - Currently expanding from Node/Python into production Golang microservices.  
   - Designed and shipped containerized distributed apps at TechSolutions, cutting release cycles by 50%.  
2. **Encryption & Data Security**  
   - Implemented JWT-based authentication and OAuth2 flows, ensuring robust API security.  
   - Familiar with key-rotation patterns and encryption best practices.  
3. **CI/CD & Containerization**  
   - End-to-end CI/CD pipelines built with GitHub Actions → strong foundation for Azure DevOps multi-stage pipelines.  
   - Docker multi-stage builds in production, optimizing image size and build speed.  
4. **Cloud Automation**  
   - AWS automation experience (EC2, S3, Lambda) → transferable to Terraform on Azure.  
   - Built infrastructure-as-code components and managed deployment drift.  
5. **Team & Process**  
   - Led code reviews, pair programming, sprint planning; wrote comprehensive unit/integration tests (Jest, Mocha).  
   - Agile mindset, strong communicator in English (C1), native Spanish.

## Company Summary
Exactpi is a Amsterdam-based scale-up (50–150 employees) founded in 2018. They deliver a **secure, scalable middleware** platform for financial transactions and data pipelines using:
- **Golang microservices** for high throughput and fault tolerance  
- **End-to-end encryption** (PKI, HSM integration)  
- **Cloud automation** (Terraform modules, multi-region architectures)  
- **Cutting-edge CI/CD** in Azure DevOps and Docker  

Mission: “Empower enterprises to build and run highly secure, globally distributed applications without the complexity of infrastructure.”  
Values: Security First, Developer Experience, Innovation at Speed, Collaborative Culture, Customer-Centric.

Recent Highlights:
- €15M Series A (Q4 2023)  
- Platform v2.0 with multi-region replication & built-in key management (Q1 2024)  
- Pilot with a major European bank on real-time encrypted transaction pipelines

## Predicted Interview Questions
1. **Golang & System Design**  
   - “Walk me through designing a geo-distributed queue in Go. How do you ensure exactly-once delivery and handle partitions?”  
   - “How do you profile and optimize a Go service under heavy load?”  
2. **Encryption & Security**  
   - “Explain your approach to key management and rotation. How would you integrate with Azure Key Vault or HashiCorp Vault?”  
   - “Describe mutual TLS authentication flow between services.”  
3. **CI/CD & DevOps**  
   - “Show me an Azure DevOps YAML pipeline you’ve worked on or how you’d structure multi-stage builds and deployments.”  
   - “How do you handle rollbacks and blue/green deployments in a containerized environment?”  
4. **Infrastructure as Code**  
   - “Give an example of a Terraform module you’ve authored. How did you structure inputs/outputs and manage state?”  
   - “How do you detect and remediate drift in production infrastructure?”  
5. **Behavioral & Collaboration**  
   - “Tell me about a time you disagreed in a code review. How did you resolve it?”  
   - “How do you stay up-to-date with new technologies and share knowledge within your team?”

## Questions to Ask Them
- Product & Technical Vision  
  - “What are the biggest technical hurdles you’re tackling in the next 6 months?”  
  - “How do you balance performance, security, and usability when designing new features?”  
- Team & Process  
  - “Can you outline the end-to-end sprint cycle and the role of the Core Developer in planning?”  
  - “How are code reviews and pair programming structured within the team?”  
- Infrastructure & Reliability  
  - “What monitoring and alerting stack do you use for production services? What on-call responsibilities come with the role?”  
  - “How mature are your Terraform modules, and what’s the approach to CI for infrastructure?”  
- Career & Growth  
  - “What metrics define success for this position at 6 and 12 months?”  
  - “What learning opportunities — conferences, certifications, internal workshops — does Exactpi support?”  

## Concepts To Know/Review
- Golang concurrency primitives: goroutines, channels, sync patterns  
- Designing idempotent, fault-tolerant microservices (circuit breakers, retries)  
- Encryption fundamentals: PKI, TLS mutual auth, HSM integration, key rotation  
- Azure DevOps pipelines: YAML schema, multi-stage, artifacts, approvals  
- Terraform best practices: module design, state locking, drift detection  
- Dockerfile optimizations: multi-stage, security scanning, image layering  
- CI/CD strategies: blue/green, canary, rollback tactics  
- Cloud-native observability: metrics (Prometheus), tracing (OpenTelemetry), logging

## Strategic Advice
Tone & Presence:
- **Confident & Collaborative:** Speak precisely; invite dialogue (“Does that approach align with what you’re building?”).  
- **Curious & Problem-Oriented:** Ask follow-up questions on ambiguity (e.g., “How do you currently manage secret rotations?”).  
- **Humble & Adaptable:** Acknowledge growth area in Golang but emphasize rapid learning curve and strong distributed-systems background.

Focus Areas:
- Emphasize your **system-level thinking** over individual code snippets.  
- Highlight **security mindset**: encryption, code hygiene, threat modeling.  
- Demonstrate **DevOps literacy**: show you can own end-to-end delivery, from code to production.

Red Flags to Watch For:
- Vagueness around **contract extension** path—clarify long-term vision.  
- Team size vs. workload—ask about bandwidth and support for new hires.  
- Level of on-call duties and SLAs—ensure expectations match your personal bandwidth.  
- True remote flexibility: confirm hybrid policy and office-day commitments.

Good luck—your blend of distributed-systems experience, security focus, and CI/CD expertise will position you as a standout candidate for Exactpi’s Core Developer role!