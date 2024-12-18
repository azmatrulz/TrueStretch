from flask import Flask, render_template, request
import os

app = Flask(__name__)

def sanitize_resolution_input(resolution_string):
    cleaned_string = resolution_string.replace('x', ' ').replace('\n', ' ').strip()
    return ' '.join(cleaned_string.split())

def make_pairs_from_string(data_string):
    try:
        integers = list(map(int, data_string.strip().split()))
        if len(integers) % 2 != 0:
            raise ValueError("The input string must contain an even number of integers.")
        return [(integers[i], integers[i + 1]) for i in range(0, len(integers), 2)]
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route("/", methods=["GET"])
def index():
    return render_template("page.html")

@app.route("/compute", methods=["POST"])
def compute():
    try:
        height = float(request.form["height"])
        breadth = float(request.form["breadth"])
        resolutions = request.form["resolutions"]
        sanitized_resolutions = sanitize_resolution_input(resolutions)
        pairs = make_pairs_from_string(sanitized_resolutions)
        
        result_strings = []
        for first, second in pairs:
            try:
                div_h = height / first
                div_b = breadth / second
                result = round(div_b / div_h, 2)
                result_strings.append(f"{first}X{second}: {result}")
            except ZeroDivisionError:
                result_strings.append(f"{first}X{second}: Error")
        
        sorted_result_strings = sorted(result_strings, key=lambda x: float(x.split(":")[1]), reverse=True)
        return '\n'.join(sorted_result_strings)
    
    except Exception as e:
        print(f"Error in compute: {e}")
        return "An error occurred while processing your request."

if __name__ == "__main__":
    app.run(debug=True)
