from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
import json

from .models import Complaint, ComplaintCategory, ComplaintComment, ComplaintHistory
from .forms import ComplaintForm, UserRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Basic validation
        if not username:
            return JsonResponse({
                'success': False, 
                'error': 'Username is required. Please enter your username.'
            })
        
        if not password:
            return JsonResponse({
                'success': False, 
                'error': 'Password is required. Please enter your password.'
            })
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'success': True, 'redirect': '/dashboard/'})
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Your account is inactive. Please contact administrator.'
                })
        else:
            # Check if username exists to provide better error message
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid password. Please check your password and try again.'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid username or password. Please check your credentials and try again.'
                })
    
    return render(request, 'complaints/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/dashboard/'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': json.loads(errors)})
    return render(request, 'complaints/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    complaints = Complaint.objects.all()
    
    # Filter based on user role
    if not user.is_staff:
        complaints = complaints.filter(created_by=user)
    
    # Statistics
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='pending').count(),
        'in_progress': complaints.filter(status='in_progress').count(),
        'resolved': complaints.filter(status='resolved').count(),
        'urgent': complaints.filter(priority='urgent', status__in=['pending', 'in_progress']).count(),
    }
    
    # Recent complaints
    recent_complaints = complaints.order_by('-created_at')[:10]
    
    # Status distribution
    status_distribution = complaints.values('status').annotate(count=Count('id'))
    
    context = {
        'stats': stats,
        'recent_complaints': recent_complaints,
        'status_distribution': list(status_distribution),
        'is_staff': user.is_staff,
    }
    return render(request, 'complaints/dashboard.html', context)


@login_required
def complaints_list(request):
    user = request.user
    complaints = Complaint.objects.all()
    
    if not user.is_staff:
        complaints = complaints.filter(created_by=user)
    
    # Search and filters
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    if search:
        complaints = complaints.filter(
            Q(ticket_number__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    
    # Pagination
    paginator = Paginator(complaints.order_by('-created_at'), 20)
    page = request.GET.get('page', 1)
    complaints_page = paginator.get_page(page)
    
    categories = ComplaintCategory.objects.all()
    
    context = {
        'complaints': complaints_page,
        'categories': categories,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search,
        'is_staff': user.is_staff,
    }
    return render(request, 'complaints/complaints_list.html', context)


@login_required
def complaint_detail(request, ticket_number):
    complaint = get_object_or_404(Complaint, ticket_number=ticket_number)
    user = request.user
    
    # Check permission
    if not user.is_staff and complaint.created_by != user:
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints_list')
    
    comments = complaint.comments.all()
    history = complaint.history.all()[:20]
    
    context = {
        'complaint': complaint,
        'comments': comments,
        'history': history,
        'is_staff': user.is_staff,
        'can_edit': user.is_staff or complaint.created_by == user,
        'status_choices': Complaint.STATUS_CHOICES,
        'priority_choices': Complaint.PRIORITY_CHOICES,
    }
    return render(request, 'complaints/complaint_detail.html', context)


@login_required
def create_complaint(request):
    if request.method == 'POST':
        try:
            form = ComplaintForm(request.POST, request.FILES)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.created_by = request.user
                # Ensure category is None if empty string or not provided
                category_id = request.POST.get('category', '').strip()
                if not category_id:
                    complaint.category = None
                complaint.save()
                
                # Create history entry
                ComplaintHistory.objects.create(
                    complaint=complaint,
                    changed_by=request.user,
                    field_name='created',
                    new_value='Complaint created'
                )
                
                return JsonResponse({
                    'success': True,
                    'ticket_number': complaint.ticket_number,
                    'redirect': f'/complaint/{complaint.ticket_number}/'
                })
            else:
                # Format errors properly
                errors_dict = {}
                for field, error_list in form.errors.items():
                    errors_dict[field] = [str(error) for error in error_list]
                return JsonResponse({'success': False, 'errors': errors_dict})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False, 
                'error': f'An error occurred: {str(e)}',
                'errors': {'__all__': [str(e)]}
            })
    
    categories = ComplaintCategory.objects.all()
    return render(request, 'complaints/create_complaint.html', {'categories': categories})


