from django.core.validators import RegexValidator


isalphavalidator = RegexValidator(
    r'^[A-Za-záàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ._\s-]*$',
    message="La saisie doit comporter uniquement des lettres avec trait d'union ou espace pour séparation.",
    code='Saisie invalide'
    )


isalphanumvalidator = RegexValidator(
    r'^[0-9A-Za-záàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'._\s-]*$',
    message="La saisie doit comporter uniquement des lettres avec trait d'union, apostrophe ou espace pour séparation et des chiffres.",
    code='Saisie invalide'
    )
