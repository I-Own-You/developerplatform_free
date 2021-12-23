from django.shortcuts import render
from .models import Project, Review
from project.models import Developer
from django.db.models import Q
from django.core.paginator import Paginator


def proj_page(request):
    projects = []

    for project in Project.objects.all():
        if project.owner.first_name and project.owner.last_name and project.owner.short_bio and project.owner.work_position:
            projects.append(project)

    if request.method == 'GET':
        search_proj = request.GET.get('search-proj')
        if bool(search_proj):
            search_proj = search_proj.strip()
            projects = Project.objects.filter(Q(title__contains=search_proj) | Q(
                owner__last_name__contains=search_proj) | Q(
                    owner__first_name__contains=search_proj))

                    
    if 'next' in request.GET:
        id = int(request.GET['next'])
        side_projects = Project.objects.filter(owner=Developer.objects.get(id=id))
        projects = side_projects
        
    
    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'projects': projects,
        'page_obj': page_obj,
    }
    return render(request, 'proj_page.html', context)

