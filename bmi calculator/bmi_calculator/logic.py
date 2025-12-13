class BMILogic:
    @staticmethod
    def calculate_bmi(weight_kg, height_m):
        if height_m <= 0:
            raise ValueError("Height must be greater than 0")
        return weight_kg / (height_m ** 2)

    @staticmethod
    def get_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
