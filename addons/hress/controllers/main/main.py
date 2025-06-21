from odoo import http
from odoo.http import request
import json
import logging
_logger = logging.getLogger(__name__)
class HressController(http.Controller):

    @http.route('/api/login', type='json', auth='public', csrf=False)
    def login(self):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            return {'success': False, 'error': 'Invalid JSON'}

        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return {'success': False, 'error': 'Missing login or password'}

        try:
            db = request.env.cr.dbname
            credential = {'login': login, 'password': password,
                          'type': 'password'}
            uid = request.session.authenticate(db, credential)
        except Exception as e:
            return {'success': False, 'error': str(e)}

        if uid:
            user = request.env['res.users'].sudo().browse(uid['uid'])
            return {
                'success': True,
                'uid': uid['uid'],
                'name': user.name,
            }

        return {'success': False, 'error': 'Invalid credentials'}
