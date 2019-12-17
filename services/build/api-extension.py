# this file is meant to be concatenated to the EchoNest servers api.py

urls = urls + (
    '/delete', 'delete',
)

class delete:
    def POST(self):
        return self.GET()

    def GET(self):
        stuff = web.input(track_id="")
        response = fp.delete(stuff.track_id)
        return json.dumps({"ok":True)
~                                                      