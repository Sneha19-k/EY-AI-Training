from fastapi import FastAPI

#instance
app= FastAPI()

# ---------------GET-------------
@app.get("/students")
def get_students():
    return{"This is a get request"}

#----------------POST----------------
@app.post("/students")
def create_students():
    return{"This is a post request"}

#-----------------PUT---------------
@app.put("/students")
def update_students():
    return{"This is a put request"}

#-----------------DELETE-------------
@app.delete("/students")
def delete_students():
    return{"This is a delete request"}