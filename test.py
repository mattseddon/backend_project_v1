import json,requests

def show_request_with_response(url,requestlist,method):
    for rqst in requestlist:
        rqst = json.loads(rqst)
        if method == "post":
            r = requests.post(url, json=rqst)
        elif method == "put":
            r = requests.put(url, json=rqst)
        print 'request:',json.dumps(rqst,indent=2)
        print 'response:',r.content

#test companies:
company_url = 'http://127.0.0.1:5000/company'

print "***SUCCESSFUL Company Posts***"
successful_company_posts = [
'{"title":"Accelo","website":"www.accelo.com"}',
# result from above: loaded successfully (notice no contacts)
'{"title":"another new company","website":"www.anotherNewcompany.com"\
,"contacts":[\
{"first_name" : "Matt","surname":"Seddon","email":"matt.seddon@anotherNewcompany.com","phone":"+61411535955"},\
{"first_name" : "Dave","surname":"Smith","email":"dave.smith@anotherNewcompany.com","phone":"+61411535955"}\
]\
}',
#loaded successfully with no errors
'{"title":"Analytx","website":"analytx.com.au"\
,"contacts":[\
{"first_name" : "Matt","surname":"Seddon","email":"matt.seddon@analytx.com.au","phone":"+61411535955"},\
{"first_name" : "Ben","surname":"Croll","email":"ben.croll@analytx.com.au","phone":"+61411111111"},\
{"first_name" : "Michael","surname":"Esposito","email":"michael.esposito@analytx.com.au","phone":"+61422222222"}\
]\
}'
#loaded successfully with no errors
]
show_request_with_response(company_url,successful_company_posts,"post")



print "***PARITALLY SUCCESSFUL Company Posts***"
partially_successful_company_posts = [
'{"title":"Jacked Up Contacts","website":"www.jackedcontacts.com"\
,"contacts":[\
{                           "surname":"No First Name","email":"nofirstname@jackedcontacts.com","phone":"+61411535955"},\
{"first_name" : "No Surname"                         ,"email":"nosurname@jackedcontacts.com"  ,"phone":"+61422222222"},\
{"first_name" : "Mr"        ,"surname":"No Email"                                             ,"phone":"+61411111111"},\
{"first_name" : "Mr"        ,"surname":"No Phone"    ,"email":"mrnophone@jackedcontacts.com"                         }]\
}',
#company will be loaded with no children
'{"title":"Jacked Up Contacts","website":"www.jackedcontacts.com"\
,"contacts":[\
{"first_name" : "Mr"        ,"surname":"No First Name","email":"nofirstname@jackedcontacts.com","phone":"+61333333333"},\
{"first_name" : "Mr"        ,"surname":"No Email"     ,"email":"mrnoemail@jackedcontacts.com"  ,"phone":"+61411111111"},\
{"first_name" : "No Surname"                          ,"email":"nosurname@jackedcontacts.com"  ,"phone":"+61422222222"},\
{"first_name" : "Mr"        ,"surname":"No Phone"     ,"email":"mrnophone@jackedcontacts.com"                         }]\
}'
#company will return existing but fixed contacts will load loaded with no children 2 pass, 2 fail
]
show_request_with_response(company_url,partially_successful_company_posts,"post")



print "***UNSUCCESSFUL Company Posts***"
unsuccessful_company_posts = [
'{"title":"Jacked Up Company"\
,"contacts":[\
{"first_name" : "Dave"  ,"surname":"Wontload" ,"email":"davewontload@jackedcompany.com"  ,"phone":"+61444444444"},\
{"first_name" : "Steve" ,"surname":"Wontload" ,"email":"mrnophone@jackedcompany.com"     ,"phone":"+61444444444"}]\
}',
#nothing loaded
'{"website":"www.jackedcompany.com"\
,"contacts":[\
{"first_name" : "Dave"  ,"surname":"Wontload" ,"email":"davewontload@jackedcompany.com"  ,"phone":"+61444444444"},\
{"first_name" : "Steve" ,"surname":"Wontload" ,"email":"mrnophone@jackedcompany.com"     ,"phone":"+61444444444"}]\
}'
#nothing loaded
]
show_request_with_response(company_url,unsuccessful_company_posts,"post")



print "***Existing Company Posts - Can add contacts***"
#!!!!!!potential danger - if first_name and surname as incorrect then a new contact will be created at this end point!!!!!!
existing_company_posts = [
'{"title":"Analytx","website":"analytx.com.au"\
,"contacts":[\
{"first_name" : "Matt","surname":"Seddon","email":"notmatt.seddon@analytx.com.au","phone":"+61411535955"},\
{"first_name" : "Ben","surname":"Croll","email":"notben.croll@analytx.com.au","phone":"+61411111111"},\
{"first_name" : "Michael","surname":"Esposito","email":"notmichael.esposito@analytx.com.au","phone":"+61422222222"}\
]\
}',
#will return existing messages for each but not change email
'{"title":"Analytx","website":"analytx.com.au"\
,"contacts":[\
{"first_name" : "Matt","surname":"Seddon","email":"notmatt.seddon@analytx.com.au","phone":"+61411535955"},\
{"first_name" : "New","surname":"Contact","email":"new.contact@analytx.com.au","phone":"+614999999999"}\
]\
}'
#existing message for Matt Seddon + new contact added
]
show_request_with_response(company_url,existing_company_posts,"post")



