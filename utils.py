"""
    Function converting year into format yyyy
    TODO range datumy vsetko dajak este dorobit
"""
def convert_year(y):
    if (y == "now"):
        return y
        
    l = 4 - len(y)
    for i in range(l):
        y = "0"+y
    return y

"""
    Function converting elastic results json into different names for html rendering
"""
def elastic_to_html(res, html_type="edit"):

    # res["_source"]["date"] = res["_source"]["date"]
    if "path" in res["_source"]:
        img_name = res["_source"]["path"]
        del res["_source"]["path"]
    else:
        img_name = ""
    
    res['_source']['date'] = res['_source']['date']['gte']+"-"+res['_source']['date']['lte'] if res['_source']['date']['lte'] != res['_source']['date']['gte'] else res['_source']['date']['lte']
    if (html_type == "show"):
        # if ("material" in res["_source"] and type(res["_source"]["material"])==list):
        #     res["_source"]["material"] = ', '.join(res["_source"]["material"])
        if (type(res["_source"]["keys"])==list):
            res["_source"]["keys"] = ', '.join(res["_source"]["keys"])
        if (type(res["_source"]["references.studies"])==list):
            res["_source"]["studies"] = '\n\n'.join(res["_source"]["references.studies"])
        else:
            res["_source"]["studies"] = res["_source"]["references.studies"]
        if "references.translation" in res["_source"]:
            res["_source"]["translation"] = res["_source"]["references.translation"]
            del res["_source"]["references.translation"]
        
        res["_source"]["edition"] = res["_source"]["references.edition"]
        del res["_source"]["references.edition"]
        del res["_source"]["references.studies"]

    del res["_source"]["added"]

    return res, img_name

"""
    Function not used
"""
def html_to_elastic(args):
    
    #res["_source"]["date"] = res["_source"]["date"]
    #path
    
    # args['material'] = args['material'].split(',')
    # args['references.studies'] = args['studies'].split('\n\n')
    # args['keys'] = args['keys'].split(',')
    args['references.studies'] = args['studies']
    args['references.translation'] = args['translation']
    args['references.edition'] = args['edition']
    
    
    return args

"""
    Function get required data from results, 
    when match_all option is used and no highlight is in results
"""
def elastic_to_html_all_filter(res):
    for el in res:

        if (type(el["_source"]["keys"])==list):
            keys = ', '.join(el["_source"]["keys"])
        else:
            keys = el["_source"]["keys"]

        el['highlight'] = { 
            "title" : [el['_source']['title']] ,
            "keys" : [keys],
            "date" : [el['_source']['date']['gte']+"-"+el['_source']['date']['lte'] if el['_source']['date']['lte'] != el['_source']['date']['gte'] else el['_source']['date']['lte']]
        }

    return res

"""
    Function check whether score are not 0
    TODO nemalo by to take vracat
"""
def check_elastic_res(res):
    for el in res:
        
        if el['_score'] == 0.0:
            print(el['_score'])
            return True

    return False

"""
    Function add date to highlight, becasue elasticserach cannot do that
"""
def append_date_to_res(res):
    for el in res:
        if 'highlight' in el:
            el['highlight']['date'] = [el['_source']['date']['gte']+"-"+el['_source']['date']['lte'] if el['_source']['date']['lte'] != el['_source']['date']['gte'] else el['_source']['date']['lte']]
        else:
            el['highlight'] = dict()
            el['highlight']['date'] = [el['_source']['date']['gte']+"-"+el['_source']['date']['lte'] if el['_source']['date']['lte'] != el['_source']['date']['gte'] else el['_source']['date']['lte']]
    return res