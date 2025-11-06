# Random meal planner for the week uk 
import random
class WeeklyMealPlanner:
    def __init__(self):
        self.meals = {
            "Monday": ["Spaghetti Bolognese", "Chicken Curry", "Vegetable Stir Fry"],
            "Tuesday": ["Tacos", "Grilled Salmon", "Caesar Salad"],
            "Wednesday": ["Beef Stew", "Pasta Primavera", "Chicken Alfredo"],
            "Thursday": ["Fish and Chips", "Veggie Burger", "Chicken Fajitas"],
            "Friday": ["Pizza", "Sushi", "Lamb Chops"],
            "Saturday": ["BBQ Ribs", "Quiche", "Salmon Teriyaki"],
            "Sunday": ["Roast Chicken", "Vegetable Lasagna", "Steak and Potatoes"]
        }

    def generate_meal_plan(self):
        meal_plan = {}
        for day, meal_options in self.meals.items():
            meal_plan[day] = random.choice(meal_options)
        return meal_plan
if __name__ == "__main__":
    planner = WeeklyMealPlanner()
    meal_plan = planner.generate_meal_plan()
    for day, meal in meal_plan.items():
        print(f"{day}: {meal}")
        print("Bon appétit!")
        print()
        
    