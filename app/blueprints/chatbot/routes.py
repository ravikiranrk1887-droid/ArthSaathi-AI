from datetime import datetime, timezone

from flask import render_template, request, jsonify

from app.blueprints.chatbot import chatbot_bp
from app.extensions import db
from app.models.chat import ChatConversation, ChatMessage
from app.services import ai_service


@chatbot_bp.route("/")
def index():
    """FinBot AI chat interface."""
    return render_template("chatbot/index.html")


@chatbot_bp.route("/api/chat", methods=["POST"])
def api_chat():
    """Send a message to FinBot AI and persist the exchange.

    Request JSON:
        message         : User's message (required)
        conversation_id : Existing conversation ID (optional; creates new if omitted)

    Response JSON:
        success         : bool
        response        : Assistant reply text
        conversation_id : int (new or existing)
    """
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"success": False, "error": "Message is required."}), 400

    conversation_id = data.get("conversation_id")
    conversation = None

    # ------------------------------------------------------------------
    # Resolve or create conversation (works for both guest and logged-in)
    # ------------------------------------------------------------------
    if conversation_id:
        conversation = db.session.get(ChatConversation, int(conversation_id))

    if not conversation:
        # Use first 60 chars of message as auto-title
        title = message[:60] + ("…" if len(message) > 60 else "")
        conversation = ChatConversation(user_id=1, title=title)  # user_id=1 as guest/demo
        db.session.add(conversation)
        db.session.flush()  # get the ID before adding messages

    # ------------------------------------------------------------------
    # Build conversation history for Gemini
    # ------------------------------------------------------------------
    history = []
    for msg in conversation.messages.order_by(ChatMessage.created_at).all():
        role = "user" if msg.role == "USER" else "model"
        history.append({"role": role, "parts": [msg.content]})

    # ------------------------------------------------------------------
    # Call Gemini
    # ------------------------------------------------------------------
    ai_result = ai_service.chat_with_finbot(message, history)

    # ------------------------------------------------------------------
    # Persist messages
    # ------------------------------------------------------------------
    user_msg = ChatMessage(conversation_id=conversation.id, role="USER", content=message)
    db.session.add(user_msg)

    assistant_msg = ChatMessage(
        conversation_id=conversation.id,
        role="ASSISTANT",
        content=ai_result["response"],
    )
    db.session.add(assistant_msg)

    conversation.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify(
        {
            "success": ai_result["success"],
            "response": ai_result["response"],
            "conversation_id": conversation.id,
            "error": ai_result.get("error"),
        }
    )


@chatbot_bp.route("/api/chat/history", methods=["GET"])
def api_chat_history():
    """Return messages for a conversation.

    Query params:
        conversation_id : required
    """
    conversation_id = request.args.get("conversation_id")
    if not conversation_id:
        return jsonify({"success": False, "error": "conversation_id is required."}), 400

    conversation = db.session.get(ChatConversation, int(conversation_id))
    if not conversation:
        return jsonify({"success": False, "error": "Conversation not found."}), 404

    messages = [m.to_dict() for m in conversation.messages.order_by(ChatMessage.created_at).all()]
    return jsonify(
        {
            "success": True,
            "conversation": conversation.to_dict(),
            "messages": messages,
        }
    )
