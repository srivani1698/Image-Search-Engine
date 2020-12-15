
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch
from django.core.paginator import Paginator, Page
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.paginator import Paginator, Page
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch

def eSearch(patentID="", pid=""):
    client = Elasticsearch()
    q = Q("bool", should=[Q("match", pid=pid),
                          Q("match", patentID=patentID)],
          minimum_should_match=1)
    s = Search(using=client, index="final").query(q)
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

def search(Q_text="",pageLowerLimit = 0, pageUpperLimit = 10, page=1):
    client = Elasticsearch()

    query = MultiMatch(query=Q_text, fields=['patentID', 'pid','origreftext','description','aspect'], fuzziness='AUTO')
    s = Search(using=client, index='final').query(query)[pageLowerLimit:pageUpperLimit]
    response = s.execute()
    totalResults = response.hits.total.value
    print(totalResults)
    paginator = esPaginator(totalResults = totalResults, perPage = 10)
    posts = paginator.paginate(page)
    search=get_results(response)
    return totalResults, search, posts


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

class esPaginator:
    def __init__(self, totalResults = 0, perPage=10):
        self.count = totalResults
        self.perPage = perPage
        self.num_pages = totalResults//perPage
        
        self.paginator = {
            'number' : 0,
            'count' : totalResults,
            'has_other_pages':False,
            'has_previous':False,
            'get_prev_page':0,
            'has_next':False,
            'get_next_page':0,
            'get_page_range':0,
            'num_pages' : 1,
        }
    def paginate(self, number):
        if self.count > self.perPage:
            self.paginator['has_other_pages'] = True
            self.paginator['has_previous'] = True if number > 1 else False
            self.paginator['has_next'] = True if number < (self.num_pages + 1) else False
            self.paginator['num_pages'] = self.count//self.perPage + 1
            self.paginator['get_page_range'] = list(range(1,self.paginator['num_pages']+1))
            if number in self.paginator['get_page_range']:
                self.paginator['number'] = number
                self.paginator['get_prev_page'] = number - 1
                self.paginator['get_next_page'] = number + 1
            else:
                self.paginator['number'] = 1
                self.paginator['get_prev_page'] = 1
                self.paginator['get_next_page'] = 1
            return self.paginator
        return self.paginator

