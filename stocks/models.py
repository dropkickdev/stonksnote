from tortoise import models, fields
from limeutils import modstr

from app.authentication.models.manager import ActiveManager
from app.authentication.models.core import DTMixin, SharedMixin



class Equity(DTMixin, SharedMixin, models.Model):
    code = fields.CharField(max_length=10)
    name = fields.CharField(max_length=191, default='')
    country = fields.CharField(max_length=2)
    industry = fields.CharField(max_length=191)
    meta = fields.JSONField(null=True)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_equities')
    is_watchlist = fields.BooleanField(default=False)

    groups = fields.ManyToManyField('models.Group', related_name='group_equities',
                                    through='stocks_equity_groups', backward_key='equity_id')
    
    class Meta:
        table = 'stocks_equity'
        unique_together = (('code', 'country'),)
        manager = ActiveManager()
        
    def __str__(self):
        return modstr(self, 'code')


class Broker(DTMixin, SharedMixin, models.Model):
    name = fields.CharField(max_length=191)
    rating = fields.FloatField(max_digits=2, decimal_places=1)
    meta = fields.JSONField(null=True)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_brokers')
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = 'stocks_broker'
        manager = ActiveManager()
        
    def __str__(self):
        return modstr(self, 'name')


class Trade(DTMixin, SharedMixin, models.Model):
    action = fields.CharField(max_length=10)
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_trades')
    
    shares = fields.IntField()
    entry_target = fields.DecimalField(max_digits=10, decimal_places=4)
    entry_actual = fields.DecimalField(max_digits=10, decimal_places=4)
    tp_target = fields.DecimalField(max_digits=10, decimal_places=4)
    tp_actual = fields.DecimalField(max_digits=10, decimal_places=4)
    stoploss_target = fields.DecimalField(max_digits=10, decimal_places=4)
    stoploss_actual = fields.DecimalField(max_digits=10, decimal_places=4)
    rrr_target = fields.DecimalField(max_digits=10, decimal_places=2)
    rrr_actual = fields.DecimalField(max_digits=10, decimal_places=2)
    opening = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    closing = fields.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    gross = fields.DecimalField(max_digits=10, decimal_places=4)
    fees = fields.JSONField(null=True)
    total = fields.DecimalField(max_digits=10, decimal_places=4)
    gainloss = fields.DecimalField(max_digits=10, decimal_places=4, index=True)
    
    note = fields.TextField()
    meta = fields.JSONField(null=True)
    altert = fields.BooleanField(default=False)
    broker = fields.ForeignKeyField('models.Broker', related_name='broker_trades')
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
        return f'{self.equity.code}: {self.shares}'
    
    @property
    def get_total(self):
        total = self.gross
        for i in self.fees.values():
            total += i
        return total
    
    
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


class Timeline(DTMixin, SharedMixin, models.Model):
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_timelines')
    status = fields.ForeignKeyField('models.Taxonomy', related_name='status_trades')
    author = fields.ForeignKeyField('models.UserMod', related_name='author_timelines')

    class Meta:
        table = 'stocks_timeline'
        manager = ActiveManager()

    def __str__(self):
        return self.id                                                              # noqa


class Collection(DTMixin, SharedMixin, models.Model):
    name = fields.CharField(max_length=191)
    description = fields.CharField(max_length=191)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_collections')
    
    class Meta:
        table = 'stocks_collection'
        manager = ActiveManager()

    def __str__(self):
        return modstr(self, 'name')