from tortoise import models, fields
from tortoise.manager import Manager
from limeutils import modstr

from app.authentication.models.manager import ActiveManager
from app.authentication.models.core import DTMixin, SharedMixin



class Equity(DTMixin, SharedMixin, models.Model):
    code = fields.CharField(max_length=10)
    exchange = fields.ForeignKeyField('models.Taxonomy', related_name='exchange_equity')
    name = fields.CharField(max_length=191, default='')
    
    country = fields.CharField(max_length=2, default='')
    industry = fields.CharField(max_length=191, default='')
    meta = fields.JSONField(null=True)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_equities')
    
    class Meta:
        table = 'stocks_equity'
        manager = ActiveManager()
        
    def __str__(self):
        return modstr(self, 'code')

    
class UserEquities(models.Model):
    user = fields.ForeignKeyField('models.UserMod', related_name='userequities')
    equity = fields.ForeignKeyField('models.Equity', related_name='userequities')
    created_at = fields.DatetimeField(auto_now_add=True)

    groups = fields.ManyToManyField('models.Taxonomy', related_name='userequities',
                                    through='stocks_userequities_groups',
                                    backward_key='userequity_id')
    
    full = Manager()
    
    class Meta:
        table = 'stocks_userequities'
        unique_together = (('user', 'equity'),)
        manager = ActiveManager()
        
    def __str__(self):
        return f'{self.user}:{self.equity}'


class Broker(DTMixin, SharedMixin, models.Model):
    name = fields.CharField(max_length=191)
    
    rating = fields.FloatField(max_digits=2, decimal_places=1, default=0)
    email = fields.CharField(max_length=191, default='')
    number = fields.CharField(max_length=191, default='')
    url = fields.CharField(max_length=191, default='')
    country = fields.CharField(max_length=2, default='')
    
    is_online = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = 'stocks_broker'
        manager = ActiveManager()
        
    def __str__(self):
        return modstr(self, 'name')


class Trade(DTMixin, SharedMixin, models.Model):
    status = fields.CharField(max_length=20)
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_trades')
    note = fields.TextField()
    
    shares = fields.IntField(default=0)
    entrypoint = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    takeprofit = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    stoploss = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    rrr = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    gross = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    fees = fields.JSONField(null=True)
    total = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    gainloss = fields.DecimalField(max_digits=10, decimal_places=4)
    
    meta = fields.JSONField(null=True)
    broker = fields.ForeignKeyField('models.Broker', related_name='broker_trades', null=True)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_trades')
    
    is_favorite = fields.BooleanField(default=False)
    is_public = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)
    
    tags = fields.ManyToManyField('models.Taxonomy', related_name='tag_trades',
                                  through='stocks_trade_tags', backward_key='trade_id')
    groups = fields.ManyToManyField('models.Taxonomy', related_name='group_trades',
                                    through='stocks_trade_groups', backward_key='trade_id')
    
    class Meta:
        table = 'stocks_trade'
        manager = ActiveManager()
        
    def __str__(self):
        return f'{self.equity}: {self.shares}'
    
    @property
    def get_total(self):
        total = self.gross
        for i in self.fees.values():
            total += i
        return total


class Action(DTMixin, SharedMixin, models.Model):
    action = fields.CharField(max_length=20)
    equity = fields.ForeignKeyField('models.Equity', related_name='actions')
    implement = fields.DatetimeField(null=True)
    
    entrypoint = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    stoploss = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    takeprofit = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    rrr = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    opening = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    closing = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    note = fields.CharField(max_length=199)
    status = fields.CharField(max_length=20)
    is_completed = fields.DatetimeField(null=True)
    
    class Meta:
        table = 'stocks_action'
        manager = ActiveManager()
    
    def __str__(self):
        return self.action
    
# class Note(DTMixin, SharedMixin, models.Model):
#     note = fields.TextField()
#     equity = fields.ForeignKeyField('models.Equity', related_name='equity_notes')
#     author = fields.ForeignKeyField('models.UserMod', related_name='author_notes')
#
#     status = fields.ManyToManyField('models.Taxonomy', related_name='tag_notes',
#                                     through='stocks_note_status', backward_key='note_id')
#     class Meta:
#         table = 'stocks_note'
#         manager = ActiveManager()
#
#     def __str__(self):
#         split = self.note.split()
#         words = 10
#         if len(split) >= words:
#             return f'{" ".join(split[:words])}...'
#         return self.note
#
#
# class TradeNote(DTMixin, models.Model):
#     trade = fields.ForeignKeyField('models.Trade', related_name='tradenotes')
#     note = fields.ForeignKeyField('models.Note', related_name='tradenotes')
#     status = fields.ForeignKeyField('models.Taxonomy', related_name='tradenotes', null=True)
#
#     class Meta:
#         table = 'stocks_note_status'
#         unique_together = (('trade_id', 'note_id'),)


# class Timeline(DTMixin, SharedMixin, models.Model):
#     equity = fields.ForeignKeyField('models.Equity', related_name='equity_timelines')
#     status = fields.ForeignKeyField('models.Taxonomy', related_name='status_trades')
#     author = fields.ForeignKeyField('models.UserMod', related_name='author_timelines')
#
#     class Meta:
#         table = 'stocks_timeline'
#         manager = ActiveManager()
#
#     def __str__(self):
#         return self.id                                                              # noqa


# class Collection(DTMixin, SharedMixin, models.Model):
#     name = fields.CharField(max_length=191)
#     description = fields.CharField(max_length=191)
#     author = fields.ForeignKeyField('models.UserMod', related_name='author_collections')
#
#     class Meta:
#         table = 'stocks_collection'
#         manager = ActiveManager()
#
#     def __str__(self):
#         return self.name