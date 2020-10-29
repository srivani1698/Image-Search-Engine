from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch

def eSearch(patentID="", pid=""):
    client = Elasticsearch()
    q = Q("bool", should=[Q("match", pid=pid),
                          Q("match", patentID=patentID)],
          minimum_should_match=1)
    s = Search(using=client, index="final").query(q)[0:20]
    response = s.execute()
    print('Total hits found : ', response.hits.total)
    search=get_results(response)
    return search

def get_results(response):
    results=[]
    for hit in response:
        result_tuple = (hit.patentID, hit.pid, hit.figid, hit.description , hit['patentID']+'-D0'+hit['pid'][2:]+'.png')
        results.append(result_tuple)
    return results

if __name__ == '__main__':
    print("Opal guy details: \n",eSearch(firstName="opal"))
    print("the first 20 Female gender details: \n", eSearch(pid))

def search(q=""):
    client = Elasticsearch()
    query = MultiMatch(query=q, fields=['patentID', 'pid','origreftext','description','aspect'], fuzziness='AUTO')
    s = Search(using=client, index='final').query(query)
    response = s.execute()
    search=get_results(response)
    return search


def Data(q):
    c = Elasticsearch()
    values = {"patentID": q['patentID'], "pid": q['pid'],"is_multiple": q['is_multiple'],"origreftext": q['origreftext'],"figid": q['figid'], "subfig": q['subfig'], "is_caption": q['is_caption'], "description": q['description'],  "aspect": q['aspect'], "object": q['object']
    }
    response = c.index( index = 'final',doc_type = '_doc',body = values
    )
    if response['result'] == "created":
        return True
    else:
        return False
