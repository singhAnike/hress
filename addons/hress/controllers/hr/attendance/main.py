from odoo import http
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class EmployeeAttendanceController(http.Controller):

    @http.route('/api/employee/checkin', type='json', auth='user', csrf=False, methods=['POST'])
    def employee_checkin(self):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

        if not employee:
            return {'success': False, 'error': 'No employee linked to this user'}

        # Check if already checked in (i.e., last attendance has check_out as False)
        last_attendance = request.env['hr.attendance'].sudo().search(
            [('employee_id', '=', employee.id)], order="check_in desc", limit=1)

        if last_attendance and not last_attendance.check_out:
            return {'success': False, 'error': 'Already checked in'}

        # Perform check-in
        request.env['hr.attendance'].sudo().create({
            'employee_id': employee.id,
            'check_in': datetime.now(),
        })

        return {'success': True, 'message': f'{employee.name} checked in successfully'}

    @http.route('/api/employee/checkout', type='json', auth='user', csrf=False, methods=['POST'])
    def employee_checkout(self):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

        if not employee:
            return {'success': False, 'error': 'No employee linked to this user'}

        # Get the open attendance (check_out is not set)
        last_attendance = request.env['hr.attendance'].sudo().search(
            [('employee_id', '=', employee.id), ('check_out', '=', False)],
            order="check_in desc", limit=1)
        
        _logger.info(f"last attendance    {last_attendance}")

        if not last_attendance:
            return {'success': False, 'error': 'No active check-in found'}

        last_attendance.write({'check_out': datetime.now()})

        return {'success': True, 'message': f'{employee.name} checked out successfully'}
