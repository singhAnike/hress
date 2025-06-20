from odoo import http
from odoo.http import request
import json

class HressController(http.Controller):

    @http.route('/api/login', type='json', auth='public', csrf=False)
    def login(self, **kwargs):
        login = kwargs.get('login')
        password = kwargs.get('password')
        db = kwargs.get('db', request.session.db)

        uid = request.session.authenticate(db, login, password)
        if uid:
            user = request.env['res.users'].sudo().browse(uid)
            return {'success': True, 'uid': uid, 'name': user.name, 'employee_id': user.employee_id.id}
        return {'success': False, 'error': 'Invalid credentials'}

    @http.route('/api/employee/me', type='json', auth='user')
    def employee_info(self):
        user = request.env.user
        employee = user.employee_id
        return {
            'name': employee.name,
            'email': employee.work_email,
            'job': employee.job_id.name,
            'department': employee.department_id.name,
        }
