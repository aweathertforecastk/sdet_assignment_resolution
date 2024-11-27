from features.steps.cleaning_service_page import CleaningServicePage


def before_scenario(context, scenario):
    context.service_page = CleaningServicePage()


def after_scenario(context, scenario):
    context.service_page = None
