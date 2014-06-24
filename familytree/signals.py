import sys

def connect_parent(sender, instance, action, reverse, model, pk_set, **kwargs):
    # if remove bob as parent of billy, then update bob's children to match
    if action == "pre_clear":	        
        for parent in instance.parents.all():
            parent.children.remove(instance)           

    # if add bob as parent to billy, then update bob's children to match 
    if action == "post_add":
        for parent in instance.parents.all():
            try:
                me = parent.children.get(id=instance.pk)
            except:
                parent.children.add(instance)

def connect_child(sender, instance, action, reverse, model, pk_set, **kwargs):
    # if remove billy as child of bob, then update billy's parents to match
    if action == "pre_clear":	        
        for child in instance.children.all():
            child.parents.remove(instance)

    # if add billy as child of bob, then update billy's parents to match
    if action == "post_add":
        for child in instance.children.all():

            try:
                me = child.parents.get(id=instance.pk)
            except:
                child.parents.add(instance)