from market import app
import sys
 

sys.path.insert(0, 'CJ_Marketing/market')

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
