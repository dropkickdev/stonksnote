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
    meta = fields.JSONField(null=True)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_brokers')
    
    class Meta:
        table = 'stocks_broker'
        manager = ActiveManager()
        
    def __str__(self):
        return modstr(self, 'name')


class Trade(DTMixin, SharedMixin, models.Model):
    action = fields.CharField(max_length=10)
    shares = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=4)
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_trades')
    fees = fields.JSONField(null=True)
    meta = fields.JSONField(null=True)
    broker = fields.ForeignKeyField('models.Broker', related_name='broker_trades')
    author = fields.ForeignKeyField('models.UserMod', related_name='author_trades')
    
    tags = fields.ManyToManyField('models.Taxonomy', related_name='tag_trades',
                                  through='stocks_trade_tags', backward_key='trade_id')
    class Meta:
        table = 'stocks_trade'
        manager = ActiveManager()
        
    def __str__(self):
        return f'{self.equity.code}: {self.shares}'
    
    @property
    def gross(self):
        return self.shares * self.price
    
    @property
    def total(self):
        total = self.gross
        for i in self.fees.values():
            total += i
        return total
    
    
class Note(DTMixin, SharedMixin, models.Model):
    note = fields.TextField()
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_notes')
    author = fields.ForeignKeyField('models.UserMod', related_name='author_notes')

    tags = fields.ManyToManyField('models.Taxonomy', related_name='tag_notes',
                                  through='stocks_note_tags', backward_key='note_id')
    class Meta:
        table = 'stocks_note'
        manager = ActiveManager()
        
    def __str__(self):
        split = self.note.split()
        words = 10
        if len(split) >= words:
            return f'{" ".join(split[:words])}...'
        return self.note
        

class Timeline(DTMixin, SharedMixin, models.Model):
    equity = fields.ForeignKeyField('models.Equity', related_name='equity_timelines')
    note = fields.ForeignKeyField('models.Note', related_name='note_timelines')
    stage = fields.ForeignKeyField('models.Taxonomy', related_name='stage_timelines')
    author = fields.ForeignKeyField('models.UserMod', related_name='author_timelines')
    
    class Meta:
        table = 'stocks_timeline'
        manager = ActiveManager()
        
    def __str__(self):
        return self.id                                                              # noqa


class Group(DTMixin, SharedMixin, models.Model):
    name = fields.CharField(max_length=191)
    description = fields.CharField(max_length=191)
    author = fields.ForeignKeyField('models.UserMod', related_name='author_groups')
    
    class Meta:
        table = 'stocks_group'
        manager = ActiveManager()

    def __str__(self):
        return modstr(self, 'name')