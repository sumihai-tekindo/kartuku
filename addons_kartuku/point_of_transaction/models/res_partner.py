from datetime import datetime
from dateutil import relativedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Partner(models.Model):
    _inherit = 'res.partner'

    pot_ids = fields.One2many('stock.location',"partner_id","Point Of Transactions")