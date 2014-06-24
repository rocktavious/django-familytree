from familytree import signals
from django.db import models
from django.db.models import Q
from django.db.models.signals import m2m_changed

def format_date_location(city=None, state=None, country=None):
    format_string = ''
    if city:
        format_string += ' - %s' % (city)
    if state:
        format_string += ', %s' % (state)
    if country:
        format_string += ' - %s' % (country)

    return u'%s' % (format_string)

class MarriageManager(models.Manager):
    def marriage_with(self, family_member):
        marriages = self.all()
        marriages = marriages.filter(Q(descendant=family_member.id) | Q(in_law=family_member.id))
        return marriages

    def marriage_of(self, family_member1, family_member2):
        marriages = self.all()
        marriages = marriages.filter(Q(descendant=family_member1.id) | Q(in_law=family_member1.id))
        marriages = marriages.filter(Q(descendant=family_member2.id) | Q(in_law=family_member2.id))
        if len(marriages) != 1 :
            return None
        else:
            return marriages[0]

    def active_marriage_with(self, family_member):
        marriages = self.marriage_with(family_member)
        marriages = marriages.filter(is_active=1)
        return marriages

class Marriage(models.Model):
    descendant = models.ForeignKey('FamilyMember', related_name='descendant')
    in_law = models.ForeignKey('FamilyMember', related_name='in_law')

    string_marriage_date = models.CharField('String Marriage Date', max_length=120, blank=True)
    date_marriage_date = models.DateField('Marriage Date', null=True, blank=True)

    marriage_city = models.CharField(max_length=120, blank=True)
    marriage_state = models.CharField(max_length=120, blank=True)
    marriage_country = models.CharField(max_length=120, blank=True)

    is_active = models.BooleanField()

    objects = MarriageManager()

    def save(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super(Marriage, self).save()

    @property
    def marriage_title(self):
        return u'%s & %s' % (self.descendant.full_name, self.in_law.full_name)

    @property
    def marriage_location(self):
        return format_date_location(self.marriage_city,self.marriage_state,self.marriage_country)

    @property
    def marriage_date(self):
        return self.string_marriage_date or self.date_marriage_date

    def _get_descendant_children_id_list(self):
        descendant_children = self.descendant.children.all()
        children_ids = list()
        for child in descendant_children :
            children_ids.append(child.pk)
        return children_ids

    def get_children(self):
        children_ids = self._get_descendant_children_id_list()
        return self.in_law.children.all().filter(pk__in=children_ids).order_by('date_birth_date')

    def get_step_children(self):
        children_ids = self._get_descendant_children_id_list()
        return self.in_law.children.all().exclude(pk__in=children_ids).order_by('date_birth_date')


    def __unicode__(self):
        return self.marriage_title

class FamilyMemberManager(models.Manager):
    def search_members(self, first=None, middle=None, last=None, maiden=None):
        querySet = self.all()
        if last:
            querySet = querySet.filter(last_name__icontains=last)
        if first:
            querySet = querySet.filter(first_name__icontains=first)
        if middle:
            querySet = querySet.filter(middle_name__icontains=middle)
        if maiden:
            querySet = querySet.filter(maiden_name__icontains=maiden)
        return querySet

    def find_exact_members(self, first=None, middle=None, last=None, maiden=None):
        querySet = self.all()
        if last:
            querySet = querySet.filter(last_name__iexact=last)
        if first:
            querySet = querySet.filter(first_name__iexact=first)
        if middle:
            querySet = querySet.filter(middle_name__iexact=middle)
        if maiden:
            querySet = querySet.filter(maiden_name__iexact=maiden)
        return querySet        

    def find_person(self, first=None, middle=None, last=None, maiden=None):
        if first == '':
            first = None
        if middle == '':
            middle = None
        if last == '':
            last = None
        if maiden == '':
            maiden = None
        firstTry = self.search_members(first, middle, last, maiden)
        if len(firstTry) != 1:
            secondTry = self.find_exact_members(first, middle, last, maiden)
            if len(secondTry) != 1:
                return None
            return secondTry[0]
        return firstTry[0]
    
    def wedding_list(self):
        jerry = self.search_members('Gerald','Donald','Rockman')[0]
        for child in jerry.children.all():
            marriages = Marriage.objects.marriage_with(child)
            print child.display_name, '|',
            for m in marriages:
                print m.in_law.display_name,
            print ''
            for kid in child.children.all():
                kid_marriages = Marriage.objects.marriage_with(kid)
                print '\t', kid.display_name, '|',
                for m2 in kid_marriages:
                    print m2.in_law.display_name
                print ''        

class FamilyMember(models.Model):
    #Name
    preferred_name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    maiden_name = models.CharField(max_length=50, blank=True)
    ordinal = models.CharField(max_length=50, blank=True)

    #Personal Info
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    step_child = models.BooleanField()

    string_birth_date = models.CharField('String Birth Date', max_length=120, blank=True)
    date_birth_date = models.DateField('Birth Date', null=True, blank=True)
    birth_city = models.CharField(max_length=120, blank=True)
    birth_state = models.CharField(max_length=120, blank=True)
    birth_country = models.CharField(max_length=120, blank=True)

    string_death_date = models.CharField('String Death Date', max_length=120, blank=True)
    date_death_date = models.DateField('Death Date', null=True, blank=True)
    death_city = models.CharField(max_length=120, blank=True)
    death_state = models.CharField(max_length=120, blank=True)
    death_country = models.CharField(max_length=120, blank=True)

    bio = models.TextField(blank=True)
    picture = models.CharField(max_length=50, blank=True)

    #Relationships
    parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)    
    children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)

    #Manager Objects
    objects = FamilyMemberManager()

    @property
    def display_name(self):
        format_string = ''
        format_string += self.full_name
        if self.maiden_name :
            format_string += ' (%s)' % (self.maiden_name)

        return u'%s' % (format_string)

    @property
    def full_name(self):
        format_string = ''
        if self.preferred_name :
            format_string += '%s' % (self.preferred_name)
        else:
            format_string += '%s %s' % (self.first_name,self.middle_name)

        if self.last_name :
            format_string += ' %s' % (self.last_name)

        if self.ordinal :
            format_string += ' - %s' % (self.ordinal)

        return u'%s' % (format_string)

    @property
    def birth_date(self):
        return self.string_birth_date or self.date_birth_date

    @property
    def birth_location(self):
        return format_date_location(self.birth_city,self.birth_state,self.birth_country)

    @property
    def death_date(self):
        return self.string_death_date or self.date_death_date

    @property
    def death_location(self):
        return format_date_location(self.death_city,self.death_state,self.death_country)

    @property
    def parents_marriage(self):
        parents = self.parents.all()
        if len(parents) == 2 :
            parents_marriage = Marriage.objects.marriage_of(parents[0],parents[1])
        else :
            parents_marriage = None

        return parents_marriage

    class Meta:
        ordering = ('first_name','last_name')
        verbose_name = "Family Member"
        verbose_name_plural = "Family Members" 

    def save(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super(FamilyMember, self).save()    

    def __unicode__(self):
        return self.full_name


#Signals
m2m_changed.connect(signals.connect_parent, sender=FamilyMember.parents.through)
m2m_changed.connect(signals.connect_child, sender=FamilyMember.children.through)