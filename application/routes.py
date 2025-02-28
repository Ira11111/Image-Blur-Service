import celery
from tasks import celery_app, process_image_task, send_email_for_subscriber_task
from email_validator import EmailNotValidError, validate_email
from flask import Flask, jsonify, request, url_for
from models import Order, User, session
from sqlalchemy.exc import IntegrityError

from archive import create_archive
from mail import send_email
from image import process_images

app = Flask(__name__)


@app.route("/blur", methods=["POST"])
def blur_images():
    email = request.form.get("email")
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"errors": "Email is not valid"}), 400

    images = request.files.getlist("images")
    print(type(images[0]))
    if images is None:
        return jsonify({"errors": "There are no images to process"}), 400

    image_data, dir_name = process_images(images)

    task_group = celery.group(process_image_task.s(*data) for data in image_data)

    result = task_group.apply_async()
    result.save()

    try:
        user = User(email=email)
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()

    order = Order(order_id=result.id, directory=dir_name, user_email=email)
    session.add(order)
    session.commit()

    return jsonify(
        {
            "order progress": url_for(
                endpoint="get_group_status",
                group_id=result.id),
            "send images": url_for(
                endpoint="send_images_to_email",
                group_id=result.id)
        }
    ), 202


@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id):
    result = celery_app.GroupResult.restore(group_id)

    if result:
        comp_tasks = result.completed_count()
        status = "Completed" if result.ready() else "Processing"
        return jsonify({'completed tasks': comp_tasks, 'group status': status}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route("/send_images/<group_id>", methods=["GET"])
def send_images_to_email(group_id):
    result = celery_app.GroupResult.restore(group_id)
    if result is None:
        return jsonify({"error": "group not found"}), 404
    else:
        if not result.ready():
            return jsonify({"error": "group not completed"}), 404
        else:
            print("API EMAIL")
            email, dir_name = session.query(Order.user_email, Order.directory).filter(Order.order_id == group_id).one()
            zip_file = create_archive(f"./{dir_name}")
            print("S1")
            send_email(order_id=group_id, receiver=email, zip_file=zip_file)
            print("S2")
            return "Email is sent", 200


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"errors": "Email is not valid"}), 400

    user = session.query(User).filter(User.email == email).one_or_none()
    if user is None:
        user = User(email=email, subscription=True)
        session.add(user)
    else:
        user.subscription = True
    session.commit()
    return "You are subscriber!!!", 201


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    email = request.form.get("email")
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"errors": "Email is not valid"}), 400

    user = session.query(User).filter(User.email == email).one_or_none()
    if user is None:
        return jsonify({"errors": "User not found"}), 404
    else:
        user.subscription = False
    return "You are not subscriber(((", 201
