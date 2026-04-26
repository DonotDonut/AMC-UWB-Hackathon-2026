from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

def add_person(request):
    return render(request, "add_person.html")

def schedules(request):
    staff_schedule = [
        {"employee": "John Smith", "days": "Monday, Tuesday, Wednesday, Friday", "time": "9:00 AM - 5:00 PM"},
        {"employee": "Jane Doe", "days": "Tuesday, Wednesday, Thursday", "time": "12:00 PM - 8:00 PM"},
        {"employee": "Mike Johnson", "days": "Monday, Wednesday, Friday", "time": "9:00 AM - 5:00 PM"},
        {"employee": "Emily Davis", "days": "Thursday, Friday, Saturday", "time": "2:00 PM - 10:00 PM"},
        {"employee": "Chris Lee", "days": "Monday, Tuesday, Friday", "time": "9:00 AM - 5:00 PM"},
    ]

    week_schedule = [
        {
            "day": "Monday",
            "shifts": [
                {"employee": "John Smith", "time": "9:00 AM - 5:00 PM", "color": "john"},
                {"employee": "Mike Johnson", "time": "9:00 AM - 5:00 PM", "color": "mike"},
            ],
        },
        {
            "day": "Tuesday",
            "shifts": [
                {"employee": "John Smith", "time": "9:00 AM - 5:00 PM", "color": "john"},
                {"employee": "Jane Doe", "time": "12:00 PM - 8:00 PM", "color": "jane"},
                {"employee": "Chris Lee", "time": "9:00 AM - 5:00 PM", "color": "chris"},
            ],
        },
        {
            "day": "Wednesday",
            "shifts": [
                {"employee": "John Smith", "time": "9:00 AM - 5:00 PM", "color": "john"},
                {"employee": "Mike Johnson", "time": "9:00 AM - 5:00 PM", "color": "mike"},
                {"employee": "Jane Doe", "time": "12:00 PM - 8:00 PM", "color": "jane"},
            ],
        },
        {
            "day": "Thursday",
            "shifts": [
                {"employee": "Jane Doe", "time": "12:00 PM - 8:00 PM", "color": "jane"},
                {"employee": "Emily Davis", "time": "2:00 PM - 10:00 PM", "color": "emily"},
            ],
        },
        {
            "day": "Friday",
            "shifts": [
                {"employee": "John Smith", "time": "9:00 AM - 5:00 PM", "color": "john"},
                {"employee": "Chris Lee", "time": "9:00 AM - 5:00 PM", "color": "chris"},
                {"employee": "Emily Davis", "time": "2:00 PM - 10:00 PM", "color": "emily"},
            ],
        },
        {
            "day": "Saturday",
            "shifts": [
                {"employee": "Emily Davis", "time": "2:00 PM - 10:00 PM", "color": "emily"},
            ],
        },
        {
            "day": "Sunday",
            "shifts": [],
        },
    ]

    return render(
        request,
        "schedules.html",
        {
            "staff_schedule": staff_schedule,
            "week_schedule": week_schedule,
        },
    )

def edit_shift(request):
    employees = ["John Smith", "Jane Doe", "Mike Johnson", "Emily Davis", "Chris Lee"]
    return render(request, "edit_shift.html", {"employees": employees})