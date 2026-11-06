from flask import render_template, jsonify, abort

from app.blueprints.education import education_bp
from app.models.lesson import Lesson, LessonCategory


@education_bp.route("/")
def index():
    """Education hub listing all categories."""
    return render_template("education/index.html")


@education_bp.route("/<category>")
def category_view(category: str):
    """List lessons within a category."""
    try:
        cat_enum = LessonCategory(category.upper())
    except ValueError:
        abort(404)
    lessons = (
        Lesson.query
        .filter_by(category=cat_enum)
        .order_by(Lesson.order_index)
        .all()
    )
    return render_template("education/category.html", category=cat_enum, lessons=lessons)


@education_bp.route("/lesson/<slug>")
def lesson_detail(slug: str):
    """Display a single lesson."""
    lesson = Lesson.query.filter_by(slug=slug).first_or_404()
    return render_template("education/lesson.html", lesson=lesson)
