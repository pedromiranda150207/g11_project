from flask import Flask, render_template, request, session
from classes.company import Company

prev_option = ""

def apps_company():
    global prev_option
    ulogin = session.get("user")
    
    if ulogin is not None:
        butshow = "enabled"
        butedit = "disabled"
        option = request.args.get("option")
        
        if option == "edit":
            butshow, butedit = "disabled", "enabled"
        elif option == "delete":
            obj = Company.current()
            Company.remove(obj.id)
            if not Company.previous():
                Company.first()
        elif option == "insert":
            butshow, butedit = "disabled", "enabled"
        elif option == 'cancel':
            pass
        elif prev_option == 'insert' and option == 'save':
            id_novo = str(Company.get_id(0))
            name = request.form.get("name", "")
            creation_date = request.form.get("creation_date", "")
            
            # Monta a string com 3 campos (id;name;creation_date)
            strobj = f"{id_novo};{name};{creation_date}"
            obj = Company.from_string(strobj)
            Company.insert(obj.id)
            Company.last()
        elif prev_option == 'edit' and option == 'save':
            obj = Company.current()
            obj.name = request.form.get("name", "")
            obj._creation_date = request.form.get("creation_date", "")
            Company.update(obj.id)
        elif option == "first":
            Company.first()
        elif option == "previous":
            Company.previous()
        elif option == "next":
            Company.nextrec()
        elif option == "last":
            Company.last()
        elif option == 'exit':
            return render_template("index.html", ulogin=session.get("user"))
            
        prev_option = option
        obj = Company.current()
        
        if option == 'insert' or len(Company.lst) == 0:
            id = Company.get_id(0)
            company_id = ""
            name = ""
            creation_date = ""
        else:
            id = obj.id
            company_id = obj.id 
            name = obj.name
            creation_date = str(obj._creation_date)
            
        return render_template("company.html", 
                               butshow=butshow, 
                               butedit=butedit, 
                               id=id,
                               company_id=company_id,
                               name=name,
                               creation_date=creation_date, 
                               ulogin=session.get("user"))
    else:
        return render_template("index.html", ulogin=ulogin)