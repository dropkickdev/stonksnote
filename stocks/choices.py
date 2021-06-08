from gettext import gettext as _
from enum import Enum


class TradeStatusChoices(str, Enum):
    plan = _('Planning')
    wait = _('Wait and see')
    buy = _('Prepare to BUY')
    sell = _('Prepare to SELL')
    late = _('Too late to enter')
