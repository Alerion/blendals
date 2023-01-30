from .create_controls_collection import create_controls_collection, create_control_object


def main() -> None:
    collection = create_controls_collection()
    control = create_control_object("Empty1")
    collection.objects.link(control)
