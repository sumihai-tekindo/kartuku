import base64
import datetime
import hashlib
import pytz
import threading
import urllib2
import urlparse

from email.utils import formataddr
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import browse_record

class Partner(models.Model):
    _inherit = 'res.partner'

    def get_partner_type(self):
        if self._context.get('partner_type',False):
            partner_type = self.env['res.partner.type'].search([('sequence','=',self._context.get('partner_type'))],limit=1)
            return partner_type and partner_type.id or False
        return False

    partner_type = fields.Many2one('res.partner.type',"Type",required=True,default=get_partner_type)
    institution = fields.Many2one('res.partner',"Institution")




    @api.model
    def create(self, vals):

        if ('employee' not in vals or not vals['employee']) and ('company_type' not in vals or vals['company_type']!='company') and ('parent_id' in vals and vals['parent_id']):
            sequence = self.env['ir.sequence'].next_by_code('partner_store')

        else:
        	partner_type = vals['partner_type']
        	partner_type = self.env['res.partner.type'].search([('id','=',partner_type)])
        	sequence = partner_type.sequence_id.next_by_id()
    	vals['ref'] = sequence
    	return super(Partner,self).create(vals)


class PartnerType(models.Model):
	_name ='res.partner.type'
	_order = 'sequence asc'

	name = fields.Char("Name",required=True)
	sequence = fields.Integer("Sequence",required=True)
	sequence_id = fields.Many2one("ir.sequence","Entry Sequence",required=True)

