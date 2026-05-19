-- NISTULA UNIFIED MESSAGING SCHEMA

-- 1. GUESTS
-- A single guest profile to unify them across all channels.
CREATE TABLE guests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. RESERVATIONS
-- Links guests to properties.
CREATE TABLE reservations (
    id VARCHAR(50) PRIMARY KEY, -- e.g., 'NIS-2024-0891'
    guest_id UUID REFERENCES guests(id) ON DELETE CASCADE,
    property_id VARCHAR(100) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed' -- confirmed, cancelled, completed
);

-- 3. CONVERSATIONS
-- A thread aggregator. A single reservation might have a WhatsApp conversation AND an Airbnb thread.
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID REFERENCES guests(id) ON DELETE CASCADE,
    reservation_id VARCHAR(50) REFERENCES reservations(id) ON DELETE SET NULL,
    source_channel VARCHAR(50) NOT NULL, -- whatsapp, airbnb, instagram
    channel_thread_id VARCHAR(255), -- External ID to reply to the correct thread
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. MESSAGES
-- Stores every individual message, tracking AI confidence and routing state.
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    sender_type VARCHAR(20) NOT NULL, -- 'guest', 'ai', 'human_agent'
    message_text TEXT NOT NULL,
    query_type VARCHAR(50), -- pre_sales_availability, complaint, etc.
    
    -- AI Tracking Fields
    is_ai_drafted BOOLEAN DEFAULT FALSE,
    ai_confidence_score NUMERIC(3,2) CHECK (ai_confidence_score >= 0.0 AND ai_confidence_score <= 1.0),
    routing_action VARCHAR(50), -- auto_send, agent_review, escalate
    final_status VARCHAR(50), -- auto_sent, agent_edited, agent_sent_manually
    
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

/*
DESIGN DECISIONS & HARDEST CHOICE:
The hardest design decision was determining how to link omnichannel messages to a single Guest entity. If a guest messages on Airbnb, we only have their Airbnb proxy email. If they message on WhatsApp, we only have their phone number. 

To solve this, I decoupled "Messages" from "Guests" by placing a "Conversations" table in the middle. The Conversations table locks onto a specific `source_channel`. This allows us to have multiple distinct threads (WhatsApp, Insta, Airbnb) that all point back to one unified `guest_id`. When our PMS syncs their phone number and email post-booking, our backend can merge previously unlinked conversation threads under the single unified Guest Profile.
*/