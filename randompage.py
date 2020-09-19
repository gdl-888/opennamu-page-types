# APP.PY에는 대충 다음과 같이 추가하면 된다.
#
# 요롷게 주소를 설정하고
# @app.route('<사용할 주소>')
# def rndpg():
#     return random_documents(conn)

def random_documents(conn):
    curs = conn.cursor()
    rndPg_list = ''
    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by random() limit 20")
    else:
        curs.execute("select title from data where title like ? || ':%' order by random() limit 20", [ns])

    for i in curs.fetchall():
        rndPg_list += '<li><a href="/w/' + url_pas(i[0]) + '">' + i[0] + '</a></li>'

    return easy_minify(flask.render_template(skin_check(),
        imp = ['임의 문서 목록', wiki_set(), custom(), other2([0, 0])],
        data = '''<form method="get">
                <div class=form-control>
                    <label>이름공간:</label>
                    <select name=namespace id="namespace" class=form-control>
                        <option value="문서" selected="">문서</option>
                        <option value="''' + load_lang('template') + '''">''' + load_lang('template') + '''</option>
                        <option value="category">category</option>
                        <option value="file">file</option>
                        <option value="user">user</option>
                        <option value="''' + wiki_set()[0] + '''">''' + wiki_set()[0] + '''</option>
                    </select>

                    <script>document.getElementById('namespace').value = \'''' + flask.request.args.get('namespace', '문서') + '''\';</script>
                </div>
                
                <div class=btns>
                    <button type="submit" class="btn btn-primary">이동</button>
                    <a class="btn btn-secondary">갱신</a>
                </div>
            </form>
            
            <ul class=wiki-list>''' + rndPg_list + '''</ul>''',
        menu = 0
    ))
