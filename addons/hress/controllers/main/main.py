from odoo import http
from odoo.http import request
import json

import logging
_logger = logging.getLogger(__name__)

class HressController(http.Controller):

    @http.route('/api/login', type='json', auth='public', csrf=False)
    def login(self):
        data = request.jsonrequest or {}
        login = data.get('login')
        password = data.get('password')

        _logger.info(f"Received login data: login={login}, password={password}")

        try:
            uid = request.session.authenticate(login, password)
        except Exception as e:
            return {'success': False, 'error': str(e)}

        if uid:
            user = request.env['res.users'].sudo().browse(uid)
            return {
                'success': True,
                'uid': uid,
                'name': user.name,
                'employee_id': user.employee_id.id
            }

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
