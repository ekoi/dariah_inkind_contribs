import autocomplete_light
from .models import TADIRAHTechnique


class TADIRAHTechniqueAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name', ]
    model = TADIRAHTechnique
    attrs = {
        # This will set the input placeholder attribute:
        'placeholder': 'Start typing...',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        #'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        #'class': 'modern-style',
    }


"""Note: adding the model as the first argument is a temporary fix for
https://github.com/yourlabs/django-autocomplete-light/issues/313.
"""
autocomplete_light.register(TADIRAHTechnique, TADIRAHTechniqueAutocomplete)
