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
    data = web.get_json_data_from_post(URL, header, postdata)
    if (len(data["arguments"]["torrents"]) < 0):
        print('An error occured, no file was found')
    else:
        #print(data)
        return data['arguments']['torrents'][0]['files']


def set_wanted_files(header, torrentid, tfiles, files):
    i = 0
    ids = []
    for fil in iter(tfiles):
        filename = os.path.split(fil["name"])[1]
        if (filename.lower() in files):
            ids.append(str(i))
        i = i + 1
    if (len(ids) > len(files)):
        print("The lens are not in good proportion! {0} ids vs {1} files".format(
            len(files), len(ids)))
        return
    else:
        print("The lens are in good proportion! {0} ids vs {1} files".format(
            len(files), len(ids)))

    if (len(ids) > 0):
        send_wanted_query(header, torrentid, ids)
    else:
        print("No query needed for folders")


def set_wanted_folders(header, torrentid, tfiles, folders):
    i = 0
    ids = []
    for fil in iter(tfiles):
        folder = os.path.split(os.path.split(fil["name"])[0])[1]
        if (folder.lower() in folders):
            ids.append(str(i))
        i = i + 1
    if (len(ids) > len(folders)):
        print("The lens are not in good proportion! {0} ids vs {1} folders".format(
            len(folders), len(ids)))
        return
    else:
        print("The lens are in good proportion! {0} ids vs {1} folders".format(
            len(folders), len(ids)))

    if (len(ids) > 0):
        send_wanted_query(header, torrentid, ids)
    else:
        print("No query needed for folders")


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
    print(postdata)
    code, text = web.post_data_to_url(URL, header, postdata)
    print('query posted')
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
