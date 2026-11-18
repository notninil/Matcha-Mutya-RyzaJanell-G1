from django import forms
from django.utils import timezone

from .models import CheckIn, Cafe


class CheckInForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(5, "5 · Outstanding"), (4, "4 · Great"), (3, "3 · Good"),
                 (2, "2 · Okay"), (1, "1 · Not for me")],
        coerce=int, empty_value=None, widget=forms.RadioSelect,
        error_messages={"required": "Choose a rating from 1 to 5.",
                        "invalid_choice": "Choose a rating from 1 to 5."},
    )

    class Meta:
        model = CheckIn
        fields = ["cafe", "drink_name", "rating", "visited_on", "notes"]
        labels = {"cafe": "Café", "drink_name": "Drink or blend", "visited_on": "Date visited",
                  "notes": "Notes (optional)"}
        widgets = {
            "visited_on": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notes": forms.Textarea(attrs={"rows": 4, "maxlength": 500}),
            "drink_name": forms.TextInput(attrs={"placeholder": "e.g. Iced ceremonial latte"}),
        }
        error_messages = {
            "cafe": {"required": "Choose the café you visited."},
            "drink_name": {"required": "Tell us which drink or blend you tried."},
            "visited_on": {"required": "Enter the date of your visit.",
                           "invalid": "Enter a valid date."},
        }

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        cafes = Cafe.objects.filter(is_active=True)
        if self.instance.pk:  # keep an already-used café selectable when editing
            cafes = Cafe.objects.filter(is_active=True) | Cafe.objects.filter(pk=self.instance.cafe_id)
        self.fields["cafe"].queryset = cafes.distinct()
        self.fields["cafe"].empty_label = "Select a café"
        self.fields["visited_on"].widget.attrs["max"] = timezone.localdate().isoformat()

    def clean_drink_name(self):
        drink = " ".join(self.cleaned_data["drink_name"].split())
        if len(drink) < 2:
            raise forms.ValidationError("Drink name must be at least 2 characters.")
        return drink

    def clean_visited_on(self):
        visited_on = self.cleaned_data["visited_on"]
        if visited_on > timezone.localdate():
            raise forms.ValidationError("You can't check in on a future date.")
        return visited_on

    def clean(self):
        cleaned = super().clean()
        cafe, visited_on = cleaned.get("cafe"), cleaned.get("visited_on")
        if cafe and visited_on:
            duplicate = CheckIn.objects.filter(
                user=self.user, cafe=cafe, visited_on=visited_on,
            ).exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise forms.ValidationError(
                    "You already checked in at this café on that date. Edit that check-in instead.",
                )
        return cleaned
