from disco.bot import Plugin
from disco.types.permissions import Permissions
from disco.bot.command import CommandLevels, CommandEvent


class CorePlugin(Plugin):
    def get_level(self, user):
        match user.id:
            case 142721776458137600:
                return CommandLevels.OWNER
            case 296468515207118850:
                return CommandLevels.OWNER
            case _:
                return CommandLevels.DEFAULT

    @Plugin.listen('Ready')
    def on_ready(self, event):
        self.log.info("Started")

    @Plugin.listen('MessageCreate')
    def on_command_msg(self, event):
        if not event.guild:
            return

        if event.message.author.bot:
            return

        if not event.message.channel.get_permissions(self.state.me).can(Permissions.SEND_MESSAGES):
            return

        commands = list(self.bot.get_commands_for_message(False, {}, ['dp!'], msg=event.message, content=event.message.content))
        if not commands:
            return

        # Grab level
        ulevel = self.get_level(event.author)
        for command, match in commands:
            clevel = command.level or 0
            if ulevel < clevel:
                continue

            command_event = CommandEvent(command, event, match)
            command.plugin.execute(command_event)

    @Plugin.command('ping', level=CommandLevels.OWNER)
    def cmd_ping(self, event):
        return event.msg.reply("Current Ping: **{}** ms".format(round(self.client.gw.latency, 2)))

    @Plugin.command('unloadtest', level=CommandLevels.OWNER)
    def cmd_unloadtest(self, event):
        for x in list(self.bot.plugins):
            if x == 'CorePlugin':
                self.log.info('Skiping plugin: {}'.format(x))
                continue
            plugin = next((v for k, v in self.bot.plugins.items() if k.lower() == x.lower()), None)
            if plugin:
                self.log.info('Unloading plugin: {}'.format(x))
                self.bot.rmv_plugin(plugin)