from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
import csv

from .forms import ActionItemForm, LeadForm
from .models import ActionItem


def home(request):
    form = LeadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("thanks")

    context = {
        "form": form,
        "features": [
            {
                "tag": "IEC 62304 & SaMD",
                "title": "Agile Design Controls",
                "desc": "Synchronize user needs, software specifications, and architecture directly with Git commits, PRs, and Jira issues.",
                "points": ["Bi-directional issue sync", "Automated DHF change logging", "IEC 62304 Class A/B/C tagging"],
                "icon": "01",
            },
            {
                "tag": "ISO 14971:2019",
                "title": "Dynamic Risk Engine",
                "desc": "Maintain living FMEA tables, hazard evaluations, and mitigation controls that automatically warn you when linked requirements shift.",
                "points": ["Pre/Post mitigation risk heatmaps", "Automated residual risk scoring", "Essential performance links"],
                "icon": "02",
            },
            {
                "tag": "Verification & Validation",
                "title": "Automated V&V Pipeline",
                "desc": "Connect automated test runners (Cypress, Playwright, PyTest) and manual protocols directly to user needs with audit-locked reports.",
                "points": ["Cryptographic test run seals", "Pass/Fail gap alerting", "Regression traceability reports"],
                "icon": "03",
            },
            {
                "tag": "21 CFR Part 11",
                "title": "Document & Signature Control",
                "desc": "Execute dual-authentication electronic signatures with immutable audit trails, revision histories, and controlled watermarking.",
                "points": ["Compliant electronic signatures", "Automated periodic review loops", "Tamper-evident audit logs"],
                "icon": "04",
            },
            {
                "tag": "Instant Submission Ready",
                "title": "One-Click DHF / DMR Compiler",
                "desc": "Eliminate weeks of manual binder assembly. Export fully bookmarked, hyperlinked DHF, DMR, and EU MDR Technical Files in seconds.",
                "points": ["FDA 510(k) & PMA ready", "EU MDR 2017/745 mapping", "Automated PDF cross-referencing"],
                "icon": "05",
            },
            {
                "tag": "Continuous Quality",
                "title": "CAPA & Non-Conformance",
                "desc": "Streamline deviation capture, 5-Why root-cause investigation, corrective action delegation, and effectiveness checks.",
                "points": ["Closed-loop action routing", "Automated escalation timers", "Risk-integrated CAPA triggers"],
                "icon": "06",
            },
        ],
        "stats": [
            ("99.8%", "Audit trace coverage"),
            ("85%", "DHF assembly time reduction"),
            ("100%", "21 CFR Part 11 compliant"),
        ],
        "frameworks_list": [
            {"code": "ISO 13485:2016", "name": "Quality Management Systems", "scope": "Medical devices - Requirements for regulatory purposes"},
            {"code": "ISO 14971:2019", "name": "Risk Management", "scope": "Application of risk management to medical devices"},
            {"code": "IEC 62304:2015", "name": "Software Lifecycle", "scope": "Medical device software life-cycle processes"},
            {"code": "21 CFR Part 11", "name": "Electronic Records", "scope": "Electronic records & electronic signatures compliance"},
            {"code": "21 CFR Part 820 / QMSR", "name": "FDA Quality System", "scope": "Current FDA Quality System Regulation & transition to QMSR"},
            {"code": "EU MDR 2017/745", "name": "European Union MDR", "scope": "Class I, IIa, IIb, and III technical documentation dossiers"},
            {"code": "IEC 62366-1", "name": "Usability Engineering", "scope": "Application of usability engineering to medical devices"},
            {"code": "HIPAA & SOC 2", "name": "Security & Privacy", "scope": "Protected health data encryption and institutional trust"},
        ],
        "integrations_list": [
            {"name": "Jira Software", "role": "Sprint & Issue Tracking", "badge": "Native Bi-directional"},
            {"name": "GitHub & GitLab", "role": "Commit & Pull Request Trace", "badge": "CI/CD Webhooks"},
            {"name": "Microsoft Azure Boards", "role": "Work Item Management", "badge": "Live Sync"},
            {"name": "TestRail & Xray", "role": "Test Case Execution", "badge": "Protocol Import"},
            {"name": "SharePoint & M365", "role": "Document Archival", "badge": "Cloud Storage"},
            {"name": "Slack & MS Teams", "role": "Approval Notifications", "badge": "Instant Alerts"},
        ],
        "trace_samples": [
            {
                "need_id": "UN-102",
                "need_text": "Device shall alert clinician immediately if patient heart rate exceeds 140 BPM.",
                "req_id": "SRS-402",
                "req_text": "Tachycardia detection algorithm shall trigger audible and visual alarm within 1.5 seconds.",
                "risk_id": "HAZ-089",
                "risk_text": "Failure or delay to alert clinician leading to acute arrhythmia decompensation.",
                "mitigation": "Dual redundant polling loop + heartbeat monitor.",
                "test_id": "TC-812",
                "test_status": "Passed",
                "evidence_id": "EVD-2024-089",
                "evidence_status": "Approved & Part 11 Signed",
            },
            {
                "need_id": "UN-105",
                "need_text": "SaMD patient diagnostic data must remain cryptographically protected in transit and rest.",
                "req_id": "SRS-518",
                "req_text": "All diagnostic telemetry payload must use AES-256 GCM encryption with rotated session keys.",
                "risk_id": "HAZ-104",
                "risk_text": "Interception or tampering of clinical diagnostic stream violating HIPAA/Part 11.",
                "mitigation": "Hardware-backed secure enclave + TLS 1.3 mutual auth.",
                "test_id": "TC-945",
                "test_status": "Passed",
                "evidence_id": "EVD-2024-104",
                "evidence_status": "Approved & Part 11 Signed",
            },
            {
                "need_id": "UN-114",
                "need_text": "System shall maintain continuous operation during transient hospital power fluctuations.",
                "req_id": "SRS-607",
                "req_text": "Power management unit shall switch to secondary lithium cell within 12ms without reboot.",
                "risk_id": "HAZ-132",
                "risk_text": "Sudden device reset during critical infusion therapy resulting in dosage interruption.",
                "mitigation": "Ultracapacitor bridging circuit + persistent state journal.",
                "test_id": "TC-1042",
                "test_status": "Passed",
                "evidence_id": "EVD-2024-132",
                "evidence_status": "Approved & Part 11 Signed",
            },
        ],
        "device_classes": [
            {
                "id": "samd",
                "name": "Software as a Medical Device (SaMD)",
                "sub": "AI/ML Diagnostic, Digital Therapeutics, Remote Patient Monitoring",
                "standards": "IEC 62304 Class B/C, FDA 21 CFR 820, HIPAA, SOC 2",
                "timeline": "6-12 Weeks to Audit Readiness",
                "highlight": "Automated Git commit linking, continuous verification runs, cloud audit trails.",
            },
            {
                "id": "class2",
                "name": "Class IIa / IIb Medical Devices",
                "sub": "Infusion pumps, surgical instruments, monitoring consoles",
                "standards": "ISO 13485, ISO 14971, IEC 60601, FDA 510(k)",
                "timeline": "8-16 Weeks to Submission",
                "highlight": "Hardware/software matrix synchronization, hazard mitigation traceability.",
            },
            {
                "id": "class3",
                "name": "Class III & Implantables",
                "sub": "Cardiac pacemakers, neurostimulators, critical life-support",
                "standards": "PMA, EU MDR Annex IX, ISO 13485, Full Design Dossier",
                "timeline": "Enterprise Continuous Validation",
                "highlight": "Full bi-directional trace rigor from clinical evaluation to post-market surveillance.",
            },
            {
                "id": "ivd",
                "name": "In Vitro Diagnostics (IVD)",
                "sub": "Molecular testing assays, point-of-care analyzers, automated reagents",
                "standards": "EU IVDR 2017/746, CLIA, ISO 13485, FDA 510(k)",
                "timeline": "10-14 Weeks to Technical File",
                "highlight": "Performance evaluation reports, analytical validation protocols, lot traceability.",
            },
        ],
        "modules": [
            ("Requirements Management", "Manage user needs, software requirements, parent-child hierarchies, and controlled version history."),
            ("Risk Management", "Identify hazards, define controls, and maintain ISO 14971 risk evidence."),
            ("Design Control", "Connect design inputs, outputs, reviews, verification, validation, and release evidence."),
            ("Test Management", "Plan, execute, review, and approve verification and validation tests."),
            ("End-to-End Traceability", "Expose gaps across requirements, risks, controls, tests, and evidence."),
            ("Document Control", "Control SOPs, DHF, DMR, technical files, approvals, and audit-ready PDFs."),
            ("CAPA Management", "Track nonconformances, root cause, actions, owners, due dates, and effectiveness."),
            ("Audit Management", "Plan audits, manage findings, assign actions, and prove readiness."),
            ("Training & Competence", "Route role-based learning, acknowledgements, reminders, and compliance status."),
            ("Post-Market Surveillance", "Keep complaints, signals, vigilance, and post-market evidence connected."),
        ],
        "steps": [
            "Create project and assign the right team.",
            "Define user needs, requirements, risks, controls, and tests.",
            "Execute, validate, approve, and generate DHF or technical documentation.",
            "Release with traceability, then continue into post-market surveillance.",
        ],
        "frameworks": ["ISO 13485", "ISO 14971", "IEC 62304", "IEC 62366", "21 CFR 820", "21 CFR Part 11", "EU MDR 2017/745"],
        "integrations": ["Jira", "Microsoft Azure Boards", "Microsoft Office", "SharePoint"],
    }
    return render(request, "website/home.html", context)


