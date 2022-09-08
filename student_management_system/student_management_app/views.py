from distutils.fancy_getopt import FancyGetopt
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from . import forms, models
from .forms import CreateStudentForm, CreateSecretaryForm, CreateAdminForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail


# Check which role user has
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_secretary(user):
    return user.groups.filter(name='SECRETARY').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if is_admin(request.user):
                return redirect('admin-dashboard')
            elif is_secretary(request.user):
                account_approval = models.SecretaryExtraInfo.objects.all().filter(user_id=request.user.id, status=True)
                if account_approval:
                    return redirect('secretary-dashboard')
                else:
                    return render(request, 'secretary-wait-approval.html')
            elif is_student(request.user):
                account_approval = models.StudentExtraInfo.objects.all().filter(user_id=request.user.id, status=True)
                if account_approval:
                    return redirect('student-dashboard')
                else:
                    return render(request, 'student-wait-approval.html')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login.html')


def register_as_page(request):
    return render(request, 'register-as.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def admin_register_page(request):
    form1 = CreateAdminForm()
    form2 = forms.CreateAdminFormExtraInfo()
    context = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = CreateAdminForm(request.POST)
        form2 = forms.CreateAdminFormExtraInfo(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            messages.success(request, 'Admin account created')

            # Creates admin group
            admin_group = Group.objects.get_or_create(name='ADMIN')
            admin_group[0].user_set.add(user)

    # return redirect('login')
    return render(request, 'register-admin.html', context)


def secretary_register_page(request):
    form1 = CreateSecretaryForm()
    form2 = forms.CreateSecretaryFormExtraInfo()
    context = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = CreateSecretaryForm(request.POST)
        form2 = forms.CreateSecretaryFormExtraInfo(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            messages.success(request, 'Secretary account created')

            email = request.POST['email']

            send_mail(
                subject = "Student Management System",
                message = "Thank you for your registration! Our admin's will accept your addmision soon.",
                from_email = None,
                recipient_list = [email],
                fail_silently = False
            )

            # Creates secretary group
            secretary_group = Group.objects.get_or_create(name='SECRETARY')
            secretary_group[0].user_set.add(user)

    # return redirect('login')
    return render(request, 'register-secretary.html', context)


def student_register_page(request):
    form1 = CreateStudentForm()
    form2 = forms.CreateStudentFormExtraInfo()
    context = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = CreateStudentForm(request.POST)
        form2 = forms.CreateStudentFormExtraInfo(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            messages.success(request, 'Student account created')

            email = request.POST['email']

            send_mail(
                subject = "Student Management System",
                message = "Thank you for your registration! Our admin's will accept your addmision soon.",
                from_email = None,
                recipient_list = [email],
                fail_silently = False
            )

            # Creates student group
            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)

    # return redirect('login')
    return render(request, 'register-student.html', context)


# Admin views
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    secretary_count = models.SecretaryExtraInfo.objects.all().filter(status=True).count()
    pending_secretary_count = models.SecretaryExtraInfo.objects.all().filter(status=False).count()
    student_count = models.StudentExtraInfo.objects.all().filter(status=True).count()
    pending_student_count = models.StudentExtraInfo.objects.all().filter(status=False).count()
    announcement = models.Announcement.objects.all()

    #data fetching to screen
    context = {
        'secretary_count': secretary_count,
        'pending_secretary_count': pending_secretary_count,
        'student_count': student_count,
        'pending_student_count': pending_student_count,
        'announcement': announcement
    }

    return render(request, 'admin/admin-index.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_secretary_view(request):
    secretaries = models.SecretaryExtraInfo.objects.all().filter(status=False)
    return render(request, 'admin/admin-approve-secretary.html', {'secretaries': secretaries})


@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_secretary_view(request, pk):
    secretary = models.SecretaryExtraInfo.objects.get(id=pk)
    secretary.status = True
    secretary.save()
    return redirect(reverse('admin-approve-secretary'))


@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_secretary_view(request, pk):
    secretary = models.SecretaryExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=secretary.user_id)
    user.delete()
    secretary.delete()
    return redirect('admin-approve-secretary')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_secretary_view(request):
    secretaries = models.SecretaryExtraInfo.objects.all().filter(status=True)
    context = {
        'secretaries': secretaries
    }
    return render(request, 'admin/admin-view-secretary.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_secretary_view(request):
    form1 = CreateSecretaryForm()
    form2 = forms.CreateSecretaryFormExtraInfo()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = CreateSecretaryForm(request.POST)
        form2 = forms.CreateSecretaryFormExtraInfo(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()
            messages.success(request, 'Secretary account created')

            # Creates secretary group
            secretary_group = Group.objects.get_or_create(name='SECRETARY')
            secretary_group[0].user_set.add(user)

    return render(request, 'admin/admin-add-secretary.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_update_secretary_view(request, pk):
    secretary = models.SecretaryExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=secretary.user_id)
    form1 = forms.UpdateSecretaryForm(instance=user)
    form2 = forms.CreateSecretaryFormExtraInfo(instance=secretary)
    context = {
        'form1': form1,
        'form2': form2
    }

    if request.method == 'POST':
        form1 = forms.UpdateSecretaryForm(request.POST, instance=user)
        form2 = forms.CreateSecretaryFormExtraInfo(request.POST, instance=secretary)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            messages.success(request, secretary.get_name+' updated successfully.')
            return redirect('admin-view-secretary')
    return render(request, 'admin/admin-update-secretary.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_delete_secretary_view(request, pk):
    secretary = models.SecretaryExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=secretary.user_id)
    user.delete()
    secretary.delete()
    return redirect('admin-view-secretary')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students = models.StudentExtraInfo.objects.all()
    context = {
        'students': students
    }
    return render(request, 'admin/admin-view-student.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students = models.StudentExtraInfo.objects.all().filter(status=False)
    return render(request, 'admin/admin-approve-student.html', {'students': students})


@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_student_view(request, pk):
    student = models.StudentExtraInfo.objects.get(id=pk)
    student.status = True
    student.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_student_view(request, pk):
    student = models.StudentExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1 = CreateStudentForm()
    form2 = forms.CreateStudentFormExtraInfo()
    context = {
        'form1': form1,
        'form2': form2
    }

    if request.method == 'POST':
        form1 = CreateStudentForm(request.POST)
        form2 = forms.CreateStudentFormExtraInfo(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()
            messages.success(request, 'Student account created')

            # Creates student group
            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)

    return render(request, 'admin/admin-add-student.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_update_student_view(request, pk):
    student = models.StudentExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    form1 = forms.UpdateStudentForm(instance=user)
    form2 = forms.CreateStudentFormExtraInfo(instance=student)
    context = {
        'form1': form1,
        'form2': form2
    }

    if request.method == 'POST':
        form1 = forms.UpdateStudentForm(request.POST, instance=user)
        form2 = forms.CreateStudentFormExtraInfo(request.POST, instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            messages.success(request, student.get_name+' updated successfully.')
            return redirect('admin-view-student')
    return render(request, 'admin/admin-update-student.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_delete_student_view(request, pk):
    student = models.StudentExtraInfo.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_announcement_view(request):
    form = forms.AnnouncementForm()
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user.first_name
            form.save()
            return redirect('admin-dashboard')

    context = {'form': form}
    return render(request, 'admin/admin-announcement.html', context)


# Secretary views
@login_required(login_url='login')
@user_passes_test(is_secretary)
def secretary_dashboard_view(request):
    announcements = models.Announcement.objects.all()
    context = {
        'announcements': announcements
    }
    return render(request, 'secretary/secretary-index.html', context)


@login_required(login_url='login')
@user_passes_test(is_secretary)
def secretary_announcement_view(request):
    form = forms.AnnouncementForm()
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user.first_name
            form.save()
            return redirect('secretary-dashboard')

    context = {'form': form}
    return render(request, 'secretary/secretary-announcement.html', context)


# Student views
@login_required(login_url='login')
@user_passes_test(is_student)
def student_dashboard_view(request):
    announcements = models.Announcement.objects.all()
    context = {
        'announcements': announcements
    }
    return render(request, 'student/student-index.html', context)
