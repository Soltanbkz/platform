from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django_filters.views import FilterView

from accounts.models import User, Student
from core.models import Session, Semester
from quiz.models import Quiz
from result.models import TakenCourse
from accounts.decorators import lecturer_required, student_required
from .forms import (
    ProgramForm,
    CourseAddForm,
    CourseAllocationForm,
    EditCourseAllocationForm,
    UploadFormFile,
    UploadFormVideo,
)
from .filters import ProgramFilter, CourseAllocationFilter
from .models import Program, Course, CourseAllocation, Upload, UploadVideo


@method_decorator([login_required], name="dispatch")
class ProgramFilterView(FilterView):
    filterset_class = ProgramFilter
    template_name = "course/program_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Programs"
        context["filter"] = self.get_filterset(self.get_filterset_class())
        return context


@login_required
@lecturer_required
def program_add(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, request.POST.get("title") + " program has been created."
            )
            return redirect("programs")
        else:
            messages.error(request, "Correct the error(S) below.")
    else:
        form = ProgramForm()

    return render(
        request,
        "course/program_add.html",
        {
            "title": "Add Program",
            "form": form,
        },
    )


@login_required
def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk).order_by("-year")
    credits = Course.objects.aggregate(Sum("credit"))

    paginator = Paginator(courses, 10)
    page = request.GET.get("page")

    courses = paginator.get_page(page)

    return render(
        request,
        "course/program_single.html",
        {
            "title": program.title,
            "program": program,
            "courses": courses,
            "credits": credits,
        },
    )


@login_required
@lecturer_required
def program_edit(request, pk):
    program = Program.objects.get(pk=pk)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(
                request, str(request.POST.get("title")) + " program has been updated."
            )
            return redirect("programs")
    else:
        form = ProgramForm(instance=program)

    return render(
        request,
        "course/program_add.html",
        {"title": "Edit Program", "form": form},
    )


@login_required
@lecturer_required
def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    title = program.title
    program.delete()
    messages.success(request, "Program " + title + " has been deleted.")

    return redirect("programs")


# ########################################################
# Course views
# ########################################################
@login_required
def course_single(request, slug):
    course = Course.objects.get(slug=slug)
    files = Upload.objects.filter(course__slug=slug)
    videos = UploadVideo.objects.filter(course__slug=slug)

    lecturers = CourseAllocation.objects.filter(courses__pk=course.id)

    return render(
        request,
        "course/course_single.html",
        {
            "title": course.title,
            "slug": slug,
            "course": course,
            "files": files,
            "videos": videos,
            "lecturers": lecturers,
            "media_url": settings.MEDIA_ROOT,
        },
    )


@login_required
@lecturer_required
def course_add(request, pk):
    users = User.objects.all()
    if request.method == "POST":
        form = CourseAddForm(request.POST)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        if form.is_valid():
            form.save()
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been created.")
            )
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(initial={"program": Program.objects.get(pk=pk)})

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Add Course",
            "form": form,
            "program": pk,
            "users": users,
        },
    )


@login_required
@lecturer_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseAddForm(request.POST, instance=course)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        if form.is_valid():
            form.save()
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been updated.")
            )
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(instance=course)

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Edit Course",
            "slug": slug,
            "form": form,
        },
    )


@login_required
@lecturer_required
def course_delete(request, slug):
    course = Course.objects.get(slug=slug)
    course.delete()
    messages.success(request, "Course " + course.title + " has been deleted.")

    return redirect("program_detail", pk=course.program.id)


# ########################################################
# Course Allocation
# ########################################################

@method_decorator([login_required], name="dispatch")
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = "course/course_allocation_form.html"

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        lecturer = form.cleaned_data["lecturer"]
        selected_courses = form.cleaned_data["courses"]
        courses = tuple(course.pk for course in selected_courses)

        try:
            allocation = CourseAllocation.objects.get(lecturer=lecturer)
        except CourseAllocation.DoesNotExist:
            allocation = CourseAllocation.objects.create(lecturer=lecturer)

        for course in selected_courses:
            allocation.courses.add(course)

        allocation.save()
        return redirect("course_allocation_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assign Course"
        context["programs"] = Program.objects.prefetch_related('course_set').all()
        context["form"] = CourseAllocationForm(user=self.request.user)
        return context


@method_decorator([login_required], name="dispatch")
class CourseAllocationFilterView(FilterView):
    filterset_class = CourseAllocationFilter
    template_name = "course/course_allocation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course Allocations"
        context["form"] = CourseAllocationForm(user=self.request.user)
        context["filter"] = self.get_filterset(self.get_filterset_class())
        context["programs"] = Program.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required
@lecturer_required
def deallocate_course(request, pk):
    course = get_object_or_404(CourseAllocation, pk=pk)
    course.delete()
    messages.success(request, "Successfully deallocated!")
    return redirect("course_allocation_view")


@login_required
@lecturer_required
def edit_allocated_course(request, pk):
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    programs = Program.objects.prefetch_related('courses').all()

    if request.method == "POST":
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, "course assigned has been updated.")
            return redirect("course_allocation_view")
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(
        request,
        "course/course_allocation_form.html",
        {"title": "Edit Course Allocated", "form": form, "allocated": pk, 'programs': programs},
    )


