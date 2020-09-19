from .tool.func import *

# 고립된 문서
def list_orf_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by title limit ?, '50'", [str(sql_num)])
    else:
        curs.execute("select title from data where title like ? || ':%' order by title limit ?, '50'", [ns, str(sql_num)])
    data_list = curs.fetchall()

    div = '''<form method="get">
                <div class=form-group>
                    <label>이름공간:</label>
                    <select name=namespace id=namespace class=form-control>
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
                    <button type=submit class="btn btn-primary">이동</button>
                    <a class="btn btn-secondary" href=''>갱신</a>
                </div>
            </form>
            
            <ul class=wiki-list>'''
    var = ''


    for data in data_list:
        curs.execute("select title from back where title = ?", [data[0]])
        if not(curs.fetchall()):
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

    div += '</ul>' + next_fix('/OrphanedPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['고립된 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

# 분류 안된 문서
def list_unc_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by title limit ?, '50'", [str(sql_num)])
    else:
        curs.execute("select title from data where title like ? || ':%' order by title limit ?, '50'", [ns, str(sql_num)])
    data_list = curs.fetchall()

    div = '''<form method="get">
                <div class=form-group>
                    <label>이름공간:</label>
                    <select name=namespace id=namespace class=form-control>
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
                    <button type=submit class="btn btn-primary">이동</button>
                    <a class="btn btn-secondary" href=''>갱신</a>
                </div>
            </form>
                <ul class=wiki-list>'''
    var = ''


    for data in data_list:
        curs.execute("select link from back where link = ? and type = 'cat'", [data[0]])
        if not(curs.fetchall()):
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

    div += '</ul>' + next_fix('/UncategorizedPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['분류되지 않은 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

# 편집된 지 오래된 문서 (리다이렉트 제외)
def list_old_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title, data, date from data order by date asc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = '''<ul class=wiki-list>'''
    var = ''

    for data in data_list:
        # 리다이렉트 포함하려면 아래 두 줄 삭제
        if re.search('^#redirect ', data[1]) or re.search('^#넘겨주기 ', data[1]):
            continue
        ddd = data[2].split(' ')[0]
        ttt = data[2].split(' ')[1]

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (수정 시각: <time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>)</li>'

    div += '</ul>' + next_fix('/OldPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['편집된 지 오래된 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

#내용이 짧은 문서 (리다이렉트 제외)
def list_short_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title from data order by length(data) asc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = '''<ul class=wiki-list>'''
    var = ''

    for data in data_list:
        if re.search('^[#]redirect ', data[1]) or re.search('^[#]넘겨주기 ', data[1]):
            continue

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (' + str(len(data[1])) + ')</li>'

    div += '</ul>' + next_fix('/ShortestPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['내용이 짧은 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

#내용이 긴 문서 (리다이렉트 제외)
def list_long_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title from data order by length(data) desc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = next_fix('/LongestPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''

    for data in data_list:
        if re.search('^[#]redirect ', data[1]) or re.search('^[#]넘겨주기 ', data[1]):
            continue

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (' + str(len(data[1])) + ')</li>'

    div += '</ul>' + next_fix('/LongestPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['내용이 긴 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))
