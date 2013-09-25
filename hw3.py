from os import listdir
from stopwords import allStopWords
from re import sub

dataset=dict(enumerate([f for f in listdir('hw3data')]))

def mapfn(fileindex,filename):
    for row in open('hw3data/'+filename,encoding='latin-1'):
        tokens = row.split(':::')
        paper_id = tokens[0]
        authors  = tokens[1].split('::')
        title = tokens[2]
        
        terms = [ sub("\W|_",'',t).lower() for t in title.split(' ') if not sub("\W|_",'',t).lower() in allStopWords]
        
        terms_freq=dict()
        terms_freq = {t:terms_freq[t]+1 if t in terms_freq else 1 for t in terms} 
        
        
        for author in authors:
            yield author,terms_freq



def reducefn(author,terms_freqs):
    term_freq=dict()
    for t_f in terms_freqs:
        for term in t_f.keys():
            term_freq[term] = term_freq[term]+t_f[term] if term in term_freq else t_f[term]
    return author,sorted(term_freq.items(),key=lambda t: t[1],reverse=True)   

intermediate=dict()
        
for (i,v) in dataset.items():
    inter = dict(mapfn(i,v))
    for a in inter.keys():
        
        intermediate[a] = intermediate[a]+[inter[a]] if a in intermediate else [inter[a]]

final = dict()
for (i,lv) in intermediate.items():
    final[i] = reducefn(i, lv)

outfile= open('out.file','w',encoding='latin-1')
for i,v in final.items():
    outfile.write(str(v[0])+"\n")
    outfile.write(str(v[1])+"\n")
    outfile.write("\n")


