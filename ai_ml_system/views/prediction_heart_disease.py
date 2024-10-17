import pandas as pd
import pickle
import warnings

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from ai_ml_system.forms import HeartDiseasePredictionForm

from django.shortcuts import render
from django.contrib import messages

warnings.filterwarnings("ignore")


def prediction_heart_disease(request):
    form = HeartDiseasePredictionForm()
    if request.POST:
        form = HeartDiseasePredictionForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            sex = form.cleaned_data["sex"]
            chest_pain_type = form.cleaned_data["chest_pain_type"]
            resting_blood_pressure = form.cleaned_data[
                "resting_blood_pressure"]  # noqa
            serum_cholestoral = form.cleaned_data["serum_cholestoral"]
            fasting_blood_sugar = form.cleaned_data["fasting_blood_sugar"]
            resting_electrocardiographic_results = form.cleaned_data[
                "resting_electrocardiographic_results"]  # noqa
            maximum_heart_rate_achieved = form.cleaned_data[
                "maximum_heart_rate_achieved"]  # noqa
            exercise_induced_angina = form.cleaned_data[
                "exercise_induced_angina"]  # noqa
            oldpeak = form.cleaned_data["oldpeak"]
            slope = form.cleaned_data["slope"]
            ca = form.cleaned_data["ca"]
            thal = form.cleaned_data["thal"]

            all_dataset = [
                age, sex, chest_pain_type, resting_blood_pressure,
                serum_cholestoral, fasting_blood_sugar,
                resting_electrocardiographic_results,
                maximum_heart_rate_achieved,
                exercise_induced_angina, oldpeak, slope, ca, thal
            ]
        else:
            all_dataset = []

        # csv read only
        with open("dataset/save_train_data/heart_db_pickle", "rb") as f:
            # new_model is the machine learning model that was loaded from the file using pickle.
            new_model = pickle.load(f)  # Python object serialization

        """
            The predict method returns a list of predictions, even if it’s just one prediction. The [0] accesses the first (and only) prediction in the list.
            The result is typically a single value (0 or 1), where 0 might mean "no heart disease" and 1 might mean "heart disease present," depending on how the model was trained.
        """
        perdictions = new_model.predict([all_dataset])[0]
        if perdictions == 0:
            messages.success(request, "Looks Like You are Fit")
        elif perdictions == 1:
            messages.warning(
                request, "Your Health is not Good, Please go For a Doctor"
            )

    context = {"form": form, }
    return render(request, "AI/prediction_heart_disease.html", context)
