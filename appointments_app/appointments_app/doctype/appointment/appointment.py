# Copyright (c) 2024, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
    def after_insert(self):
        self.queue_number = self.add_to_appointment_queue()
        self.save(ignore_permissions=True)

    def add_to_appointment_queue(self):
        filters = {
            "date": self.date,
            "shift": self.shift,
            "clinic": self.clinic,
        }
        appointment_queue_exists = frappe.db.exists(
            "Appointment Queue",
            filters,
        )

        if appointment_queue_exists:
            q = frappe.get_doc("Appointment Queue", filters)
        else:
            q = frappe.new_doc("Appointment Queue")
            q.update(filters)
            q.save(ignore_permissions=True)

        q.append("queue", {"appointment": self.name, "status": "Pending"})
        q.save(ignore_permissions=True)

        return len(q.queue)
