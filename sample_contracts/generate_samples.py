"""Generate sample Word contracts for demo purposes."""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


def create_sample_nda():
    doc = Document()
    doc.add_heading("NON-DISCLOSURE AGREEMENT", 0).alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        "This Non-Disclosure Agreement (\"Agreement\") is entered into as of January 15, 2025, "
        "between Atos SE, a corporation organized under the laws of France, with its principal "
        "place of business at 80 Quai Voltaire, 95870 Bezons, France (\"Disclosing Party\"), "
        "and TechVenture GmbH, a corporation organized under the laws of Germany, located at "
        "Hauptstraße 12, 10115 Berlin, Germany (\"Receiving Party\")."
    )

    doc.add_heading("1. Definition of Confidential Information", level=1)
    doc.add_paragraph(
        "\"Confidential Information\" means any and all technical and non-technical information "
        "disclosed by Disclosing Party to Receiving Party, including but not limited to: "
        "trade secrets, inventions, ideas, processes, formulas, source code, data, programs, "
        "business plans, customer lists, financial information, and any other proprietary information."
    )
    doc.add_paragraph(
        "Confidential Information does NOT include information that: (a) is or becomes publicly "
        "available through no fault of Receiving Party; (b) was rightfully known to Receiving "
        "Party prior to disclosure; (c) is independently developed by Receiving Party without "
        "use of Confidential Information."
    )

    doc.add_heading("2. Obligations of Receiving Party", level=1)
    doc.add_paragraph(
        "Receiving Party agrees to: (a) hold Confidential Information in strict confidence; "
        "(b) not disclose Confidential Information to any third party without prior written "
        "consent; (c) use Confidential Information solely for evaluating a potential business "
        "relationship between the parties; (d) limit access to those employees with a need to know."
    )

    doc.add_heading("3. Term", level=1)
    doc.add_paragraph(
        "This Agreement shall commence on the Effective Date and continue for a period of two (2) "
        "years. Obligations of confidentiality shall survive termination of this Agreement for "
        "a period of one (1) year."
    )

    doc.add_heading("4. Return of Information", level=1)
    doc.add_paragraph(
        "Upon written request by Disclosing Party, Receiving Party shall promptly return or "
        "destroy all Confidential Information and certify such destruction in writing."
    )

    doc.add_heading("5. No License", level=1)
    doc.add_paragraph(
        "Nothing in this Agreement grants Receiving Party any rights in or to Confidential "
        "Information except as expressly set forth herein."
    )

    doc.add_heading("6. Governing Law", level=1)
    doc.add_paragraph(
        "This Agreement shall be governed by and construed in accordance with the laws of France, "
        "without regard to its conflict of law provisions."
    )

    doc.add_heading("7. Signatures", level=1)
    doc.add_paragraph("IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.")
    doc.add_paragraph("\nAtos SE\nBy: ___________________________\nName:\nTitle:\nDate:")
    doc.add_paragraph("\nTechVenture GmbH\nBy: ___________________________\nName:\nTitle:\nDate:")

    path = os.path.join(os.path.dirname(__file__), "sample_nda.docx")
    doc.save(path)
    print(f"Created: {path}")