# ########################################################
# File Upload views
# ########################################################
@login_required
@lecturer_required
def handle_file_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded successfully.")
            )
            return redirect("course_single", slug=slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormFile()

    return render(
        request,
        "course/upload_file.html",
        {
            "title": "Upload File",
            "form": form,
            "slug": slug,
            "course": course,
        },
    )


@login_required
@lecturer_required
def handle_file_edit(request, slug, pk):
    course = Course.objects.get(slug=slug)
    file = get_object_or_404(Upload, pk=pk)

    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=file)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been updated successfully.")
            )
            return redirect("course_single", slug=slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormFile(instance=file)

    return render(
        request,
        "course/upload_file.html",
        {
            "title": "Edit File",
            "form": form,
            "slug": slug,
            "course": course,
        },
    )


@login_required
@lecturer_required
def handle_file_delete(request, slug, pk):
    file = Upload.objects.get(pk=pk)
    file.delete()
    messages.success(request, file.title + " has been deleted successfully.")

    return redirect("course_single", slug=slug)


# ########################################################
# Video Upload views
# ########################################################
@login_required
@lecturer_required
def handle_video_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded successfully.")
            )
            return redirect("course_single", slug=slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormVideo()

    return render(
        request,
        "course/upload_video.html",
        {
            "title": "Upload Video",
            "form": form,
            "slug": slug,
            "course": course,
        },
    )

@login_required
# @lecturer_required
def handle_video_single(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, course__slug=slug, slug=video_slug)
    videos = UploadVideo.objects.filter(course=video.course).order_by('id')
    quiz = Quiz.objects.filter(course=video.course).first()
    video_index = list(videos).index(video)
    quizzes = Quiz.objects.filter(course=video.course).order_by('id')
    return render(request, "upload/video_single.html", {"video": video, 'video_index': video_index,'quizzes': quizzes,})

@login_required
@lecturer_required
def handle_video_edit(request, slug, pk):
    course = Course.objects.get(slug=slug)
    video = get_object_or_404(UploadVideo, pk=pk)

    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES, instance=video)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been updated successfully.")
            )
            return redirect("course_single", slug=slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormVideo(instance=video)

    return render(
        request,
        "course/upload_video.html",
        {
            "title": "Edit Video",
            "form": form,
            "slug": slug,
            "course": course,
        },
    )


@login_required
@lecturer_required
def handle_video_delete(request, slug, pk):
    video = UploadVideo.objects.get(pk=pk)
    video.delete()
    messages.success(request, video.title + " has been deleted successfully.")

    return redirect("course_single", slug=slug)


# ########################################################


# ########################################################
# Course Registration
# ########################################################
@login_required
@student_required
def course_registration(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.create(student=student, course=course)
            obj.save()
        messages.success(request, "Courses registered successfully!")
        return redirect("course_registration")
    else:
        current_semester = Semester.objects.filter(is_current_semester=True).first()
        if not current_semester:
            messages.error(request, "No active semester found.")
            return render(request, "course/course_registration.html")

        # student = Student.objects.get(student__pk=request.user.id)
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)

        courses = (
            Course.objects.filter(
                program__pk=student.program.id,
                level=student.level,
                semester=current_semester,
            )
            .exclude(id__in=t)
            .order_by("year")
        )
        all_courses = Course.objects.filter(
            level=student.level, program__pk=student.program.id
        )

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
        if (
            registered_courses.count() == 0
        ):  # Check if number of registered courses is 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
        }
        return render(request, "course/course_registration.html", context)


@login_required
@student_required
def course_drop(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
        messages.success(request, "Successfully Dropped!")
        return redirect("course_registration")


# ########################################################


@login_required
def user_course_list(request):
    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id)

        return render(request, "course/user_course_list.html", {"courses": courses})

    elif request.user.is_student:
        student = Student.objects.get(student__pk=request.user.id)
        taken_courses = TakenCourse.objects.filter(
            student__student__id=student.student.id
        )
        courses = Course.objects.filter().filter(
            program__pk=student.program.id
        )

        return render(
            request,
            "course/user_course_list.html",
            {"student": student, "taken_courses": taken_courses, "courses": courses},
        )

    else:
        return render(request, "course/user_course_list.html")