from django.core.validators import RegexValidator


isalphavalidator = RegexValidator(
    r'^[A-Za-záàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ._\ -]*$',
    message="La saisie doit comporter uniquement des lettres avec trait d'union ou espace pour séparation.",
    code='Saisie invalide'
    )


ischarfieldvalidator = RegexValidator(
    r'^[^&¤@=%<>#~`/§%=\^\$\\\|\{\}\[\]\+\*\.]*$',
    message="La saisie ne doit pas comporter de caractères spéciaux.",
    code='Saisie invalide'
    )
