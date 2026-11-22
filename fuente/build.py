import re,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from i18n import ROWS,FRAG
src=open(os.path.join(os.path.dirname(__file__),"plantilla.html")).read()
ALL=[('es','ES',''),('ca','CA','ca/'),('en','EN','en/'),('fr','FR','fr/')]
out=sys.argv[1]
# 'es' = solo español, sin selector (hasta que Matias diga de publicar los idiomas); 'all' = los cuatro
MODE=sys.argv[2] if len(sys.argv)>2 else 'es'
LANGS=ALL if MODE=='all' else ALL[:1]
if MODE!='all':
    src=re.sub(r'  <div class="lang">.*?</div>\n','',src,flags=re.S)
def build(code,idx,prefix):
    t=src
    depth='../' if prefix else ''
    links=''.join(f'<a href="{depth}{p}" hreflang="{c}" lang="{c}"'+(' aria-current="page"' if c==code else '')+f'>{l}</a>' for c,l,p in LANGS)
    t=t.replace('{{LANGS}}',links)
    alt=''.join(f'<link rel="alternate" hreflang="{c}" href="https://www.olivanegra.es/{p}">' for c,l,p in LANGS)+'<link rel="alternate" hreflang="x-default" href="https://www.olivanegra.es/">'
    t=t.replace('</title>','</title>\n'+alt,1)
    if idx:
        t=t.replace('<html lang="es">',f'<html lang="{code}">')
        d={r[0]:r[idx] for r in ROWS}
        for f in FRAG:t=t.replace(f[0],f[idx])
        # text nodes
        def tx(m):
            s=m.group(1);k=re.sub(r'\s+',' ',s.strip())
            if k in d:
                lead=s[:len(s)-len(s.lstrip())];trail=s[len(s.rstrip()):]
                return '>'+lead+d[k].replace('&','&amp;')+trail+'<'
            ka=k.replace('&amp;','&')
            if ka in d:
                lead=s[:len(s)-len(s.lstrip())];trail=s[len(s.rstrip()):]
                return '>'+lead+d[ka].replace('&','&amp;')+trail+'<'
            return m.group(0)
        head,body=t.split('<body>',1)
        body=re.sub(r'>([^<>]+)<',tx,body)
        # attributes
        def at(m):
            v=m.group(2).replace('&amp;','&')
            return f'{m.group(1)}="{d[v].replace("&","&amp;")}"' if v in d else m.group(0)
        body=re.sub(r'\b(alt|aria-label|data-t|title)="([^"]*)"',at,body)
        # JS string literals
        def js(m):
            v=m.group(1)
            return '"'+d[v].replace('"','\\"')+'"' if v in d else m.group(0)
        i=body.index('<script>\n{')
        body=body[:i]+re.sub(r'"([^"\n]+)"',js,body[i:])
        t=head+'<body>'+body
        t=t.replace('src="img/','src="../img/').replace('src="media/','src="../media/').replace('poster="media/','poster="../media/')
        t=t.replace('`<img src="img/${f}.jpg"','`<img src="../img/${f}.jpg"').replace('src="media/${f}','src="../media/${f}').replace('data-src="media/${f}','data-src="../media/${f}').replace('"media/${f}.jpg"','"../media/${f}.jpg"')
        t=t.replace("src=\"img/","src=\"../img/")
    dst=os.path.join(out,prefix)
    os.makedirs(dst,exist_ok=True)
    open(os.path.join(dst,'index.html'),'w').write(t)
    return t
for i,(c,l,p) in enumerate(LANGS):
    t=build(c,i,p)
    print(c,len(t))
