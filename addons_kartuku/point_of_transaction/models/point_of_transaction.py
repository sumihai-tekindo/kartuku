from datetime import datetime
from dateutil import relativedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


from odoo import tools



class Location(models.Model):
	_inherit="stock.location"

	active = fields.Boolean("Active")
	pot = fields.Boolean("Point of Transaction")
	warehouse_ids = fields.One2many('stock.warehouse','name',"Warehouse")
	partner_ids = fields.One2many('stock.location.pot','location_id',"Partner")
	warehouse_id = fields.Many2one('stock.warehouse',"Warehouse")
	


class LocationPot(models.Model):
	_name="stock.location.pot"
	_rec_name="partner_id"

	location_id=fields.Many2one("stock.location","Location")
	state_id=fields.Many2one('res.partner',string="State")
	partner_id = fields.Many2one("res.partner",string="Partner",domain="[('partner_type.sequence','=',1)]")
	institution_id = fields.Many2one("res.partner",string="Institution",domain="[('partner_type.sequence','=',2)]")
	merchant_id = fields.Many2one("res.partner",string="Merchant",domain="[('partner_type.sequence','=',3)]")
	store_id = fields.Many2one('res.partner',string="Store", domain="[('employee','=',False),('company_type','=','person'),('parent_id','!=',False)]")
	tid = fields.Char('T-ID')
	mid = fields.Char('M-ID')



class PotAnalysis(models.Model):
	_name = "pot.analysis"
	_description = "PoT Analysis"
	_auto = False
	_rec_name = 'location_id'

	location_id=fields.Many2one("stock.location","Location")
	institution_id = fields.Many2one("res.partner",string="Institution",domain="[('partner_type.sequence','=',2)]")
	merchant_id = fields.Many2one("res.partner",string="Merchant",domain="[('partner_type.sequence','=',3)]")
	store_id = fields.Many2one('res.partner',string="Store", domain="[('employee','=',False),('company_type','=','person'),('parent_id','!=',False)]")
	state_id=fields.Many2one('res.partner',string="State")
	partner_id = fields.Many2one("res.partner",string="Partner",domain="[('partner_type.sequence','=',1)]")
	tid = fields.Char('T-ID')
	mid = fields.Char('M-ID')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self.env.cr, self._table)
		self.env.cr.execute("""create or replace view pot_analysis as (
			select slp.id as id, 
			sl.id as location_id ,
			institution.id as institution_id,
			merchant.id as merchant_id,
			store.id as store_id,
			store_state.id as state_id,
			slp.partner_id as partner_id,
			slp.mid as mid ,slp.tid as tid 
			from stock_location_pot slp
			left join stock_location sl on slp.location_id=sl.id
			left join res_partner as store on sl.partner_id=store.id
			left join res_country_state as store_state on store.state_id=store_state.id
			left join res_partner as merchant on merchant.id=store.parent_id
			left join res_partner as institution on merchant.institution=institution.id
			group by slp.id,sl.id,institution.id,merchant.id,store.id,store_state.id,slp.partner_id,slp.mid,slp.tid 
			)

			""")