def thanks(request):
    return render(request, "website/thanks.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("workspace")
    error = None
    next_url = request.POST.get("next", request.GET.get("next", ""))
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}, require_https=request.is_secure()):
        next_url = ""
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username", "").strip(), password=request.POST.get("password", ""))
        if user is not None:
            login(request, user)
            return redirect(next_url or "workspace")
        error = "The username or password is incorrect."
    return render(request, "website/login.html", {"error": error, "next": next_url, "username": request.POST.get("username", "")})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def workspace(request):
    form = ActionItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        messages.success(request, "Action created.")
        return redirect("workspace")
    items = ActionItem.objects.filter(owner=request.user)
    total = items.count()
    completed = items.filter(status="done").count()
    today = timezone.localdate()
    overdue = items.exclude(status="done").filter(due_date__lt=today).count()
    query = request.GET.get("q", "").strip()[:160]
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    filtered = items
    if query:
        filtered = filtered.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status in dict(ActionItem.STATUSES):
        filtered = filtered.filter(status=status)
    else:
        status = ""
    if priority in dict(ActionItem.PRIORITIES):
        filtered = filtered.filter(priority=priority)
    else:
        priority = ""
    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="smarteye-actions.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Title", "Description", "Priority", "Status", "Due date"])
        for item in filtered:
            # Neutralize spreadsheet formulas in user-authored cells.
            cells = [f"ACT-{item.pk:04d}", item.title, item.description, item.get_priority_display(), item.get_status_display(), item.due_date or ""]
            writer.writerow(["'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value for value in cells])
        return response
    context = {
        "action_form": form, "items": filtered, "query": query,
        "selected_status": status, "selected_priority": priority,
        "statuses": ActionItem.STATUSES, "priorities": ActionItem.PRIORITIES,
        "total": total, "open_count": total - completed, "completed": completed,
        "overdue": overdue, "completion": round(completed / total * 100) if total else 0,
        "today": today,
    }
    return render(request, "website/workspace.html", context)


@login_required(login_url="login")
@require_POST
def update_action(request, pk):
    item = get_object_or_404(ActionItem, pk=pk, owner=request.user)
    status = request.POST.get("status")
    if status not in dict(ActionItem.STATUSES):
        return HttpResponseBadRequest("Invalid action status.")
    item.status = status
    item.save(update_fields=["status", "updated_at"])
    messages.success(request, "Action status updated.")
    return redirect("workspace")
