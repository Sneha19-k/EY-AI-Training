use university
switched to db university
db.students.insertOne({
  student_id:1,
  name: "Rahul",
  age:21,
  city:"Mumbai",
  course:"AI",
  marks:85
  })
{
 acknowledged: true,
 insertedId: ObjectId('68dfa49b4327d5a1173a219d')
}
db.students.insertMany([
  { student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "ML", marks: 90 },
  { student_id: 3, name: "Arjun", age: 20, city: "Bengaluru", course: "Data Science", marks: 78 },
  { student_id: 4, name: "Neha", age: 23, city: "Hyderabad", course: "AI", marks: 88 },
  { student_id: 5, name: "Vikram", age: 21, city: "Chennai", course: "ML", marks: 95 }
])

{
 acknowledged: true,
 insertedIds: {
   '0': ObjectId('68dfa66f4327d5a1173a219e'),
   '1': ObjectId('68dfa66f4327d5a1173a219f'),
   '2': ObjectId('68dfa66f4327d5a1173a21a0'),
   '3': ObjectId('68dfa66f4327d5a1173a21a1')
 }
}
db.students.find()
{
 _id: ObjectId('68dfa49b4327d5a1173a219d'),
 student_id: 1,
 name: 'Rahul',
 age: 21,
 city: 'Mumbai',
 course: 'AI',
 marks: 85
}
{
 _id: ObjectId('68dfa66f4327d5a1173a219e'),
 student_id: 2,
 name: 'Priya',
 age: 22,
 city: 'Delhi',
 course: 'ML',
 marks: 90
}
{
 _id: ObjectId('68dfa66f4327d5a1173a219f'),
 student_id: 3,
 name: 'Arjun',
 age: 20,
 city: 'Bengaluru',
 course: 'Data Science',
 marks: 78
}
{
 _id: ObjectId('68dfa66f4327d5a1173a21a0'),
 student_id: 4,
 name: 'Neha',
 age: 23,
 city: 'Hyderabad',
 course: 'AI',
 marks: 88
}
{
 _id: ObjectId('68dfa66f4327d5a1173a21a1'),
 student_id: 5,
 name: 'Vikram',
 age: 21,
 city: 'Chennai',
 course: 'ML',
 marks: 95
}
db.students.findOne({name: "Rahul"})
{
 _id: ObjectId('68dfa49b4327d5a1173a219d'),
 student_id: 1,
 name: 'Rahul',
 age: 21,
 city: 'Mumbai',
 course: 'AI',
 marks: 85
}
db.students.find({marks:{$gt: 85}})
{
 _id: ObjectId('68dfa66f4327d5a1173a219e'),
 student_id: 2,
 name: 'Priya',
 age: 22,
 city: 'Delhi',
 course: 'ML',
 marks: 90
}
{
 _id: ObjectId('68dfa66f4327d5a1173a21a0'),
 student_id: 4,
 name: 'Neha',
 age: 23,
 city: 'Hyderabad',
 course: 'AI',
 marks: 88
}
{
 _id: ObjectId('68dfa66f4327d5a1173a21a1'),
 student_id: 5,
 name: 'Vikram',
 age: 21,
 city: 'Chennai',
 course: 'ML',
 marks: 95
}
db.students.find({},{name: 1,course: 1, id: 0})
MongoServerError[Location31254]: Cannot do exclusion on field id in inclusion projection
db.students.find({},{name: 1,course: 1, _id: 0})
{
 name: 'Rahul',
 course: 'AI'
}
{
 name: 'Priya',
 course: 'ML'
}
{
 name: 'Arjun',
 course: 'Data Science'
}
{
 name: 'Neha',
 course: 'AI'
}
{
 name: 'Vikram',
 course: 'ML'
}
db.students.updateOne({name: "Neha"}, {$set: {marks: 92, course: "Advanced AI"}})
{
 acknowledged: true,
 insertedId: null,
 matchedCount: 1,
 modifiedCount: 1,
 upsertedCount: 0
}
db.students.updateMany({course: "AI"}{$set: {grade: "A"}})
SyntaxError: Unexpected token, expected "," (1:37)

[0m[31m[1m>[22m[39m[90m 1 |[39m db[33m.[39mstudents[33m.[39mupdateMany({course[33m:[39m [32m"AI"[39m}{$set[33m:[39m {grade[33m:[39m [32m"A"[39m}})
 [90m   |[39m                                      [31m[1m^[22m[39m[0m
db.students.updateMany({course: "AI"},{$set: {grade: "A"}})
{
 acknowledged: true,
 insertedId: null,
 matchedCount: 1,
 modifiedCount: 1,
 upsertedCount: 0
}
db.students.deleteOne({name: "Arjun"})
{
 acknowledged: true,
 deletedCount: 1
}
db.students.deleteMany({marks: {$lt:80}})

