# coding=utf-8

from django import forms


class HelpEmailForm(forms.Form):
    PROBLEM_CHOICES = (
        ('EMR Help: Medical Question', 'Tengo una pregunta médica'),
        ('EMR Help: Program Question',
            'Tengo una pregunta sobre este programa'),
    )

    problem = forms.ChoiceField(label="¿Qué tipo de problema?",
                                choices=PROBLEM_CHOICES)
    explanation = forms.CharField(label="Explique su problema:",
                                  widget=forms.Textarea, max_length=10000,
                                  required=False)
