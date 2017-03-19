import os
import stringutils
import web


URL = 'http://127.0.0.1:9091/transmission/rpc'


def get_sessionid():
    code, text = web.post_data_to_url(URL)
    sessionid = stringutils.substringafter(text,
                                           '<code>X-Transmission-Session-Id: ')
    sessionid = stringutils.substringbefore(sessionid,
                                            '</code>')
    return sessionid


def get_transmission_files(header, torrentid):
    postdata = ('{'
                   '    "arguments": {'
                   '        "id" : ' + torrentid + ','
                   '        "fields": ['
                   '            "files"'
                   '        ]'
                   '    },'
                   '    "method": "torrent-get"'
                   '}')
    print (postdata)
    data = web.get_json_data_from_post(URL, header, postdata)
    if (len(data["arguments"]["torrents"]) < 0):
        print('An error occured, no file was found')
    else:
        print(data)
        return data['arguments']['torrents'][0]['files']


def set_wanted_files(header, torrentid, tfiles, files):
    i = 0
    ids = []
    for fil in iter(tfiles):
        filename = os.path.split(fil["name"])[1]
        if (filename in files):
            ids.append(str(i))
        i = i + 1
    if (len(ids) > len(files)):
        print("The len are not in good proportion! {0} vs {1}".format(
            len(files), len(ids)))
    else:
        print("The len are in good proportion! {0} vs {1}".format(
            len(files), len(ids)))
        send_wanted_query(header, torrentid, ids)


def set_wanted_folders(header, torrentid, tfiles, folders):
    i = 0
    ids = []
    for fil in iter(tfiles):
        folder = os.path.split(os.path.split(fil["name"])[0])[1]
        print(folder)
        if (folder in folders):
            ids.append(str(i))
        i = i + 1
    if (len(ids) > len(folders)):
        print("The len are not in good proportion! {0} vs {1}".format(
            len(folders), len(ids)))
    else:
        print("The len are in good proportion! {0} vs {1}".format(
            len(folders), len(ids)))
    send_wanted_query(header, torrentid, ids)


def send_wanted_query(header, torrentid, ids):
    postdata = ('{'
                   '    "arguments": {'
                   '        "ids" : ' + torrentid + ','
                   '        "files-wanted": ['
                   '            ' + ', '.join(ids) + ''
                   '        ]'
                   '    },'
                   '    "method": "torrent-set"'
                   '}')
    code, text = web.post_data_to_url(URL, header, postdata)
    print(text)


def set_them_files(torrentid, files):
    sessionid = get_sessionid()
    header = {'X-Transmission-Session-Id': sessionid}
    tfiles = get_transmission_files(header, torrentid)
    set_wanted_files(header, torrentid, tfiles, files)


def set_them_folders(torrentid, folders):
    sessionid = get_sessionid()
    header = {'X-Transmission-Session-Id': sessionid}
    tfiles = get_transmission_files(header, torrentid)
    set_wanted_folders(header, torrentid, tfiles, folders)


if __name__ == '__main__':
    # NEED TO BE MANUALLY REPLACED
    torrentid = '4'
    # NEED TO BE MANUALLY REPLACED
    folders = {'Dungeons.&.Dragons.HD.Chronicles.of.Mystara.Update.2-FTS'}
    set_them_folders(torrentid, folders)