def create_sample_sow():
    doc = Document()
    doc.add_heading("STATEMENT OF WORK", 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading("Cloud Migration Services — Project Aurora", level=2).alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        "This Statement of Work (\"SOW\") is entered into as of March 1, 2025, between "
        "Atos IT Solutions and Services, Inc. (\"Service Provider\") and RetailCorp SA "
        "(\"Client\"), and is incorporated into the Master Services Agreement dated February 1, 2025."
    )

    doc.add_heading("1. Project Scope", level=1)
    doc.add_paragraph(
        "Service Provider shall deliver cloud migration services for Client's legacy ERP system "
        "to Microsoft Azure. The scope includes: infrastructure assessment, migration planning, "
        "data migration, testing, and go-live support. Out of scope: end-user training, "
        "post-migration support beyond 30 days, and third-party license procurement."
    )

    doc.add_heading("2. Deliverables", level=1)
    deliverables = [
        "D1 — Infrastructure Assessment Report (due: April 15, 2025)",
        "D2 — Migration Plan and Architecture Design (due: May 1, 2025)",
        "D3 — Migrated Environment (dev/staging) (due: June 30, 2025)",
        "D4 — Production Migration and Go-Live (due: August 15, 2025)",
        "D5 — Post-Migration Validation Report (due: September 15, 2025)",
    ]
    for d in deliverables:
        doc.add_paragraph(d, style="List Bullet")

    doc.add_heading("3. Payment Terms", level=1)
    doc.add_paragraph(
        "Total contract value: EUR 450,000. Payment schedule: 20% upon SOW signature, "
        "20% upon delivery of D2, 30% upon delivery of D3, 30% upon delivery of D5. "
        "Invoices payable within 45 days of receipt."
    )

    doc.add_heading("4. Roles and Responsibilities", level=1)
    doc.add_paragraph(
        "Service Provider: Project Manager (J. Martin), Lead Cloud Architect (S. Kumar), "
        "2x Migration Engineers. Client: IT Project Sponsor, IT Infrastructure Lead, "
        "ERP System Owner."
    )

    doc.add_heading("5. Governing Law", level=1)
    doc.add_paragraph(
        "This SOW shall be governed by the laws of France. Disputes shall be resolved by "
        "the Commercial Court of Paris."
    )

    path = os.path.join(os.path.dirname(__file__), "sample_sow.docx")
    doc.save(path)
    print(f"Created: {path}")


