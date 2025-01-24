import frappe

@frappe.whitelist(allow_guest=True)
def handle_webhook():
    data = frappe.request.json
    frappe.log_error("Classplus webhook data", data)

    first_name = data.get("name")
    mobile_no = data.get("number")
    email_id = data.get("email")
    course_name = data.get("course_name")
    webinar_name = data.get("webinar_name")
    event_type = data.get("eventType")

    if not (first_name and mobile_no):
        frappe.throw("Name and Mobile Number are required!")

    lead_doc = {
        "doctype": "Lead",
        "first_name": first_name,
        "mobile_no": mobile_no,
        "email_id": email_id,
        "source": "Classplus"
    }

    if event_type == "USER_SIGNS_UP_ON_THE_APP":
        lead_doc["event_"] = "Signed up on the app"
    elif event_type == "USER_BUYS_COURSE":
        lead_doc["event_"] = "Bought Course"
        lead_doc["course_name"] = course_name
    elif event_type == "USER_DROPS_FROM_PAYMENT_PAGE":
        lead_doc["event_"] = "Dropped from payment page"
        lead_doc["course_name"] = course_name
        lead_doc["webinar_name"] = webinar_name
    elif event_type == "WEBINAR_LANDING_PAGE_USER_REGISTERS_FOR_WORKSHOP":
        lead_doc["webinar_name"] = webinar_name
        lead_doc["event_"] = "Registered for workshop"

    lead = frappe.get_doc(lead_doc)
    lead.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {"status": "success", "message": "Lead created successfully!"}