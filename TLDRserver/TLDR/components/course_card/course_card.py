from django_components import component

@component.register("course_card")
class Calendar(component.Component):
    template_name = "course_card/course_card.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, number_of_lectures):
        return {
            'number_of_lectures': number_of_lectures,
        }

    class Media:
        css = "course_card/course_card.css"
        js = "course_card/course_card.js"