def create_mclinic_sow_1():
    """SOW 1: M Clinic Predictive Readmission Model — well-structured, follows Atos standards."""
    doc = Document()
    doc.add_heading("STATEMENT OF WORK", 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading("Predictive Patient Readmission Model — Project PRISM", level=2).alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        "This Statement of Work (\"SOW\") is entered into as of February 3, 2025, between "
        "Atos IT Solutions and Services, S.A.U. (\"Service Provider\") and M Clinic, S.A., "
        "a healthcare institution organized under the laws of Spain, with its principal place "
        "of business at Carrer del Rosselló 76, 08029 Barcelona, Spain (\"Client\"), and is "
        "incorporated into the Master Services Agreement (\"MSA\") dated January 10, 2025 "
        "(MSA Reference: MSA-MCLINIC-2025-001)."
    )

    doc.add_heading("1. Project Scope", level=1)
    doc.add_paragraph(
        "Service Provider shall design, develop, validate, and deploy a machine learning model "
        "to predict 30-day hospital readmission risk for patients discharged from Client's "
        "cardiology and internal medicine units. The model will be trained on anonymised "
        "electronic health record (EHR) data provided by Client and integrated into Client's "
        "existing clinical decision support platform (Cerner Millennium)."
    )
    doc.add_paragraph("The following are explicitly OUT OF SCOPE:")
    out_of_scope = [
        "Procurement or licensing of third-party data sources",
        "Modifications to the Cerner Millennium platform beyond agreed API integration points",
        "Clinical validation studies or regulatory submissions (CE marking, FDA clearance)",
        "End-user training beyond two (2) train-the-trainer sessions",
        "Ongoing model maintenance after the warranty period defined in Section 8",
    ]
    for item in out_of_scope:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("2. Deliverables and Acceptance Criteria", level=1)
    doc.add_paragraph(
        "Each deliverable below is subject to formal written acceptance by Client within "
        "ten (10) business days of delivery. Acceptance shall not be unreasonably withheld. "
        "If Client does not respond within ten (10) business days, the deliverable shall be "
        "deemed accepted."
    )
    deliverables = [
        ("D1", "Data Assessment and Feasibility Report", "March 14, 2025",
         "Report documents data quality findings, feature candidates, and a confirmed feasibility recommendation."),
        ("D2", "Model Architecture and Development Plan", "April 4, 2025",
         "Document specifies model approach, validation strategy, KPIs, and updated project timeline."),
        ("D3", "Baseline Model (v1.0) with Performance Report", "June 6, 2025",
         "Model achieves minimum AUC-ROC ≥ 0.78 on held-out test set. Performance report provided."),
        ("D4", "Integrated Model in Staging Environment", "July 18, 2025",
         "End-to-end integration tested in Client's staging environment with sign-off from Client IT Lead."),
        ("D5", "Production Deployment and Go-Live", "September 5, 2025",
         "Model live in production. Monitoring dashboard active. Go-live report signed by both parties."),
        ("D6", "Post-Deployment Validation Report (90-day)", "December 5, 2025",
         "Report demonstrates sustained AUC-ROC ≥ 0.75 over 90 days of production operation."),
    ]
    for code, name, due, criteria in deliverables:
        doc.add_paragraph(f"{code} — {name} (Due: {due})", style="List Bullet")
        p = doc.add_paragraph(f"Acceptance criteria: {criteria}")
        p.paragraph_format.left_indent = Pt(36)

    doc.add_heading("3. Payment Terms", level=1)
    doc.add_paragraph(
        "Total contract value: EUR 320,000 (excluding VAT). Payment schedule linked to deliverable acceptance:"
    )
    payments = [
        "15% (EUR 48,000) — upon SOW execution",
        "15% (EUR 48,000) — upon acceptance of D2",
        "25% (EUR 80,000) — upon acceptance of D3",
        "25% (EUR 80,000) — upon acceptance of D5",
        "20% (EUR 64,000) — upon acceptance of D6",
    ]
    for p in payments:
        doc.add_paragraph(p, style="List Bullet")
    doc.add_paragraph(
        "All invoices are payable within thirty (30) calendar days of receipt. Late payments "
        "shall accrue interest at the European Central Bank base rate plus 8%, as per Directive 2011/7/EU."
    )

    doc.add_heading("4. Roles and Responsibilities", level=1)
    doc.add_paragraph("Service Provider shall provide:")
    sp_roles = [
        "Project Manager: single point of accountability for delivery and escalation",
        "Lead Data Scientist: responsible for model architecture and validation",
        "2× Senior ML Engineers: feature engineering, training pipeline, and API development",
        "Integration Engineer: Cerner Millennium API integration",
    ]
    for r in sp_roles:
        doc.add_paragraph(r, style="List Bullet")
    doc.add_paragraph("Client shall provide:")
    client_roles = [
        "Clinical Project Sponsor: executive decision-making authority",
        "Data Access Manager: responsible for EHR data extraction and anonymisation",
        "IT Integration Lead: Cerner Millennium access and environment provisioning",
        "Clinical Expert (Cardiology/Internal Medicine): domain validation of model outputs",
    ]
    for r in client_roles:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("5. Change Management", level=1)
    doc.add_paragraph(
        "Any change to scope, timeline, or budget must be submitted via a written Change Request "
        "(\"CR\") using the template in Annex A. Service Provider shall assess and respond to each "
        "CR within five (5) business days with an impact assessment covering effort, cost, and "
        "schedule. No change shall be implemented without a CR approved in writing by both parties' "
        "designated project managers."
    )

    doc.add_heading("6. Intellectual Property", level=1)
    doc.add_paragraph(
        "All intellectual property developed exclusively for this engagement and funded entirely "
        "by Client under this SOW (\"Custom IP\") shall be owned by Client upon full payment. "
        "Service Provider retains ownership of all pre-existing intellectual property, tools, "
        "frameworks, and methodologies (\"Background IP\") used in delivery. Service Provider "
        "grants Client a perpetual, non-exclusive, royalty-free licence to use Background IP "
        "solely to the extent embedded in the Custom IP deliverables."
    )

    doc.add_heading("7. Data Protection and Confidentiality", level=1)
    doc.add_paragraph(
        "All personal data processed under this SOW shall be handled in accordance with "
        "Regulation (EU) 2016/679 (GDPR). Service Provider acts as Data Processor; Client acts "
        "as Data Controller. A Data Processing Agreement (\"DPA\") is attached as Annex B and "
        "forms part of this SOW. Both parties shall maintain the confidentiality of the other "
        "party's Confidential Information for the duration of this SOW and for five (5) years thereafter."
    )

    doc.add_heading("8. Warranty", level=1)
    doc.add_paragraph(
        "Service Provider warrants that deliverables will conform to agreed acceptance criteria "
        "for a period of ninety (90) days following acceptance of D5 (\"Warranty Period\"). "
        "During the Warranty Period, Service Provider shall remedy any non-conformance at no "
        "additional cost to Client within ten (10) business days of written notification."
    )

    doc.add_heading("9. Limitation of Liability", level=1)
    doc.add_paragraph(
        "Each party's aggregate liability under this SOW shall not exceed the total fees paid "
        "or payable under this SOW in the twelve (12) months preceding the event giving rise to "
        "the claim. Neither party shall be liable for indirect, consequential, or punitive damages."
    )

    doc.add_heading("10. Termination", level=1)
    doc.add_paragraph(
        "Either party may terminate this SOW for convenience upon thirty (30) calendar days' "
        "written notice. In the event of termination for convenience by Client, Client shall pay "
        "for all work completed and accepted up to the termination date, plus reasonable "
        "wind-down costs not to exceed EUR 15,000. Either party may terminate immediately upon "
        "written notice if the other party is in material breach and fails to cure within fifteen "
        "(15) business days of written notice."
    )

    doc.add_heading("11. Force Majeure", level=1)
    doc.add_paragraph(
        "Neither party shall be liable for failure or delay in performance to the extent caused "
        "by circumstances beyond its reasonable control, including natural disasters, acts of "
        "government, pandemics, or cyberattacks. The affected party shall notify the other within "
        "five (5) business days and shall use reasonable efforts to mitigate the impact."
    )

    doc.add_heading("12. Governing Law and Dispute Resolution", level=1)
    doc.add_paragraph(
        "This SOW shall be governed by the laws of France. Any dispute shall first be referred "
        "to the parties' respective senior management for resolution within thirty (30) days. "
        "Unresolved disputes shall be submitted to binding arbitration under the ICC Rules, "
        "with the seat of arbitration in Paris, France, conducted in English."
    )

    doc.add_heading("13. Signatures", level=1)
    doc.add_paragraph("IN WITNESS WHEREOF, the parties have executed this Statement of Work as of the date first written above.")
    doc.add_paragraph("\nAtos IT Solutions and Services, S.A.U.\nBy: ___________________________\nName:\nTitle:\nDate:")
    doc.add_paragraph("\nM Clinic, S.A.\nBy: ___________________________\nName:\nTitle:\nDate:")

    path = os.path.join(os.path.dirname(__file__), "mclinic_sow_readmission.docx")
    doc.save(path)
    print(f"Created: {path}")