@login_required
@require_http_methods(["POST"])
def update_complaint_status(request, ticket_number):
    complaint = get_object_or_404(Complaint, ticket_number=ticket_number)
    
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    data = json.loads(request.body)
    new_status = data.get('status')
    resolution_notes = data.get('resolution_notes', '')
    
    if new_status not in dict(Complaint.STATUS_CHOICES):
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    old_status = complaint.status
    complaint.status = new_status
    if resolution_notes:
        complaint.resolution_notes = resolution_notes
    complaint.save()
    
    # Create history entry
    ComplaintHistory.objects.create(
        complaint=complaint,
        changed_by=request.user,
        field_name='status',
        old_value=old_status,
        new_value=new_status
    )
    
    return JsonResponse({'success': True, 'status': new_status})


@login_required
@require_http_methods(["POST"])
def assign_complaint(request, ticket_number):
    complaint = get_object_or_404(Complaint, ticket_number=ticket_number)
    
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    data = json.loads(request.body)
    user_id = data.get('user_id')
    
    if user_id:
        from django.contrib.auth.models import User
        assigned_user = get_object_or_404(User, id=user_id)
        old_assigned = complaint.assigned_to.username if complaint.assigned_to else 'Unassigned'
        complaint.assigned_to = assigned_user
        complaint.save()
        
        ComplaintHistory.objects.create(
            complaint=complaint,
            changed_by=request.user,
            field_name='assigned_to',
            old_value=old_assigned,
            new_value=assigned_user.username
        )
    else:
        old_assigned = complaint.assigned_to.username if complaint.assigned_to else 'Unassigned'
        complaint.assigned_to = None
        complaint.save()
        
        ComplaintHistory.objects.create(
            complaint=complaint,
            changed_by=request.user,
            field_name='assigned_to',
            old_value=old_assigned,
            new_value='Unassigned'
        )
    
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def add_comment(request, ticket_number):
    complaint = get_object_or_404(Complaint, ticket_number=ticket_number)
    
    user = request.user
    if not user.is_staff and complaint.created_by != user:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    data = json.loads(request.body)
    comment_text = data.get('comment', '')
    is_internal = data.get('is_internal', False)
    
    if not comment_text:
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
    
    comment = ComplaintComment.objects.create(
        complaint=complaint,
        user=user,
        comment=comment_text,
        is_internal=is_internal and user.is_staff
    )
    
    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'comment': comment.comment,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_internal': comment.is_internal
        }
    })


@login_required
def api_complaints(request):
    """API endpoint for fetching complaints"""
    user = request.user
    complaints = Complaint.objects.all()
    
    if not user.is_staff:
        complaints = complaints.filter(created_by=user)
    
    # Apply filters
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    search = request.GET.get('search')
    
    if status:
        complaints = complaints.filter(status=status)
    if priority:
        complaints = complaints.filter(priority=priority)
    if search:
        complaints = complaints.filter(
            Q(ticket_number__icontains=search) |
            Q(title__icontains=search)
        )
    
    complaints_list = []
    for complaint in complaints.order_by('-created_at')[:100]:
        complaints_list.append({
            'id': complaint.id,
            'ticket_number': complaint.ticket_number,
            'title': complaint.title,
            'status': complaint.status,
            'priority': complaint.priority,
            'created_by': complaint.created_by.username,
            'assigned_to': complaint.assigned_to.username if complaint.assigned_to else None,
            'created_at': complaint.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'category': complaint.category.name if complaint.category else None,
        })
    
    return JsonResponse({'complaints': complaints_list})


@login_required
def api_stats(request):
    """API endpoint for dashboard statistics"""
    user = request.user
    complaints = Complaint.objects.all()
    
    if not user.is_staff:
        complaints = complaints.filter(created_by=user)
    
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='pending').count(),
        'in_progress': complaints.filter(status='in_progress').count(),
        'resolved': complaints.filter(status='resolved').count(),
        'closed': complaints.filter(status='closed').count(),
        'urgent': complaints.filter(priority='urgent', status__in=['pending', 'in_progress']).count(),
    }
    
    return JsonResponse(stats)
