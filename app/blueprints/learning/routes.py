from flask import render_template, request, jsonify

from app.blueprints.learning import learning_bp
from app.extensions import db
from app.models.lesson import Lesson, LessonProgress
from app.models.quiz import QuizQuestion, QuizResult


DEMO_USER_ID = 1  # placeholder until auth is integrated


@learning_bp.route("/")
def index():
    """Learning path overview."""
    return render_template("learning/index.html")


@learning_bp.route("/api/learning/progress", methods=["GET", "POST"])
def progress():
    if request.method == "GET":
        records = LessonProgress.query.filter_by(user_id=DEMO_USER_ID).all()
        return jsonify({"success": True, "data": [
            {
                "lesson_id": r.lesson_id,
                "completed": r.completed,
                "completion_date": r.completion_date.isoformat() if r.completion_date else None,
                "time_spent": r.time_spent,
            }
            for r in records
        ]})

    # POST — mark a lesson complete
    data = request.get_json(silent=True) or {}
    lesson_id = data.get("lesson_id")
    if not lesson_id:
        return jsonify({"success": False, "error": "lesson_id is required."}), 400

    lesson = db.session.get(Lesson, int(lesson_id))
    if not lesson:
        return jsonify({"success": False, "error": "Lesson not found."}), 404

    from datetime import datetime, timezone
    progress_rec = LessonProgress.query.filter_by(
        user_id=DEMO_USER_ID, lesson_id=lesson_id
    ).first()

    if not progress_rec:
        progress_rec = LessonProgress(user_id=DEMO_USER_ID, lesson_id=lesson_id)
        db.session.add(progress_rec)

    progress_rec.completed = True
    progress_rec.completion_date = datetime.now(timezone.utc)
    progress_rec.time_spent = int(data.get("time_spent", 0))
    db.session.commit()

    return jsonify({"success": True, "message": "Progress saved."})


@learning_bp.route("/api/learning/quiz", methods=["POST"])
def submit_quiz():
    """Submit quiz answers and get the result.

    Request JSON:
        lesson_id : int
        answers   : list[int]  — selected option index for each question (0-based)
    """
    data = request.get_json(silent=True) or {}
    lesson_id = data.get("lesson_id")
    answers = data.get("answers", [])

    if not lesson_id:
        return jsonify({"success": False, "error": "lesson_id is required."}), 400

    questions = QuizQuestion.query.filter_by(lesson_id=int(lesson_id)).all()
    if not questions:
        return jsonify({"success": False, "error": "No questions found for this lesson."}), 404

    if len(answers) != len(questions):
        return jsonify({
            "success": False,
            "error": f"Expected {len(questions)} answers, received {len(answers)}."
        }), 400

    # Grade the quiz
    score = 0
    feedback = []
    for i, question in enumerate(questions):
        selected = answers[i]
        correct = question.correct_index
        is_correct = (selected == correct)
        if is_correct:
            score += 1
        feedback.append({
            "question_id": question.id,
            "question": question.question,
            "selected": selected,
            "correct": correct,
            "is_correct": is_correct,
            "explanation": question.explanation,
        })

    # Persist result
    quiz_result = QuizResult(
        user_id=DEMO_USER_ID,
        lesson_id=int(lesson_id),
        score=score,
        total=len(questions),
        answers_json=answers,
    )
    db.session.add(quiz_result)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": {
            "score": score,
            "total": len(questions),
            "percentage": round(score / len(questions) * 100, 1) if len(questions) > 0 else 0,
            "feedback": feedback,
            "result": quiz_result.to_dict(),
        },
        "result": quiz_result.to_dict(),
        "feedback": feedback,
    })


@learning_bp.route("/api/learning/quiz-history", methods=["GET"])
def quiz_history():
    """Return past quiz attempts for the user."""
    results = (
        QuizResult.query
        .filter_by(user_id=DEMO_USER_ID)
        .order_by(QuizResult.taken_at.desc())
        .all()
    )
    data = []
    for r in results:
        lesson = db.session.get(Lesson, r.lesson_id)
        d = r.to_dict()
        d["lesson_title"] = lesson.title if lesson else "Unknown Lesson"
        d["lesson_slug"] = lesson.slug if lesson else ""
        data.append(d)
    return jsonify({"success": True, "data": data})


@learning_bp.route("/api/learning/restart", methods=["POST"])
def restart_lesson():
    """Reset completion progress for a lesson so user can retake it."""
    data = request.get_json(silent=True) or {}
    lesson_id = data.get("lesson_id")
    if not lesson_id:
        return jsonify({"success": False, "error": "lesson_id is required."}), 400

    rec = LessonProgress.query.filter_by(user_id=DEMO_USER_ID, lesson_id=int(lesson_id)).first()
    if rec:
        rec.completed = False
        db.session.commit()

    return jsonify({"success": True, "message": "Lesson progress reset."})

