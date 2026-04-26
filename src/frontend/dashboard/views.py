from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

def add_person(request):
    return render(request, "add_person.html")

def schedules(request):
    schedule_data = [
        {
            "employee": "John Smith",
            "date": "May 20, 2024",
            "day": "Monday",
            "shift": "9:00 AM - 5:00 PM",
        },
        {
            "employee": "Jane Doe",
            "date": "May 21, 2024",
            "day": "Tuesday",
            "shift": "12:00 PM - 8:00 PM",
        },
        {
            "employee": "Mike Johnson",
            "date": "May 22, 2024",
            "day": "Wednesday",
            "shift": "9:00 AM - 5:00 PM",
        },
        {
            "employee": "Emily Davis",
            "date": "May 23, 2024",
            "day": "Thursday",
            "shift": "2:00 PM - 10:00 PM",
        },
        {
            "employee": "Chris Lee",
            "date": "May 24, 2024",
            "day": "Friday",
            "shift": "9:00 AM - 5:00 PM",
        },
    ]

    return render(request, "schedules.html", {"schedules": schedule_data})

def edit_shift(request):
    employees = ["John Smith", "Jane Doe", "Mike Johnson", "Emily Davis", "Chris Lee"]
    return render(request, "edit_shift.html", {"employees": employees})