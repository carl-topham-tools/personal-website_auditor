import peewee
from peewee import *

from settings.settings import *


class Backlog(peewee.Model):
    url = peewee.CharField()
    session_uuid = peewee.CharField()
    starting_url = peewee.CharField()
    depth = peewee.IntegerField()
    performance = peewee.BooleanField()

    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('url', 'session_uuid', 'starting_url'), True),
        )
try:
    Backlog.create_table()
except:
    pass


class BacklogItem(object):

    def delete(self, session_uuid):
        query = Backlog.delete().where(Backlog.session_uuid == session_uuid)
        query.execute()

    def add(self, url, starting_url, session_uuid, depth, performance):

        item = Backlog(
            url=url,
            session_uuid=session_uuid,
            starting_url=starting_url,
            depth=depth,
            performance=performance
        )
        item.save()

    def upsert(self, url, starting_url, session_uuid, depth, performance):
        try:
            # Update existing
            _ = Backlog.get(
                Backlog.url == url,
                Backlog.session_uuid == session_uuid
            )
            # if it exists then skip it
        except:
            # Create new status entry
            self.add(url, starting_url, session_uuid, depth, performance)

    def count(self):
        return Backlog.select().count()

    def first(self):
        data = Backlog.select().get()
        return data

    def popFirst(self):
        first = Backlog.select().get()
        first.delete_instance()

    def count_session(self, session_uuid):
        return Backlog.filter(Backlog.session_uuid == session_uuid).count()

    def first_session(self, session_uuid):
        data = Backlog.filter(Backlog.session_uuid == session_uuid).get()
        return data

    def pop_first_session(self, session_uuid):
        first = Backlog.filter(Backlog.session_uuid == session_uuid).get()
        first.delete_instance()
