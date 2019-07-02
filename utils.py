

def elastic_to_html(res):

    # res["_source"]["date"] = res["_source"]["date"]
    # del res["_source"]["path"]

    if (type(res["_source"]["material"])==list):
        res["_source"]["material"] = ', '.join(res["_source"]["material"])
    if (type(res["_source"]["keys"])==list):
        res["_source"]["keys"] = ', '.join(res["_source"]["keys"])
    if (type(res["_source"]["references.studies"])==list):
        res["_source"]["studies"] = '\n\n'.join(res["_source"]["references.studies"])
    else:
        res["_source"]["studies"] = res["_source"]["references.studies"]

    res["_source"]["translation"] = res["_source"]["references.translation"]
    res["_source"]["edition"] = res["_source"]["references.edition"]

    del res["_source"]["references.edition"]
    del res["_source"]["references.translation"]
    del res["_source"]["references.studies"]
    
    return res

def html_to_elastic(args):
    
    #res["_source"]["date"] = res["_source"]["date"]
    #path
    
    args['material'] = args['material'].split(',')
    args['references.studies'] = args['studies'].split('\n\n')
    args['references.translation'] = args['translation']
    args['references.edition'] = args['edition']
    args['keys'] = args['keys'].split(',')
    
    return args

def elastic_to_html_all_filter(res):
    for el in res:
        el['highlight'] = { 
            "title" : [el['_source']['title']] ,
            "keys" : [', '.join(el["_source"]["keys"])],
            "date" : [el['_source']['date']]
        }

    return res