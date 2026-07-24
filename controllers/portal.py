# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class CustomerPortalRps(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(CustomerPortalRps, self)._prepare_home_portal_values(counters)
        if 'rps_count' in counters:
            # Count the RPS documents linked to the current user (as lecturer or koordinator)
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
            if employee:
                domain = ['|', ('dosen_ids', 'in', [employee.id]), ('koordinator_id', '=', employee.id)]
                values['rps_count'] = request.env['sirita.rps'].sudo().search_count(domain)
            else:
                values['rps_count'] = 0
        return values

    @http.route(['/my/rps', '/my/rps/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rps(self, page=1, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        rps_model = request.env['sirita.rps']
        
        # Identify associated lecturer/employee
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return request.render("sirita_rps.portal_no_lecturer_found", {})
            
        domain = ['|', ('dosen_ids', 'in', [employee.id]), ('koordinator_id', '=', employee.id)]
        
        # Pager config
        rps_count = rps_model.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/rps",
            total=rps_count,
            page=page,
            step=10
        )
        
        records = rps_model.sudo().search(domain, limit=10, offset=pager['offset'])
        
        # Fetch all courses for creation dropdown
        courses = request.env['sirita.rps.course'].sudo().search([], order="name asc")
        prodis = request.env['hr.department'].sudo().search([('department_type', '=', 'prodi')], order="name asc")
        kurikulums = request.env['sirita.rps.kurikulum'].sudo().search([], order="name desc")
        
        values.update({
            'rps_records': records,
            'courses': courses,
            'prodis': prodis,
            'kurikulums': kurikulums,
            'page_name': 'rps_portal_list',
            'pager': pager,
            'default_url': '/my/rps',
            'error': kw.get('error'),
        })
        return request.render("sirita_rps.portal_my_rps_list", values)

    @http.route(['/my/rps/create'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_rps_create(self, **post):
        prodi_id = int(post.get('prodi_id', 0))
        kurikulum_id = int(post.get('kurikulum_id', 0))
        matkul_id = int(post.get('matkul_id', 0))
        name = post.get('name', '').strip()
        
        if not prodi_id or not kurikulum_id or not matkul_id:
            return request.redirect('/my/rps?error=missing_fields')
            
        matkul = request.env['sirita.rps.course'].sudo().browse(matkul_id)
        if not matkul.exists():
            return request.redirect('/my/rps?error=invalid_matkul')
            
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return request.redirect('/my/rps?error=no_lecturer')
            
        # Check if an RPS for this matkul already exists
        existing_rps = request.env['sirita.rps'].sudo().search([
            ('matkul_id', '=', matkul.id),
            ('state', 'in', ['draft', 'submitted', 'approved'])
        ], limit=1)
        if existing_rps:
            return request.redirect('/my/rps?error=duplicate_rps')
            
        # Create new RPS
        rps_vals = {
            'name': name or f"RPS {matkul.name}",
            'prodi_id': prodi_id,
            'kurikulum_id': kurikulum_id,
            'matkul_id': matkul.id,
            'koordinator_id': employee.id,
            'dosen_ids': [(4, employee.id)],
            'state': 'draft',
        }
        
        new_rps = request.env['sirita.rps'].sudo().create(rps_vals)
        return request.redirect(f'/my/rps/{new_rps.id}')

    @http.route(['/my/rps/<int:rps_id>'], type='http', auth="user", website=True)
    def portal_rps_detail(self, rps_id, **kw):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        # Access check
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id):
            return request.redirect('/my/rps')
            
        cpls = request.env['sirita.rps.cpl'].sudo().search([('prodi_id', '=', rps.prodi_id.id)], order="kode asc")
        metodes = request.env['sirita.rps.metode'].sudo().search([], order="name asc")

        values = {
            'rps': rps,
            'cpls': cpls,
            'metodes': metodes,
            'page_name': 'rps_portal_detail',
        }
        return request.render("sirita_rps.portal_rps_detail_page", values)

    @http.route(['/my/rps/<int:rps_id>/update_overview'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_rps_update_overview(self, rps_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        metode_ids = [int(m) for m in post.getlist('metode_ids')]
        
        rps.write({
            'deskripsi': post.get('deskripsi', ''),
            'pustaka_utama': post.get('pustaka_utama', ''),
            'pustaka_pendukung': post.get('pustaka_pendukung', ''),
            'media_software': post.get('media_software', ''),
            'media_hardware': post.get('media_hardware', ''),
            'metode_ids': [(6, 0, metode_ids)]
        })
        return request.redirect(f'/my/rps/{rps.id}#overview')

    @http.route(['/my/rps/<int:rps_id>/update_cpmk'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_rps_update_cpmk(self, rps_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        cpmk_id = post.get('cpmk_id')
        cpl_ids = [int(c) for c in post.getlist('cpl_ids')]
        
        vals = {
            'kode': post.get('kode', ''),
            'name': post.get('name', ''),
            'bobot': float(post.get('bobot', 0.0) or 0.0),
            'cpl_ids': [(6, 0, cpl_ids)]
        }
        
        if cpmk_id:
            cpmk = request.env['sirita.rps.cpmk'].sudo().browse(int(cpmk_id))
            if cpmk.exists() and cpmk.rps_id.id == rps.id:
                cpmk.write(vals)
        else:
            vals['rps_id'] = rps.id
            request.env['sirita.rps.cpmk'].sudo().create(vals)
            
        return request.redirect(f'/my/rps/{rps.id}#cpmk')

    @http.route(['/my/rps/<int:rps_id>/delete_cpmk/<int:cpmk_id>'], type='http', auth="user", methods=['POST', 'GET'], website=True, csrf=True)
    def portal_rps_delete_cpmk(self, rps_id, cpmk_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        cpmk = request.env['sirita.rps.cpmk'].sudo().browse(cpmk_id)
        if cpmk.exists() and cpmk.rps_id.id == rps.id:
            cpmk.unlink()
            
        return request.redirect(f'/my/rps/{rps.id}#cpmk')

    @http.route(['/my/rps/<int:rps_id>/update_weekly'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_rps_update_weekly(self, rps_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        week_id = post.get('week_id')
        cpmk_ids = [int(c) for c in post.getlist('cpmk_ids')]
        
        vals = {
            'week': int(post.get('week', 1) or 1),
            'sub_cpmk': post.get('sub_cpmk', ''),
            'bahan_kajian': post.get('bahan_kajian', ''),
            'metode_pembelajaran': post.get('metode_pembelajaran', ''),
            'indikator': post.get('indikator', ''),
            'kriteria': post.get('kriteria', ''),
            'bobot': float(post.get('bobot', 0.0) or 0.0),
            'cpmk_ids': [(6, 0, cpmk_ids)]
        }
        
        if week_id:
            week = request.env['sirita.rps.weekly'].sudo().browse(int(week_id))
            if week.exists() and week.rps_id.id == rps.id:
                week.write(vals)
        else:
            vals['rps_id'] = rps.id
            request.env['sirita.rps.weekly'].sudo().create(vals)
            
        return request.redirect(f'/my/rps/{rps.id}#weekly')

    @http.route(['/my/rps/<int:rps_id>/delete_weekly/<int:week_id>'], type='http', auth="user", methods=['POST', 'GET'], website=True, csrf=True)
    def portal_rps_delete_weekly(self, rps_id, week_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        week = request.env['sirita.rps.weekly'].sudo().browse(week_id)
        if week.exists() and week.rps_id.id == rps.id:
            week.unlink()
            
        return request.redirect(f'/my/rps/{rps.id}#weekly')

    @http.route(['/my/rps/<int:rps_id>/submit_rps'], type='http', auth="user", methods=['POST', 'GET'], website=True, csrf=True)
    def portal_rps_submit_rps(self, rps_id, **post):
        rps = request.env['sirita.rps'].sudo().browse(rps_id)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee or (employee.id not in rps.dosen_ids.ids and rps.koordinator_id.id != employee.id) or rps.state != 'draft':
            return request.redirect('/my/rps')
            
        rps.write({'state': 'submitted'})
        return request.redirect(f'/my/rps/{rps.id}')
