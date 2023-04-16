from disco.bot import Plugin


class plugintoremove(Plugin):
    def load(self, ctx):
        self.log.info("I HAVE LOADED")

    def unload(self, ctx):
        self.log.info("I HAVE UNLOADED")