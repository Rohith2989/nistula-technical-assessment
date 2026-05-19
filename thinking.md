# Nistula - Part 3 Thinking Questions

### Question A — The Immediate Response
**The Reply:**
"I am so sorry you are dealing with this at 3 AM. I completely understand your frustration, especially with guests arriving soon. I have immediately paged our night emergency caretaker to check the water heater. Regarding your refund request, I have escalated this as a high-priority ticket for management to review the moment they are online at 8 AM. The caretaker should be reaching out to you momentarily."

**Why I chose this wording:**
At 3 AM, an angry guest doesn't want to talk to a robot; they want action. This wording validates their frustration, explicitly states the physical action being taken (paging the caretaker), and sets a firm but polite boundary that refunds are handled by management in the morning, preventing the AI from accidentally authorizing a payout.

### Question B — The System Design
1. **Classification & Action:** The webhook receives the payload, the AI classifies it as a `complaint` with a `confidence_score` of 0.95. Because the type is `complaint`, the router bypasses `auto_send` and forces an `escalate` action, but automatically replies with the drafted de-escalation message above.
2. **Alerting Layer:** A high-priority webhook is fired to PagerDuty or Twilio, sending an automated SMS and automated Voice Call to the on-duty night caretaker indicating: "URGENT: No hot water at Villa B1."
3. **Escalation Protocol:** The system initiates a 15-minute countdown. If the caretaker does not acknowledge the ticket via a WhatsApp button click ("I am on it"), the system escalates by calling the secondary contact (the Villa Manager or Founder).
4. **CRM Logging:** The guest's CRM profile is flagged with a "Negative Experience" tag, pinning the ticket to the top of the Unified Inbox for the 8 AM management shift to review the refund request.

### Question C — The Learning
Three identical infrastructure complaints in two months is an operational failure, not an anomaly.

**What the system should do:**
The Conversation Intelligence layer (Layer 5) should detect this recurring `complaint` cluster under "Villa B1 + Hot Water" and generate a flag on the Owner's Analytics Dashboard showing a systemic hardware degradation. 

**What I would build to prevent it:**
I would build an automated Preventative Maintenance trigger linked to the PMS. At 2:00 PM on the day of every check-in, the system automatically sends a WhatsApp message to the caretaker with a checklist. The caretaker *must* reply to the bot with a photo of the geyser switched on or type "Hot water verified." If the bot doesn't receive this confirmation by 3:00 PM, it alerts the villa manager *before* the guest arrives, preventing the 3 AM disaster entirely.