from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from familytree.models import FamilyMember, Marriage
    
def family_member(request, member_id):
    person = get_object_or_404(FamilyMember, pk=member_id)
    marriages = Marriage.objects.marriage_with(person)
    return render_to_response('familytree/member_info.html', {'person':person, 'marriages':marriages})
	
def family_member_search(request):
	first = request.GET.get('first',None)
	middle = request.GET.get('middle',None)
	last = request.GET.get('last',None)
	maiden = request.GET.get('maiden',None)
	person_list = FamilyMember.objects.search_members(first, middle, last, maiden)
	if not person_list:
		raise Http404
		#return HttpResponse('Search Fields were %s - %s - %s - %s'%(first_name, middle_name, last_name, maiden_name)) 
	return render_to_response('familytree/member_list.html', {'person_list':person_list})