#test contacts:
contact_url = 'http://127.0.0.1:5000/contact'

print "***SUCCESSFUL Contact Posts***"
successful_contact_posts = ['{"first_name":"Mr","surname":"Accelo"\
,"companies":[\
{"title" : "CRM & Sales"  ,"website":"accelo.com"  ,"email":"mraccelo@crmsales.com"  ,"phone":"+61455555555"},\
{"title" : "Finance","website":"accelo.com","email":"mraccelo@finance.com","phone":"+61455555555"}, \
{"title" : "Time And Projects","website":"accelo.com","email":"mraccelo@time.com","phone":"+61455555555"} \
]\
}'
#successfully create 3 new companies
]
show_request_with_response(contact_url,successful_contact_posts,"post")



print "***PARTIALLY SUCCESSFUL Contact Posts***"
partially_successful_contact_posts = ['{"first_name":"Steve","surname":"Smith"\
,"companies":[\
{"title" : "Smith Plumbing"  ,"website":"smithplumbing.com"  ,"email":"Steve@smithplumbing.com"  ,"phone":"+61466666666"},\
{"title" : "No Website"                                      ,"email":"wontload@nowebsite.com"  ,"phone":"+61466666666"}\
]\
}'
#Steve smith will be loaded with Smith Plumbing the record with no website will be rejected
]
show_request_with_response(contact_url,partially_successful_contact_posts,"post")



print "***UNSUCCESSFUL Contact Posts***"
unsuccessful_contact_posts = ['{"first_name":"I SHOULD NOT","surname":"BE HERE"}',
#won't load - needs a company
'{"first_name":"I SHOULD NOT","surname":"BE HERE"\
,"companies":[\
{"title" : "No Website"                       ,"email":"wontload@nowebsite.com"  ,"phone":"+61466666666"}\
]\
}',
#still won't load - needs a company
'{"first_name":"I SHOULD NOT","surname":"BE HERE"\
,"companies":[\
{"title" : "No Phone","website":"nophone.com","email":"ISHOULDNOTBEHERE@nophone.com"}\
]\
}'

]

show_request_with_response(contact_url,unsuccessful_contact_posts,"post")




print "***EXISTING Contact Posts***"
existing_contact_posts = ['{"first_name":"Mr","surname":"Accelo"\
,"companies":[\
{"title" : "CRM & Sales"  ,"website":"accelo.com"  ,"email":"IWILLNOTCHANGEmraccelo@crmsales.com"  ,"phone":"+61455555555"},\
{"title" : "Finance","website":"accelo.com","email":"IWILLNOTCHANGEmraccelo@finance.com","phone":"+61455555555"}, \
{"title" : "Purchasing","website":"accelo.com","email":"mraccelo@purchasing.com","phone":"+61455555555"} \
]\
}'
#successfully creates 1 new company and returns existing for the other 3 with no changes
]
show_request_with_response(contact_url,existing_contact_posts,"post")



matt_analytx_url = 'http://127.0.0.1:5000/contact/matt.seddon/analytx'

print "***SUCCESSFUL Contact Put***"
successful_contact_puts = [
     '{"first_name": "Matthew"}',
     '{"first_name" : "Matt","surname":"Seddon","email":"matthew.seddon@analytx.com.au","book":"bingo bango"}'
     #will successfully change even though extra data is entered and phone is missing
]
show_request_with_response(matt_analytx_url,successful_contact_puts,"put")

print "***UNSUCCESSFUL Contact Put***"
unsuccessful_contact_puts = [
      '{"id":"trying to change my id is a bad idea"}'
     ,'{"company_id":"trying to change my id is a bad idea"}'
     ,'{"contact_id":"trying to change my id is a bad idea"}'
     #will successfully change even though extra data is entered
]
show_request_with_response(matt_analytx_url,unsuccessful_contact_puts,"put")


analytx_url = 'http://127.0.0.1:5000/company/analytx'

print "***SUCCESSFUL Company Put***"
successful_company_puts = [
     '{"title": "Analytx Pty Ltd"}',
     '{"website": "www.analytx.com.au"}'
]
show_request_with_response(analytx_url,successful_company_puts,"put")

print "***UNSUCCESSFUL Contact Put***"
unsuccessful_company_puts = [
      '{"id":"trying to change my id is a bad idea"}'
]
show_request_with_response(analytx_url,unsuccessful_company_puts,"put")

#check the get endpoints:
print "***GET ME SOME DATA***"

def get(url):
    print "***GET",url+'***'
    r = requests.get(url)
    print r.content

get('http://127.0.0.1:5000/companies')
get('http://127.0.0.1:5000/company/analytx')
get('http://127.0.0.1:5000/company/analytx/contacts')
get('http://127.0.0.1:5000/contacts')
get('http://127.0.0.1:5000/contact/matt.seddon')
get('http://127.0.0.1:5000/contact/matt.seddon/companies')
