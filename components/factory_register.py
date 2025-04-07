from kivy.factory import Factory


def register_factory():
    r = Factory.register
    r("CoverImage", module="components.image")
    r("CustomLabel", module="components.label")
    r("BackgroundColorBehavior", module="components.behaviors")
    r("AdaptiveBehavior", module="components.behaviors")
    r("CustomButton", module="components.button")
    r("CustomCheckBox", module="components.checkbox")
    r("StencilBehavior", module="components.behaviors")
