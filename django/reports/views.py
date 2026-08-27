from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import Conversation

from .forms import ReportUploadForm
from .models import Report
from .services import ReportProcessingError, process_report


@login_required
def home(request):
    form = ReportUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            conversation = Conversation.objects.create(
                user=request.user,
                report=report,
                title=f'Chat about {report.name}',
            )
        try:
            result = process_report(report)
        except ReportProcessingError as exc:
            messages.error(request, f'We could not process that report: {exc}')
            return redirect('home')

        if result.get('status') != 'completed':
            messages.error(request, 'We could not finish processing that report.')
            return redirect('home')

        return redirect('conversation', conversation_id=conversation.id)
    reports = Report.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(user=request.user).select_related('report')
    recent_report = reports.first()
    return render(request, 'home.html', {
        'form': form,
        'reports': reports,
        'conversations': conversations,
        'recent_report': recent_report,
    })


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    return render(request, 'reports/detail.html', {'report': report})