def create_mclinic_sow_2():
    """SOW 2: M Clinic Medical Imaging Classifier — inconsistent standards, missing clauses."""
    doc = Document()
    doc.add_heading("Statement of Work", 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading("AI-Based Radiology Image Classification System", level=2).alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        "This document constitutes a Statement of Work agreed between Atos (hereinafter \"Atos\") "
        "and M Clinic (hereinafter sometimes referred to as \"the Hospital\" or \"the institution\"). "
        "Work shall commence on or around 1st April 2025 and is related to an AI imaging project. "
        "This SOW should be read alongside any previously signed agreements between the two organisations."
    )
    # NOTE: No MSA reference, inconsistent party names, vague start date

    doc.add_heading("Scope of Work", level=1)
    # NOTE: Not numbered, different heading style than SOW 1
    doc.add_paragraph(
        "Atos will build a deep learning classifier to identify and flag anomalies in chest X-ray "
        "and CT scan images uploaded to M Clinic's radiology PACS system (GE Centricity). The "
        "solution will cover the following pathologies: pneumonia, pleural effusion, pulmonary "
        "nodules (>6mm), and cardiomegaly. The Hospital is responsible for providing labelled "
        "training data and access to the PACS environment."
    )
    doc.add_paragraph(
        "Things NOT included: we won't be doing any work on MRI images in this phase. "
        "Integration with any systems other than GE Centricity is also out of scope."
    )
    # NOTE: Informal language, incomplete out-of-scope

    doc.add_heading("Milestones and Outputs", level=1)
    # NOTE: Uses "Milestones" instead of "Deliverables", no formal acceptance criteria
    milestones = [
        "Milestone 1 — Kick-off and data review: April 2025",
        "Milestone 2 — First model prototype: June 2025",
        "Milestone 3 — Refined model after clinical feedback: August 2025",
        "Milestone 4 — System deployed to production: October 2025",
    ]
    for m in milestones:
        doc.add_paragraph(m, style="List Bullet")
    doc.add_paragraph(
        "Outputs will be reviewed and signed off by M Clinic's radiology team. Specific "
        "performance targets to be agreed during the project."
    )
    # NOTE: No concrete acceptance criteria, performance targets undefined

    doc.add_heading("Fees and Payment", level=1)
    # NOTE: Different section name ("Fees and Payment" vs "Payment Terms")
    doc.add_paragraph(
        "The total cost for this engagement is EUR 290,000 plus applicable taxes. "
        "Invoices will be issued as follows: 20% at start, 30% at Milestone 2, 50% at Milestone 4. "
        "Payment is expected within 45 days of invoice date."
    )
    # NOTE: Net 45 vs Net 30 in SOW 1, vague milestone-to-payment linkage

    doc.add_heading("Team", level=1)
    doc.add_paragraph(
        "Atos will assign a project lead and the necessary technical staff to deliver the above. "
        "M Clinic will need to make available radiology staff for feedback sessions and an IT "
        "contact for system access."
    )
    # NOTE: No named roles, no commitment to specific headcount

    doc.add_heading("Intellectual Property", level=1)
    doc.add_paragraph(
        "The model and associated code produced during this engagement will belong to Atos. "
        "M Clinic will receive a licence to use the solution for internal clinical purposes. "
        "M Clinic may not resell or sublicence the solution to third parties."
    )
    # NOTE: IP ownership is REVERSED vs SOW 1 — Atos retains ownership here
    # This is a major inconsistency that the compare tool should flag

    doc.add_heading("Data and Privacy", level=1)
    doc.add_paragraph(
        "All patient data used for training must be fully anonymised by the Hospital before "
        "being shared with Atos. Atos will handle this data securely and delete it upon project "
        "completion. Both parties agree to maintain confidentiality of project information "
        "during the project."
    )
    # NOTE: No GDPR DPA mentioned, confidentiality duration not specified (vs 5 years in SOW 1)

    doc.add_heading("Termination", level=1)
    doc.add_paragraph(
        "Either party can end this agreement by giving 15 days notice in writing. "
        "In this case, M Clinic will pay for work completed up to that point."
    )
    # NOTE: 15 days vs 30 days in SOW 1, no wind-down cost cap, informal language

    doc.add_heading("Applicable Law", level=1)
    # NOTE: Different section name ("Applicable Law" vs "Governing Law and Dispute Resolution")
    doc.add_paragraph(
        "This SOW is governed by the laws of Spain. Any disputes will be handled by the "
        "competent courts of Barcelona."
    )
    # NOTE: Spain vs France — inconsistency with Atos standard and SOW 1

    doc.add_heading("Signatures", level=1)
    doc.add_paragraph("Agreed and signed on behalf of the parties:")
    doc.add_paragraph("\nAtos\nSigned: ___________________________\nName:\nDate:")
    doc.add_paragraph("\nM Clinic\nSigned: ___________________________\nName:\nDate:")
    # NOTE: Missing titles, informal "Signed" vs "By:", no full legal entity names

    path = os.path.join(os.path.dirname(__file__), "mclinic_sow_imaging.docx")
    doc.save(path)
    print(f"Created: {path}")


if __name__ == "__main__":
    create_sample_nda()
    create_sample_sow()
    create_mclinic_sow_1()
    create_mclinic_sow_2()
    print("Sample contracts generated successfully.")
